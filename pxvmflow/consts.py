from enum import Enum, StrEnum


class ProxmoxType(StrEnum):
    """ Types of virtual environments managed by Proxmox. """

    LXC = "lxc"
    QEMU = "qemu"


class ProxmoxState(StrEnum):
    """ States of VM/LXC """

    RUNNING = "running"
    STOPPED = "stopped"


class ProxmoxCommand(StrEnum):
    """ Supported proxmox commands """
    CURRENT = "current"
    START = "start"

