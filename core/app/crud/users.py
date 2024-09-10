from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UserDbModel


async def create_user(user: UserDbModel, db_session: AsyncSession) -> UserDbModel:
    db_session.add(user)

    await db_session.commit()
    await db_session.refresh(user)

    return user


async def get_user_by_username(username: str, db_session: AsyncSession) -> UserDbModel:
    try:
        result = await db_session.execute(select(UserDbModel).where(UserDbModel.username == username))
        user = result.scalars().first()
        return user
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None


async def get_users_count(db_session: AsyncSession) -> int:
    return await db_session.scalar(select(func.count()).select_from(UserDbModel))
