from fastapi import APIRouter, Response, status

router = APIRouter(tags=["auth"])


@router.post('/login')
async def login():
    return Response(status_code=status.HTTP_200_OK)


@router.post('/logout')
async def logout():
    pass


@router.post('/register')
async def register():
    pass
