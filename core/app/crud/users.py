from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import UserDbModel, UserSettingsDbModel


async def create_user(user: UserDbModel, db_session: AsyncSession) -> UserDbModel:
    db_session.add(user)

    await db_session.commit()
    await db_session.refresh(user)

    return user


async def get_user_by_username(username: str, db_session: AsyncSession, include_options: bool = False) -> UserDbModel:
    try:
        query = select(UserDbModel).where(UserDbModel.username == username)

        if include_options:
            query = query.options(selectinload(UserDbModel.user_settings))

        result = await db_session.execute(query)
        user = result.scalars().first()
        return user
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None


async def get_users_count(db_session: AsyncSession) -> int:
    return await db_session.scalar(select(func.count()).select_from(UserDbModel))


async def get_user_settings(username: str, db_session: AsyncSession) -> list[UserSettingsDbModel]:
    try:
        user = await get_user_by_username(username, db_session, True)

        return user.user_settings
    except SQLAlchemyError as e:
        print(f"Database error: {e}")


async def save_user_settings(username: str, settings: [UserSettingsDbModel], db_session: AsyncSession):
    try:
        user = await get_user_by_username(username, db_session, True)
        existing_settings = {s.name: s for s in user.user_settings}
        for new_setting in settings:
            if new_setting.name in existing_settings:
                existing_settings[new_setting.name].value = new_setting.value
            else:
                new_setting.user_id = user.id
                user.user_settings.append(new_setting)

        await db_session.commit()

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
