import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

EXPORT_SHEET_REFERENCE = {
    "doener_main_sheet": {
        "sheet_id": "1A5RJWVoN6YjoTbrZ12aB-uc25WHyeRzm_fsbMbuwaDo",
        "sheet_name": "Tabellenblatt1"
    }
}

SCOPES= ["https://www.googleapis.com/auth/spreadsheets"]

def create_column_letter(col):
  if col > 26:
    return create_column_letter(col // 26) + chr(col % 26 + 64)
  else:
    return chr(col + 64)

def write_sheet(sheet_id: str, range: str, content: list):
  """
  
  Args:
      sheet_id (str): The id of the Google sheets docunment. See EXPORT_SHEET_REFERENCE or sheet URL.
      range (str): the range in which we want to add text
      content (list): list of lists with the content. 
  """
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

  # try:
  if True:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()#.get(spreadsheetId=sheet_id).execute()
    print(sheet_id, range, content[0][0])
    
    # Check if the sheet already exists
    table_name = range.split("!")[0]
    sheet_names = [i["properties"]["title"] for i in sheet.get(spreadsheetId=sheet_id).execute()["sheets"]]
    if table_name in sheet_names:
      sheet.values().clear(spreadsheetId=sheet_id, range=range).execute()
    else:
      sheet.batchUpdate(spreadsheetId=sheet_id, body={"requests": [{"addSheet": {"properties": {"title": table_name}}}]}).execute()
    
    sheet.values().update(spreadsheetId=sheet_id, range=range, valueInputOption="RAW", body={"values": content}).execute()
  # except:
  #   print("Error: Unable to access the Google Sheets API.")

def get_last_row_id(result_sheet):
  return result_sheet
  

def get_range_for_new_entry(sheet_id: str):
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    creds.refresh(Request())
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
    result = {}
    for sheet_name, properties in sheet_names.items():
      result[sheet_name] = {
          "rowCount": properties["rowCount"],
          "columnCount": properties["columnCount"],
        }
      
      range_name = f"{sheet_name}!A1:{create_column_letter(properties['columnCount'])}{properties['rowCount']}"
      print(range_name)
      sheet_result = (
          sheet.values()
          .get(spreadsheetId=sheet_id, range=range_name)
          .execute()
      )
      result[sheet_name] = sheet_result.get("values", [])
    return get_last_row_id(result[EXPORT_SHEET_REFERENCE["doener_main_sheet"]["sheet_name"]])
  except:
    print("failed to get sheet range")
      
      
if __name__ == "__main__":
    # Read the recipes from the Google Sheets
    a = get_range_for_new_entry(EXPORT_SHEET_REFERENCE["doener_main_sheet"]["sheet_id"])
    print(a)