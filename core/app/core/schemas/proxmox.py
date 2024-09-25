from typing import Optional

from pydantic import BaseModel, Field


class Node(BaseModel):
    node: str = Field(description="The cluster node name.")
    status: str = Field(description="Node status.")
    uptime: Optional[int] = Field(default=None, description="Node uptime in seconds.")


class VirtualMachine(BaseModel):
    vmid: int = Field(description="The (unique) ID of the VM/Container.")
    name: str = Field(description="VM/Container name.")
    status: str = Field(description="VM/LXC Container status.")
    uptime: Optional[int] = Field(default=None, description="Uptime in seconds.")
