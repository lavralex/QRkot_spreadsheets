from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.core.constants import SPREADSHEET_LINK
from app.crud.charity_project import charity_project_crud
from app.schemas.google_schema import Googl
from app.services.google_api import spreadsheets_create, set_user_permissions, spreadsheets_update_value

router = APIRouter()


@router.post(
    '/',
    response_model=Googl,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """Только для суперюзеров.
        Создает Google таблицу с топом самых быстрых по закрытию проектов
    """
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    charity_projects = await (
        charity_project_crud.get_projects_by_completion_rate(session)
    )
    missed_projects_count = await spreadsheets_update_value(
        spreadsheet_id,
        charity_projects,
        wrapper_services

    )
    if not missed_projects_count:
        message = None
    else:
        message = f'Количество проектов не попавшик в таблицу: {missed_projects_count}'
    link = f'{SPREADSHEET_LINK}{spreadsheet_id}'
    return {'link': link, 'message': message, 'projects': charity_projects}
