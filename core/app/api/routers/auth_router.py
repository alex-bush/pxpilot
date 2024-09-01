from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.models.auth import RegisterModel, AuthResponse, UserInDB
from api.services.auth_service import AuthService
from api.services.user_service import UserService

router = APIRouter(tags=["auth"])


@router.post('/login')
async def login(auth_form: Annotated[OAuth2PasswordRequestForm, Depends()],
                auth_service: Annotated[AuthService, Depends(AuthService)],
                user_service: UserService = Depends(UserService)) -> AuthResponse:
    db_user = await user_service.get_user(auth_form.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    user = UserInDB(**db_user.__dict__)

    if not auth_service.verify_password(auth_form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access_token_expires = timedelta(minutes=60*24*7)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return AuthResponse(access_token=access_token, token_type='bearer')


@router.post('/logout')
async def logout():
    pass


@router.post('/register')
async def register(register_form: RegisterModel,
                   auth_service: Annotated[AuthService, Depends(AuthService)],
                   user_service: UserService = Depends(UserService)):
    db_user = await user_service.get_user(register_form.username)
    if db_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

    user = UserInDB(**register_form.__dict__)
    user.password = auth_service.get_password_hash(register_form.password)

    if await user_service.register_user(user):
        return status.HTTP_201_CREATED
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
