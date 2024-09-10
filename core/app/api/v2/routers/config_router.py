from typing import Annotated, Optional

from fastapi import APIRouter, Response, status
from fastapi.params import Depends

from core.schemas.notifications import Notifications
from core.schemas.vms import VmStartupSettings, CreateVmStartupSettings
from services.auth_service import get_current_user
from services.config_service import ConfigService
from services.notification_service import NotificationService

router = APIRouter(prefix="/settings", tags=["config v2"], dependencies=[Depends(get_current_user)])


@router.get('/startups')
async def get_vms(config_service: Annotated[ConfigService, Depends(ConfigService)]) -> Optional[list[VmStartupSettings]]:
    return await config_service.get_vm_startup_settings()


@router.post('/startups')
async def add_vms(vms: list[CreateVmStartupSettings], config_service: Annotated[ConfigService, Depends(ConfigService)]):
    return await config_service.set_vm_startups_settings(vms)


@router.get('/notifications')
async def get_notification_settings(notification_service: Annotated[NotificationService,
                                    Depends(NotificationService)]) -> Optional[Notifications]:
    settings = await notification_service.get_notificator()
    return settings if settings is not None else Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/notifications')
async def save_notification_settings(
        n: Notifications,
        notification_service: Annotated[NotificationService, Depends(NotificationService)]):
    return await notification_service.save_notificator(n)
