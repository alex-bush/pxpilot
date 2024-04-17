import time

from pxvmflow.exceptions import UnknownHealthcheckException
from pxvmflow.pxtool import ProxmoxClient
from pxvmflow.consts import *
from pxvmflow.host_validator import HostValidator
from pxvmflow.config import *
from pxvmflow.pxtool.px import ProxmoxVMInfo


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

        px_vms = self.get_all_vm(self._px_client.get("nodes")[0]["node"])

        self.start_vms(self._config.start_options, px_vms)

        self.clean_up(self._config.start_options, px_vms)

    def get_all_vm(self, node) -> dict[int, ProxmoxVMInfo]:
        """ Get actual vm list from proxmox """

        def fetch_entities(entity_type):
            return [ProxmoxVMInfo(id=int(entity["vmid"]), type=entity_type, status=entity["status"], node=node)
                    for entity in self._px_client.get(f"nodes/{node}/{entity_type}")]

        entities = dict()
        for lxc in fetch_entities(ProxmoxType.LXC):
            entities[lxc.id] = lxc
        for qemu in fetch_entities(ProxmoxType.QEMU):
            entities[qemu.id] = qemu

        return entities

    def get_status(self, vm: ProxmoxVMInfo) -> str:
        """ Return current running status of VM """

        return self._px_client.get_status(vm.node, vm.type, vm.id)["status"]

    def start_vm(self, vm: ProxmoxVMInfo):
        """ Start VM """

        self._px_client.start_vm(vm.node, vm.type, vm.id)

    def clean_up(self, start_options, px_vms: [int, ProxmoxVMInfo]):
        for start_item in start_options:
            LOGGER.debug(f"VM [{start_item.id}]: Shutdown.")

            vm_to_start = px_vms[start_item.id]
            from proxmoxer import ResourceException
            try:
                self._px_client.stop_vm(vm_to_start.node, vm_to_start.type, vm_to_start.id)
            except ResourceException as ex:
                LOGGER.warn(f"Error occurred during stop vm: {ex.content}")

    def is_running(self, vm: ProxmoxVMInfo, hc: HealthCheckOptions):
        """ retrieve the status of VM/LXC and check that VM/LXC is running """

        if self.get_status(vm) == ProxmoxState.RUNNING:
            if hc is not None and hc.address is not None:
                try:
                    return HostValidator().validate(hc)
                except UnknownHealthcheckException as ex:
                    LOGGER.error(f"VM [{vm.id}]: Validation error: {ex}")
                    return True

            LOGGER.debug(f"VM [{vm.id}]: HealthCheckOptions is not provided.")
            return True
        else:
            return False

    def start_vms(self, start_options, px_vms: [int, ProxmoxVMInfo]):
        """

        :param start_options: list of VMStartOptions contains settings for start Vms
        :param px_vms: List of information about existing VMs from proxmox
        """
        for start_item in start_options:
            vm_to_start = px_vms[start_item.id]

            if not start_item.enabled:
                LOGGER.debug(f"VM [{vm_to_start.id}]: Starting disabled in config. Skipped.")
                continue

            if vm_to_start.status != ProxmoxState.STOPPED:
                LOGGER.info(f"VM [{vm_to_start.id}]: Virtual machine already started. No action needed.")
                continue

            LOGGER.debug(f"VM [{vm_to_start.id}]: Start virtual machine.")
            self.start_vm(vm_to_start)

            if start_item.run_timeout is not None:
                time.sleep(start_item.run_timeout)

            flag = True
            while flag:
                if self.is_running(vm_to_start, start_item.healthcheck):
                    flag = False
                    LOGGER.info(f"VM [{vm_to_start.id}]: Virtual machine successfully started.")
                else:
                    LOGGER.debug(f"VM [{vm_to_start.id}]: Host is unreachable. Waiting...")

                time.sleep(5)
