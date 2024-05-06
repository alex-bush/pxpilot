import time
from datetime import datetime

from .models import VMContext, StartResult, StartStatus
from .host_validator import HostValidator, UnknownHealthcheckError
from pxpilot.logging_config import LOGGER
from pxpilot.pxtool.models import VMState
from pxpilot.pxtool.vm_service import VMService


DEFAULT_START_TIMEOUT = 300
CHECK_TIMEOUT = 5


class VMStarter:
    def __init__(self, vm_service: VMService, host_validator: HostValidator = None):
        self._vm_service = vm_service
        self._host_validator = host_validator

    def start(self, flow_item: VMContext | None) -> StartResult:
        vm_launch_settings = flow_item.vm_launch_settings
        vm_info = flow_item.vm_info

        if vm_launch_settings is None:
            LOGGER.info(f"VM ID [{vm_info.vm_id}]: not found in startup configuration. Skipped.")
            return StartResult(StartStatus.INFO_MISSED)

        if vm_info is None:
            LOGGER.info(f"VM ID [{vm_launch_settings.vm_id}]: not found on Proxmox server. Skipped.")
            return StartResult(StartStatus.INFO_MISSED)

        if not vm_launch_settings.enabled:
            LOGGER.info(f"VM ID [{vm_info.vm_id}]: Starting disabled in config. Skipped.")
            return StartResult(StartStatus.DISABLED)

        if vm_info.status != VMState.STOPPED:
            LOGGER.info(f"VM ID [{vm_info.vm_id}]: Virtual machine already started. No action needed.")
            flow_item.status = StartStatus.ALREADY_STARTED
            return StartResult(StartStatus.ALREADY_STARTED, self._get_now())

        return self._start_vm_and_wait(flow_item)

    def _start_vm_and_wait(self, flow_item):
        LOGGER.debug(f"VM ID [{flow_item.vm_id}]: Starting virtual machine.")

        vm_info = flow_item.vm_info
        vm_launch_settings = flow_item.vm_launch_settings

        start_time = self._get_now()

        self._vm_service.start_vm(vm_info)

        if not vm_launch_settings.startup_parameters.await_running:
            return StartResult(status=StartStatus.STARTED, start_time=start_time, end_time=start_time)

        if (vm_launch_settings.startup_parameters is not None
                and vm_launch_settings.startup_parameters.startup_timeout is not None):
            timeout = vm_launch_settings.startup_parameters.startup_timeout
        else:
            timeout = DEFAULT_START_TIMEOUT

        still_starting = True
        while still_starting:
            if self.check_healthcheck(flow_item):
                LOGGER.info(f"VM [{vm_info.vm_id}]: Virtual machine successfully started.")
                return StartResult(status=StartStatus.STARTED, start_time=start_time, end_time=self._get_now())
            elif ((end_time := self._get_now()) - start_time).seconds > timeout:
                LOGGER.warn(f"Timeout {timeout} exceed")
                return StartResult(status=StartStatus.TIMEOUT, start_time=start_time, end_time=end_time)
            else:
                LOGGER.info(f"VM [{vm_info.vm_id}]: The host is not yet available. Waiting...")

            time.sleep(CHECK_TIMEOUT)

    def check_healthcheck(self, flow_item: VMContext) -> bool:
        hc = flow_item.vm_launch_settings.healthcheck
        vm = flow_item.vm_info

        if self._vm_service.get_vm_status(vm) == VMState.RUNNING:
            if hc is not None and hc.target_url is not None:
                try:
                    return self._host_validator.validate(hc)
                except UnknownHealthcheckError as ex:
                    LOGGER.error(f"VM [{vm.vm_id}]: Unknown healthcheck type: {ex}")
                    return True  # cannot check healthcheck but state is running

            LOGGER.info(f"VM [{vm.vm_id}]: State is running. HealthCheckOptions is not provided.")
            return True
        else:
            return False

    @staticmethod
    def _get_now():
        return datetime.now()
