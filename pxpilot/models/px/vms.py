from dataclasses import dataclass
from typing import Optional

from pxpilot.models.configuration.vm_start_settings import VmStartOptions
from pxpilot.pxtool import VirtualMachine
from pxpilot.vm_management.models import StartStatus


@dataclass
class VMContext:
    """
    Combined object for storing all information about VM

    Attributes:
        vm_id (int): ID of virtual machine
        vm_launch_settings (VMLaunchSettings): virtual machine startup settings
        vm_info (VirtualMachine): virtual machine info from Proxmox
        status: last known status or current vm status
    """
    vm_id: int
    vm_launch_settings: Optional[VmStartOptions]
    vm_info: Optional[VirtualMachine]
    status: StartStatus = StartStatus.UNKNOWN
