from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import ProxmoxSettingsDbModel, VmStartupSettingsDbModel, HealthcheckDbModel


async def get_proxmox_settings(db_session: AsyncSession):
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
                        existing_settings.extra_settings.append(extra)

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


async def add_or_update_vm_with_healthchecks(vm: VmStartupSettingsDbModel, healthchecks: [HealthcheckDbModel],
                                             db_session: AsyncSession) -> VmStartupSettingsDbModel:
    try:
        async with db_session.begin():
            await add_vm(vm, db_session)
            await add_or_update_healthchecks(vm.id, healthchecks, db_session)

            return await get_vm_by_id(vm.id, db_session)
    except IntegrityError as e:
        print(e)
        await db_session.rollback()
    except Exception as e:
        print(e)
        await db_session.rollback()


async def add_vm(vm: VmStartupSettingsDbModel, db_session: AsyncSession):
    is_new = True
    if vm.id is not None:
        existing_vm = await db_session.execute(
            select(VmStartupSettingsDbModel).where(VmStartupSettingsDbModel.id == vm.id)
        )

        if existing_vm:
            is_new = False

            existing_vm.name = vm.name
            existing_vm.description = vm.description
            existing_vm.enabled = vm.enabled
            existing_vm.enable_dependencies = vm.enable_dependencies
            existing_vm.node_name = vm.node_name
            existing_vm.startup_timeout = vm.startup_timeout
            existing_vm.vm_id = vm.vm_id
            existing_vm.dependencies = vm.dependencies

    if is_new:
        db_session.add(vm)


async def add_or_update_healthchecks(vm_id: int, healthchecks: [HealthcheckDbModel], db_session: AsyncSession):
    await db_session.execute(
        delete(HealthcheckDbModel).where(HealthcheckDbModel.vms_id == vm_id)
    )

    for hc in healthchecks:
        new_hc = HealthcheckDbModel(
            target_url=hc.target_url,
            check_method=hc.check_method,
            vms_id=vm_id
        )
        db_session.add(new_hc)
