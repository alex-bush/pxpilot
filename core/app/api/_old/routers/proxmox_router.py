# from typing import List, Annotated
#
# from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Response
#
# from api.models.models import ProxmoxValidationResultModel, ProxmoxVm, ProxmoxSettingsModel
# from api.services.auth_service import get_current_user
# from api.services.proxmox_service import ProxmoxService
# from core.exceptions.exceptions import ProxmoxConfigurationError
# from pxpilot.pilot import start
#
# router = APIRouter(prefix="/proxmox", tags=["proxmox"], dependencies=[Depends(get_current_user)])
#
#
# @router.post("/px-validate")
# async def validate_proxmox_connection(connection_settings: ProxmoxSettingsModel,
#                                       px_service: Annotated[ProxmoxService, Depends(ProxmoxService)]) -> ProxmoxValidationResultModel:
#
#     return px_service.test_proxmox_connection(connection_settings)
#
#
# @router.get("/get_vms")
# async def get_available_vms_from_proxmox(px_service: ProxmoxService = Depends(ProxmoxService)) -> List[ProxmoxVm]:
#     try:
#         return px_service.get_vms()
#     except ProxmoxConfigurationError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#
#
# @router.get("/run_pilot")
# async def run_pilot(bg: BackgroundTasks):
#     bg.add_task(start, "config.yaml")
#     return Response(status_code=status.HTTP_202_ACCEPTED)
