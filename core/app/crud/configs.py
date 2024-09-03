from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import ProxmoxSettings


async def get_proxmox_settings(db_session: AsyncSession):
    query = select(ProxmoxSettings).options(selectinload(ProxmoxSettings.extra_settings))
    result = await db_session.execute(query)
    st = result.scalars().first()
    return st


async def save_proxmox_settings(settings: ProxmoxSettings, db_session: AsyncSession) -> ProxmoxSettings:
    """
    Save or update a ProxmoxSettings instance and its related ProxmoxExtraSettings.

    :param settings: ProxmoxSettings instance to be saved or updated.
    :param db_session: The AsyncSession for database operations.
    """

    try:
        is_new = True
        if settings.id is not None:
            existing_settings = await db_session.execute(
                select(ProxmoxSettings).options(selectinload(ProxmoxSettings.extra_settings)).filter_by(
                    id=settings.id)
            )
            existing_settings = existing_settings.scalars().first()

            if existing_settings:
                is_new = False

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