from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiConfig(BaseModel):
    prefix: str = "/api"
    token_url: str = "/api/login"
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


class DatabaseConfig(BaseModel):
    connection_string_async: str
    connection_string: str


class ProxmoxConfig(BaseModel):
    auth_header: str = "PVEAPIToken"
    api_prefix: str = "/api2/json"


class AppConfig(BaseModel):
    single_healthcheck: bool = True

    # If True pilot worker will start during FastAPI starting
    pilot_enabled: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiConfig = ApiConfig()
    proxmox: ProxmoxConfig = ProxmoxConfig()
    app: AppConfig = AppConfig()
    db: DatabaseConfig


settings = Settings()
print(settings.db.connection_string_async)
