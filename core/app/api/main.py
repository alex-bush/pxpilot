import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .v1.routers.routers import include_routers as include_routers_v1
from .services.background_worker import run_pxpilot_worker
from core import logging_config
from core.config import settings
from core.database import async_db_helper
from core.__about__ import __title__, __version__


logging_config.setup_logging()
logging.getLogger("aiosqlite").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    executor = None
    try:
        # if settings.app.pilot_enabled:
        executor = run_pxpilot_worker()
    except Exception as e:
        logger.exception(e)

    yield

    await async_db_helper.dispose()
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
    "http://127.0.0.1:8000"
]
api.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

include_routers_v1(api, settings.api.prefix)

logger.debug(f"Created api {'API ' + __title__}: {__version__}")
