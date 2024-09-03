from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(...)


class UserCreate(UserBase):
    password: str = Field(...)


class UserRead(UserCreate):
    id: int
