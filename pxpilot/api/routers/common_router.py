from fastapi import APIRouter

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@router.get("/healthcheck/v1")
def healthcheck():
    return {"status": "ok"}
