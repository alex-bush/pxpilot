from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    user_settings: Mapped[list['UserSettings']] = relationship(
        'UserSettings', back_populates='user', cascade='all, delete-orphan'
    )


class UserSettings(Base):
    __tablename__ = 'user_settings'

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    value: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='user_settings')
