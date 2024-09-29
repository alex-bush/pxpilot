from pydantic import BaseModel, Field


class UserSetting(BaseModel):
    name: str = Field(...)
    value: str = Field(...)
