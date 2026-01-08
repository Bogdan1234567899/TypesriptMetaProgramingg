import os

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8561396736:AAE53G6rmoBtMUg5Nesl_bXXPnAhqS7LBNI").strip()
    DB_PATH = os.getenv("DB_PATH", "finance_bot.sqlite3").strip()

    GOOGLE_KEY_PATH = os.getenv("GOOGLE_KEY_PATH", "./config/key.json").strip()
    SHEETS_URL = os.getenv("SHEETS_URL", "https://docs.google.com/spreadsheets/d/1ti9nwM2NBtWFnZEYMmQT0gnc8cAAUmtxeSgwGaZY6l4/edit?gid=0#gid=0").strip()
    SHEETS_FINANCE_SHEET = os.getenv("SHEETS_FINANCE_SHEET", "Finance").strip()
    SHEETS_TEST_SHEET = os.getenv("SHEETS_TEST_SHEET", "BalanceTest").strip()
    SHEETS_SUMMARY_SHEET = os.getenv("SHEETS_SUMMARY_SHEET", "Summary").strip()

    DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID", "1nQxr9tJE9pcpOdL5PEsjo-Bsq6bhXd8A").strip()

    ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()}

    SUMMARY_ENABLED = os.getenv("SUMMARY_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off", ""}
    SUMMARY_INTERVAL_MINUTES = int(os.getenv("SUMMARY_INTERVAL_MINUTES", "60").strip() or "60")
