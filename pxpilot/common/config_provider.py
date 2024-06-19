from threading import Lock
from typing import Dict, Any, List, Optional

import yaml

from pxpilot.common.i_config import IConfig
from pxpilot.models.configuration.app_settings import ProxmoxSettings, AppSettings, CommonSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions, HealthCheckOptions, HealthcheckType, \
    StartOptions


class ConfigProvider(IConfig):
    _instance: Optional[IConfig] = None
    _lock: Lock = Lock()

    def __init__(self, file_path: str):
        if ConfigProvider._instance is not None:
            raise Exception("For use ConfigProvider use get_instance first.")

        self.file_path = file_path

    @classmethod
    def get_instance(cls, file_path: str) -> IConfig:
        with cls._lock:
            if cls._instance is None:
                cls._instance = ConfigProvider(file_path)

            return cls._instance

    def get_app_config(self) -> AppSettings:
        proxmox_settings = self.load_px_settings()
        notifications_settings = self.load_notifications_settings()
        start_vms_settings = self.load_start_vms_settings()
        common_settings = CommonSettings(**self._load_yaml_config(self.file_path).get("settings", {}))

        app_settings = AppSettings(
            proxmox_settings=proxmox_settings,
            notification_settings=notifications_settings,
            start_vms_settings=start_vms_settings, app_settings=common_settings)

        return app_settings

    def load_px_settings(self) -> ProxmoxSettings:
        config_data = self._load_yaml_config(self.file_path)

        proxmox_config = ProxmoxSettings()
        proxmox_config.px_settings = self._load_section(config_data, "proxmox_config",
                                                        None)  # config_data.get("proxmox_config", None)

        return proxmox_config

    def load_notifications_settings(self) -> Any:
        config_data = self._load_yaml_config(self.file_path)
        notification_settings = self._load_section(config_data, "notification_options",
                                                   {})  # config_data.get("notification_options", {})

        return notification_settings

    def load_start_vms_settings(self) -> List[VmStartOptions]:
        vms = []
        config_data = self._load_yaml_config(self.file_path)

        for vm_data in self._load_section(config_data, "vms", []):
            # Extract and parse nested configurations
            healthcheck_data = vm_data.pop("healthcheck", None)
            startup_data = vm_data.pop("startup_parameters", None)

            healthcheck = self._parse_healthcheck(healthcheck_data)
            startup_parameters = self._parse_startup_parameters(startup_data)

            vm = VmStartOptions(
                **vm_data,
                healthcheck=healthcheck,
                startup_parameters=startup_parameters
            )
            vms.append(vm)
        return vms

    def save_px_settings(self, px_settings: ProxmoxSettings):
        pass

    def save_notifications_settings(self):
        pass

    def save_start_vms_settings(self, vms: List[VmStartOptions]):
        pass

    @staticmethod
    def _load_section(config_data, section: str, tp):
        return config_data.get(section, tp)

    @staticmethod
    def _load_yaml_config(path: str) -> Dict[str, Any]:
        """Helper function to load a YAML configuration file."""
        with open(path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def _parse_healthcheck(healthcheck_data: Dict[str, Any]) -> Optional[HealthCheckOptions]:
        """Parse health check data into a HealthCheckOptions object."""
        if healthcheck_data:
            healthcheck_type = HealthcheckType[healthcheck_data["check_method"].upper()]
            return HealthCheckOptions(target_url=healthcheck_data["target_url"], check_method=healthcheck_type)
        return None

    @staticmethod
    def _parse_startup_parameters(startup_data: Dict[str, Any]) -> Optional[StartOptions]:
        """Parse startup parameters data into a StartupParameters object."""
        if startup_data:
            return StartOptions(
                await_running=startup_data.get("await_running", False),
                startup_timeout=startup_data.get("startup_timeout", 0)
            )
        return StartOptions()
