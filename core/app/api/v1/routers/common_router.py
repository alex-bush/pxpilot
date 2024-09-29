from typing import Annotated

from fastapi import APIRouter, Depends

from api.services.auth_service import get_current_user
from core.schemas.common import HealthcheckModel, AppStateModel
from core.__about__ import __version__
from core.schemas.user import UserRead
from core.schemas.user_settings import UserSetting
from services.user_service import UserService

router = APIRouter(prefix="/status", tags=["App status"])


@router.get("/healthcheck")
async def healthcheck_v1() -> HealthcheckModel:
    return HealthcheckModel(status="ok", version=__version__)


@router.get("/state")
async def get_app_state(user_service: Annotated[UserService, Depends(UserService)]) -> AppStateModel:
    is_user_created = await user_service.is_user_created()
    return AppStateModel(version=__version__, is_first_run=not is_user_created)


@router.get("/app-settings")
async def get_app_settings(user_service: Annotated[UserService, Depends(UserService)],
                           user: Annotated[UserRead, Depends(get_current_user)]) -> list[UserSetting]:
    return await user_service.get_user_settings(user.username)


@router.post("/app-settings")
async def save_app_settings(settings: list[UserSetting],
                            user_service: Annotated[UserService, Depends(UserService)],
                            user: Annotated[UserRead, Depends(get_current_user)]):
    return await user_service.save_user_settings(user.username, settings)
