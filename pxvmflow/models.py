from enum import Enum
from dataclasses import dataclass


class EntityType(Enum):
    LXC = 1
    VM = 2


@dataclass
class PxEntity:
    id: int
    type: EntityType
    status: str
    node: str
