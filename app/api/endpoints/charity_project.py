from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.core.user import current_superuser
from app.services.investing import investing
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate,
    CharityProjectDB
)
from app.api.validators import (
    check_project_exists, check_name_duplicate, check_project_investment, check_project_closed,
    check_project_before_delete
)
from app.models import Donation

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Посмотреть проекты."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Cоздать новый проект.
        Доступно только суперюзерам.
    """
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await investing(new_project, Donation, session)
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить проект.
        Доступно только суперюзерам.
    """
    project = await check_project_exists(project_id, session)
    check_project_investment(project, obj_in)
    check_project_closed(project)
    await check_name_duplicate(obj_in.name, session)
    project = await charity_project_crud.update(project, obj_in, session)
    await investing(project, Donation, session)
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удалить проект.
        Доступно только суперюзерам.
    """
    project = await check_project_exists(project_id, session)
    check_project_before_delete(project)
    return await charity_project_crud.remove(project, session)
