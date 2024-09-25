from http import HTTPStatus
from typing import Annotated, Optional

from aiohttp import InvalidUrlClientError
from fastapi.params import Depends

from core.database.database import logger
from core.exceptions.exceptions import NotAuthorizedError, HttpError, ArgumentError, SettingsError
from core.schemas.common import ProxmoxValidationResponse
from core.schemas.proxmox import VirtualMachine
from core.schemas.proxmox_settings import ProxmoxSettingsCreate, ProxmoxSettings
from services.config_service import ConfigService
from services.proxmox_api_wrapper import ProxmoxAPIWrapper


class ProxmoxService:
    def __init__(self, config_service: Annotated[ConfigService, Depends(ConfigService)]):
        self._config_service = config_service

    async def get_nodes(self):
        settings = await self._config_service.get_px_settings()

        px_wrapper = self._create_proxmox_wrapper(settings)
        return await px_wrapper.get_nodes()

    async def get_virtual_machines(self) -> Optional[list[VirtualMachine]]:
        settings = await self._config_service.get_px_settings()
        if settings is None:
            logger.warn('Proxmox connection settings are empty.')
            raise SettingsError('Settings not set')

        px_wrapper = self._create_proxmox_wrapper(settings)
        nodes = await px_wrapper.get_nodes()
        result = []
        for node in nodes:
            if node.node is not None:
                qemu = await px_wrapper.get_virtual_machine(node.node, 'qemu')
                result.extend(qemu)

                lxc = await px_wrapper.get_virtual_machine(node.node, 'lxc')
                result.extend(lxc)
        return result

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
            return ProxmoxValidationResponse(is_valid=False, status_code=HTTPStatus.BAD_REQUEST,
                                             message=f'Invalid Url: {str(e)}')
        except Exception as e:
            return ProxmoxValidationResponse(is_valid=False, status_code=500, message=str(e))

    @staticmethod
    def _create_proxmox_wrapper(settings: ProxmoxSettings):
        if settings is None:
            raise ArgumentError('settings is None')
        if settings.hostname is None:
            raise ArgumentError('hostname is None')

        return ProxmoxAPIWrapper(
            base_url=settings.hostname,
            token_id=settings.token,
            token_secret=settings.token_value,
            verify_ssl=settings.get_as_bool('verify_ssl'))
