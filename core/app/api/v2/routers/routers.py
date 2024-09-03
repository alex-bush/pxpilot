from fastapi import FastAPI

from . import auth_router, config_router, common_router


def include_routers(api: FastAPI, prefix: str):
    api.include_router(auth_router.router, prefix=prefix + "/v2")
    api.include_router(config_router.router, prefix=prefix + "/v2")
    api.include_router(common_router.router, prefix=prefix + "/v2")
