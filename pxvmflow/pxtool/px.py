from dataclasses import dataclass

import proxmoxer
from proxmoxer import ProxmoxAPI, ResourceException

from pxvmflow.consts import ProxmoxCommand, VMType
from pxvmflow.exceptions import ProxmoxError

__all__ = ["ProxmoxVMInfo", "ProxmoxClient"]


@dataclass
class ProxmoxVMInfo:
    vm_id: int
    vm_type: VMType
    name: str
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

        self.build_client()

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

    def px_get(self, command):
        """ Execute GET request using proxmoxer """

        try:
            return self._proxmox(command).get()
        except ResourceException as ex:
            raise ProxmoxError(ex.content)

    def px_post(self, command):
        """ Execute POST request using proxmoxer """

        try:
            return self._proxmox(command).post()
        except ResourceException as ex:
            raise ProxmoxError(ex.content)

    def start_vm(self, node, vm_type, vm_id):
        """
        Start virtual machine.
        :param node: The cluster node name.
        :param vm_type: lxc/qemu
        :param vm_id: The (unique) ID of the VM.
        """
        self.px_post(f"nodes/{node}/{vm_type}/{vm_id}/status/{ProxmoxCommand.START}")

    def stop_vm(self, node, vm_type, vm_id):
        self.px_post(f"nodes/{node}/{vm_type}/{vm_id}/status/{ProxmoxCommand.SHUTDOWN}")

    def get_status(self, node, vm_type, vm_id):
        """
        Get virtual machine status.
        :param node: The cluster node name.
        :param vm_type: lxc/qemu
        :param vm_id: The (unique) ID of the VM.
        :return: Status of requested LXC/VM(qemu)
        """
        return self.px_get(f"nodes/{node}/{vm_type}/{vm_id}/status/{ProxmoxCommand.CURRENT}")
