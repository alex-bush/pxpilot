from typing import List

import requests
from fastapi import status
from proxmoxer import ResourceException

from api.models.models import ProxmoxValidationResultModel, ProxmoxVm
from pxpilot.common.i_config import ConfigType
from pxpilot.models.configuration import config_builder
from pxpilot.pxtool import ProxmoxClient
from pxpilot.pxtool.proxmox_client import create_vm_service


class ProxmoxService:
    def __init__(self):
        self._proxmox_client = self.init()

    def init(self):
        cfg = config_builder.get_config_provider(ConfigType.ruamel, 'config.yaml')
        return create_vm_service(cfg.load_px_settings().px_settings)

    def test_proxmox_connection(self, host: str, token_name: str, token_value: str) -> ProxmoxValidationResultModel:
        proxmox_client = ProxmoxClient(host=host, token=token_name, token_value=token_value, verify_ssl=False)
        try:
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
            return ProxmoxValidationResultModel(is_valid=False, status_code=status.HTTP_400_BAD_REQUEST, message=e.__doc__)

    def get_vms(self) -> List[ProxmoxVm]:
        vms = self._proxmox_client.get_all_vms()
        return [ProxmoxVm(
            id=item.vm_id,
            name=item.name,
            node=item.node,
            status=item.status,
            type=item.vm_type) for item in vms.values()]
