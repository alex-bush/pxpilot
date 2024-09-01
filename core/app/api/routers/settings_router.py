from fastapi import APIRouter, Depends

from api.models.models import SiteSettings
from api.services.auth_service import get_current_user

router = APIRouter(prefix="/settings", tags=["settings"], dependencies=[Depends(get_current_user)])


@router.post("/settings")
async def save_site_settings(settings: SiteSettings):
    pass
