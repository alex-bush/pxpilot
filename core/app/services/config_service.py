from typing import Annotated, Optional

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.schemas.proxmox_settings import ProxmoxSettingsCreate, ProxmoxSettings
from core.models.proxmox_settings import ProxmoxSettingsDbModel, ProxmoxExtraSettingsDbModel
from crud.configs import get_proxmox_settings, save_proxmox_settings


class ConfigService:
    def __init__(self, session: Annotated[AsyncSession, Depends(db_helper.session)]):
        self._session = session

    async def get_px_settings(self) -> Optional[ProxmoxSettings]:
        px_settings = await get_proxmox_settings(self._session)
        if px_settings:
            return ProxmoxSettings.model_validate(px_settings)
        return None

    async def set_px_settings(self, px_settings: ProxmoxSettingsCreate):
        settings_data = px_settings.model_dump()
        extra_settings_data = settings_data.pop('extra_settings', [])
        setting = ProxmoxSettingsDbModel(**settings_data)

        setting.extra_settings = [
            ProxmoxExtraSettingsDbModel(name=extra['name'], value=extra['value'])
            for extra in extra_settings_data
        ]

        await save_proxmox_settings(setting, self._session)
