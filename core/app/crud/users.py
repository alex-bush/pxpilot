from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def create_user(user: User, db_session: AsyncSession) -> User:
    db_session.add(user)

    await db_session.commit()
    await db_session.refresh(user)

    return user


async def get_user_by_username(username: str, db_session: AsyncSession) -> User:
    user = (await db_session.scalars(select(User).where(User.username == username))).first()
    return user
