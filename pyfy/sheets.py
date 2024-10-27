import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEFAULT_TOKEN_FILE = "googleapi-token.json"
DEFAULT_CREDENTIALS_FILES = "googleapi-credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def get_credentials(
        cache_credentials: bool = True,
        cached_token_filename: str = None):
    credentials = None
    if cache_credentials:
        if not cached_token_filename:
            cached_token_filename = DEFAULT_TOKEN_FILE
    if os.path.exists(cached_token_filename):
        credentials = Credentials.from_authorized_user_file(cached_token_filename)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                DEFAULT_CREDENTIALS_FILES,
                SCOPES)
            credentials = flow.run_local_server(port=0)
        if cache_credentials:
            with open(cached_token_filename, "w") as token:
                token.write(credentials.to_json())

    return credentials

def get_service(credentials):
    try:
        service = build("sheets", "v4", credentials=credentials)
        return service.spreadsheets()
        
    except HttpError as error:
        # TODO Log error
        return None

def read_cell(
        spreadsheet_id: str,
        sheet_name: str,
        column: str,
        row: int,
        credentials = None):
    if not credentials:
        credentials = get_credentials()

    try:
        sheets = get_service(credentials)

        result = sheets.values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!{column}{row}").execute()
        
        values = result.get("values", [])

        for row in values:
            print(values)
    except HttpError as error:
        print(error)

def test():
    from dotenv import load_dotenv

    load_dotenv()

    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    read_cell(SPREADSHEET_ID, "2024", "A", 1)
