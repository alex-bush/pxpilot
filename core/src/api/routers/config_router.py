from typing import List

from fastapi import APIRouter, Depends, Response, status

from api.models.models import ProxmoxSettingsModel, NotificationsModel, VmStartOptionsModel
from api.routers.builders import get_config_service
from api.services.auth_service import get_current_user
from api.services.config_service import ConfigService

router = APIRouter(prefix="/config", tags=["config"], dependencies=[Depends(get_current_user)])


@router.post("/reload")
async def reload(config_service: ConfigService = Depends(get_config_service)):
    config_service.reload_config()
    return Response(status_code=status.HTTP_200_OK)


@router.get("/px")
async def get_proxmox_connection_settings(
        config_service: ConfigService = Depends(get_config_service)) -> ProxmoxSettingsModel:
    settings = config_service.get_proxmox_settings()

    return settings if settings is not None else Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/notifications")
async def get_notification_settings(config_service: ConfigService = Depends(get_config_service)) -> NotificationsModel:
    settings = config_service.get_notifications_settings()
    return settings if settings is not None else Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/startups")
async def get_startups_settings(config_service: ConfigService = Depends(get_config_service)) -> List[VmStartOptionsModel]:
    settings = config_service.get_startup_settings()
    return settings if settings is not None else Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/px")
async def save_proxmox_connection_settings(px_settings: ProxmoxSettingsModel,
                                           config_service: ConfigService = Depends(get_config_service)):
    config_service.save_proxmox_settings(px_settings)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/notifications")
async def save_notification_settings(notifications_setting: NotificationsModel,
                                     config_service: ConfigService = Depends(get_config_service)):
    config_service.save_notifications_setting(notifications_setting)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/startups")
async def save_startups_settings(start_vms_options: List[VmStartOptionsModel],
                                 config_service: ConfigService = Depends(get_config_service)):
    config_service.save_start_vms_options(start_vms_options)
    return Response(status_code=status.HTTP_202_ACCEPTED)