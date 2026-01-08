from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from handlers.common import ensure_user
from services.chart_service import build_charts
from services.stats_service import build_stats
from services.sheets_service import (
    delete_finance_record as sheets_delete_finance_record,
    is_enabled as sheets_is_enabled,
)
from services.database_service import (
    get_balance_questions,
    get_budgets,
    get_financial_report,
    get_financial_records_raw,
    get_last_financial_record_id,
    delete_financial_record,
    get_month_spent_by_category,
    set_user_language,
)
from services.i18n import lang_label, normalize_lang, t
from services.psychological_test_service import PsychologicalTestSession, build_scales


def back_markup(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "back_to_menu"), callback_data="back_to_menu")]])


def menu_markup(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(t(lang, "menu_add_expense"), callback_data="add_expense"),
                InlineKeyboardButton(t(lang, "menu_add_income"), callback_data="add_income"),
            ],
            [
                InlineKeyboardButton(t(lang, "menu_report"), callback_data="report"),
                InlineKeyboardButton(t(lang, "menu_charts"), callback_data="charts"),
            ],
            [
                InlineKeyboardButton(t(lang, "menu_stats"), callback_data="stats"),
                InlineKeyboardButton(t(lang, "menu_delete_last"), callback_data="delete_last"),
            ],
            [
                InlineKeyboardButton(t(lang, "menu_budgets"), callback_data="budgets"),
                InlineKeyboardButton(t(lang, "menu_set_budget"), callback_data="set_budget"),
            ],
            [
                InlineKeyboardButton(t(lang, "menu_test"), callback_data="start_test"),
                InlineKeyboardButton(t(lang, "menu_questions"), callback_data="questions"),
            ],
            [InlineKeyboardButton(t(lang, "menu_language"), callback_data="lang")],
        ]
    )


def lang_markup(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Українська", callback_data="set_lang:uk"),
                InlineKeyboardButton("Русский", callback_data="set_lang:ru"),
                InlineKeyboardButton("English", callback_data="set_lang:en"),
            ],
            [InlineKeyboardButton("⬅️", callback_data="back_to_menu")],
        ]
    )


def questions_markup(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("➕", callback_data="questions_add")],
            [InlineKeyboardButton("⬅️", callback_data="back_to_menu")],
        ]
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    await update.message.reply_text(t(lang, "menu_title"), reply_markup=menu_markup(lang))


async def menu_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = ensure_user(update)
    user_id = update.effective_user.id
    data = query.data or ""

    if data == "back_to_menu":
        context.user_data.pop("awaiting", None)
        context.user_data.pop("psych_test", None)
        context.user_data.pop("psych_test_msg", None)
        try:
            await query.edit_message_text(t(lang, "menu_title"), reply_markup=menu_markup(lang))
        except Exception:
            await query.message.reply_text(t(lang, "menu_title"), reply_markup=menu_markup(lang))
        return

    if data == "add_expense":
        context.user_data["awaiting"] = {"type": "add_expense", "chat_id": query.message.chat_id, "message_id": query.message.message_id}
        await query.edit_message_text(t(lang, "ask_add_expense"), reply_markup=back_markup(lang))
        return

    if data == "add_income":
        context.user_data["awaiting"] = {"type": "add_income", "chat_id": query.message.chat_id, "message_id": query.message.message_id}
        await query.edit_message_text(t(lang, "ask_add_income"), reply_markup=back_markup(lang))
        return

    if data == "set_budget":
        context.user_data["awaiting"] = {"type": "set_budget", "chat_id": query.message.chat_id, "message_id": query.message.message_id}
        await query.edit_message_text(t(lang, "ask_set_budget"), reply_markup=back_markup(lang))
        return

    if data == "stats":
        await _send_stats(query.message, user_id, lang, 30)
        return

    if data == "delete_last":
        await _delete_last(query.message, user_id, lang)
        return

    if data == "report":
        await _send_report(query.message, user_id, lang, 30)
        return

    if data == "budgets":
        await _send_budgets(query.message, user_id, lang)
        return

    if data == "charts":
        await _send_charts(query.message, user_id, lang, 30)
        return

    if data == "start_test":
        extra = get_balance_questions(user_id)
        scales = build_scales(lang, extra)
        session = PsychologicalTestSession(user_id=user_id, lang=lang, scales=scales)
        context.user_data["psych_test"] = session.to_json()
        context.user_data["psych_test_msg"] = {"chat_id": query.message.chat_id, "message_id": query.message.message_id}
        await query.edit_message_text(t(lang, "start_test") + "\n\n" + session.current_prompt(), reply_markup=back_markup(lang))
        return

    if data == "questions":
        await _send_questions(query.message, user_id, lang)
        return

    if data == "questions_add":
        context.user_data["awaiting"] = {"type": "add_question", "chat_id": query.message.chat_id, "message_id": query.message.message_id}
        await query.edit_message_text(t(lang, "ask_add_question"), reply_markup=back_markup(lang))
        return

    if data == "lang":
        try:
            await query.edit_message_text(t(lang, "choose_language"), reply_markup=lang_markup(lang))
        except Exception:
            await query.message.reply_text(t(lang, "choose_language"), reply_markup=lang_markup(lang))
        return

    if data.startswith("set_lang:"):
        new_lang = normalize_lang(data.split(":", 1)[1])
        set_user_language(user_id, new_lang)
        text = t(new_lang, "lang_set", lang=lang_label(new_lang)) + "\n\n" + t(new_lang, "menu_title")
        try:
            await query.edit_message_text(text, reply_markup=menu_markup(new_lang))
        except Exception:
            await query.message.reply_text(text, reply_markup=menu_markup(new_lang))
        return


