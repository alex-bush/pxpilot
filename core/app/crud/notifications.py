from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import NotifiersDbModel


async def get_notifiers(db_session: AsyncSession) -> Sequence[NotifiersDbModel]:
    query = select(NotifiersDbModel).options(selectinload(NotifiersDbModel.options))
    result = await db_session.execute(query)
    st = result.scalars().all()
    return st


async def save_notifier(notifiers: Sequence[NotifiersDbModel], db_session: AsyncSession) -> None:
    try:
        for notifier in notifiers:
            existing_notifier = await db_session.execute(
                select(NotifiersDbModel)
                .options(selectinload(NotifiersDbModel.options))
                .where(NotifiersDbModel.name == notifier.name)
            )
            existing_notifier = existing_notifier.scalar_one_or_none()

            if existing_notifier:
                existing_notifier.name = notifier.name
                existing_notifier.enabled = notifier.enabled

                existing_options = {opt.name: opt for opt in existing_notifier.options}
                new_options = {opt.name: opt for opt in notifier.options}

                for name, option in new_options.items():
                    if name in existing_options:
                        existing_options[name].value = option.value
                    else:
                        existing_notifier.options.append(option)

                for name in set(existing_options) - set(new_options):
                    existing_notifier.options.remove(existing_options[name])

            else:
                db_session.add(notifier)

        await db_session.commit()

    except IntegrityError as e:
        await db_session.rollback()
        raise ValueError(f"Integrity error: {str(e)}") from e

    except Exception as e:
        await db_session.rollback()
        raise ValueError(f"An error occurred: {str(e)}") from e
