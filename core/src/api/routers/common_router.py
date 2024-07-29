from fastapi import APIRouter, Depends

from api.models.models import HealthcheckModel, AppStateModel, ConfigState, SiteSettings
from api.routers.builders import get_config_service
from api.services.config_service import ConfigService
from api.services.user_service import UserService
from pxpilot.__about__ import __version__

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@router.get("/healthcheck/v1")
async def healthcheck_v1() -> HealthcheckModel:
    return HealthcheckModel(status="ok", version=__version__)


@router.get("/state")
async def get_app_state(config_service: ConfigService = Depends(get_config_service),
                        user_service: UserService = Depends(UserService)) -> AppStateModel:
    is_config_initialized = True if await config_service.get_config_state() is ConfigState.Initialized else False
    is_first_run = False if await user_service.is_any_users() else True
    return AppStateModel(
        is_config_initialized=is_config_initialized,
        is_first_run=is_first_run,
        version=__version__,
        dark_theme=False)
