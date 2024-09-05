from typing import Optional, List

from pydantic import BaseModel, Field


class CreateHealthcheck(BaseModel):
    id: Optional[int] = Field(None)
    vms_id: Optional[int] = Field(None)
    target_url: Optional[str] = None
    check_method: Optional[str] = None


class Healthcheck(CreateHealthcheck):
    id: int

    class Config:
        from_attributes = True


class CreateVmStartupSettings(BaseModel):
    id: Optional[int] = Field(None)
    vm_id: int
    node_name: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: bool = False
    enable_dependencies: bool = False
    startup_timeout: int = 120
    dependencies: Optional[str] = None
    healthcheck: Optional[List[CreateHealthcheck]] = []


class VmStartupSettings(CreateVmStartupSettings):
    id: int
    dependencies: Optional[str] = None
    healthcheck: Optional[List[Healthcheck]] = []

    class Config:
        from_attributes = True
