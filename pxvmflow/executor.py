import time
from datetime import datetime

from pxvmflow.config import HealthCheckOptions, VMStartOptions
from pxvmflow.consts import VMType, VMState, STATUS_POLL_INTERVAL
from pxvmflow.exceptions import UnknownHealthcheckException, ProxmoxException
from pxvmflow.logging_config import LOGGER
from pxvmflow.notifications import NotificationManager
from pxvmflow.pxtool import *
from pxvmflow.host_validator import HostValidator


class Executor:
    """
    Manages the execution processes for starting and monitoring virtual machines (VMs)
    in a Proxmox environment using given Proxmox client and configuration options.
    """

    def __init__(self, proxmox_client: ProxmoxClient, start_options: [VMStartOptions],
                 host_validator: HostValidator = None,
                 notification_manager: NotificationManager = None):
        """
        Initializes the Executor with necessary components.

        Args:
            proxmox_client (ProxmoxClient): Client to interact with the Proxmox API.
            start_options (List[VMStartOptions]): Configuration options for VM startup.
            host_validator (HostValidator):
            notification_manager (NotificationManager, optional): Manager for handling notifications. Defaults to None.
        """

        self._px_client = proxmox_client
        self._start_options = start_options
        self._notification_manager = notification_manager
        self._host_validator = host_validator

    def start(self):
        """
        Starts the execution process for all enabled VMs as specified in the start options.
        """

        if len(self._start_options) == 0 or sum(1 for item in self._start_options if item.enabled) == 0:
            LOGGER.info(F"There is no available virtual machine to start in configuration. Exiting...")
            return

        if self._px_client is None:
            raise AttributeError("proxmox client is not set")

        if self._notification_manager is not None:
            self._notification_manager.start(datetime.now())

        sta = self.get_vms_to_start(self._start_options)

        px_vms = self.get_all_vm(self._px_client.px_get("nodes")[0]["node"])

        self.start_vms(sta, px_vms)

        self.clean_up(sta, px_vms)

    def get_all_vm(self, node) -> dict[int, ProxmoxVMInfo]:
        """
        Retrieves a list of all VMs from a specified node.

        Args:
            node (str): Node identifier in the Proxmox environment.

        Returns:
            Dict[int, ProxmoxVMInfo]: Dictionary of VM information indexed by VM IDs.
        """

        def fetch_entities(vm_type):
            return [
                ProxmoxVMInfo(vm_id=int(entity["vmid"]), vm_type=vm_type, name=entity["name"], status=entity["status"],
                              node=node)
                for entity in self._px_client.px_get(f"nodes/{node}/{vm_type}")]

        entities = dict()
        for lxc in fetch_entities(VMType.LXC):
            entities[lxc.vm_id] = lxc
        for qemu in fetch_entities(VMType.QEMU):
            entities[qemu.vm_id] = qemu

        return entities

    def start_vms(self, start_options: [VMStartOptions], px_vms: [int, ProxmoxVMInfo]) -> None:
        """
        Attempts to start a list of virtual machines based on their start options and current state.

        Args:
            start_options (List[VMStartOptions]): List of configurations detailing which VMs to start and their respective settings.
            px_vms (Dict[int, ProxmoxVMInfo]): Dictionary containing the current state of VMs fetched from Proxmox, keyed by VM ID.

        This method iterates through the list of start options, checking each VM's current state against the desired state
        and starts the VM if necessary.

        If a health check is specified, it also verifies the VM's operational status post-start using the specified health check.
        """

        for start_item in start_options:
            if start_item.vm_id not in px_vms:
                LOGGER.info(f"VM [{start_item.vm_id}]: Id not found in startup configuration. Skipped.")
                continue

            vm_to_start = px_vms[start_item.vm_id]

            if not start_item.enabled:
                LOGGER.info(f"VM [{vm_to_start.vm_id}]: Starting disabled in config. Skipped.")
                continue

            if vm_to_start.status != VMState.STOPPED:
                self.notification_log(vm_to_start, "running", datetime.now(), 0)
                LOGGER.info(f"VM [{vm_to_start.vm_id}]: Virtual machine already started. No action needed.")
                continue

            LOGGER.debug(f"VM [{vm_to_start.vm_id}]: Starting virtual machine.")
            start_time = datetime.now()
            self.start_vm(vm_to_start)

            if start_item.run_timeout is not None:
                time.sleep(start_item.run_timeout)

            flag = True
            while flag:
                end_time = datetime.now()
                if self.is_running(vm_to_start, start_item.healthcheck):
                    flag = False
                    end_time = datetime.now()
                    self.notification_log(vm_to_start, "started", end_time, end_time - start_time)

                    LOGGER.info(f"VM [{vm_to_start.vm_id}]: Virtual machine successfully started.")
                elif start_item.startup_parameters is not None and (
                        end_time - start_time).seconds > start_item.startup_parameters.startup_timeout:
                    self.notification_log(vm_to_start, "timeout", end_time, end_time - start_time)
                    flag = False

                    LOGGER.warn("Timeout exceed")
                else:
                    LOGGER.info(f"VM [{vm_to_start.vm_id}]: The host is not yet available. Waiting...")

                time.sleep(STATUS_POLL_INTERVAL)

    def is_running(self, vm: ProxmoxVMInfo, hc: HealthCheckOptions) -> bool:
        """
        Checks if a given virtual machine (VM) is currently running and optionally performs a health check.

        Args:
            vm (ProxmoxVMInfo): The virtual machine information object, which includes details like VM ID, node, and type.
            hc (HealthCheckOptions): Configuration for the health check to be performed on the VM, if any.

        Returns:
            bool: True if the VM is running and meets the health check criteria (if specified), otherwise False.

        Raises:
            UnknownHealthcheckException: If an unknown health check type is specified in the HealthCheckOptions.
        """

        if self.get_status(vm) == VMState.RUNNING:
            if hc is not None and hc.target_url is not None:
                try:
                    return self._host_validator.validate(hc)
                except UnknownHealthcheckException as ex:
                    LOGGER.error(f"VM [{vm.vm_id}]: Unknown healthcheck type: {ex}")
                    return True

            LOGGER.info(f"VM [{vm.vm_id}]: State is running. HealthCheckOptions is not provided.")
            return True
        else:
            return False

    def get_status(self, vm: ProxmoxVMInfo) -> str:
        """ Return current running status of VM """

        return self._px_client.get_status(vm.node, vm.vm_type, vm.vm_id)["status"]

    def start_vm(self, vm: ProxmoxVMInfo) -> None:
        """
        Initiates the startup of a specific VM.

        Args:
            vm (ProxmoxVMInfo): VM information including the type and ID.
        """

        self._px_client.start_vm(vm.node, vm.vm_type, vm.vm_id)

    def get_vms_to_start(self, start_options: [VMStartOptions]) -> [VMStartOptions]:
        """
        Filters and returns a list of VMs that are enabled and ready to be started based on dependencies.

        Args:
            start_options (List[VMStartOptions]): List of VM startup options.

        Returns:
            List[VMStartOptions]: VMs ready to be started.
        """

        return start_options

    def clean_up(self, start_options, px_vms: [int, ProxmoxVMInfo]) -> None:
        for start_item in start_options:
            if start_item.vm_id not in px_vms:
                continue

            LOGGER.debug(f"VM [{start_item.vm_id}]: Shutdown.")

            vm_to_start = px_vms[start_item.vm_id]
            try:
                self._px_client.stop_vm(vm_to_start.node, vm_to_start.vm_type, vm_to_start.vm_id)
            except ProxmoxException as ex:
                LOGGER.warn(f"Error occurred during stop vm: {ex}")

    def notification_log(self, vm: ProxmoxVMInfo, status, start_time, duration):
        if self._notification_manager is not None:
            self._notification_manager.append_status(vm.vm_type, vm.vm_id, vm.name, status, start_time, duration)
