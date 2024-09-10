from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.services.auth_service import PwdTokenService
from core.schemas.auth import RegisterModel, AuthResponse
from core.schemas.user import UserCreate
from services.user_service import UserService


router = APIRouter(tags=["auth"])


@router.post('/login')
async def login(auth_form: Annotated[OAuth2PasswordRequestForm, Depends()],
                pwd_service: Annotated[PwdTokenService, Depends(PwdTokenService)],
                user_service: Annotated[UserService, Depends(UserService)]) -> AuthResponse:
    user = await user_service.get_user_by_username(auth_form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    if not pwd_service.verify_password(auth_form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access_token_expires = timedelta(minutes=60*24*7)
    access_token = pwd_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return AuthResponse(access_token=access_token, token_type='bearer')


@router.post('/logout')
async def logout():
    pass


@router.post('/register')
async def register(reg_form: RegisterModel,
                   pwd_service: Annotated[PwdTokenService, Depends(PwdTokenService)],
                   user_service: UserService = Depends(UserService)):
    if await user_service.get_user_by_username(reg_form.username) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

    user = UserCreate(**reg_form.__dict__)
    user.password = pwd_service.hash_password(reg_form.password)

    if await user_service.create_user(user):
        return status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
