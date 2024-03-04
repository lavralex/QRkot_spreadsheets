from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def update_data(object: Union[Donation, CharityProject]):
    object.invested_amount = object.full_amount
    object.fully_invested = True
    object.close_date = datetime.now()
    return object


def invest(
    target: Union[Donation, CharityProject],
    source: Union[Donation, CharityProject]
):
    remains_target = target.full_amount - target.invested_amount
    remains_source = source.full_amount - source.invested_amount
    if remains_target > remains_source:
        target.invested_amount += remains_source
        source = update_data(source)
    elif remains_target == remains_source:
        target = update_data(target)
        source = update_data(source)
    else:
        source.invested_amount += remains_target
        target = update_data(target)
    return target, source


async def investing(
    target: Union[Donation, CharityProject],
    model: Union[Donation, CharityProject],
    session: AsyncSession
):
    sources = await session.execute(
        select(model).where(
            model.fully_invested == False # noqa
        ).order_by(model.create_date)
    )
    sources = sources.scalars().all()
    for source in sources:
        target, source = invest(target, source)
        session.add(target)
        session.add(source)
    await session.commit()
    await session.refresh(target)
    return target