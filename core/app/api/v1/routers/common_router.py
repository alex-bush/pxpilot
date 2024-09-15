from typing import Annotated

from fastapi import APIRouter, Depends

from core.schemas.common import HealthcheckModel, AppStateModel
from core.__about__ import __version__
from services.user_service import UserService

router = APIRouter(prefix="/status", tags=["App status"])


@router.get("/healthcheck")
async def healthcheck_v1() -> HealthcheckModel:
    return HealthcheckModel(status="ok", version=__version__)


@router.get("/state")
async def get_app_state(user_service: Annotated[UserService, Depends(UserService)]) -> AppStateModel:
    is_user_created = await user_service.is_user_created()
    return AppStateModel(version=__version__, is_first_run=not is_user_created)
