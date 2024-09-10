from http import HTTPStatus
from typing import Annotated

from aiohttp import InvalidUrlClientError
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from core.exceptions.exceptions import NotAuthorizedError, HttpError, ArgumentError, SettingsError
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

    async def get_virtual_machines(self):
        settings = await self._config_service.get_px_settings()
        if settings is None:
            raise SettingsError('Settings not set')

        def get_vm(q):
            return {
                    'id': q.get('vmid'),
                    'name': q.get('name'),
                    'type': q.get('type'),
                    'status': q.get('status')
                }

        px_wrapper = self._get_wrapper(settings)
        nodes = self.get_data(await px_wrapper.get_nodes())
        result = []
        for node in nodes:
            node_name = node.get('node', None)
            if node_name is not None:
                qemu = self.get_data(await px_wrapper.get_virtual_machine(node_name, 'qemu'))
                result.extend([get_vm(q) for q in qemu])

                lxc = self.get_data(await px_wrapper.get_virtual_machine(node_name, 'lxc'))
                result.extend([get_vm(q) for q in lxc])
        return result

    def get_data(self, data):
        if data is None:
            return []
        return data.get('data', [])

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
        except InvalidUrlClientError as e:
            return ProxmoxValidationResponse(is_valid=False, status_code=HTTPStatus.BAD_REQUEST, message=f'Invalid Url: {str(e)}')
        except Exception as e:
            return ProxmoxValidationResponse(is_valid=False, status_code=500, message=str(e))

    @staticmethod
    def _get_wrapper(settings):
        if settings is None:
            raise ArgumentError('settings is None')
        if settings.hostname is None:
            raise ArgumentError('hostname is None')

        return ProxmoxAPIWrapper(
            base_url=settings.hostname,
            token_id=settings.token,
            token_secret=settings.token_value,
            verify_ssl=settings.get_as_bool('verify_ssl'))
