from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings
from app.core.constants import (
    FORMAT, TITLE, SHEETS_VERSION, DRIVE_VERSION, PERMISSION_TYPE,
    PERMISSION_ROLE, MAJOR_DIMENSION, VALUE_INPUT_OPTION,
    SPREADSHEET_BODY, UPDATE_BODY_VALUES, ROW_COUNT, UPDATE_BODY_VALUES,
    TOP_LEFT_CELL, BOTTOM_RIGHT_CELL
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    spreadsheet_body = SPREADSHEET_BODY.copy()
    title = f'{TITLE} {now_date_time}'
    spreadsheet_body['properties']['title'] = title
    spreadsheet_body['sheets'][0]['properties']['title'] = title
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': PERMISSION_TYPE,
        'role': PERMISSION_ROLE,
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    free_rows = ROW_COUNT - len(UPDATE_BODY_VALUES)
    charity_projects_count = len(charity_projects)
    missed_projects_count = 0
    if len(charity_projects) > free_rows:
        missed_projects_count = charity_projects_count - free_rows
        charity_projects = charity_projects[:free_rows]
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    table_values = UPDATE_BODY_VALUES.copy()
    table_values[0][1] = now_date_time
    for project in charity_projects:
        new_row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description),
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': MAJOR_DIMENSION,
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'{TOP_LEFT_CELL}:{BOTTOM_RIGHT_CELL}',
            valueInputOption=VALUE_INPUT_OPTION,
            json=update_body
        )
    )
    return missed_projects_count
