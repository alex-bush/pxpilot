from dataclasses import dataclass

import proxmoxer
from proxmoxer import ProxmoxAPI

from pxvmflow.consts import ProxmoxCommand, ProxmoxType


@dataclass
class ProxmoxVMInfo:
    id: int
    type: ProxmoxType
    status: str
    node: str


class ProxmoxClient:
    _proxmox: ProxmoxAPI

    def __init__(self, host, port, user, realm, password, verify_ssl):
        self._host = host
        self._port = port
        self._user = user
        self._realm = realm
        self._password = password
        self._verify_ssl = verify_ssl

    def build_client(self) -> None:
        if "@" in self._user:
            user_id = self._user
        else:
            user_id = f"{self._user}@{self._realm}"

        self._proxmox = proxmoxer.ProxmoxAPI(
            self._host,
            port=self._port,
            user=user_id,
            password=self._password,
            verify_ssl=self._verify_ssl,
            timeout=30,
        )

    def get_client(self):
        return self._proxmox

    def get(self, command):
        return self._proxmox(command).get()

    def post(self, command):
        return self._proxmox(command).post()

    def start_vm(self, node, type, id):
        self.post(f"nodes/{node}/{type}/{id}/status/{ProxmoxCommand.START}")

    def stop_vm(self, node, type, id):
        self.post(f"nodes/{node}/{type}/{id}/status/{ProxmoxCommand.SHUTDOWN}")

    def get_status(self, node, type, id):
        return self.get(f"nodes/{node}/{type}/{id}/status/{ProxmoxCommand.CURRENT}")
