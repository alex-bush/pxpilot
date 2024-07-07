from typing import Optional, List, Any, Dict

from pydantic import BaseModel, Field, field_validator, ValidationError

from pxpilot.models.configuration.vm_start_settings import HealthcheckType


class ProxmoxSettingsModel(BaseModel):
    """
    Basic information about connection settings for proxmox
    """
    host: str
    token_name: str
    token_value: str
    extra_settings: Optional[Dict[str, Any]] = {}


class ProxmoxSettingsLightModel(BaseModel):
    host: str
    token_name: str
    token_value: str


class ProxmoxValidationResultModel(BaseModel):
    is_valid: bool
    status_code: int
    message: Optional[str] = None


class StartOptionsModel(BaseModel):
    await_running: bool = False
    startup_timeout: int = 120


class HealthCheckOptionsModel(BaseModel):
    target_url: str = Field(..., description="Target URL")
    check_method: HealthcheckType = Field(default=HealthcheckType.PING, description="Check method")


class VmStartOptionsModel(BaseModel):
    vm_id: int
    name: Optional[str] = Field(None, description="VM name")
    description: Optional[str] = Field(None, description="Short description of VM")
    enabled: Optional[bool] = Field(True, description="Enable or disable starting VM")

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

    @classmethod
    @field_validator('smtp_port')
    def validate_port(cls, v):
        if isinstance(v, int):
            return v
        raise ValidationError("Port must be an number")


class NotificationsModel(BaseModel):
    telegram: Optional[TelegramModel] = None
    email: Optional[EmailModel] = None


class HealthcheckModel(BaseModel):
    status: str
    version: str


class ProxmoxVm(BaseModel):
    id: int
    name: Optional[str]
    status: Optional[str] = None
    node: Optional[str] = None
    type: Optional[str] = None
