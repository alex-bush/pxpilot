from pydantic import BaseModel


class LoginModel(BaseModel):
    username: str
    password: str


class RegisterModel(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
