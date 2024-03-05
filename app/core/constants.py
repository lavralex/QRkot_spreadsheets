MAX_CHARITY_NAME_LENGTH = 100
MIN_CHARITY_NAME_LENGTH = 1
MIN_DESCRIPTION_LENGTH = 1
INVESTED_DEFAULT = 0
FORMAT = "%Y/%m/%d %H:%M:%S"
LOCALE = 'ru_RU'
SHEET_TYPE = 'GRID'
SHEET_ID = 0
TITLE = 'Отчёт от'
ROW_COUNT = 100
COLUMN_COUNT = 11
SHEETS_VERSION = 'v4'
DRIVE_VERSION = 'v3'
PERMISSION_TYPE = 'user'
PERMISSION_ROLE = 'writer'
MAJOR_DIMENSION = 'ROWS'
TOP_LEFT_CELL = 'A1'
BOTTOM_RIGHT_CELL = f'C{ROW_COUNT}'
VALUE_INPUT_OPTION = 'USER_ENTERED'
SPREADSHEET_BODY = {
    'properties': {
        'title': 'title',
        'locale': LOCALE
    },
    'sheets': [{
        'properties': {
            'sheetType': SHEET_TYPE,
            'sheetId': SHEET_ID,
            'title': 'title',
            'gridProperties': {
                'rowCount': ROW_COUNT,
                'columnCount': COLUMN_COUNT
            }
        }
    }]
}
UPDATE_BODY_VALUES = [
    ['Отчёт от', 'date'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
SPREADSHEET_LINK = 'https://docs.google.com/spreadsheets/d/'
