import datetime
import gspread
from google.oauth2.service_account import Credentials

from config.config import Config

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(Config.GOOGLE_KEY_PATH, scopes=scopes)
gc = gspread.authorize(creds)

ss = gc.open_by_url(Config.SHEETS_URL)
print("OK spreadsheet:", ss.title)
print("Worksheets:", [w.title for w in ss.worksheets()])

try:
    ws = ss.worksheet(Config.SHEETS_FINANCE_SHEET)
except gspread.WorksheetNotFound:
    ws = ss.add_worksheet(title=Config.SHEETS_FINANCE_SHEET, rows=1000, cols=20)

headers = ["record_id", "user_id", "created_at", "type", "amount", "category", "description", "photo_ref"]
if ws.row_values(1) != headers:
    ws.update("A1:H1", [headers])

row = [
    999999,
    0,
    datetime.datetime.now().replace(microsecond=0).isoformat(),
    "expense",
    1.23,
    "Test",
    "Ping",
    "",
]
ws.append_row(row, value_input_option="USER_ENTERED")
print("APPENDED to:", ws.title)
