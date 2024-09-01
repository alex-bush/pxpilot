from fastapi import FastAPI

from . import auth_router


def include_routers(api: FastAPI, prefix: str):
    api.include_router(auth_router.router, prefix=prefix + "/v2")
