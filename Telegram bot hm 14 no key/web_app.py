from flask import Flask, request

from services.plotly_service import build_plotly_html
from services.sheets_service import fetch_finance_records, is_enabled

app = Flask(__name__)

@app.get("/")
def index():
    if not is_enabled():
        return "Google Sheets not configured"
    user_id = request.args.get("user_id", "").strip()
    days = request.args.get("days", "30").strip()
    try:
        d = int(days)
    except Exception:
        d = 30
    uid = None
    if user_id.isdigit():
        uid = int(user_id)
    records = fetch_finance_records(user_id=uid, days=d)
    return build_plotly_html(records, title_prefix="")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
