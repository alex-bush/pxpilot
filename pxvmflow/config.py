from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import yaml
from typing import Dict, Any

from yaml.parser import ParserError

from pxvmflow.consts import LOGGER


class ValidationType(Enum):
    PING = "ping"
    HTTP = "http"


@dataclass
class HealthCheckOptions:
    address: str
    type: ValidationType


@dataclass
class VMStartOptions:
    id: int
    node: str
    run_timeout: Optional[int] = None
    dependencies: List[int] = field(default_factory=list)
    healthcheck: Optional[HealthCheckOptions] = None


@dataclass
class ProxmoxConfig:
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
    def load(self, file_path) -> ProxmoxConfig | None:
        def load_yaml_config(file_path: str) -> Dict[str, Any]:
            with open(file_path, "r") as file:
                return yaml.safe_load(file)

        def parse_healthcheck(healthcheck_data):
            if healthcheck_data:
                healthcheck_type = ValidationType[healthcheck_data["type"].upper()]
                return HealthCheckOptions(address=healthcheck_data["address"], type=healthcheck_type)

        try:
            config_data = load_yaml_config(file_path)
        except ParserError as e:
            LOGGER.exception(e)
            return None

        proxmox_config = ProxmoxConfig(**config_data["proxmox_config"])

        vms = []
        for vm_data in config_data["vms"]:
            healthcheck_data = vm_data.pop("healthcheck", None)
            healthcheck = parse_healthcheck(healthcheck_data)
            vm = VMStartOptions(**vm_data, healthcheck=healthcheck)
            vms.append(vm)

        proxmox_config.start_options = vms

        return proxmox_config

