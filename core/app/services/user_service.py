from core.models import UserDbModel
from core.schemas.user import UserRead, UserCreate
from crud.users import get_user_by_username, create_user, get_users_count
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
