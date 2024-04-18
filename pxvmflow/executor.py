import time

from pxvmflow.config import ProxmoxConfig, HealthCheckOptions
from pxvmflow.consts import ProxmoxType, ProxmoxState
from pxvmflow.exceptions import UnknownHealthcheckException, ProxmoxException
from pxvmflow.logging_config import LOGGER
from pxvmflow.pxtool import *
from pxvmflow.host_validator import HostValidator


class Executor:
    """ Main logic class """

    _px_client: ProxmoxClient = None
    _config: ProxmoxConfig = None

    def __init__(self, config: ProxmoxConfig):
        self._host = config.url
        self._port = config.port
        self._user = config.user
        self._realm = config.realm
        self._password = config.password
        self._verify_ssl = config.verify_ssl

        self._config = config

    def start(self):
        """ entry point """

        if len(self._config.start_options) == 0 or sum(1 for item in self._config.start_options if item.enabled) == 0:
            LOGGER.info(F"There is no available virtual machine to start in configuration. Exiting...")
            return

        if self._px_client is None:
            self._px_client = ProxmoxClient(self._host, self._port, user=self._user, realm=self._realm,
                                        password=self._password, verify_ssl=self._verify_ssl)

        sta = self.get_vms_to_start(self._config.start_options)

        px_vms = self.get_all_vm(self._px_client.px_get("nodes")[0]["node"])

        self.start_vms(sta, px_vms)

        self.clean_up(sta, px_vms)

    def get_vms_to_start(self, start_options):
        """ Prepare a list of virtual machines to start by dependencies """

        return start_options

    def get_all_vm(self, node) -> dict[int, ProxmoxVMInfo]:
        """ Get actual vm list from proxmox """

        def fetch_entities(vm_type):
            return [ProxmoxVMInfo(vm_id=int(entity["vmid"]), vm_type=vm_type, status=entity["status"], node=node)
                    for entity in self._px_client.px_get(f"nodes/{node}/{vm_type}")]

        entities = dict()
        for lxc in fetch_entities(ProxmoxType.LXC):
            entities[lxc.vm_id] = lxc
        for qemu in fetch_entities(ProxmoxType.QEMU):
            entities[qemu.vm_id] = qemu

        return entities

    def get_status(self, vm: ProxmoxVMInfo) -> str:
        """ Return current running status of VM """

        return self._px_client.get_status(vm.node, vm.vm_type, vm.vm_id)["status"]

    def start_vm(self, vm: ProxmoxVMInfo) -> None:
        """ Start VM """

        self._px_client.start_vm(vm.node, vm.vm_type, vm.vm_id)

    def clean_up(self, start_options, px_vms: [int, ProxmoxVMInfo]) -> None:
        for start_item in start_options:
            LOGGER.debug(f"VM [{start_item.vm_id}]: Shutdown.")

            vm_to_start = px_vms[start_item.vm_id]
            try:
                self._px_client.stop_vm(vm_to_start.node, vm_to_start.vm_type, vm_to_start.vm_id)
            except ProxmoxException as ex:
                LOGGER.warn(f"Error occurred during stop vm: {ex}")

    def is_running(self, vm: ProxmoxVMInfo, hc: HealthCheckOptions) -> bool:
        """ retrieve the status of VM/LXC and check that VM/LXC is running """

        if self.get_status(vm) == ProxmoxState.RUNNING:
            if hc is not None and hc.target_url is not None:
                try:
                    return HostValidator().validate(hc)
                except UnknownHealthcheckException as ex:
                    LOGGER.error(f"VM [{vm.vm_id}]: Validation error: {ex}")
                    return True

            LOGGER.info(f"VM [{vm.vm_id}]: State is running. HealthCheckOptions is not provided.")
            return True
        else:
            return False

    def start_vms(self, start_options, px_vms: [int, ProxmoxVMInfo]) -> None:
        """

        :param start_options: list of VMStartOptions contains settings for start Vms
        :param px_vms: List of information about existing VMs from proxmox
        """
        for start_item in start_options:
            vm_to_start = px_vms[start_item.vm_id]

            if not start_item.enabled:
                LOGGER.info(f"VM [{vm_to_start.vm_id}]: Starting disabled in config. Skipped.")
                continue

            if vm_to_start.status != ProxmoxState.STOPPED:
                LOGGER.info(f"VM [{vm_to_start.vm_id}]: Virtual machine already started. No action needed.")
                continue

            LOGGER.debug(f"VM [{vm_to_start.vm_id}]: Starting virtual machine.")
            self.start_vm(vm_to_start)

            # if start_item.run_timeout is not None:
            #     time.sleep(start_item.run_timeout)

            flag = True
            while flag:
                if self.is_running(vm_to_start, start_item.healthcheck):
                    flag = False
                    LOGGER.info(f"VM [{vm_to_start.vm_id}]: Virtual machine successfully started.")
                else:
                    LOGGER.info(f"VM [{vm_to_start.vm_id}]: The host is not yet available. Waiting...")

                time.sleep(5)
