from core.models import UserDbModel, UserSettingsDbModel
from core.schemas.user import UserRead, UserCreate
from core.schemas.user_settings import UserSetting
from crud.users import get_user_by_username, create_user, get_users_count, save_user_settings, get_user_settings
from services.base_service import BaseDbService


class UserService(BaseDbService):
    async def is_user_created(self) -> bool:
        return True if await get_users_count(self._session) > 0 else False

    async def get_user_by_username(self, username: str) -> UserRead | None:
        user = await get_user_by_username(username, self._session)

        if not user:
            return None

        return UserRead(**user.__dict__)

    async def create_user(self, user: UserCreate) -> UserRead:
        user = await create_user(UserDbModel(**user.model_dump()), self._session)
        return UserRead(**user.__dict__)

    async def get_user_settings(self, username: str) -> list[UserSetting]:
        user_settings = await get_user_settings(username, self._session)

        return [UserSetting(**setting.__dict__) for setting in user_settings]

    async def save_user_settings(self, username: str, settings: [UserSetting]):
        db_settings = [UserSettingsDbModel(name=stg.name, value=stg.value) for stg in settings]
        return await save_user_settings('user', db_settings, self._session)
