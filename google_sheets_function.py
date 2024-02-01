from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

def google_sheets_function(email, rollnumber, timestamp=None, spreadsheet_id='1y4o8UzkPq35PtpcHIEXR3dMaA-1oCcxhYcq0Jiyer-c', sheet_name='Sheet1', credentials_file='credentials.json'):
    # If timestamp is not provided, use the current timestamp
    if timestamp is None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Define the data to be sent
    data = [
        [timestamp, email, rollnumber]
    ]

    try:
        # Authenticate with Google Sheets API
        credentials = service_account.Credentials.from_service_account_file(credentials_file)
        service = build('sheets', 'v4', credentials=credentials)

        # Append data to the spreadsheet
        sheet = service.spreadsheets()
        result = sheet.values().append(
            spreadsheetId=spreadsheet_id,
            range=sheet_name + '!A1',
            valueInputOption='RAW',
            body={'values': data}
        ).execute()

        print('Data appended successfully to Google Sheets.')
        return True

    except Exception as e:
        print(f'Error occurred while appending data to Google Sheets: {e}')
        return False
