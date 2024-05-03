from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Optional, Dict, Any, List

from pxpilot.pxtool import VirtualMachine


class StartStatus(Enum):
    UNKNOWN = auto()
    OK = auto

    STARTING = auto()
    STARTED = auto()
    ALREADY_STARTED = auto()
    STOPPED = auto()
    TIMEOUT = auto()
    FAILED = auto()

    INFO_MISSED = auto()
    DISABLED = auto()
    DEPENDENCY_FAILED = auto()


@dataclass
class StartResult:
    status: StartStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    message: Optional[str] = None


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
class AppSettings:
    auto_start_dependency: bool = False
    auto_shutdown: bool = False
    self_host: Optional[Dict[str, Any]] = None


@dataclass
class AppConfig:
    app_settings: AppSettings
    proxmox_config: ProxmoxSettings
    notification_settings: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class VMContext:
    vm_id: int
    vm_launch_settings: Optional[VMLaunchSettings]
    vm_info: Optional[VirtualMachine]
    status: StartStatus = StartStatus.UNKNOWN
