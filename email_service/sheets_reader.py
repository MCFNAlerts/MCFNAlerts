from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from email_service.credentials_loader import get_sheets_service
from config import SHEET_ID

def get_subscribers(sheet_name="ActiveSubscribers"):
    # creds = Credentials.from_service_account_file("google_credentials.json")
    service = get_sheets_service()
    
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SHEET_ID, range=f"{sheet_name}!A:A")
        .execute()
    )
    
    rows = result.get("values", [])
    emails = [r[0].strip().lower() for r in rows if r and "@" in r[0]]
    return emails
