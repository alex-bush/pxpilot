from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UserDbModel


async def create_user(user: UserDbModel, db_session: AsyncSession) -> UserDbModel:
    db_session.add(user)

    await db_session.commit()
    await db_session.refresh(user)

    return user


async def get_user_by_username(username: str, db_session: AsyncSession) -> UserDbModel:
    user = (await db_session.scalars(select(UserDbModel).where(UserDbModel.username == username))).first()
    return user
