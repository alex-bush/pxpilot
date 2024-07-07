from typing import List

from fastapi import APIRouter, Depends

from api.models.models import ProxmoxSettingsLightModel, ProxmoxValidationResultModel, ProxmoxVm
from api.services.proxmox_service import ProxmoxService

router = APIRouter(prefix="/proxmox", tags=["proxmox"])


@router.post("/px-validate")
async def validate_proxmox_connection(connection_settings: ProxmoxSettingsLightModel,
                                      px_service: ProxmoxService = Depends(ProxmoxService)) -> ProxmoxValidationResultModel:
    return px_service.test_proxmox_connection(connection_settings.host, connection_settings.token_name,
                                              connection_settings.token_value)


@router.get("/get_vms", response_model=List[ProxmoxVm])
async def get_available_vms_from_proxmox(px_service: ProxmoxService = Depends(ProxmoxService)) -> List[ProxmoxVm]:
    return px_service.get_vms()
