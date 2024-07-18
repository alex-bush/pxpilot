from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List

from pxpilot.models.configuration.vm_start_settings import VmStartOptions


@dataclass
class ProxmoxSettings:
    px_settings: Dict[str, str] = field(default_factory=dict)


@dataclass
class CommonSettings:
    auto_start_dependency: bool = False
    auto_shutdown: bool = False
    self_host: Optional[Dict[str, Any]] = None


@dataclass
class AppSettings:
    app_settings: CommonSettings = None

    proxmox_settings: ProxmoxSettings = None

    start_vms_settings: List[VmStartOptions] = None

    notification_settings: Dict[str, Any] = None


@dataclass
class User:
    username: str
    token: str
