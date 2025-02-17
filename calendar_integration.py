# calendar_integration.py
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def create_event(summary, description, start, end):
    creds = Credentials(
        None,
        refresh_token=os.getenv('GOOGLE_REFRESH_TOKEN'),
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start,  # Expected format: "YYYY-MM-DDTHH:MM:SS"
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'UTC',
        },
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event
