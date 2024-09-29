from typing import Optional

from core.config import settings
from core.models import HealthcheckDbModel, VmStartupSettingsDbModel
from core.models.proxmox_settings import ProxmoxSettingsDbModel, ProxmoxExtraSettingsDbModel
from core.models.vms import StartingSettingsDbModel
from core.schemas.proxmox_settings import ProxmoxSettingsCreate, ProxmoxSettings
from core.schemas.vms import VmStartupSettings, Healthcheck, CreateVmStartupSettings, StaringSettings, \
    StaringSettingsCreate
from crud.configs import get_proxmox_settings, save_proxmox_settings, get_vms_settings, \
    save_vm_startup, delete_vm_startup_settings_by_ids, get_starting_setting, add_starting_setting
from services.base_service import BaseDbService


class ConfigService(BaseDbService):
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

    async def get_vm_startup_settings(self) -> Optional[list[VmStartupSettings]]:
        vms_data = await get_vms_settings(self._session)
        if vms_data:
            vms = []
            for vm_data in vms_data:
                vms.append(self.convert(vm_data))

            return vms
        return None

    async def set_vm_startups_settings(self, vm_startup_settings: list[CreateVmStartupSettings]):
        existing = await get_vms_settings(self._session)
        existing_ids = {startup.id for startup in existing}
        new_ids = {startup.id for startup in vm_startup_settings if startup.id is not None}
        ids_for_delete = existing_ids - new_ids

        for vm_startup in vm_startup_settings:
            await self.add_vm_startup_settings(vm_startup)

        await delete_vm_startup_settings_by_ids(ids_for_delete, self._session)

    async def add_vm_startup_settings(self, vm: CreateVmStartupSettings) -> VmStartupSettings:
        vm_db = VmStartupSettingsDbModel(
            id=vm.id,
            vm_id=vm.vm_id,
            node_name=vm.node_name,
            name=vm.name,
            description=vm.description,
            enabled=vm.enabled,
            enable_dependencies=vm.enable_dependencies,
            startup_timeout=vm.startup_timeout,
            wait_until_running=vm.wait_until_running,
            dependencies=','.join([str(item) for item in vm.dependencies])
        )

        health_checks = None
        if settings.app.single_healthcheck:
            if vm.healthcheck is not None:
                health_checks = [
                    HealthcheckDbModel(
                        vms_id=vm.id,
                        target_url=vm.healthcheck.target_url,
                        check_method=vm.healthcheck.check_method
                    )
                ]
        else:
            if vm.health_checks is not None:
                health_checks = [
                    HealthcheckDbModel(
                        vms_id=vm.id,
                        target_url=hc.target_url,
                        check_method=hc.check_method
                    ) for hc in vm.health_checks
                ]

        saved_vm = await save_vm_startup(vm_db, health_checks, self._session)
        return self.convert(saved_vm)

    async def get_settings(self) -> StaringSettings:
        starting_setting = await get_starting_setting(None, self._session)
        if starting_setting:
            return StaringSettings.model_validate(starting_setting)

        return StaringSettings(id=0)

    async def set_settings(self, starting_setting: StaringSettingsCreate):
        sid = (await get_starting_setting(None, self._session)).id

        update_model = StartingSettingsDbModel(**starting_setting.model_dump())
        if sid != 0:
            update_model.id = sid

        await add_starting_setting(update_model, self._session)

    @staticmethod
    def convert(vm_data: VmStartupSettingsDbModel) -> VmStartupSettings:
        hs = [Healthcheck.model_validate(h) for h in vm_data.healthcheck]

        dps = []
        if vm_data.dependencies is not None and len(vm_data.dependencies) > 0:
            dps = [int(item.strip()) for item in vm_data.dependencies.split(',')]

        vm = {
            "id": vm_data.id,
            "vm_id": vm_data.vm_id,
            "node_name": vm_data.node_name,
            "name": vm_data.name,
            "description": vm_data.description,
            "enabled": vm_data.enabled,
            "enable_dependencies": vm_data.enable_dependencies,
            "wait_until_running": vm_data.wait_until_running,
            "startup_timeout": vm_data.startup_timeout,
            "dependencies": dps,
            "health_checks": hs,
            "healthcheck": hs[0] if len(hs) == 1 else None,
        }

        vm_schema = VmStartupSettings.model_validate(vm)
        return vm_schema
