from typing import Dict

from services.sheets_service import append_finance_record, append_test_result, is_enabled


def sync_finance_record(record: Dict, photo_ref: str = "") -> bool:
    if not is_enabled():
        return False
    try:
        append_finance_record(
            record_id=int(record["record_id"]),
            user_id=int(record["user_id"]),
            created_at=record["created_at"].replace(microsecond=0).isoformat(),
            record_type=str(record.get("type") or ""),
            amount=float(record.get("amount") or 0),
            category=str(record.get("category") or ""),
            description=str(record.get("description") or ""),
            photo_ref=str(photo_ref or record.get("photo_ref") or ""),
        )
        return True
    except Exception:
        return False


def sync_test(user_id: int, taken_at: str, scores: Dict[str, int], average: float) -> bool:
    if not is_enabled():
        return False
    try:
        append_test_result(user_id=user_id, taken_at=taken_at, scores=scores, average=average)
        return True
    except Exception:
        return False
