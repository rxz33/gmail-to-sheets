from googleapiclient.discovery import build
from src.gmail_service import get_credentials

def get_sheets_service():
    creds = get_credentials()
    return build("sheets", "v4", credentials=creds)

def append_rows(spreadsheet_id: str, range_name: str, rows: list[list[str]]):
    service = get_sheets_service()
    body = {"values": rows}
    service.spreadsheets().values().append(
        spreadsheetId = spreadsheet_id,
        range = range_name, 
        valueInputOption = "RAW",
        insertDataOption = "INSERT_ROWS",
        body = body,
    ).execute()