from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден'
        )
    return project


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await (
        charity_project_crud.get_id_by_name(
            model=CharityProject,
            name=project_name,
            session=session
        )
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


def check_project_investment(
    project: CharityProject,
    obj_in: CharityProjectUpdate,
):
    invested_amount = project.invested_amount
    if obj_in.full_amount and obj_in.full_amount < invested_amount:
        raise HTTPException(
            status_code=400,
            detail=f'Требуемая сумма проекта должна быть больше инвестированной: {invested_amount}'
        )


def check_project_closed(
    project: CharityProject
):
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_project_before_delete(
    project: CharityProject
):
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
