import json
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

import gspread
from google.oauth2 import service_account

from config.config import Config

_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_client = None
_spreadsheet = None

def _enabled() -> bool:
    return bool(Config.GOOGLE_KEY_PATH and Config.SHEETS_URL)

def is_enabled() -> bool:
    return _enabled()

def _get_client() -> gspread.Client:
    global _client
    if _client is not None:
        return _client
    if not _enabled():
        raise RuntimeError("Google Sheets not configured")
    creds = service_account.Credentials.from_service_account_file(Config.GOOGLE_KEY_PATH, scopes=_SCOPES)
    _client = gspread.authorize(creds)
    return _client

def _get_spreadsheet():
    global _spreadsheet
    if _spreadsheet is not None:
        return _spreadsheet
    _spreadsheet = _get_client().open_by_url(Config.SHEETS_URL)
    return _spreadsheet

def _ensure_worksheet(title: str, headers: List[str]):
    ss = _get_spreadsheet()
    try:
        ws = ss.worksheet(title)
    except Exception:
        ws = ss.add_worksheet(title=title, rows=1000, cols=max(10, len(headers) + 2))
    values = ws.get_all_values()
    if not values:
        ws.append_row(headers)
    else:
        first = values[0]
        if [h.strip() for h in first] != headers:
            ws.clear()
            ws.append_row(headers)
    return ws

def finance_ws():
    headers = ["RecordId", "UserId", "CreatedAt", "Type", "Amount", "Category", "Description", "PhotoRef"]
    return _ensure_worksheet(Config.SHEETS_FINANCE_SHEET, headers)

def test_ws():
    headers = ["UserId", "TakenAt", "ScoresJson", "Average"]
    return _ensure_worksheet(Config.SHEETS_TEST_SHEET, headers)

def summary_ws():
    headers = ["Timestamp", "Income24h", "Expense24h", "Net24h"]
    return _ensure_worksheet(Config.SHEETS_SUMMARY_SHEET, headers)

def append_finance_record(
    record_id: int,
    user_id: int,
    created_at: str,
    record_type: str,
    amount: float,
    category: str,
    description: str,
    photo_ref: str = "",
) -> None:
    ws = finance_ws()
    ws.append_row(
        [int(record_id), int(user_id), str(created_at), str(record_type), float(amount), str(category), str(description), str(photo_ref)],
        value_input_option="USER_ENTERED",
    )

def append_test_result(user_id: int, taken_at: str, scores: Dict[str, int], average: float) -> None:
    ws = test_ws()
    ws.append_row([int(user_id), str(taken_at), json.dumps(scores, ensure_ascii=False), float(average)], value_input_option="USER_ENTERED")

def _parse_dt(value: str) -> Optional[datetime]:
    v = (value or "").strip()
    if not v:
        return None
    try:
        dt = datetime.fromisoformat(v)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        try:
            return datetime.strptime(v, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        except Exception:
            return None

def fetch_finance_records(user_id: Optional[int] = None, days: Optional[int] = None) -> List[Dict]:
    ws = finance_ws()
    rows = ws.get_all_records()
    since = None
    if days is not None:
        since = datetime.now(timezone.utc) - timedelta(days=int(days))
    out: List[Dict] = []
    for r in rows:
        try:
            rid = int(r.get("RecordId") or 0)
        except Exception:
            continue
        try:
            uid = int(r.get("UserId") or 0)
        except Exception:
            uid = 0
        if user_id is not None and uid != int(user_id):
            continue
        created = _parse_dt(str(r.get("CreatedAt") or ""))
        if since is not None and created is not None and created < since:
            continue
        rec = {
            "record_id": rid,
            "user_id": uid,
            "created_at": created,
            "type": str(r.get("Type") or ""),
            "amount": float(r.get("Amount") or 0),
            "category": str(r.get("Category") or ""),
            "description": str(r.get("Description") or ""),
            "photo_ref": str(r.get("PhotoRef") or ""),
        }
        out.append(rec)
    out.sort(key=lambda x: (x["created_at"] or datetime.min.replace(tzinfo=timezone.utc)))
    return out

def delete_finance_record(record_id: int) -> bool:
    ws = finance_ws()
    col = ws.col_values(1)
    target = str(int(record_id))
    for idx, val in enumerate(col, start=1):
        if idx == 1:
            continue
        if str(val).strip() == target:
            ws.delete_rows(idx)
            return True
    return False

def update_summary_24h() -> Optional[Tuple[float, float, float]]:
    if not _enabled():
        return None
    records = fetch_finance_records(user_id=None, days=1)
    income = 0.0
    expense = 0.0
    for r in records:
        amt = float(r["amount"])
        typ = (r["type"] or "").lower()
        if typ == "income" or amt > 0:
            income += abs(amt)
        else:
            expense += abs(amt)
    net = income - expense
    ws = summary_ws()
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    ws.append_row([now, float(income), float(expense), float(net)], value_input_option="USER_ENTERED")
    return income, expense, net
