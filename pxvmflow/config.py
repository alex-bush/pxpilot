from dataclasses import dataclass, field
from typing import List, Optional
import yaml
from typing import Dict, Any

from yaml.parser import ParserError


@dataclass
class HealthCheck:
    address: str
    type: str


@dataclass
class VM:
    id: int
    name: str
    run_timeout: Optional[int] = None
    dependencies: List[int] = field(default_factory=list)
    healthcheck: Optional[HealthCheck] = None


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

    vms: List[VM] = field(default_factory=list)


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


class VmFlowConfig:
    def load(self, file_path) -> ProxmoxConfig | None:
        try:
            config_data = load_yaml_config(file_path)
        except ParserError as e:
            print(e)
            return None

        proxmox_config = ProxmoxConfig(**config_data['proxmox_config'])

        vms = []
        for vm_data in config_data['vms']:
            healthcheck_data = vm_data.pop('healthcheck', None)
            healthcheck = HealthCheck(**healthcheck_data) if healthcheck_data else None
            vm = VM(**vm_data, healthcheck=healthcheck)
            vms.append(vm)

        proxmox_config.vms = vms

        return proxmox_config
