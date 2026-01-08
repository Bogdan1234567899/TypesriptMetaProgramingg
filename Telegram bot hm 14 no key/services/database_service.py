import json
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

from config.config import Config

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
                UserId INTEGER PRIMARY KEY,
                Username TEXT,
                FirstName TEXT,
                LastName TEXT,
                Language TEXT,
                CreatedAt TEXT NOT NULL
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS FinancialRecords (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId INTEGER NOT NULL,
                Amount REAL NOT NULL,
                Category TEXT NOT NULL,
                Description TEXT NOT NULL,
                CreatedAt TEXT NOT NULL,
                FOREIGN KEY(UserId) REFERENCES Users(UserId) ON DELETE CASCADE
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Budgets (
                UserId INTEGER NOT NULL,
                Period TEXT NOT NULL,
                Category TEXT NOT NULL,
                Amount REAL NOT NULL,
                CreatedAt TEXT NOT NULL,
                PRIMARY KEY(UserId, Period, Category),
                FOREIGN KEY(UserId) REFERENCES Users(UserId) ON DELETE CASCADE
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS PsychologicalTests (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                UserId INTEGER NOT NULL,
                TakenAt TEXT NOT NULL,
                ScoresJson TEXT NOT NULL,
                Average REAL NOT NULL,
                FOREIGN KEY(UserId) REFERENCES Users(UserId) ON DELETE CASCADE
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS BalanceQuestions (
                UserId INTEGER NOT NULL,
                Sphere TEXT NOT NULL,
                Prompt TEXT NOT NULL,
                CreatedAt TEXT NOT NULL,
                PRIMARY KEY(UserId, Sphere),
                FOREIGN KEY(UserId) REFERENCES Users(UserId) ON DELETE CASCADE
            );
            """
        )

def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def user_exists(user_id: int) -> bool:
    with _connect() as conn:
        row = conn.execute("SELECT 1 FROM Users WHERE UserId=? LIMIT 1;", (user_id,)).fetchone()
    return row is not None

def add_user(user_id: int, username: Optional[str], first_name: Optional[str], last_name: Optional[str], language: str) -> None:
    now = _utcnow_iso()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO Users(UserId, Username, FirstName, LastName, Language, CreatedAt)
            VALUES(?, ?, ?, ?, ?, ?)
            ON CONFLICT(UserId) DO UPDATE SET
                Username=excluded.Username,
                FirstName=excluded.FirstName,
                LastName=excluded.LastName,
                Language=COALESCE(Users.Language, excluded.Language);
            """,
            (user_id, username, first_name, last_name, language, now),
        )

def get_user_language(user_id: int) -> Optional[str]:
    with _connect() as conn:
        row = conn.execute("SELECT Language FROM Users WHERE UserId=? LIMIT 1;", (user_id,)).fetchone()
    if not row:
        return None
    return row["Language"]

def set_user_language(user_id: int, language: str) -> None:
    with _connect() as conn:
        conn.execute("UPDATE Users SET Language=? WHERE UserId=?;", (language, user_id))

def add_financial_data(user_id: int, amount: float, category: str, description: str) -> int:
    now = _utcnow_iso()
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO FinancialRecords(UserId, Amount, Category, Description, CreatedAt)
            VALUES(?, ?, ?, ?, ?);
            """,
            (user_id, amount, category, description, now),
        )
        return int(cur.lastrowid or 0)


def get_financial_report(user_id: int, days: int = 30) -> Dict:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT Amount, Category
            FROM FinancialRecords
            WHERE UserId=? AND CreatedAt >= ?
            ORDER BY CreatedAt DESC;
            """,
            (user_id, since.replace(microsecond=0).isoformat()),
        ).fetchall()

    income_total = 0.0
    expense_total = 0.0
    income_by_cat: Dict[str, float] = {}
    expense_by_cat: Dict[str, float] = {}

    for r in rows:
        amount = float(r["Amount"])
        category = str(r["Category"])
        if amount >= 0:
            income_total += amount
            income_by_cat[category] = income_by_cat.get(category, 0.0) + amount
        else:
            expense_total += abs(amount)
            expense_by_cat[category] = expense_by_cat.get(category, 0.0) + abs(amount)

    return {
        "days": days,
        "count": len(rows),
        "income_total": income_total,
        "expense_total": expense_total,
        "net_total": income_total - expense_total,
        "income_by_category": income_by_cat,
        "expense_by_category": expense_by_cat,
    }

def _period_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")

def _month_range(period: str) -> Tuple[datetime, datetime]:
    year, month = period.split("-")
    y = int(year)
    m = int(month)
    start = datetime(y, m, 1, tzinfo=timezone.utc)
    if m == 12:
        end = datetime(y + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(y, m + 1, 1, tzinfo=timezone.utc)
    return start, end

def set_budget(user_id: int, category: str, amount: float, period: Optional[str] = None) -> None:
    p = period or _period_now()
    now = _utcnow_iso()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO Budgets(UserId, Period, Category, Amount, CreatedAt)
            VALUES(?, ?, ?, ?, ?)
            ON CONFLICT(UserId, Period, Category) DO UPDATE SET
                Amount=excluded.Amount,
                CreatedAt=excluded.CreatedAt;
            """,
            (user_id, p, category, amount, now),
        )

def get_budgets(user_id: int, period: Optional[str] = None) -> Dict[str, float]:
    p = period or _period_now()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT Category, Amount FROM Budgets WHERE UserId=? AND Period=? ORDER BY Category;",
            (user_id, p),
        ).fetchall()
    return {str(r["Category"]): float(r["Amount"]) for r in rows}

def get_month_spent_by_category(user_id: int, category: str, period: Optional[str] = None) -> float:
    p = period or _period_now()
    start, end = _month_range(p)
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT Amount
            FROM FinancialRecords
            WHERE UserId=? AND Category=? AND CreatedAt >= ? AND CreatedAt < ?;
            """,
            (user_id, category, start.isoformat(), end.isoformat()),
        ).fetchall()
    spent = 0.0
    for r in rows:
        a = float(r["Amount"])
        if a < 0:
            spent += abs(a)
    return spent

def add_psychological_test(user_id: int, scores: Dict[str, int]) -> float:
    now = _utcnow_iso()
    avg = sum(scores.values()) / max(len(scores), 1)
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO PsychologicalTests(UserId, TakenAt, ScoresJson, Average)
            VALUES(?, ?, ?, ?);
            """,
            (user_id, now, json.dumps(scores, ensure_ascii=False), float(avg)),
        )
    return float(avg)

def get_last_psychological_test(user_id: int) -> Optional[Tuple[str, Dict[str, int], float]]:
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT TakenAt, ScoresJson, Average
            FROM PsychologicalTests
            WHERE UserId=?
            ORDER BY TakenAt DESC
            LIMIT 1;
            """,
            (user_id,),
        ).fetchone()
    if not row:
        return None
    scores = json.loads(row["ScoresJson"])
    return (str(row["TakenAt"]), {str(k): int(v) for k, v in scores.items()}, float(row["Average"]))

