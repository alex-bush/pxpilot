from datetime import datetime
from typing import List

from pxpilot.config import VMLaunchSettings, AppSettings
from pxpilot.models import VMContext, StartStatus
from pxpilot.pxtool.exceptions import ProxmoxError
from pxpilot.logging_config import LOGGER
from pxpilot.notifications import NotificationManager
from pxpilot.pxtool import VMService
from pxpilot.pxtool.models import VirtualMachine, VMState
from pxpilot.vm_starter import VMStarter


class Executor:
    """
    Manages the execution processes for starting and monitoring virtual machines (VMs)
    in a Proxmox environment using given Proxmox client and configuration options.
    """

    def __init__(self, vm_service: VMService, start_options: [VMLaunchSettings],
                 settings: AppSettings, starter: VMStarter = None,
                 notification_manager: NotificationManager = None, is_debug=False):
        """
        Initializes the Executor with necessary components.

        Args:
            proxmox_client (ProxmoxClient): Client to interact with the Proxmox API.
            start_options (List[VMLaunchSettings]): Configuration options for VM startup.
            host_validator (HostValidator):
            notification_manager (NotificationManager, optional): Manager for handling notifications. Defaults to None.
        """

        self._vm_service = vm_service
        self._launch_settings_list = start_options
        self._notification_manager = notification_manager
        self._app_settings = settings
        self._vm_starter = starter
        self._is_debug = is_debug

    def start(self):
        """
        Starts the execution process for all enabled VMs as specified in the start options.
        """
        LOGGER.debug("Start.")

        if len(self._launch_settings_list) == 0 or sum(1 for item in self._launch_settings_list if item.enabled) == 0:
            LOGGER.info(F"There is no available virtual machine to start in configuration. Exiting...")
            return

        if self._vm_service is None:
            raise AttributeError("proxmox client is not set")

        if self._notification_manager is not None:
            self._notification_manager.start(datetime.now())

        proxmox_vms = self._vm_service.get_all_vms()
        LOGGER.debug(f"Found {len(proxmox_vms)} virtual machines: {proxmox_vms}")

        vm_context_list = self.get_vms_to_start(self._launch_settings_list, proxmox_vms)
        LOGGER.debug(f"Loaded {len(vm_context_list)} start VM options.")

        self.main_loop(vm_context_list)
        LOGGER.debug(f"{vm_context_list}")

        if self._is_debug:
            self.clean_up(vm_context_list)

        if self._app_settings.auto_shutdown:
            self.self_shutdown(self._app_settings.self_host)

    def main_loop(self, vm_context_list: List[VMContext]) -> None:
        for vm_context in (vm_context for vm_context in vm_context_list
                           if vm_context.vm_launch_settings is not None):
            LOGGER.debug(f"VM ID [{vm_context.vm_id}]: begin.")
            duration = 0

            ready_to_go = self.is_ready_to_go(vm_context, vm_context_list)
            LOGGER.debug(f"Ready to go: {ready_to_go}.")
            if ready_to_go == StartStatus.DEPENDENCY_FAILED:
                LOGGER.debug(f"VM ID [{vm_context.vm_id}]: dependency failed.")
                self.notification_log(vm_context, "dependency_failed", datetime.now(), duration)
                continue
            elif ready_to_go == StartStatus.INFO_MISSED:
                LOGGER.debug(f"VM ID [{vm_context.vm_id}]: VM not found on Proxmox.")
                continue
            elif ready_to_go == StartStatus.ALREADY_STARTED:
                LOGGER.debug(f"VM ID [{vm_context.vm_id}]: complete.")
                self.notification_log(vm_context, "already_started", datetime.now(), 0)
                continue

            start_result = self._vm_starter.start(vm_context)

            if start_result.end_time is not None:
                duration = start_result.end_time - start_result.start_time

            match start_result.status:
                case StartStatus.ALREADY_STARTED:
                    self.notification_log(vm_context, "already_started", start_result.start_time, 0)
                case StartStatus.STARTED:
                    self.notification_log(vm_context, "started", start_result.start_time, duration)
                case StartStatus.TIMEOUT:
                    self.notification_log(vm_context, "timeout", start_result.start_time, duration)
                case StartStatus.DISABLED:
                    self.notification_log(vm_context, "disabled", start_result.start_time, duration)

            LOGGER.debug(f"VM ID [{vm_context.vm_id}]: complete.")

    def is_ready_to_go(self, vm_context: VMContext, vm_context_list: List[VMContext]) -> StartStatus:
        if vm_context.vm_info is None or vm_context.vm_launch_settings is None:
            return StartStatus.INFO_MISSED

        if self._vm_starter.check_healthcheck(vm_context):
            return StartStatus.ALREADY_STARTED

        if len(vm_context.vm_launch_settings.dependencies) > 0:
            deps = {}

            for dep_vm_context in [item for item in vm_context_list if
                                   item.vm_id in vm_context.vm_launch_settings.dependencies]:
                dep_status = self._vm_starter.check_healthcheck(dep_vm_context)
                if dep_status:
                    LOGGER.debug(f"VM ID [{vm_context.vm_id}]: dependency [{dep_vm_context.vm_id}] is running.")
                    deps[dep_vm_context.vm_id] = True
                else:
                    LOGGER.debug(f"VM ID [{vm_context.vm_id}]: dependency [{dep_vm_context.vm_id}] is not running.")
                    deps[dep_vm_context.vm_id] = False

            return StartStatus.OK if all(deps.values()) else StartStatus.DEPENDENCY_FAILED

        return StartStatus.OK

    def get_vms_to_start(self, start_options: [VMLaunchSettings], px_vms: dict[int, VirtualMachine]) -> [VMContext]:
        """
        Filters and returns a list of VMs that are enabled and ready to be started based on dependencies.

        :param start_options: List of VM startup options.
        :param px_vms:
        :return: VMs ready to be started.
        """
        sos = []
        for so in start_options:
            si = VMContext(vm_id=so.vm_id, vm_launch_settings=so, status=StartStatus.UNKNOWN, vm_info=None)
            if so.vm_id in px_vms:
                si.vm_info = px_vms.pop(so.vm_id)
            sos.append(si)

        for vm_id, vm in px_vms.items():
            si = VMContext(vm_id=vm_id, vm_info=vm, status=StartStatus.UNKNOWN, vm_launch_settings=None)
            sos.append(si)
        return sos

    def clean_up(self, vm_contexts: List[VMContext]) -> None:
        LOGGER.debug("Cleaning up - shutdown all started vms.")
        for vm in vm_contexts:
            if vm.vm_launch_settings is None or vm.vm_info is None:
                continue

            LOGGER.debug(f"VM [{vm.vm_id}]: Shutdown.")

            try:
                self._vm_service.stop_vm(vm.vm_info)
            except ProxmoxError as ex:
                LOGGER.warn(f"Error occurred during stop vm: {ex}")

    def notification_log(self, flow_item: VMContext, status, start_time, duration):
        if self._notification_manager is not None:
            self._notification_manager.append_status(flow_item.vm_info.vm_type, flow_item.vm_id,
                                                     f"{flow_item.vm_info.node}: {flow_item.vm_info.name}", status,
                                                     start_time, duration)

    def self_shutdown(self, target):
        LOGGER.debug(f"VM [{target["vm_id"]}]: Shutdown.")
        try:
            self._vm_service.stop_vm(VirtualMachine(vm_id=target["vm_id"], vm_type=target["type"], name="", status=None, node=target["node"]))
        except ProxmoxError as ex:
            LOGGER.warn(f"Error occurred during stop vm: {ex}")
