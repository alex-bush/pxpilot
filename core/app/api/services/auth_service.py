from datetime import timedelta, timezone, datetime
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext

from core.config import settings
from services.user_service import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api.token_url)

# todo: test key from fastapi docs, do not use it on production
SECRET_KEY = settings.api.secret_key
ALGORITHM = "HS256"


class PwdTokenService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return pwd_context.verify(password, hashed)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           pwd_service: Annotated[PwdTokenService, Depends(PwdTokenService)],
                           user_service: UserService = Depends(UserService)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'})

    try:
        payload = pwd_service.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError as err:
        print(err)
        raise credentials_exception

    user = await user_service.get_user_by_username(username)
    if not user:
        raise credentials_exception

    return user
