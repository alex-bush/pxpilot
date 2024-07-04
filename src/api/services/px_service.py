import requests
from fastapi import status
from proxmoxer import ResourceException

from api.models.models import ProxmoxValidationResultModel
from pxpilot.pxtool import ProxmoxClient


class PxService:
    def __init__(self):
        pass

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
