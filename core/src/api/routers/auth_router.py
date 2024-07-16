from fastapi import APIRouter, Response, status, HTTPException

from api.models.auth import RegisterModel, AuthModel, AuthResponse

router = APIRouter(tags=["auth"])


@router.post('/login')
async def login(auth_form: AuthModel) -> AuthResponse:
    if auth_form.username == 'user':
        return AuthResponse(token=auth_form.password)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post('/logout')
async def logout():
    pass


@router.post('/register')
async def register(register_form: RegisterModel):
    if register_form.username == 'user':
        return status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
