import time

from pxvmflow.pxtool import ProxmoxClient
from pxvmflow.models import PxEntity
from pxvmflow.consts import *
from pxvmflow.host_validator import HostValidator, ValidationType
from pxvmflow.config import *


class Executor:
    """ Main logic class """

    _px_client: ProxmoxClient

    def __init__(self, config: ProxmoxConfig):
        self._host = config.url
        self._port = config.port
        self._user = config.user
        self._realm = config.realm
        self._password = config.password
        self._verify_ssl = config.verify_ssl

    def start(self):
        """ entry point """

        client = ProxmoxClient(self._host, self._port, user=self._user, realm=self._realm,
                               password=self._password, verify_ssl=self._verify_ssl)
        self._px_client = client.build_client()

        entities = self.get_all_vm(client.get("nodes")[0]["node"])

        for e in entities:
            print(e.id, ": ", self.get_status(e))

        print(entities)

        self.main_loop(entities)

    def get_all_vm(self, node) -> list[PxEntity]:
        def fetch_entities(entity_type):
            return [PxEntity(id=int(entity["vmid"]), type=entity_type, status=entity["status"], node=node)
                    for entity in self._px_client.get(f"nodes/{node}/{entity_type}")]

        entities = []
        entities.extend(fetch_entities(ProxmoxType.LXC))
        entities.extend(fetch_entities(ProxmoxType.QEMU))

        return entities

    def get_status(self, vm: PxEntity) -> str:
        """ get status of VM/LXC """

        state = self._px_client.get(f"nodes/{vm.node}/{vm.type}/{vm.id}/status/{ProxmoxCommand.CURRENT}")
        print(state)
        return state['status']

    def start_vm(self, vm: PxEntity):
        self._px_client.post(f"nodes/{vm.node}/{vm.type}/{vm.id}/status/{ProxmoxCommand.START}")

    def is_running(self, vm: PxEntity):
        """ retrieve the status of VM/LXC and check that VM/LXC is running """

        if self.get_status(vm) == ProxmoxState.RUNNING:
            return HostValidator.validate("192.168.1.1", ValidationType.PING)
        else:
            return False

    def main_loop(self, entities: list[PxEntity]):
        """ run list of VM/LXC and wait for start is complete """

        for vm in entities:
            if vm.status == ProxmoxState.STOPPED:
                flag = True
                self.start_vm(vm)

                while flag:
                    if self.is_running(vm):
                        flag = False
                        print(f"{time.time()}: VM id={vm.id} successfully started.")
                    else:
                        print(f"{time.time()}: VM id={vm.id} is being started.")

                    time.sleep(5)
