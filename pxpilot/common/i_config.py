from enum import Enum
from typing import Protocol, Any, List

from pxpilot.models.configuration.app_settings import AppSettings, ProxmoxSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions


class ConfigType(Enum):
    yaml = 1
    ruamel = 2


class IConfig(Protocol):
    def get_app_config(self) -> AppSettings: pass

    def load_px_settings(self) -> ProxmoxSettings: pass

    def load_notifications_settings(self) -> Any: pass

    def load_start_vms_settings(self) -> List[VmStartOptions]: pass

    def save_px_settings(self, px_settings: ProxmoxSettings): pass

    def save_notifications_settings(self): pass

    def save_start_vms_settings(self, vms: List[VmStartOptions]): pass
