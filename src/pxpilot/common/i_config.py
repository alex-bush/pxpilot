from enum import Enum
from typing import Protocol, List, Dict

from pxpilot.models.configuration.app_settings import AppSettings, ProxmoxSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions


class ConfigType(Enum):
    yaml = 1
    ruamel = 2


class IConfig(Protocol):
    """
    Interface(protocol) for config providers.
    """
    def check_config(self) -> bool:
        pass

    def get_app_config(self) -> AppSettings:
        """ Get all AppSettings"""
        pass

    def load_px_settings(self) -> ProxmoxSettings:
        """ Get proxmox connection settings """
        pass

    def load_notifications_settings(self) -> Dict[str, Dict]:
        """ Get notification settings for telegram and email """
        pass

    def load_start_vms_settings(self) -> List[VmStartOptions]:
        """ Get start vms settings """
        pass

    def save_px_settings(self, px_settings: ProxmoxSettings):
        """ Save proxmox connection settings """
        pass

    def save_notifications_settings(self, settings: Dict[str, Dict]):
        """ Save notification settings """
        pass

    def save_start_vms_settings(self, vms: List[VmStartOptions]):
        """ Save start vms settings """
        pass

    def reload_settings(self):
        """ Reload app settings from the storage """
        pass
