import proxmoxer
from proxmoxer import ProxmoxAPI, ResourceException
from requests.exceptions import SSLError

from core.tools.retry import retry
from .models import ProxmoxCommand, VMType, VirtualMachine, VMState
from core.exceptions.exceptions import ProxmoxError, ProxmoxConfigurationError, FatalProxmoxError

from .models import ProxmoxVMFields
from .vm_service import VMService


def create_vm_service(config) -> VMService:
    return ProxmoxClient(**config)


class ProxmoxClient(VMService):
    """ Proxmoxer client """

    _proxmox: ProxmoxAPI

    def __init__(self, **kwargs):
        self._build_client(**kwargs)

    def _build_client(self, **kwargs) -> None:
        if "token" in kwargs:
            try:
                user, token_name = kwargs.pop("token").split("!")
                kwargs["user"] = user
                kwargs["token_name"] = token_name
            except ValueError:
                raise ProxmoxConfigurationError("Configuration problem: error on parsing token. Expected format: 'user@pve!token'")

        self._proxmox = proxmoxer.ProxmoxAPI(host=kwargs.pop("host"), **kwargs)

    def start_vm(self, vm: VirtualMachine) -> None:
        """
        Initiates the startup of a specific VM.

        Args:
            vm (VirtualMachine): VM to start.
        """

        self._px_post(f"nodes/{vm.node}/{vm.vm_type}/{vm.vm_id}/status/{ProxmoxCommand.START}")

    def get_vm_status(self, vm: VirtualMachine) -> VMState:
        """ Return current running status of VM """

        status = self._px_get(f"nodes/{vm.node}/{vm.vm_type}/{vm.vm_id}/status/{ProxmoxCommand.CURRENT}")
        return VMState(status[ProxmoxVMFields.VM_STATUS])

    def get_all_vms(self, node: str | None = None) -> dict[int, VirtualMachine]:
        """
        Retrieves a list of all VMs from a specified node.

        Args:
            node (str): Node identifier in the Proxmox environment.
            If not specified, VMs from all nodes will be returned.

        Returns:
            Dict[int, VirtualMachine]: Dictionary of VM list.
        """

        def fetch_by_type(vm_type, node_name):
            return [
                VirtualMachine(vm_id=int(vm[ProxmoxVMFields.VM_ID]), vm_type=vm_type, name=vm[ProxmoxVMFields.VM_NAME],
                               status=VMState(vm[ProxmoxVMFields.VM_STATUS]), node=node_name)
                for vm in self._px_get(f"nodes/{node_name}/{vm_type}")]

        def fetch_all(node_name):
            result = dict()
            for lxc in fetch_by_type(VMType.LXC, node_name):
                result[lxc.vm_id] = lxc
            for qemu in fetch_by_type(VMType.QEMU, node_name):
                result[qemu.vm_id] = qemu
            return result

        vms = dict()
        px_nodes = []
        if node is None:
            px_nodes.extend([px_node["node"] for px_node in self._px_get("nodes") if px_node["status"] == "online"])
        else:
            px_nodes.append(node)

        for n in px_nodes:
            vms.update(fetch_all(n))

        return vms

    def stop_vm(self, vm: VirtualMachine):
        self._px_post(f"nodes/{vm.node}/{vm.vm_type}/{vm.vm_id}/status/{ProxmoxCommand.SHUTDOWN}")

    def test_connection(self):
        return self._proxmox("version").get()

    @retry(tries=5, delay=5, excludes=(SSLError, ResourceException, ProxmoxError,))
    def _px_get(self, command):
        """ Execute GET request using proxmoxer """

        try:
            return self._proxmox(command).get()
        except SSLError:
            raise FatalProxmoxError("An SSL error occurred.")
        except ResourceException as ex:
            raise ProxmoxError(ex)

    @retry(tries=5, delay=5, excludes=(SSLError, ResourceException, ProxmoxError,))
    def _px_post(self, command):
        """ Execute POST request using proxmoxer """

        try:
            return self._proxmox(command).post()
        except ResourceException as ex:
            raise ProxmoxError(ex.content)
