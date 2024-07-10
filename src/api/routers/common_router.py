from fastapi import APIRouter, Depends

from api.models.models import HealthcheckModel, AppStateModel, ConfigState
from api.routers.builders import get_config_service
from api.services.config_service import ConfigService
from pxpilot.__about__ import __version__

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@router.get("/healthcheck/v1")
def healthcheck_v1() -> HealthcheckModel:
    return HealthcheckModel(status="ok", version=__version__)


@router.get("/state")
def get_app_state(config_service: ConfigService = Depends(get_config_service)) -> AppStateModel:
    is_config_initialized = True if config_service.get_config_state() is ConfigState.Initialized else False
    return AppStateModel(is_config_initialized=is_config_initialized)
