from threading import Lock
from typing import Any, List, Optional

from ruamel.yaml import YAML

from pxpilot.common import IConfig
from pxpilot.models.configuration.app_settings import ProxmoxSettings, AppSettings, CommonSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions, HealthCheckOptions, StartOptions, \
    HealthcheckType


class ConfigProviderV2(IConfig):
    _instance: Optional[IConfig] = None
    _lock: Lock = Lock()
    _file_path: str = None
    _app_config: AppSettings = None

    def __init__(self, file_path: str):
        if ConfigProviderV2._instance is not None:
            raise Exception("For use ConfigProvider use get_instance first.")

        self._file_path = file_path
        self._app_config = self._load_settings(file_path)

    @classmethod
    def get_instance(cls, file_path: str) -> IConfig:
        with cls._lock:
            if cls._instance is None:
                cls._instance = ConfigProviderV2(file_path)

            return cls._instance

    @property
    def app_config(self) -> AppSettings:
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
        pass

    def save_notifications_settings(self):
        pass

    def save_start_vms_settings(self, vms: List[VmStartOptions]):
        pass

    @staticmethod
    def _load_settings(path: str) -> AppSettings:
        yaml = YAML()
        with open(path, "r") as file:
            data = yaml.load(file)

            proxmox_config = dict(**data['proxmox_config'])

            settings = CommonSettings(**data['settings'])

            notification_settings = {key: dict(**value) for key, value in data['notification_options'].items() if
                                     isinstance(value, dict)}

            vms = []
            for vm_data in data['vms']:
                healthcheck_data = vm_data.get('healthcheck')
                healthcheck = None
                if healthcheck_data:
                    if 'check_method' in healthcheck_data and isinstance(healthcheck_data['check_method'], str):
                        healthcheck_data['check_method'] = HealthcheckType(healthcheck_data['check_method'])

                    healthcheck = HealthCheckOptions(**healthcheck_data)

                startup_parameters_data = vm_data.get('startup_parameters', {})
                startup_parameters = StartOptions(**startup_parameters_data)

                vm = VmStartOptions(**vm_data)
                vm.healthcheck = healthcheck
                vm.startup_parameters = startup_parameters
                vm.dependencies = vm_data.get('dependencies', [])

                vms.append(vm)

            return AppSettings(
                proxmox_settings=ProxmoxSettings(proxmox_config),
                app_settings=settings,
                notification_settings=notification_settings,
                start_vms_settings=vms
            )
