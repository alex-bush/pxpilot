from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Optional

from pxpilot.config import VMLaunchSettings
from pxpilot.pxtool import VirtualMachine


class StartStatus(Enum):
    UNKNOWN = auto()
    OK = auto

    STARTING = auto()
    STARTED = auto()
    ALREADY_STARTED = auto()
    STOPPED = auto()
    TIMEOUT = auto()
    FAILED = auto()

    INFO_MISSED = auto()
    DISABLED = auto()
    DEPENDENCY_FAILED = auto()


@dataclass
class StartResult:
    status: StartStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    message: Optional[str] = None


@dataclass
class VMContext:
    vm_id: int
    vm_launch_settings: Optional[VMLaunchSettings]
    vm_info: Optional[VirtualMachine]
    status: StartStatus = StartStatus.UNKNOWN
