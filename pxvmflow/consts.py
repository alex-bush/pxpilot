from enum import Enum, StrEnum

STATUS_POLL_INTERVAL = 2


class VMType(StrEnum):
    """
    Enumerates the types of virtual environments managed by Proxmox.

    Attributes:
        LXC (str): Represents a Linux container managed by Proxmox.
        QEMU (str): Represents a full virtual machine managed by Proxmox using QEMU.
    """

    LXC = "lxc"
    QEMU = "qemu"


class VMState(StrEnum):
    """
    Defines the possible states of virtual machines (VMs) or Linux containers (LXCs) managed by Proxmox.

    Attributes:
        RUNNING (str): The state indicating that the VM/LXC is currently active and running.
        STOPPED (str): The state indicating that the VM/LXC is currently inactive and not running.
    """

    RUNNING = "running"
    STOPPED = "stopped"


class ProxmoxCommand(StrEnum):
    """
    Lists the supported commands for managing the state of VMs/LXCs in a Proxmox environment.

    Attributes:
        CURRENT (str): A command to retrieve the current status of a VM/LXC.
        START (str): A command to start a stopped VM/LXC.
        SHUTDOWN (str): A command to gracefully shut down a running VM/LXC.
    """

    CURRENT = "current"
    START = "start"
    SHUTDOWN = "shutdown"
