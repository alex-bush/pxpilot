from typing import Optional, List

from pydantic import BaseModel, Field

from pxpilot.models.configuration.vm_start_settings import HealthcheckType


class ProxmoxSettingsModel(BaseModel):
    """
    Basic information about connection settings for proxmox
    """
    host: str
    token_name: str
    token_value: str


class StartOptionsModel(BaseModel):
    await_running: bool = False
    startup_timeout: int = 120


class HealthCheckOptionsModel(BaseModel):
    target_url: str
    check_method: HealthcheckType = HealthcheckType.PING


class VmStartOptionsModel(BaseModel):
    vm_id: int
    name: Optional[str] = Field(None, alias="name")
    description: Optional[str] = Field(None, alias="description")
    enabled: Optional[bool] = True

    startup_parameters: StartOptionsModel = Field(default_factory=StartOptionsModel)
    dependencies: List[int] = Field(default_factory=list)
    healthcheck: Optional[HealthCheckOptionsModel] = None


class TelegramModel(BaseModel):
    enabled: bool = True
    token: str
    chat_id: str


class EmailModel(BaseModel):
    enabled: bool = True
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    from_email: str
    to_email: str


class NotificationsModel(BaseModel):
    telegram: Optional[TelegramModel] = None
    email: Optional[EmailModel] = None
