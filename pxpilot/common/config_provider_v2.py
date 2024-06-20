from threading import Lock
from typing import Any, List, Optional, Dict

from ruamel.yaml import YAML

from pxpilot.common import IConfig
from pxpilot.common.constants import ConfigSections
from pxpilot.models.configuration.app_settings import ProxmoxSettings, AppSettings, CommonSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions, HealthCheckOptions, StartOptions, \
    HealthcheckType


class ConfigProviderV2(IConfig):
    _instance: Optional[IConfig] = None
    _lock: Lock = Lock()
    _file_path: str = None
    _app_config: AppSettings = None
    _yaml_data: None

    def __init__(self, file_path: str):
        if ConfigProviderV2._instance is not None:
            raise Exception("For use ConfigProvider use get_instance first.")

        self._file_path = file_path
        self.reload_settings()

    @classmethod
    def get_instance(cls, file_path: str) -> IConfig:
        with cls._lock:
            if cls._instance is None:
                cls._instance = ConfigProviderV2(file_path)

            return cls._instance

    @property
    def app_config(self) -> AppSettings:
        if self._app_config is None:
            self.reload_settings()

        return self._app_config

    def get_app_config(self) -> AppSettings:
        return self.app_config

    def load_px_settings(self) -> ProxmoxSettings:
        return self.app_config.proxmox_settings

    def load_notifications_settings(self) -> Any:
        return self.app_config.notification_settings

    def load_start_vms_settings(self) -> List[VmStartOptions]:
        return self.app_config.start_vms_settings

    def save_px_settings(self, px_settings: ProxmoxSettings):
        self._yaml_data[ConfigSections.PROXMOX_CONFIG] = px_settings.px_settings
        for key, value in px_settings.px_settings.items():
            if self._yaml_data[ConfigSections.PROXMOX_CONFIG][key] != value:
                self._yaml_data[ConfigSections.PROXMOX_CONFIG][key] = value

        self._save_config(self._file_path, self._yaml_data)

    def save_notifications_settings(self, settings: Dict[str, Dict]):
        for key, value in settings.items():
            for i_key, i_value in value.items():
                self._yaml_data[ConfigSections.NOTIFICATION_OPTIONS][key][i_key] = i_value

        self._save_config(self._file_path, self._yaml_data)

    def save_start_vms_settings(self, vms: List[VmStartOptions]):
        pass

    def reload_settings(self):
        self._app_config, self._yaml_data = self._load_settings(self._file_path)

    def _save_config(self, file_name, data, reload: bool = True):
        yaml = YAML()
        with open(file_name, "w") as file:
            yaml.dump(data, file)

        if reload:
            self.reload_settings()

    @staticmethod
    def _load_settings(path: str) -> (AppSettings, Any):
        yaml = YAML()
        with open(path, "r") as file:
            data = yaml.load(file)

            proxmox_config = dict(**data[ConfigSections.PROXMOX_CONFIG])

            settings = CommonSettings(**data[ConfigSections.COMMON_SETTINGS])

            notification_settings = {key: dict(**value) for key, value in data[ConfigSections.NOTIFICATION_OPTIONS].items() if
                                     isinstance(value, dict)}

            vms = []
            for vm_data in data['vms']:
                healthcheck_data = vm_data.get('healthcheck')
                healthcheck = None
                if healthcheck_data:
                    h_data = healthcheck_data.copy()
                    if 'check_method' in h_data and isinstance(h_data['check_method'], str):
                        h_data['check_method'] = HealthcheckType(h_data['check_method'])

                    healthcheck = HealthCheckOptions(**h_data)

                startup_parameters_data = vm_data.get(ConfigSections.STARTUP_PARAMETERS, {})
                startup_parameters = StartOptions(**startup_parameters_data)

                vm = VmStartOptions(**vm_data)
                vm.healthcheck = healthcheck
                vm.startup_parameters = startup_parameters
                vm.dependencies = vm_data.get('dependencies', [])

                vms.append(vm)

            return (
                AppSettings(
                    proxmox_settings=ProxmoxSettings(proxmox_config),
                    app_settings=settings,
                    notification_settings=notification_settings,
                    start_vms_settings=vms
                ),
                data)
