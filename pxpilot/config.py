from typing import Dict, Any
from typing import Optional

import yaml
from yaml.parser import ParserError

from pxpilot.logging_config import LOGGER
from pxpilot.vm_management.models import AppConfig, HealthCheckOptions, ValidationType, StartupParameters, \
    ProxmoxSettings, AppSettings, VMLaunchSettings


class ConfigManager:
    def load(self, file_path: str) -> Optional[AppConfig]:
        """Load configuration from a YAML file into a ProxmoxConfig object."""

        def load_yaml_config(path: str) -> Dict[str, Any]:
            """Helper function to load a YAML configuration file."""
            with open(path, "r") as file:
                return yaml.safe_load(file)

        def parse_healthcheck(healthcheck_data: Dict[str, Any]) -> Optional[HealthCheckOptions]:
            """Parse health check data into a HealthCheckOptions object."""
            if healthcheck_data:
                healthcheck_type = ValidationType[healthcheck_data["check_method"].upper()]
                return HealthCheckOptions(target_url=healthcheck_data["target_url"], check_method=healthcheck_type)
            return None

        def parse_startup_parameters(startup_data: Dict[str, Any]) -> Optional[StartupParameters]:
            """Parse startup parameters data into a StartupParameters object."""
            if startup_data:
                return StartupParameters(
                    await_running=startup_data.get("await_running", False),
                    startup_timeout=startup_data.get("startup_timeout", 0)
                )
            return StartupParameters()

        def parse_notification_parameters(notification_data: Dict[str, Any]) -> Dict[str, Any]:
            return notification_data

        try:
            config_data = load_yaml_config(file_path)
        except ParserError as e:
            LOGGER.exception("Failed to parse configuration file: %s", e)
            return None

        proxmox_config = ProxmoxSettings()
        proxmox_config.px_settings = config_data["proxmox_config"]

        settings = AppSettings(**config_data["settings"])

        notification_settings = parse_notification_parameters(config_data["notification_options"])

        vms = []
        for vm_data in config_data["vms"]:
            # Extract and parse nested configurations
            healthcheck_data = vm_data.pop("healthcheck", None)
            startup_data = vm_data.pop("startup_parameters", None)

            healthcheck = parse_healthcheck(healthcheck_data)
            startup_parameters = parse_startup_parameters(startup_data)

            vm = VMLaunchSettings(
                **vm_data,
                healthcheck=healthcheck,
                startup_parameters=startup_parameters
            )
            vms.append(vm)

        proxmox_config.start_options = vms

        app_settings = AppConfig(app_settings=settings, proxmox_config=proxmox_config,
                                 notification_settings=notification_settings)

        return app_settings
