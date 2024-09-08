import aiohttp

from core.config import settings
from core.exceptions.exceptions import NotAuthorizedError, HttpError


class ProxmoxAPIWrapper:
    def __init__(self, base_url: str, token_id: str, token_secret: str, verify_ssl: bool = False):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'{settings.proxmox.auth_header}={token_id}={token_secret}'
        }
        self.verify_ssl = verify_ssl

    async def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{settings.proxmox.api_prefix}/{endpoint}"

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

    async def get_version(self):
        return await self._request('GET', 'version')

    async def get_nodes(self):
        return await self._request('GET', 'nodes')

    async def get_node_status(self, node_name):
        return await self._request('GET', f'nodes/{node_name}/status')
