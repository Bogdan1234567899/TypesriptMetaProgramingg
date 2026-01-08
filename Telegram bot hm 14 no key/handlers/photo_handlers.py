from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from handlers.common import ensure_user
from handlers.menu_handlers import menu_markup
from services.database_service import (
    add_financial_data,
    get_budgets,
    get_financial_record_by_id,
    get_month_spent_by_category,
)
from services.drive_service import upload_image_bytes
from services.i18n import t
from services.sync_service import sync_finance_record


async def photo_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    caption = (update.message.caption or "").strip()
    parts = caption.split()
    if len(parts) < 3:
        await update.message.reply_text(t(lang, "photo_format"), reply_markup=menu_markup(lang))
        return
    kind = parts[0].lower()
    if kind not in {"expense", "income"}:
        await update.message.reply_text(t(lang, "photo_format"), reply_markup=menu_markup(lang))
        return
    try:
        amount = float(parts[1].replace(",", "."))
    except ValueError:
        await update.message.reply_text(t(lang, "need_amount_number"), reply_markup=menu_markup(lang))
        return
    amount = abs(amount)
    if amount <= 0:
        await update.message.reply_text(t(lang, "need_amount_positive"), reply_markup=menu_markup(lang))
        return
    category = parts[2].strip()
    description = " ".join(parts[3:]).strip() if len(parts) > 3 else "photo"
    signed_amount = amount if kind == "income" else -amount

    record_id = add_financial_data(user_id, signed_amount, category, description)
    record = get_financial_record_by_id(user_id, record_id)

    photo_ref = ""
    try:
        ph = update.message.photo[-1]
        file = await context.bot.get_file(ph.file_id)
        data = await file.download_as_bytearray()
        link = upload_image_bytes(bytes(data), f"{user_id}_{record_id}.jpg")
        photo_ref = link or ph.file_id
    except Exception:
        photo_ref = ""

    if record:
        sync_finance_record(record, photo_ref=photo_ref)

    text = t(lang, "record_added")
    if kind == "expense":
        budgets = get_budgets(user_id)
        if category in budgets:
            spent = get_month_spent_by_category(user_id, category)
            limit = budgets[category]
            if spent > limit:
                text += "\n" + t(lang, "budget_over", category=category, spent=spent, limit=limit)
            else:
                left = limit - spent
                text += "\n" + t(lang, "budget_left", category=category, left=left, limit=limit)
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=menu_markup(lang))
