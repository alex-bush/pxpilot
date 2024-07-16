from pydantic import BaseModel


class AuthModel(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str


class RegisterModel(BaseModel):
    username: str
    password: str
