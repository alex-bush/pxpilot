import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.services.background_worker import run_pxpilot_worker
from pxpilot.__about__ import __title__, __version__
from api.routers import config_router, auth_router, common_router, proxmox_router

logger = logging.getLogger(__name__)

run_pilot = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    executor = None
    try:
        if run_pilot:
            executor = run_pxpilot_worker()
    except Exception as e:
        logger.exception(e)

    yield

    executor.shutdown() if executor is not None else None


api = FastAPI(
    title='API ' + __title__,
    version=__version__,
    description="API for managing the configuration of pxpilot.",
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
api.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

api_prefix = '/api'

api.include_router(common_router.router, prefix=api_prefix)
api.include_router(auth_router.router, prefix=api_prefix)
api.include_router(config_router.router, prefix=api_prefix)
api.include_router(proxmox_router.router, prefix=api_prefix)

logger.debug(f"Created api {'API ' + __title__}: {__version__}")

