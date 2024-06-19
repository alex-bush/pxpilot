from typing import Dict

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UserService:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def get_user(self, username: str) -> User:
        return self.users[username]

    def set_user(self, user: User):
        self.users[user.username] = user
