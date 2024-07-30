
from fastapi import Depends

from api.models.auth import UserModel, UserInDB
from api.routers.builders import get_config_service
from api.services.config_service import ConfigService


class UserService:
    def __init__(self, config_service: ConfigService = Depends(get_config_service)):
        self._config_service = config_service

    async def register_user(self, register_form: UserInDB):
        user = UserModel(username=register_form.username, password=register_form.password)

        self._config_service.save_user(user)

        return True

    async def get_user(self, username: str) -> UserModel:
        users = self._config_service.load_users()
        user = next((user for user in users if user.username == username), None)
        return user

    async def is_any_users(self) -> True:
        users = self._config_service.load_users()
        return users is not None and len(users) > 0
