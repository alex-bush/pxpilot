from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import ProxmoxSettingsDbModel, VmStartupSettingsDbModel, HealthcheckDbModel, \
    ProxmoxExtraSettingsDbModel


async def get_proxmox_settings(db_session: AsyncSession) -> ProxmoxSettingsDbModel:
    query = select(ProxmoxSettingsDbModel).options(selectinload(ProxmoxSettingsDbModel.extra_settings))
    result = await db_session.execute(query)
    st = result.scalars().first()
    return st


async def save_proxmox_settings(settings: ProxmoxSettingsDbModel, db_session: AsyncSession) -> ProxmoxSettingsDbModel:
    """
    Save or update a ProxmoxSettings instance and its related ProxmoxExtraSettings.

    :param settings: ProxmoxSettings instance to be saved or updated.
    :param db_session: The AsyncSession for database operations.
    """

    try:
        is_new = True
        if settings.id is not None:
            existing_settings = await db_session.execute(
                select(ProxmoxSettingsDbModel).options(selectinload(ProxmoxSettingsDbModel.extra_settings)).filter_by(
                    id=settings.id)
            )
            existing_settings = existing_settings.scalars().first()

            if existing_settings:
                is_new = False

                existing_settings.hostname = settings.hostname
                existing_settings.token = settings.token
                existing_settings.token_value = settings.token_value
                existing_settings.validated = settings.validated

                # Update or add extra settings
                existing_extra_settings = {extra.name: extra for extra in existing_settings.extra_settings}
                for extra in settings.extra_settings:
                    if extra.name in existing_extra_settings:
                        # Update existing extra setting
                        existing_extra = existing_extra_settings[extra.name]
                        existing_extra.value = extra.value
                    else:
                        # Add new extra setting
                        extra.proxmox_settings_id = existing_settings.id
                        db_session.add(ProxmoxExtraSettingsDbModel(name=extra.name, value=extra.value, proxmox_settings_id=existing_settings.id))

                # Delete extra settings
                requested_extra_names = {extra.name for extra in settings.extra_settings}
                for existing_name in existing_extra_settings.keys():
                    if existing_name not in requested_extra_names:
                        await db_session.delete(existing_extra_settings[existing_name])


        if is_new:
            db_session.add(settings)

        await db_session.commit()
        return settings

    except IntegrityError as e:
        await db_session.rollback()
        raise ValueError(f"Integrity error: {str(e)}") from e
    except Exception as e:
        await db_session.rollback()
        raise ValueError(f"An error occurred: {str(e)}") from e


async def get_vms_settings(db_session: AsyncSession) -> Sequence[VmStartupSettingsDbModel]:
    query = (select(VmStartupSettingsDbModel).options(
        selectinload(VmStartupSettingsDbModel.healthcheck),
    ))
    result = await db_session.execute(query)
    return result.scalars().all()


async def get_vm_by_id(id: int, db_session: AsyncSession) -> VmStartupSettingsDbModel:
    query = (select(VmStartupSettingsDbModel).options(
        selectinload(VmStartupSettingsDbModel.healthcheck)
    )).where(VmStartupSettingsDbModel.id == id)
    result = await db_session.execute(query)
    return result.scalars().first()


async def save_vm_startup(vm: VmStartupSettingsDbModel, healthchecks: [HealthcheckDbModel], db_session: AsyncSession):
    is_new = True
    if vm.id is not None:
        existing = await db_session.execute(
            select(VmStartupSettingsDbModel).where(VmStartupSettingsDbModel.id == vm.id)
        )
        existing_vm = existing.scalars().first()

        if existing_vm:
            is_new = False

            existing_vm.name = vm.name
            existing_vm.description = vm.description
            existing_vm.enabled = vm.enabled
            existing_vm.enable_dependencies = vm.enable_dependencies
            existing_vm.node_name = vm.node_name
            existing_vm.startup_timeout = vm.startup_timeout
            existing_vm.wait_until_running = vm.wait_until_running
            existing_vm.vm_id = vm.vm_id
            existing_vm.dependencies = vm.dependencies
            existing_vm.id = vm.id

    if is_new:
        db_session.add(vm)

    await db_session.execute(
        delete(HealthcheckDbModel).where(HealthcheckDbModel.vms_id == vm.id)
    )

    if healthchecks:
        for hc in healthchecks:
            new_hc = HealthcheckDbModel(
                target_url=hc.target_url,
                check_method=hc.check_method,
                vms_id=vm.id
            )
            db_session.add(new_hc)

    await db_session.commit()

    # Return updated object
    return await get_vm_by_id(vm.id, db_session)

async def delete_vm_startup_settings_by_ids(ids_to_delete: set[int], db_session: AsyncSession):
    if not ids_to_delete:
        return

    await db_session.execute(
        delete(VmStartupSettingsDbModel).where(VmStartupSettingsDbModel.id.in_(ids_to_delete))
    )

    await db_session.commit()
