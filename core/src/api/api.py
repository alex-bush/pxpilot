import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pxpilot.__about__ import __title__, __version__
from api.routers import config_router, auth_router, common_router, proxmox_router, settings_router

logger = logging.getLogger(__name__)


api = FastAPI(
    title='API ' + __title__,
    version=__version__,
    description="API for managing the configuration of pxpilot.",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]
api.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

api_prefix = '/api'

api.include_router(common_router.router, prefix=api_prefix)
api.include_router(auth_router.router, prefix=api_prefix)
api.include_router(config_router.router, prefix=api_prefix)
api.include_router(proxmox_router.router, prefix=api_prefix)
api.include_router(settings_router.router, prefix=api_prefix)

logger.debug(f"Created api {'API ' + __title__}: {__version__}")