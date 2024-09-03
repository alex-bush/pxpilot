from typing import List, Optional

from pydantic import BaseModel, Field


class ProxmoxExtraSettingsBase(BaseModel):
    name: str = Field(..., description="Name for the extra setting")
    value: Optional[str] = Field(None, description="Value for the extra setting")

class ProxmoxExtraSettingsCreate(ProxmoxExtraSettingsBase):
    proxmox_settings_id: Optional[int] = Field(default=None)

class ProxmoxExtraSettings(ProxmoxExtraSettingsBase):
    id: int
    proxmox_settings_id: int

    class Config:
        from_attributes = True

class ProxmoxSettingsBase(BaseModel):
    hostname: str = Field(..., description="Hostname of the Proxmox server")
    token: str = Field(..., description="Token used for authentication")
    token_value: str = Field(..., description="Value of the authentication token")
    validated: bool = Field(False, description="Whether the Proxmox settings are validated")

# Schema for creating ProxmoxSettings with nested extra settings
class ProxmoxSettingsCreate(ProxmoxSettingsBase):
    id: Optional[int] = Field(None, description="Id of the extra setting")
    extra_settings: List[ProxmoxExtraSettingsCreate] = Field(
        default_factory=list, description="List of extra settings for the Proxmox server"
    )

class ProxmoxSettings(ProxmoxSettingsBase):
    id: int
    extra_settings: List[ProxmoxExtraSettings] = Field(
        default_factory=list, description="List of extra settings for the Proxmox server"
    )

    class Config:
        from_attributes = True