from fastapi import APIRouter

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@router.get("/healthcheck/v1")
def healthcheck_v1():
    return {"status": "ok"}
