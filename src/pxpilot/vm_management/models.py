from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Optional


class StartStatus(Enum):
    UNKNOWN = auto()
    OK = auto()

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
    """
    Start result with start status, error message and start/end time
    """
    status: StartStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    message: Optional[str] = None
