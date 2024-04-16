import time

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
            vm_to_start: ProxmoxVMInfo = px_vms[start_item.id]
            LOGGER.debug(
                f"VM [{vm_to_start.id}]: Shutdown.")
            self._px_client.stop_vm(vm_to_start.node, vm_to_start.type, vm_to_start.id)

    def is_running(self, vm: ProxmoxVMInfo, hc: HealthCheckOptions):
        """ retrieve the status of VM/LXC and check that VM/LXC is running """

        if self.get_status(vm) == ProxmoxState.RUNNING:
            if hc is not None and hc.address is not None:
                return HostValidator().validate(hc)
            LOGGER.debug(f"VM [{vm.id}]: HealthCheckOptions is missing.")
            return True
        else:
            return False

    def start_vms(self, start_options, px_vms: [int, ProxmoxVMInfo]):
        for start_item in start_options:
            vm_to_start = px_vms[start_item.id]

            if not start_item.enabled:
                LOGGER.debug(f"VM [{vm_to_start.id}]: Disabled. Skipped.")
                continue

            if vm_to_start.status == ProxmoxState.STOPPED:
                LOGGER.debug(f"VM [{vm_to_start.id}]: Start.")
                self.start_vm(vm_to_start)

                if start_item.run_timeout is not None:
                    time.sleep(start_item.run_timeout)

                flag = True
                while flag:
                    if self.is_running(vm_to_start, start_item.healthcheck):
                        flag = False
                        LOGGER.debug(f"VM [{vm_to_start.id}]: Successfully started.")
                    else:
                        LOGGER.debug(f"VM [{vm_to_start.id}]: Starting...")

                    time.sleep(5)
            else:
                LOGGER.debug(f"VM [{vm_to_start.id}]: Already started. No action needed.")
