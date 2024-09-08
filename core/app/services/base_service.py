from abc import ABC
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper


class BaseDbService(ABC):
    def __init__(self, session: Annotated[AsyncSession, Depends(db_helper.session)]):
        self._session = session
