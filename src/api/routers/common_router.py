from fastapi import APIRouter

from api.models.models import HealthcheckModel
from pxpilot.__about__ import __version__

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@router.get("/healthcheck/v1")
def healthcheck_v1() -> HealthcheckModel:
    return HealthcheckModel(status="ok", version=__version__)
