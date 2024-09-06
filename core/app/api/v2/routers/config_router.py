from typing import Annotated, Optional

from fastapi import APIRouter
from fastapi.params import Depends

from core.schemas.notifications import Notifications
from core.schemas.vms import VmStartupSettings, CreateVmStartupSettings
from services.config_service import ConfigService
from services.notification_service import NotificationService

router = APIRouter(prefix="/settings", tags=["config v2"])


@router.get('/vms')
async def get_vms(config_service: Annotated[ConfigService, Depends(ConfigService)]) -> Optional[list[VmStartupSettings]]:
    return await config_service.get_vms()


@router.post('/vms')
async def add_vm(vm: CreateVmStartupSettings, config_service: Annotated[ConfigService, Depends(ConfigService)]):
    return await config_service.add_vms(vm)


@router.get('/config/notifications')
async def get_notification_settings(notification_service: Annotated[NotificationService, Depends(NotificationService)]):
    return await notification_service.get_notificator()


@router.post('/config/notifications')
async def save_notification_settings(n: Notifications, notification_service: Annotated[NotificationService, Depends(NotificationService)]):
    return await notification_service.save_notificator(n)
