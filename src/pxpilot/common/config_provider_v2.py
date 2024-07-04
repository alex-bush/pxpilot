import copy
import logging
from threading import Lock
from typing import Any, List, Optional, Dict

from ruamel.yaml import YAML

from pxpilot.common import IConfig
from pxpilot.common.constants import ConfigSections
from pxpilot.models.configuration.app_settings import ProxmoxSettings, AppSettings, CommonSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions, HealthCheckOptions, StartOptions, \
    HealthcheckType


logger = logging.getLogger(__name__)


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
                logger.debug('Creating ConfigProvider instance')
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

    def load_notifications_settings(self) -> Dict[str, Dict]:
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
        vms_list = []
        for vm in vms:
            vm_data = {
                ConfigSections.VM_ID: vm.vm_id,
                ConfigSections.ENABLED: vm.enabled,
                ConfigSections.STARTUP_PARAMETERS: {
                    ConfigSections.AWAIT_RUNNING: vm.startup_parameters.await_running,
                    ConfigSections.STARTUP_TIMEOUT: vm.startup_parameters.startup_timeout
                },
                ConfigSections.DEPENDENCIES: vm.dependencies,
            }
            if vm.healthcheck:
                vm_data[ConfigSections.HEALTHCHECK] = {
                    ConfigSections.TARGET_URL: vm.healthcheck.target_url,
                    ConfigSections.CHECK_METHOD: vm.healthcheck.check_method.value
                }
            vm_data.update(vm.other)
            vms_list.append(vm_data)

        self._yaml_data[ConfigSections.VMS] = vms_list
        self._save_config(self._file_path, self._yaml_data)

    def reload_settings(self):
        """ Reload app settings and internal yaml data """
        self._app_config, self._yaml_data = self._load_settings(self._file_path)

    def _save_config(self, file_name, data, reload: bool = True):
        """ Save config in yaml file and reload """
        logger.debug(f'Saving config to {file_name}')
        yaml = YAML()
        with open(file_name, "w") as file:
            yaml.dump(data, file)

        if reload:
            self.reload_settings()

    @staticmethod
    def _load_settings(path: str) -> (AppSettings, Any):
        logger.debug(f'Loading app settings from {path}')

        yaml = YAML()
        yaml.preserve_quotes = True
        with open(path, "r") as file:
            data = yaml.load(file)

        proxmox_config = dict(**data[ConfigSections.PROXMOX_CONFIG])

        settings = CommonSettings(**data[ConfigSections.COMMON_SETTINGS])

        notification_settings = {key: dict(**value) for key, value in
                                 data[ConfigSections.NOTIFICATION_OPTIONS].items() if
                                 isinstance(value, dict)}

        vms = []
        for vm_data in data[ConfigSections.VMS]:
            vm_data_temp = copy.deepcopy(vm_data)

            vm_id = vm_data_temp.pop(ConfigSections.VM_ID, None)
            enabled = vm_data_temp.pop(ConfigSections.ENABLED, True)
            startup_parameters_data = vm_data_temp.pop(ConfigSections.STARTUP_PARAMETERS, {})
            dependencies = vm_data_temp.pop(ConfigSections.DEPENDENCIES, [])
            healthcheck_data = vm_data_temp.pop(ConfigSections.HEALTHCHECK, None)
            other = vm_data_temp

            healthcheck = None
            if healthcheck_data:
                h_data = healthcheck_data.copy()
                if ConfigSections.CHECK_METHOD in h_data and isinstance(h_data[ConfigSections.CHECK_METHOD], str):
                    h_data[ConfigSections.CHECK_METHOD] = HealthcheckType(h_data.pop(ConfigSections.CHECK_METHOD))

                healthcheck = HealthCheckOptions(**h_data)

            vm = VmStartOptions(
                vm_id,
                enabled,
                startup_parameters=StartOptions(**startup_parameters_data),
                dependencies=dependencies,
                healthcheck=healthcheck,
                other=other
            )

            vms.append(vm)

        return (
            AppSettings(
                proxmox_settings=ProxmoxSettings(proxmox_config),
                app_settings=settings,
                notification_settings=notification_settings,
                start_vms_settings=vms
            ),
            data)
