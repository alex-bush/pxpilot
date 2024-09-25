import logging

import aiohttp
from aiohttp import ClientError

from core.config import settings
from core.exceptions.exceptions import NotAuthorizedError, HttpError
from core.schemas.proxmox import Node, VirtualMachine

logger = logging.getLogger(__name__)


class ProxmoxAPIWrapper:
    def __init__(self, base_url: str, token_id: str, token_secret: str, verify_ssl: bool = False):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'{settings.proxmox.auth_header}={token_id}={token_secret}'
        }
        self.verify_ssl = verify_ssl

    async def get_version(self):
        return await self._get('version')

    async def get_nodes(self) -> list[Node]:
        response_json = await self._get('nodes')
        nodes = [Node.model_validate(node_data) for node_data in response_json['data']]

        return nodes

    async def get_virtual_machine(self, node_name: str, vm_type: str) -> list[VirtualMachine]:
        if node_name is None:
            raise AttributeError('Node name is required')

        response = await self._get(f'nodes/{node_name}/{vm_type}')
        vms = [VirtualMachine.model_validate(vm) for vm in response['data']]

        return vms

    async def get_node_status(self, node_name):
        return await self._get(f'nodes/{node_name}/status')

    async def _get(self, endpoint, **kwargs):
        return await self._request('GET', endpoint, **kwargs)

    async def _post(self, endpoint, **kwargs):
        return await self._request('POST', endpoint, **kwargs)

    async def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{settings.proxmox.api_prefix}/{endpoint}"

        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.request(method, url, ssl=self.verify_ssl, **kwargs) as response:
                    match response.status:
                        case code if 200 <= code <= 299:
                            return await response.json()
                        case code if 300 <= code <= 399:
                            return await response.json()
                        case code if 400 <= code <= 499:
                            raise NotAuthorizedError(f"{response.reason}", status_code=response.status)
                        case _:
                            error_text = await response.text()
                            raise HttpError(f"Error: {error_text}. Reason: {response.reason}", status_code=response.status)
        except (NotAuthorizedError, HttpError) as error:
            logger.error(error)
            raise error
        except ClientError as error:
            logger.error(error)
            if error.os_error is not None and isinstance(error.os_error, TimeoutError):
                raise HttpError(f'Timeout error: {str(error.os_error)}')
            raise HttpError(f'Error: {str(error)}')
        except Exception as error:
            logger.error(error)
            raise HttpError(f'Error: {str(error)}')