def set_balance_question(user_id: int, sphere: str, prompt: str) -> None:
    now = _utcnow_iso()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO BalanceQuestions(UserId, Sphere, Prompt, CreatedAt)
            VALUES(?, ?, ?, ?)
            ON CONFLICT(UserId, Sphere) DO UPDATE SET
                Prompt=excluded.Prompt,
                CreatedAt=excluded.CreatedAt;
            """,
            (user_id, sphere, prompt, now),
        )

def get_balance_questions(user_id: int) -> List[Tuple[str, str]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT Sphere, Prompt FROM BalanceQuestions WHERE UserId=? ORDER BY Sphere;",
            (user_id,),
        ).fetchall()
    return [(str(r["Sphere"]), str(r["Prompt"])) for r in rows]

def delete_balance_question(user_id: int, sphere: str) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM BalanceQuestions WHERE UserId=? AND Sphere=?;", (user_id, sphere))


def get_last_financial_record_id(user_id: int) -> int:
    with _connect() as conn:
        row = conn.execute(
            "SELECT Id FROM FinancialRecords WHERE UserId=? ORDER BY Id DESC LIMIT 1;",
            (user_id,),
        ).fetchone()
    if not row:
        return 0
    return int(row["Id"])

def delete_financial_record(user_id: int, record_id: int) -> bool:
    with _connect() as conn:
        row = conn.execute("SELECT Id FROM FinancialRecords WHERE UserId=? AND Id=? LIMIT 1;", (user_id, record_id)).fetchone()
        if not row:
            return False
        conn.execute("DELETE FROM FinancialRecords WHERE UserId=? AND Id=?;", (user_id, record_id))
    return True

def get_financial_records_raw(user_id: int, days: int = 30) -> List[Dict]:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    with _connect() as conn:
        rows = conn.execute(
            "SELECT Id, UserId, Amount, Category, Description, CreatedAt FROM FinancialRecords WHERE UserId=? AND CreatedAt>=? ORDER BY CreatedAt;",
            (user_id, since.replace(microsecond=0).isoformat()),
        ).fetchall()
    out: List[Dict] = []
    for r in rows:
        out.append(
            {
                "record_id": int(r["Id"]),
                "user_id": int(r["UserId"]),
                "created_at": datetime.fromisoformat(str(r["CreatedAt"])),
                "type": "income" if float(r["Amount"]) > 0 else "expense",
                "amount": float(r["Amount"]),
                "category": str(r["Category"]),
                "description": str(r["Description"]),
                "photo_ref": "",
            }
        )
    return out

def get_financial_record_by_id(user_id: int, record_id: int) -> Optional[Dict]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT Id, UserId, Amount, Category, Description, CreatedAt FROM FinancialRecords WHERE UserId=? AND Id=? LIMIT 1;",
            (user_id, record_id),
        ).fetchone()
    if not row:
        return None
    created = datetime.fromisoformat(str(row["CreatedAt"]))
    amt = float(row["Amount"])
    return {
        "record_id": int(row["Id"]),
        "user_id": int(row["UserId"]),
        "created_at": created,
        "type": "income" if amt > 0 else "expense",
        "amount": amt,
        "category": str(row["Category"]),
        "description": str(row["Description"]),
        "photo_ref": "",
    }
