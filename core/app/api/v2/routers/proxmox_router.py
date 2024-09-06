from typing import Annotated, Optional

from fastapi import APIRouter
from fastapi.params import Depends

from core.schemas.proxmox_settings import ProxmoxSettings, ProxmoxSettingsCreate
from services.config_service import ConfigService

router = APIRouter(prefix="/proxmox", tags=["proxmox v2"])

@router.get('/settings')
async def get_proxmox_settings(config_service: Annotated[ConfigService, Depends(ConfigService)]) -> Optional[ProxmoxSettings]:
    return await config_service.get_px_settings()


@router.post('/settings')
async def save_proxmox_settings(settings: ProxmoxSettingsCreate,
                                config_service: Annotated[ConfigService, Depends(ConfigService)]) -> None:
    return await config_service.set_px_settings(settings)

@router.post('/validate')
async def validate_proxmox_settings():
    pass

@router.get('/virtual-machines')
async def get_vms():
    pass

@router.post('/run-pilot')
async def run_px_pilot():
    pass
