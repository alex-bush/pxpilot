from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import BaseIdDbModel


class UserDbModel(BaseIdDbModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    user_settings: Mapped[list['UserSettingsDbModel']] = relationship(
        'UserSettingsDbModel', back_populates='user', cascade='all, delete-orphan'
    )


class UserSettingsDbModel(BaseIdDbModel):
    __tablename__ = 'user_settings'

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    value: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    user: Mapped['UserDbModel'] = relationship('UserDbModel', back_populates='user_settings')
