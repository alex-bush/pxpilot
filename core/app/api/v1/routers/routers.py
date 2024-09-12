from fastapi import FastAPI

from . import auth_router, config_router, common_router, proxmox_router
from .. import API_VERSION


def include_routers(api: FastAPI, prefix: str):
    api.include_router(auth_router.router, prefix=prefix + API_VERSION)
    api.include_router(config_router.router, prefix=prefix + API_VERSION)
    api.include_router(common_router.router, prefix=prefix + API_VERSION)
    api.include_router(proxmox_router.router, prefix=prefix + API_VERSION)
