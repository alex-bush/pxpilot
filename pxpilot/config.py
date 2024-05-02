from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any
from typing import List, Optional

import yaml
from yaml.parser import ParserError

from pxpilot.logging_config import LOGGER


class ValidationType(Enum):
    PING = "ping"
    HTTP = "http"


@dataclass
class HealthCheckOptions:
    """
    Defines the options for performing health checks on a VM or container.

    Attributes:
        target_url (str): The URL or IP address to be used for the health check.
        check_method (ValidationType): The method of health check to be performed, such as PING or HTTP request.
    """

    target_url: str
    check_method: ValidationType


@dataclass
class StartupParameters:
    """
    Configures parameters that define the startup behavior of a VM or container.

    Attributes:
        await_running (bool): If True, the system will wait until the VM is fully up and running. Defaults to False.
        startup_timeout (int): The maximum number of seconds to wait for the VM to become fully operational. Defaults to 120 seconds.
    """

    await_running: bool = False
    startup_timeout: int = 120


@dataclass
class VMLaunchSettings:
    """
    Represents configuration options for initializing a VM or container on a Proxmox node.

    Attributes:
        vm_id (int): The unique identifier of the VM or container.
        node (str): The node within the Proxmox environment where the VM is hosted.
        enabled (bool): Indicates whether the VM should be started automatically. Defaults to True.
        startup_parameters (Optional[StartupParameters]): Additional parameters that influence the VM's startup process.
        dependencies (List[int]): A list of VM IDs that this VM depends on before it can start.
        healthcheck (Optional[HealthCheckOptions]): Health check configuration to monitor the VM or container post-startup.
    """

    vm_id: int
    node: str
    enabled: bool = True
    startup_parameters: Optional[StartupParameters] = None
    dependencies: List[int] = field(default_factory=list)
    healthcheck: Optional[HealthCheckOptions] = None


@dataclass
class ProxmoxSettings:
    """
    Contains the configuration for connecting and managing a Proxmox server environment.

    Attributes:
        start_options (List[VMLaunchSettings]): A list of VM start configurations to be managed.
    """

    px_settings: Any = None
    start_options: List[VMLaunchSettings] = field(default_factory=list)


@dataclass
class NotificationSettings:
    token: str
    chat_id: int | str


@dataclass
class AppSettings:
    auto_start_dependency: bool = False
    auto_shutdown: bool = False
    self_host: Optional[Dict[str, Any]] = None


@dataclass
class AppConfig:
    app_settings: AppSettings
    proxmox_config: ProxmoxSettings
    notification_settings: List[Dict[str, Any]] = field(default_factory=list)


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
            return None

        def parse_notification_parameters(notification_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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

        app_settings = AppConfig(app_settings=settings, proxmox_config=proxmox_config, notification_settings=notification_settings)

        return app_settings
