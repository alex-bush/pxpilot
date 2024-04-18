from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import yaml
from typing import Dict, Any

from yaml.parser import ParserError

from pxvmflow.logging_config import LOGGER


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
class VMStartOptions:
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
class ProxmoxConfig:
    """
    Contains the configuration for connecting and managing a Proxmox server environment.

    Attributes:
        url (str): The URL of the Proxmox server.
        port (int): The port number on which the Proxmox server is accessible.
        realm (str): Authentication realm for Proxmox server access.
        token_id (str): The API token ID used for authentication.
        token_secret (str): The secret associated with the API token.
        user (str): Username used for server authentication.
        password (str): Password for the user account.
        verify_ssl (bool): If True, SSL certificate verification is performed during connection. Defaults to False.
        start_options (List[VMStartOptions]): A list of VM start configurations to be managed.
    """

    url: str
    port: int
    realm: str
    token_id: str
    token_secret: str
    user: str
    password: str
    verify_ssl: bool

    start_options: List[VMStartOptions] = field(default_factory=list)


class VmFlowConfig:
    def load(self, file_path: str) -> Optional[ProxmoxConfig]:
        """Load configuration from a YAML file into a ProxmoxConfig object."""
        def load_yaml_config(file_path: str) -> Dict[str, Any]:
            """Helper function to load a YAML configuration file."""
            with open(file_path, "r") as file:
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

        try:
            config_data = load_yaml_config(file_path)
        except ParserError as e:
            LOGGER.exception("Failed to parse configuration file: %s", e)
            return None

        proxmox_config = ProxmoxConfig(**config_data["proxmox_config"])

        vms = []
        for vm_data in config_data["vms"]:
            # Extract and parse nested configurations
            healthcheck_data = vm_data.pop("healthcheck", None)
            startup_data = vm_data.pop("startup_parameters", None)

            healthcheck = parse_healthcheck(healthcheck_data)
            startup_parameters = parse_startup_parameters(startup_data)

            vm = VMStartOptions(
                **vm_data,
                healthcheck=healthcheck,
                startup_parameters=startup_parameters
            )
            vms.append(vm)

        proxmox_config.start_options = vms

        return proxmox_config
