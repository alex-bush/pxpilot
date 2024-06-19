from typing import List

from fastapi import APIRouter, Depends, Response, status

from pxpilot.api.services.config_service import ConfigService, ProxmoxSettingsModel, NotificationsModel, \
    VmStartOptionsModel
from pxpilot.common.i_config import ConfigType
from pxpilot.models.configuration import config_builder

router = APIRouter(prefix="/config", tags=["config"])


def _get_config_service() -> ConfigService:
    config_provider = config_builder.get_config_provider(ConfigType.ruamel,  "config.yaml")
    return ConfigService(config_provider=config_provider)


@router.get("/px")
async def get_proxmox_connection_settings(
        config_service: ConfigService = Depends(_get_config_service)) -> ProxmoxSettingsModel:
    settings = config_service.get_proxmox_settings()
    return settings


@router.get("/notifications")
async def get_notification_settings(config_service: ConfigService = Depends(_get_config_service)) -> NotificationsModel:
    settings = config_service.get_notifications_settings()
    return settings


@router.get("/startups")
async def get_startups_settings(config_service: ConfigService = Depends(_get_config_service)) -> List[VmStartOptionsModel]:
    settings = config_service.get_startup_settings()
    return settings


@router.post("/px")
async def save_proxmox_connection_settings(px_settings: ProxmoxSettingsModel,
                                           config_service: ConfigService = Depends(_get_config_service)):
    config_service.save_proxmox_settings(px_settings)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/notifications")
async def save_notification_settings(notifications_setting: NotificationsModel,
                                     config_service: ConfigService = Depends(_get_config_service)):
    pass


@router.post("/startups")
async def save_startups_settings(start_vms_options: List[VmStartOptionsModel],
                                 config_service: ConfigService = Depends(_get_config_service)):
    pass
