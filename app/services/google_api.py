from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings
from app.core.constants import (
    FORMAT, LOCALE, SHEET_TYPE, SHEET_ID, TITLE, ROW_COUNT, COLUMN_COUNT,
    SHEETS_VERSION, DRIVE_VERSION, PERMISSION_TYPE, PERMISSION_ROLE,
    MAJOR_DIMENSION, RANGE, VALUE_INPUT_OPTION
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    spreadsheet_body = {
        'properties': {
            'title': f'{TITLE}{now_date_time}',
            'locale': LOCALE
        },
        'sheets': [{
            'properties': {
                'sheetType': SHEET_TYPE,
                'sheetId': SHEET_ID,
                'title': f'{TITLE}{now_date_time}',
                'gridProperties': {
                    'rowCount': ROW_COUNT,
                    'columnCount': COLUMN_COUNT
                }
            }
        }]
    }
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
        carity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in carity_projects:
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
            range=RANGE,
            valueInputOption=VALUE_INPUT_OPTION,
            json=update_body
        )
    )
