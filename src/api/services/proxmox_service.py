from typing import List

import requests
from fastapi import status
from proxmoxer import ResourceException

from api.models.models import ProxmoxValidationResultModel, ProxmoxVm
from pxpilot.common.exceptions import ProxmoxConfigurationError
from pxpilot.common.i_config import ConfigType
from pxpilot.models.configuration import config_builder
from pxpilot.pxtool import ProxmoxClient, VMService
from pxpilot.pxtool.proxmox_client import create_vm_service


class ProxmoxService:
    def __init__(self):
        self._proxmox_client: VMService | None = None

    @property
    def proxmox_client(self) -> VMService | None:
        if self._proxmox_client is not None:
            return self._proxmox_client

        cfg = config_builder.get_config_provider(ConfigType.ruamel, 'config.yaml')
        if cfg is None:
            return None

        px_settings = cfg.load_px_settings()
        if px_settings is None:
            return None

        self._proxmox_client = create_vm_service(cfg.load_px_settings().px_settings)
        return self._proxmox_client

    @staticmethod
    def test_proxmox_connection(host: str, token_name: str, token_value: str) -> ProxmoxValidationResultModel:
        try:
            proxmox_client = ProxmoxClient(host=host, token=token_name, token_value=token_value, verify_ssl=False)
            response = proxmox_client.test_connection()
            if 'version' in response:
                return ProxmoxValidationResultModel(is_valid=True, status_code=status.HTTP_200_OK)
            return ProxmoxValidationResultModel(is_valid=False, status_code=status.HTTP_400_BAD_REQUEST,
                                                message="No exception but version was not returned")
        except requests.exceptions.ConnectionError as e:
            return ProxmoxValidationResultModel(is_valid=False, status_code=status.HTTP_408_REQUEST_TIMEOUT, message=e.__doc__)
        except ResourceException as e:
            return ProxmoxValidationResultModel(is_valid=False, status_code=e.status_code, message=e.__str__())
        except Exception as e:
            return ProxmoxValidationResultModel(is_valid=False, status_code=status.HTTP_400_BAD_REQUEST, message=str(e))

    def get_vms(self) -> List[ProxmoxVm]:
        if self.proxmox_client is None:
            raise ProxmoxConfigurationError('ProxmoxClient is not initialized')

        vms = self.proxmox_client.get_all_vms()
        return [ProxmoxVm(
            id=item.vm_id,
            name=item.name,
            node=item.node,
            status=item.status,
            type=item.vm_type) for item in vms.values()]
