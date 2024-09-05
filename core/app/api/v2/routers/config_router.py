from typing import Annotated, Optional

from fastapi import APIRouter
from fastapi.params import Depends

from core.schemas.proxmox_settings import ProxmoxSettings, ProxmoxSettingsCreate
from core.schemas.vms import VmStartupSettings, CreateVmStartupSettings
from services.config_service import ConfigService

router = APIRouter(tags=["auth v2"])


@router.get('/px')
async def get_proxmox_settings(config_service: Annotated[ConfigService, Depends(ConfigService)]) -> Optional[ProxmoxSettings]:
    return await config_service.get_px_settings()


@router.post('/px')
async def save_proxmox_settings(settings: ProxmoxSettingsCreate,
                                config_service: Annotated[ConfigService, Depends(ConfigService)]) -> None:
    return await config_service.set_px_settings(settings)


@router.get('/vms')
async def get_vms(config_service: Annotated[ConfigService, Depends(ConfigService)]) -> Optional[list[VmStartupSettings]]:
    return await config_service.get_vms()


@router.post('/vms')
async def add_vm(vm: CreateVmStartupSettings, config_service: Annotated[ConfigService, Depends(ConfigService)]):
    return await config_service.add_vms(vm)
