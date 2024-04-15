from dataclasses import dataclass

from pxvmflow.consts import ProxmoxType


@dataclass
class PxEntity:
    id: int
    type: ProxmoxType
    status: str
    node: str
