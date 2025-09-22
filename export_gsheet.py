import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

EXPORT_SHEET_REFERENCE = {
    "monthly_report": {
        "sheet_id": "ADD_ID",
    }
}

def write_sheet(sheet_id: str, content: list):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()#.get(spreadsheetId=sheet_id).execute()
    sheet_names = {}
    for subsheet in sheet.get(spreadsheetId=sheet_id).execute()["sheets"]:
      sheet_names[subsheet["properties"]["title"]] = {
        "rowCount": subsheet["properties"]["gridProperties"]["rowCount"],
        "columnCount": subsheet["properties"]["gridProperties"]["columnCount"],
      }


if __name__ == "__main__":
    # Read the recipes from the Google Sheets
    pass