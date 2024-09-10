from typing import Optional

from pydantic import BaseModel, Field, field_validator, ValidationError


class TelegramNotifier(BaseModel):
    enabled: bool = Field(False, description='Enable or disable telegram')
    chat_id: str = ''
    token: str = ''


class EmailNotifier(BaseModel):
    enabled: bool = Field(False, description='Enable or disable email')
    smtp_server: str = ''
    smtp_port: int = 587
    smtp_user: str = ''
    smtp_password: str = ''
    from_email: str = ''
    to_email: str = ''

    @classmethod
    @field_validator('smtp_port')
    def validate_port(cls, v):
        if isinstance(v, int):
            return v
        raise ValidationError("Port must be an number")


class Notifications(BaseModel):
    telegram: Optional[TelegramNotifier] = None
    email: Optional[EmailNotifier] = None
