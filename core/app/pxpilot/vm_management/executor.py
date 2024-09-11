import logging
from datetime import datetime

from pxpilot.models.configuration.app_settings import AppSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions
from pxpilot.models.px.vms import VMContext
from pxpilot.vm_management.models import StartStatus
from core.exceptions.exceptions import ProxmoxError, FatalProxmoxError
from pxpilot.notifications import NotificationManager
from pxpilot.pxtool import VMService
from pxpilot.pxtool.models import VirtualMachine
from pxpilot.vm_management.vm_starter import VMStarter

logger = logging.getLogger(__name__)


class Executor:
    """
    Manages the execution processes for starting virtual machines
    """

    def __init__(self, vm_service: VMService, start_options: [VmStartOptions],
                 settings: AppSettings, starter: VMStarter = None,
                 notification_manager: NotificationManager = None, is_debug=False):
        """
        Initializes the Executor with necessary components.

        Args:
            :param vm_service: VMService: Client to interact with the Proxmox API.
            :param start_options: [VMLaunchSettings]: Configuration options for VM startup.
            :param notification_manager: NotificationManager, optional: Manager for handling notifications. Defaults to None.
            :param starter: VMStarter
            :param settings: AppSettings
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
        logger.debug("Start.")

        if self._launch_settings_list is None or len(self._launch_settings_list) == 0 or sum(1 for item in self._launch_settings_list if item.enabled) == 0:
            logger.info("There is no available virtual machine to start in configuration. Exiting...")
            return

        if self._vm_service is None:
            raise AttributeError("proxmox client is not set")

        if self._notification_manager is not None:
            self._notification_manager.start(datetime.now())

        vm_context_list: dict[int, VMContext] = {}
        try:
            proxmox_vms = self._vm_service.get_all_vms()
            logger.debug(f"Found {len(proxmox_vms)} virtual machines on Proxmox server: {proxmox_vms}")

            vm_context_list.update(self.get_vms_to_start(self._launch_settings_list, proxmox_vms))
            logger.debug(f"Loaded {len(vm_context_list)} start VM options from config.")

            self.main_loop(vm_context_list)
            logger.debug(f"{vm_context_list}")
        except FatalProxmoxError as ex:
            logger.exception(ex)
            self._notification_manager.append_error(str(ex))

            return
        except ProxmoxError as ex:
            logger.exception(ex)
            self._notification_manager.append_error(str(ex))

        if self._is_debug and vm_context_list is not None:
            self.clean_up(vm_context_list)

        if self._app_settings.auto_shutdown and self._app_settings.self_host is not None:
            localhost = vm_context_list[self._app_settings.self_host["vm_id"]].vm_info
            self.self_shutdown(localhost)

    def main_loop(self, vm_context_list: dict[int, VMContext]) -> None:
        for vm_context in (vm_context for vm_context in vm_context_list.values()
                           if vm_context.vm_launch_settings is not None):
            logger.debug(f"VM ID [{vm_context.vm_id}]: begin.")
            duration = 0

            ready_to_go = self.is_ready_to_go(vm_context, vm_context_list)
            logger.debug(f"Ready to go: {ready_to_go}.")
            if ready_to_go == StartStatus.DEPENDENCY_FAILED:
                logger.debug(f"VM ID [{vm_context.vm_id}]: dependency failed.")
                self.notification_log(vm_context, "dependency_failed", datetime.now(), duration)
                continue
            elif ready_to_go == StartStatus.INFO_MISSED:
                logger.debug(f"VM ID [{vm_context.vm_id}]: VM not found on Proxmox.")
                continue
            elif ready_to_go == StartStatus.ALREADY_STARTED:
                logger.debug(f"VM ID [{vm_context.vm_id}]: complete.")
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

            logger.debug(f"VM ID [{vm_context.vm_id}]: complete.")

    def is_ready_to_go(self, vm_context: VMContext, vm_context_list: dict[int, VMContext]) -> StartStatus:
        if vm_context.vm_info is None or vm_context.vm_launch_settings is None:
            return StartStatus.INFO_MISSED

        if self._vm_starter.check_healthcheck(vm_context):
            logger.debug(f"VM ID [{vm_context.vm_id}]: healthcheck pass. {StartStatus.ALREADY_STARTED}")
            return StartStatus.ALREADY_STARTED

        if len(vm_context.vm_launch_settings.dependencies) > 0:
            deps = {}

            for dep_vm_context in (item for item in vm_context_list.values() if
                                   item.vm_id in vm_context.vm_launch_settings.dependencies):
                dep_status = self._vm_starter.check_healthcheck(dep_vm_context)
                if dep_status:
                    logger.debug(f"VM ID [{vm_context.vm_id}]: dependency [{dep_vm_context.vm_id}] is running.")
                    deps[dep_vm_context.vm_id] = True
                else:
                    logger.debug(f"VM ID [{vm_context.vm_id}]: dependency [{dep_vm_context.vm_id}] is not running.")
                    deps[dep_vm_context.vm_id] = False

            return StartStatus.OK if all(deps.values()) else StartStatus.DEPENDENCY_FAILED

        logger.debug(f"VM ID [{vm_context.vm_id}]: healthcheck not passed, no dependency. Return {StartStatus.OK}")
        return StartStatus.OK

    def get_vms_to_start(self, start_options: list[VmStartOptions], px_vms: dict[int, VirtualMachine]) -> dict[int, VMContext]:
        """
        Filters and returns a list of VMs that are enabled and ready to be started based on dependencies.

        :param start_options: list[VMLaunchSettings] launch settings
        :param px_vms: dict[int, VirtualMachine] proxmox vm list
        :return: Completed dict of VMs from proxmox and starting option from config
        """
        contexts = dict()
        for so in start_options:
            vmc = VMContext(vm_id=so.vm_id, vm_launch_settings=so, status=StartStatus.UNKNOWN, vm_info=None)
            if so.vm_id in px_vms:
                vmc.vm_info = px_vms.pop(so.vm_id)
            contexts[so.vm_id] = vmc

        for vm_id, vm in px_vms.items():
            vmc = VMContext(vm_id=vm_id, vm_info=vm, status=StartStatus.UNKNOWN, vm_launch_settings=None)
            contexts[vm_id] = vmc

        return contexts

    def clean_up(self, vm_contexts: dict[int, VMContext]) -> None:
        logger.debug("Cleaning up - shutdown all started vms.")
        for vm in vm_contexts.values():
            if vm.vm_launch_settings is None or vm.vm_info is None:
                continue

            logger.debug(f"VM [{vm.vm_id}]: Shutdown.")

            try:
                self._vm_service.stop_vm(vm.vm_info)
            except ProxmoxError as ex:
                logger.warning(f"Error occurred during stop vm: {ex}")

    def notification_log(self, flow_item: VMContext, status, start_time, duration):
        if self._notification_manager is not None:
            self._notification_manager.append_status(flow_item.vm_info.vm_type, flow_item.vm_id,
                                                     f"{flow_item.vm_info.node}: {flow_item.vm_info.name}", status,
                                                     start_time, duration)

    def self_shutdown(self, target: VirtualMachine):
        logger.debug(f"VM [{target.vm_id}]: Shutdown.")
        try:
            self._vm_service.stop_vm(target)
        except ProxmoxError as ex:
            logger.warning(f"Error occurred during stop vm: {ex}")
