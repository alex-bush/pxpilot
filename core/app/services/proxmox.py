from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.exceptions.exceptions import NotAuthorizedError, HttpError
from core.schemas.common import ProxmoxValidationResponse
from core.schemas.proxmox_settings import ProxmoxSettingsCreate
from services.base_service import BaseDbService
from services.config_service import ConfigService
from services.proxmox_api_wrapper import ProxmoxAPIWrapper


class ProxmoxService(BaseDbService):
    def __init__(self, config_service: Annotated[ConfigService, Depends(ConfigService)],
                 session: Annotated[AsyncSession, Depends(db_helper.session)]):
        super().__init__(session)
        self._config_service = config_service

    async def get_nodes(self):
        settings = await self._config_service.get_px_settings()

        px_wrapper = self._get_wrapper(settings)
        return await px_wrapper.get_nodes()

    @staticmethod
    async def validate_connection(settings: ProxmoxSettingsCreate) -> ProxmoxValidationResponse:
        px_wrapper = ProxmoxAPIWrapper(base_url=settings.hostname,
                                       token_id=settings.token,
                                       token_secret=settings.token_value,
                                       verify_ssl=settings.get_as_bool('verify_ssl'))
        try:
            await px_wrapper.get_version()
            return ProxmoxValidationResponse(is_valid=True)
        except NotAuthorizedError as e:
            return ProxmoxValidationResponse(is_valid=False, status_code=e.status_code, message=str(e))
        except HttpError as e:
            return ProxmoxValidationResponse(is_valid=False, status_code=e.status_code, message=str(e))
        except Exception as e:
            return ProxmoxValidationResponse(is_valid=False, status_code=500, message=str(e))

    @staticmethod
    def _get_wrapper(settings):
        return ProxmoxAPIWrapper(
            base_url=settings.hostname,
            token_id=settings.token,
            token_secret=settings.token_value,
            verify_ssl=settings.get_as_bool('verify_ssl'))
