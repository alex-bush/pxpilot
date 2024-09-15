import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from core.config import settings

logger = logging.getLogger(__name__)


class AsyncDatabaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def dispose(self) -> None:
        logger.debug('disposing')
        await self.engine.dispose()

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        logger.debug('session')
        async with self.session_factory() as session:
            yield session


async_db_helper = AsyncDatabaseHelper(url=settings.db.connection_string_async)
