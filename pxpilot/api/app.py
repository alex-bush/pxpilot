from fastapi import FastAPI

from pxpilot.__about__ import __title__, __version__, __description__
from .routers import config_router, auth_router
from .services.user_service import UserService

user_service = UserService()

api = FastAPI(title=__title__, version=__version__, description=__description__)

api_prefix = '/api'

api.include_router(auth_router.router, prefix=api_prefix)
api.include_router(config_router.router, prefix=api_prefix)
