from typing import Annotated, Optional

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.models import HealthcheckDbModel, VmStartupSettingsDbModel
from core.models.proxmox_settings import ProxmoxSettingsDbModel, ProxmoxExtraSettingsDbModel
from core.schemas.proxmox_settings import ProxmoxSettingsCreate, ProxmoxSettings
from core.schemas.vms import VmStartupSettings, Healthcheck, CreateVmStartupSettings
from crud.configs import get_proxmox_settings, save_proxmox_settings, get_vms_settings, \
    add_or_update_vm_with_healthchecks


class ConfigService:
    def __init__(self, session: Annotated[AsyncSession, Depends(db_helper.session)]):
        self._session = session

    async def get_px_settings(self) -> Optional[ProxmoxSettings]:
        px_settings = await get_proxmox_settings(self._session)
        if px_settings:
            return ProxmoxSettings.model_validate(px_settings)
        return None

    async def set_px_settings(self, px_settings: ProxmoxSettingsCreate):
        settings_data = px_settings.model_dump()
        extra_settings_data = settings_data.pop('extra_settings', [])
        setting = ProxmoxSettingsDbModel(**settings_data)

        setting.extra_settings = [
            ProxmoxExtraSettingsDbModel(name=extra['name'], value=extra['value'])
            for extra in extra_settings_data
        ]

        await save_proxmox_settings(setting, self._session)

    async def get_vms(self) -> Optional[list[VmStartupSettings]]:
        vms_data = await get_vms_settings(self._session)
        if vms_data:
            vms = []
            for vm_data in vms_data:
                vms.append(self.convert(vm_data))

            return vms
        return None

    async def add_vms(self, vm: CreateVmStartupSettings) -> VmStartupSettings:
        vm_db = VmStartupSettingsDbModel(
            id=vm.id,
            vm_id=vm.vm_id,
            node_name=vm.node_name,
            name=vm.name,
            description=vm.description,
            enabled=vm.enabled,
            enable_dependencies=vm.enable_dependencies,
            startup_timeout=vm.startup_timeout,
            dependencies=vm.dependencies,
        )

        healthchecks = [
            HealthcheckDbModel(
                vms_id=vm.id,
                target_url=hc.target_url,
                check_method=hc.check_method
            ) for hc in vm.healthcheck
        ]

        saved_vm = await add_or_update_vm_with_healthchecks(vm_db, healthchecks, self._session)
        return self.convert(saved_vm)

    @staticmethod
    def convert(vm_data: VmStartupSettingsDbModel) -> VmStartupSettings:
        hs = [Healthcheck.model_validate(h) for h in vm_data.healthcheck]

        vm = {
            "id": vm_data.id,
            "vm_id": vm_data.vm_id,
            "node_name": vm_data.node_name,
            "name": vm_data.name,
            "description": vm_data.description,
            "enabled": vm_data.enabled,
            "enable_dependencies": vm_data.enable_dependencies,
            "startup_timeout": vm_data.startup_timeout,
            "dependencies": vm_data.dependencies,
            "healthcheck": hs
        }

        vm_schema = VmStartupSettings.model_validate(vm)
        return vm_schema
