from typing import Annotated, Optional

from fastapi import APIRouter
from fastapi.params import Depends

from core.schemas.proxmox_settings import ProxmoxSettings
from services.config_service import ConfigService

router = APIRouter(tags=["auth v2"])

@router.get('/px')
async def get_proxmox_settings(config_service: Annotated[ConfigService, Depends(ConfigService)]) -> Optional[ProxmoxSettings]:
    return await config_service.get_px_settings()

@router.post('/px')
async def save_proxmox_settings(settings: ProxmoxSettings, config_service: Annotated[ConfigService, Depends(ConfigService)]) -> None:
    return await config_service.set_px_settings(settings)