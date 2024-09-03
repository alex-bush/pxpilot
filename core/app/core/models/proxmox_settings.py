from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseIdDbModel


class ProxmoxSettingsDbModel(BaseIdDbModel):
    __tablename__ = 'proxmox_settings'

    hostname: Mapped[str] = mapped_column(unique=True, nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)
    token_value: Mapped[str] = mapped_column(nullable=False)
    validated: Mapped[bool] = mapped_column(nullable=False, default=False)

    extra_settings: Mapped[list['ProxmoxExtraSettingsDbModel']] = relationship(
        'ProxmoxExtraSettingsDbModel', back_populates='proxmox_settings', cascade='all, delete-orphan'
    )


class ProxmoxExtraSettingsDbModel(BaseIdDbModel):
    __tablename__ = 'proxmox_extra_settings'

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    value: Mapped[str] = mapped_column(nullable=True)

    proxmox_settings_id: Mapped[int] = mapped_column(ForeignKey('proxmox_settings.id'), nullable=False)

    proxmox_settings: Mapped['ProxmoxSettingsDbModel'] = relationship(
        'ProxmoxSettingsDbModel', back_populates='extra_settings'
    )
