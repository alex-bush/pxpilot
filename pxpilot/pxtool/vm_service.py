from typing import Protocol

from .models import VMState, VirtualMachine


class VMService(Protocol):
    def get_vm_status(self, vm: VirtualMachine) -> VMState:
        pass

    def start_vm(self, vm: VirtualMachine) -> None:
        pass

    def stop_sm(self, vm: VirtualMachine) -> None:
        pass

    def get_all_vms(self, node) -> dict[int, VirtualMachine]:
        pass
