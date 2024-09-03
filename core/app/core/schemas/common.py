from pydantic import BaseModel, Field


class HealthcheckModel(BaseModel):
    status: str
    version: str


class AppStateModel(BaseModel):
    is_first_run: bool = Field(True)
    # is_config_initialized: bool = Field(False)
    version: str = Field(...)
    dark_theme: bool = Field(False)