from sqlalchemy import ForeignKey, Integer, String, Boolean, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseIdDbModel


class StartingSettingsDbModel(BaseIdDbModel):
    """ Common settings for starting up virtual machines"""
    __tablename__ = "starting_settings"
    uptime_threshold: Mapped[int] = Column(Integer, nullable=False, default=0)
    enable: Mapped[bool] = Column(Boolean, nullable=False, default=True)


class VmStartupSettingsDbModel(BaseIdDbModel):
    """ Starting setting for particular virtual machine """
    __tablename__ = 'vm_startup_settings'

    vm_id: Mapped[int] = mapped_column(Integer, nullable=False)
    node_name: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    enable_dependencies: Mapped[bool] = mapped_column(Boolean, default=False)
    wait_until_running: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    startup_timeout: Mapped[int] = mapped_column(Integer, default=120)

    dependencies: Mapped[str] = mapped_column(String, nullable=True)

    healthcheck: Mapped[list['HealthcheckDbModel']] = relationship(
        'HealthcheckDbModel',
        back_populates='vm_startup_settings'
    )


class HealthcheckDbModel(BaseIdDbModel):
    __tablename__ = 'healthcheck'

    vms_id: Mapped[int] = mapped_column(ForeignKey('vm_startup_settings.id'), nullable=False)
    target_url: Mapped[str] = mapped_column(String, default=None)
    check_method: Mapped[str] = mapped_column(String, default=None)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    vm_startup_settings: Mapped['VmStartupSettingsDbModel'] = relationship(
        'VmStartupSettingsDbModel',
        back_populates='healthcheck'
    )
