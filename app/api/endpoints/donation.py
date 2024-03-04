from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import User, CharityProject, Donation
from app.schemas.donation import DonationCreate, DonationDB
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.services.investing import investing

router = APIRouter()

EXCLUDE_FIELDS = {
    'user_id',
    'invested_amount',
    'close_date',
    'fully_invested'
}


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Cписок пожертвований
        Доступно только суперюзерам.
    """
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude=EXCLUDE_FIELDS
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Cписок пожертвований пользователя."""
    return await donation_crud.get_by_user(
        model=Donation,
        session=session,
        user=user
    )


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude=EXCLUDE_FIELDS
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    '''Создать пожертвование'''
    new_donation = await donation_crud.create(donation, session, user)
    await investing(new_donation, CharityProject, session)
    await session.refresh(new_donation)
    return new_donation
