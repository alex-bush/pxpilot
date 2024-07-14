from dataclasses import dataclass
from enum import StrEnum


class ProxmoxVMFields:
    VM_ID = "vmid"
    VM_NAME = "name"
    VM_STATUS = "status"


class VMType(StrEnum):
    """
    Types of virtual environments managed by Proxmox.

    Attributes:
        LXC (str): Represents a Linux container managed by Proxmox.
        QEMU (str): Represents a full virtual machine managed by Proxmox using QEMU.
    """

    LXC = "lxc"
    QEMU = "qemu"


class VMState(StrEnum):
    """
    Possible states of virtual machines managed by Proxmox.

    Attributes:
        RUNNING (str): The state indicating that the VM/LXC is currently active and running.
        STOPPED (str): The state indicating that the VM/LXC is currently inactive and not running.
    """

    RUNNING = "running"
    STOPPED = "stopped"


@dataclass
class VirtualMachine:
    vm_id: int
    vm_type: VMType
    name: str
    status: VMState
    node: str


class ProxmoxCommand(StrEnum):
    """
    Supported api commands for managing the state of VMs/LXCs in a Proxmox environment.

    Attributes:
        CURRENT (str): A command to retrieve the current status of a VM/LXC.
        START (str): A command to start a stopped VM/LXC.
        SHUTDOWN (str): A command to gracefully shut down a running VM/LXC.
    """

    CURRENT = "current"
    START = "start"
    SHUTDOWN = "shutdown"