async def _send_report(message, user_id: int, lang: str, days: int) -> None:
    report = get_financial_report(user_id, days)
    if report["count"] == 0:
        await message.reply_text(t(lang, "report_empty"))
        return

    lines = [
        t(lang, "report_title", days=report["days"]),
        t(lang, "income_total", income=report["income_total"]),
        t(lang, "expense_total", expense=report["expense_total"]),
        t(lang, "net_total", net=report["net_total"]),
        "",
    ]

    inc = report["income_by_category"]
    exp = report["expense_by_category"]

    if inc:
        lines.append(t(lang, "by_category_income"))
        for cat, val in sorted(inc.items(), key=lambda x: (-x[1], x[0].lower())):
            lines.append(f"• {cat}: <b>{val:.2f}</b>")
        lines.append("")
    if exp:
        lines.append(t(lang, "by_category_expense"))
        for cat, val in sorted(exp.items(), key=lambda x: (-x[1], x[0].lower())):
            lines.append(f"• {cat}: <b>{val:.2f}</b>")

    await message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)


async def _send_stats(message, user_id: int, lang: str, days: int) -> None:
    records = get_financial_records_raw(user_id, days)
    if not records:
        await message.reply_text(t(lang, "report_empty"))
        return

    s = build_stats(records)
    inc = s["income"]
    exp = s["expense"]
    net = float(s["net"]["sum"])

    lines = [
        t(lang, "stats_title", days=days),
        t(lang, "stats_income_line", count=int(inc["count"]), sum=float(inc["sum"]), mean=float(inc["mean"]), median=float(inc["median"])),
        t(lang, "stats_expense_line", count=int(exp["count"]), sum=float(exp["sum"]), mean=float(exp["mean"]), median=float(exp["median"])),
        t(lang, "stats_net_line", net=net),
    ]
    await message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)


async def _delete_last(message, user_id: int, lang: str) -> None:
    record_id = get_last_financial_record_id(user_id)
    if record_id <= 0:
        await message.reply_text(t(lang, "delete_none"))
        return

    local_ok = delete_financial_record(user_id, record_id)
    sheets_ok = False
    if sheets_is_enabled():
        try:
            sheets_ok = sheets_delete_finance_record(record_id)
        except Exception:
            sheets_ok = False

    if not local_ok and not sheets_ok:
        await message.reply_text(t(lang, "delete_not_found", record_id=record_id))
        return

    await message.reply_text(t(lang, "delete_done", record_id=record_id, local=int(local_ok), sheets=int(sheets_ok)))


async def _send_budgets(message, user_id: int, lang: str) -> None:
    budgets = get_budgets(user_id)
    if not budgets:
        await message.reply_text(t(lang, "budgets_empty"))
        return
    lines = [t(lang, "budgets_title")]
    for cat, lim in sorted(budgets.items(), key=lambda x: x[0].lower()):
        spent = get_month_spent_by_category(user_id, cat)
        lines.append(f"• {cat}: <b>{spent:.2f}</b> / <b>{lim:.2f}</b>")
    await message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)


async def _send_questions(message, user_id: int, lang: str) -> None:
    qs = get_balance_questions(user_id)
    if not qs:
        await message.reply_text(t(lang, "questions_empty"), reply_markup=questions_markup(lang))
        return
    lines = [t(lang, "questions_title")]
    for s, p in qs:
        lines.append(f"• <b>{s}</b>: {p}")
    await message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=questions_markup(lang))


async def _send_charts(message, user_id: int, lang: str, days: int) -> None:
    report = get_financial_report(user_id, days)
    exp = report.get("expense_by_category") or {}
    inc = report.get("income_by_category") or {}

    if not exp and not inc:
        await message.reply_text(t(lang, "charts_empty"))
        return

    if exp:
        title_msg = t(lang, "charts_expense_title", days=days)
        title_plot = title_msg.replace("<b>", "").replace("</b>", "")
        bar, pie = build_charts(exp, title_plot)
        if bar and pie:
            await message.reply_text(title_msg, parse_mode=ParseMode.HTML)
            await message.reply_photo(bar)
            await message.reply_photo(pie)

    if inc:
        title_msg = t(lang, "charts_income_title", days=days)
        title_plot = title_msg.replace("<b>", "").replace("</b>", "")
        bar, pie = build_charts(inc, title_plot)
        if bar and pie:
            await message.reply_text(title_msg, parse_mode=ParseMode.HTML)
            await message.reply_photo(bar)
            await message.reply_photo(pie)
