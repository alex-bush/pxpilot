from fastapi import APIRouter, Depends

from api.models.models import HealthcheckModel, ProxmoxSettingsLightModel, ProxmoxValidationResultModel
from api.services.px_service import PxService
from pxpilot.__about__ import __version__

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@router.get("/healthcheck/v1")
def healthcheck_v1() -> HealthcheckModel:
    return HealthcheckModel(status="ok", version=__version__)


@router.post("/px-validate")
async def validate_proxmox_connection(connection_settings: ProxmoxSettingsLightModel,
                                      px_service: PxService = Depends(PxService)) -> ProxmoxValidationResultModel:
    return px_service.test_proxmox_connection(connection_settings.host, connection_settings.token_name,
                                              connection_settings.token_value)
