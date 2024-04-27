import time
from datetime import datetime

from .models import VMContext, StartResult
from .executor import StartStatus
from .host_validator import HostValidator, UnknownHealthcheckError
from .logging_config import LOGGER
from .pxtool.models import VMState
from .pxtool.vm_service import VMService


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
            return StartResult(StartStatus.ALREADY_STARTED, datetime.now())

        return self._start_vm_and_wait(flow_item)

    def _start_vm_and_wait(self, flow_item):
        LOGGER.debug(f"VM ID [{flow_item.vm_id}]: Starting virtual machine.")

        vm_info = flow_item.vm_info
        vm_launch_settings = flow_item.vm_launch_settings

        start_time = datetime.now()

        self._vm_service.start_vm(vm_info)

        still_starting = True
        while still_starting:
            if self.check_healthcheck(flow_item):
                LOGGER.info(f"VM [{vm_info.vm_id}]: Virtual machine successfully started.")
                return StartResult(status=StartStatus.STARTED, start_time=start_time, end_time=datetime.now())
            elif (vm_launch_settings.startup_parameters is not None
                  and ((end_time := datetime.now()) - start_time).seconds > vm_launch_settings.startup_parameters.startup_timeout):
                LOGGER.warn("Timeout exceed")
                return StartResult(status=StartStatus.TIMEOUT, start_time=start_time, end_time=end_time)
            else:
                LOGGER.info(f"VM [{vm_info.vm_id}]: The host is not yet available. Waiting...")

            time.sleep(5)

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

