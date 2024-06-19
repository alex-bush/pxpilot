import enum
from dataclasses import dataclass, field
from typing import List, Optional


class HealthcheckType(enum.StrEnum):
    PING = "ping"
    HTTP = "http"


@dataclass
class HealthCheckOptions:
    target_url: str
    check_method: HealthcheckType = HealthcheckType.PING


@dataclass
class StartOptions:
    await_running: bool = False
    startup_timeout: int = 120


@dataclass
class VmStartOptions:
    vm_id: int
    enabled: bool = True
    startup_parameters: StartOptions = field(default_factory=StartOptions)
    dependencies: List[int] = field(default_factory=list)
    healthcheck: Optional[HealthCheckOptions] = None
