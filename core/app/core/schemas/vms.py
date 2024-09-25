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
    enabled: bool = True
    enable_dependencies: bool = False
    startup_timeout: int = 120
    wait_until_running: bool = True
    dependencies: Optional[list[int]] = None
    health_checks: Optional[List[CreateHealthcheck]] = []
    healthcheck: Optional[CreateHealthcheck] = None


class VmStartupSettings(CreateVmStartupSettings):
    id: int
    dependencies: Optional[list[int]] = None
    health_checks: Optional[List[Healthcheck]] = []
    healthcheck: Optional[Healthcheck] = None

    class Config:
        from_attributes = True


class StaringSettingsCreate(BaseModel):
    uptime_threshold: int = 0
    enable: bool = False


class StaringSettings(StaringSettingsCreate):
    id: int

    class Config:
        from_attributes = True
