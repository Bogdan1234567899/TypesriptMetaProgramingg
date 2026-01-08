from telegram import Update

from services.database_service import add_user, get_user_language
from services.i18n import normalize_lang

def ensure_user(update: Update) -> str:
    u = update.effective_user
    inferred = normalize_lang(getattr(u, "language_code", None) or "")
    add_user(u.id, getattr(u, "username", None), getattr(u, "first_name", None), getattr(u, "last_name", None), inferred)
    lang = get_user_language(u.id)
    return normalize_lang(lang or inferred)
