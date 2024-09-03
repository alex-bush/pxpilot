from typing import Annotated, Optional

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.schemas.proxmox_settings import ProxmoxSettings as ProxmoxSettingsSchema
from core.models.proxmox_settings import ProxmoxSettings as ProxmoxSettingsModel, ProxmoxExtraSettings as ProxmoxExtraSettingsModel
from crud.configs import get_proxmox_settings, save_proxmox_settings


class ConfigService:
    def __init__(self, session: Annotated[AsyncSession, Depends(db_helper.session)]):
        self._session = session

    async def get_px_settings(self) -> Optional[ProxmoxSettingsSchema]:
        px_settings = await get_proxmox_settings(self._session)
        if px_settings:
            return ProxmoxSettingsSchema.model_validate(px_settings)
        return None

    async def set_px_settings(self, px_settings: ProxmoxSettingsSchema):
        settings_data = px_settings.model_dump()
        extra_settings_data = settings_data.pop('extra_settings', [])
        setting = ProxmoxSettingsModel(**settings_data)

        setting.extra_settings = [
            ProxmoxExtraSettingsModel(id=extra['id'], name=extra['name'], value=extra['value'])
            for extra in extra_settings_data
        ]

        await save_proxmox_settings(setting, self._session)
