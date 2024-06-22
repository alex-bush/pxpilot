from typing import List, Dict

from pxpilot.api.models.models import ProxmoxSettingsModel, VmStartOptionsModel, StartOptionsModel, NotificationsModel, \
    TelegramModel, EmailModel
from pxpilot.common import IConfig
from pxpilot.models.configuration.app_settings import ProxmoxSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions, HealthCheckOptions, StartOptions


class ConfigService:
    """
    Service for getting/saving the config sections from/to source by using a config provider.
    Convert data from dataclasses to pydantic models to pass to the frontend and vice versa
    """
    def __init__(self, config_provider: IConfig):
        self._config = config_provider

    def reload_config(self):
        self._config.reload_settings()

    def get_proxmox_settings(self) -> ProxmoxSettingsModel:
        """ Get proxmox settings from config provider and return as pydantic model. """
        px_settings = self._config.load_px_settings()
        px_settings_model = ProxmoxSettingsModel(
            host=px_settings.px_settings.get("host", ""),
            token_name=px_settings.px_settings.get("token", ""),
            token_value=px_settings.px_settings.get("token_value", "")
        )
        px_settings_model.extra_settings = {k: v for k, v in px_settings.px_settings.items()
                                            if k not in ["host", "token", "token_value"]}

        return px_settings_model

    def save_proxmox_settings(self, px_settings: ProxmoxSettingsModel) -> None:
        """
        Save proxmox settings using config provider. Convert pydantic model to dataclass
        """
        px = ProxmoxSettings()
        px.px_settings = {
            "host": px_settings.host,
            "token": px_settings.token_name,
            "token_value": px_settings.token_value
        }
        px.px_settings.update(dict(px_settings.extra_settings))

        self._config.save_px_settings(px)

    def get_notifications_settings(self) -> NotificationsModel:
        """
        Get notifications settings for telegram and email from config provider and return as pydantic model.
        """
        notification_settings = self._config.load_notifications_settings()

        notifications_model = self._convert_notification(notification_settings)
        return notifications_model

    def save_notifications_setting(self, settings: NotificationsModel):
        notifications_settings = {}

        if settings.telegram is not None:
            notifications_settings['telegram'] = settings.telegram.dict()
        if settings.email is not None:
            notifications_settings['email'] = settings.email.dict()

        self._config.save_notifications_settings(notifications_settings)

    def save_start_vms_options(self, vms: List[VmStartOptionsModel]):
        vm_options = []
        for vm in vms:
            vm_opt = VmStartOptions(
                vm_id=vm.vm_id,
                enabled=vm.enabled,
            )
            vm_opt.other.update(dict(**{
                'name': vm.name,
                'description': vm.description
            }))
            if vm.healthcheck is not None:
                vm_opt.healthcheck = HealthCheckOptions(**vm.healthcheck.__dict__)
            if vm.dependencies is not None:
                vm_opt.dependencies = list(vm.dependencies)
            if vm.startup_parameters is not None:
                vm_opt.startup_parameters = StartOptions(**vm.startup_parameters.__dict__)
            vm_options.append(vm_opt)

        self._config.save_start_vms_settings(vm_options)

    def get_startup_settings(self) -> List[VmStartOptionsModel]:
        """
        Get settings for start virtual machines from config provider and return as pydantic model.
        """
        vms = self._config.load_start_vms_settings()

        startup_settings_models = []
        for vm in vms:
            startup_settings_models.append(self._convert_startups(vm))

        return startup_settings_models

    @staticmethod
    def _convert_notification(settings: Dict[str, Dict]) -> NotificationsModel:
        """
        Convert Notification settings dataclasses to pydantic model.
        """
        notifications_model = NotificationsModel()
        if 'telegram' in settings:
            telegram_model = TelegramModel(
                enabled=settings['telegram'].get('enabled', True),
                token=settings['telegram'].get('token', ''),
                chat_id=settings['telegram'].get('chat_id', '')
            )
            notifications_model.telegram = telegram_model
        if 'email' in settings:
            email_model = EmailModel(
                enabled=settings['email'].get('enabled', True),
                smtp_server=settings['email'].get('smtp_server', 0),
                smtp_port=settings['email'].get('smtp_port', ''),
                smtp_user=settings['email'].get('smtp_user', ''),
                smtp_password=settings['email'].get('smtp_password', ''),
                from_email=settings['email'].get('from_email', ''),
                to_email=settings['email'].get('to_email', '')
            )
            notifications_model.email = email_model

        return notifications_model

    @staticmethod
    def _convert_startups(start_vm_options: VmStartOptions) -> VmStartOptionsModel:
        """
        Convert start virtual machines settings dataclasses to pydantic model.
        """
        startup_parameters = StartOptionsModel(**start_vm_options.startup_parameters.__dict__)
        dependencies = list(start_vm_options.dependencies)
        other = start_vm_options.other

        vm_start_options_model = VmStartOptionsModel(
            vm_id=start_vm_options.vm_id,
            enabled=start_vm_options.enabled,
            name=other['name'],
            description=other['description'],
            startup_parameters=startup_parameters,
            dependencies=dependencies,
        )

        if start_vm_options.healthcheck is not None:
            vm_start_options_model.healthcheck = HealthCheckOptions(**start_vm_options.healthcheck.__dict__)

        return vm_start_options_model
