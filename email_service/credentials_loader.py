import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

def load_credentials():
    json_str = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    info = json.loads(json_str)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return creds

def get_sheets_service():
    return build("sheets", "v4", credentials=load_credentials())

def get_gmail_service():
    return build("gmail", "v1", credentials=load_credentials())
