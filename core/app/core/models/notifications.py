from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseIdDbModel


class NotifiersDbModel(BaseIdDbModel):
    __tablename__ = 'notifiers'

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    enabled: Mapped[bool] = mapped_column(Boolean)

    options: Mapped[list['NotifierSettingsDbModel']] = relationship('NotifierSettingsDbModel',
                                                                    back_populates="notifier")


class NotifierSettingsDbModel(BaseIdDbModel):
    __tablename__ = 'notifier_settings'

    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=True)

    notifier_id: Mapped[int] = mapped_column(ForeignKey('notifiers.id'), nullable=False)

    notifier: Mapped['NotifiersDbModel'] = relationship('NotifiersDbModel', back_populates="options")
