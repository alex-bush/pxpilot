import time

from pxvmflow.pxtool import ProxmoxClient
from pxvmflow.models import PxEntity, EntityType


def get_entity_path(entity_type):
    """  Returns the URL path segment for either an LXC container or a QEMU VM based on the provided entity type. """
    return "lxc" if entity_type == EntityType.LXC else "qemu"


class Executor:
    _px_client: ProxmoxClient

    def __init__(self, config):
        self._host = config.PROXMOX_URL
        self._port = config.PROXMOX_PORT
        self._user = config.PROXMOX_USER
        self._realm = config.PROXMOX_REALM
        self._password = config.PROXMOX_PASSWORD
        self._verify_ssl = config.VERIFY_SSL

    def start(self):
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
            entity_path = get_entity_path(entity_type)

            return [PxEntity(id=int(entity["vmid"]), type=entity_type, status=entity["status"], node=node)
                    for entity in self._px_client.get(f"nodes/{node}/{entity_path}")]

        entities = []
        entities.extend(fetch_entities(EntityType.LXC))
        entities.extend(fetch_entities(EntityType.VM))

        return entities

    def get_status(self, vm: PxEntity):
        entity_path = get_entity_path(vm.type)
        state = self._px_client.get(f"nodes/{vm.node}/{entity_path}/{vm.id}/status/current")
        print(state)
        return state['status']

    def start_vm(self, vm: PxEntity):
        entity_path = get_entity_path(vm.type)
        self._px_client.post(f"nodes/{vm.node}/{entity_path}/{vm.id}/status/start")

    def is_running(self, vm: PxEntity):
        return self.get_status(vm) == "running"

    def main_loop(self, entities: list[PxEntity]):
        for vm in entities:
            if vm.status == "stopped":
                flag = True
                self.start_vm(vm)

                while flag:
                    if self.is_running(vm):
                        flag = False
                        print(f"{time.time()}: VM id={vm.id} successfully started.")
                    else:
                        print(f"{time.time()}: VM id={vm.id} is being started.")

                    time.sleep(5)
