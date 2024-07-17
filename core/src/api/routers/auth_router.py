from fastapi import APIRouter, Response, status, HTTPException, Depends

from api.models.auth import RegisterModel, AuthModel, AuthResponse
from api.services.user_service import UserService

router = APIRouter(tags=["auth"])


@router.post('/login')
async def login(auth_form: AuthModel, user_service: UserService = Depends(UserService)) -> AuthResponse:
    u = await user_service.get_user(auth_form.username)
    if u is not None:
        return AuthResponse(token=auth_form.password)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post('/logout')
async def logout():
    pass


@router.post('/register')
async def register(register_form: RegisterModel, user_service: UserService = Depends(UserService)):
    if await user_service.register_user(register_form):
        return status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
