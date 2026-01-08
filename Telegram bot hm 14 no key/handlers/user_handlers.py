import io
from datetime import datetime, timezone

from telegram import InputFile, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from handlers.common import ensure_user
from handlers.menu_handlers import menu_markup
from services.chart_service import build_charts
from services.database_service import (
    add_financial_data,
    add_psychological_test,
    delete_financial_record,
    get_balance_questions,
    get_budgets,
    get_financial_record_by_id,
    get_financial_records_raw,
    get_financial_report,
    get_last_financial_record_id,
    get_last_psychological_test,
    get_month_spent_by_category,
    set_balance_question,
    set_budget,
)
from services.i18n import t
from services.plotly_service import build_plotly_html
from services.sheets_service import (
    delete_finance_record as sheets_delete_finance_record,
    fetch_finance_records as sheets_fetch_finance_records,
    is_enabled as sheets_is_enabled,
)
from services.stats_service import build_stats
from services.psychological_test_service import PsychologicalTestSession, build_scales, make_recommendations
from services.sync_service import sync_finance_record, sync_test


async def add_financial_record_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    if len(context.args) < 3:
        await update.message.reply_text(t(lang, "format_add_record"), reply_markup=menu_markup(lang))
        return
    try:
        amount = float(context.args[0].replace(",", "."))
    except ValueError:
        await update.message.reply_text(t(lang, "need_amount_number"), reply_markup=menu_markup(lang))
        return
    category = context.args[1].strip()
    description = " ".join(context.args[2:]).strip()
    record_id = add_financial_data(user_id, amount, category, description)
    record = get_financial_record_by_id(user_id, record_id)
    if record:
        sync_finance_record(record)

    text = t(lang, "record_added")
    if amount < 0:
        budgets = get_budgets(user_id)
        if category in budgets:
            spent = get_month_spent_by_category(user_id, category)
            limit = budgets[category]
            if spent > limit:
                text += "\n" + t(lang, "budget_over", category=category, spent=spent, limit=limit)
            else:
                left = limit - spent
                text += "\n" + t(lang, "budget_left", category=category, left=left, limit=limit)
    await update.message.reply_text(text, reply_markup=menu_markup(lang))


async def expense_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    if len(context.args) < 3:
        await update.message.reply_text(t(lang, "format_expense"), reply_markup=menu_markup(lang))
        return
    try:
        amount = float(context.args[0].replace(",", "."))
    except ValueError:
        await update.message.reply_text(t(lang, "need_amount_number"), reply_markup=menu_markup(lang))
        return
    amount = abs(amount)
    if amount <= 0:
        await update.message.reply_text(t(lang, "need_amount_positive"), reply_markup=menu_markup(lang))
        return
    category = context.args[1].strip()
    description = " ".join(context.args[2:]).strip()
    record_id = add_financial_data(user_id, -amount, category, description)
    record = get_financial_record_by_id(user_id, record_id)
    if record:
        sync_finance_record(record)

    text = t(lang, "expense_added")
    budgets = get_budgets(user_id)
    if category in budgets:
        spent = get_month_spent_by_category(user_id, category)
        limit = budgets[category]
        if spent > limit:
            text += "\n" + t(lang, "budget_over", category=category, spent=spent, limit=limit)
        else:
            left = limit - spent
            text += "\n" + t(lang, "budget_left", category=category, left=left, limit=limit)
    await update.message.reply_text(text, reply_markup=menu_markup(lang))


async def income_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    if len(context.args) < 3:
        await update.message.reply_text(t(lang, "format_income"), reply_markup=menu_markup(lang))
        return
    try:
        amount = float(context.args[0].replace(",", "."))
    except ValueError:
        await update.message.reply_text(t(lang, "need_amount_number"), reply_markup=menu_markup(lang))
        return
    amount = abs(amount)
    if amount <= 0:
        await update.message.reply_text(t(lang, "need_amount_positive"), reply_markup=menu_markup(lang))
        return
    category = context.args[1].strip()
    description = " ".join(context.args[2:]).strip()
    record_id = add_financial_data(user_id, amount, category, description)
    record = get_financial_record_by_id(user_id, record_id)
    if record:
        sync_finance_record(record)
    await update.message.reply_text(t(lang, "income_added"), reply_markup=menu_markup(lang))


async def financial_report_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    days = 30
    if context.args:
        try:
            days = int(context.args[0])
        except ValueError:
            days = 30
    report = get_financial_report(user_id, days)
    if report["count"] == 0:
        await update.message.reply_text(t(lang, "report_empty"), reply_markup=menu_markup(lang))
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

    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=menu_markup(lang))


async def budget_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    if len(context.args) < 2:
        await update.message.reply_text(t(lang, "format_set_budget"), reply_markup=menu_markup(lang))
        return
    category = " ".join(context.args[:-1]).strip()
    try:
        amount = float(context.args[-1].replace(",", "."))
    except ValueError:
        await update.message.reply_text(t(lang, "need_amount_number"), reply_markup=menu_markup(lang))
        return
    if amount <= 0:
        await update.message.reply_text(t(lang, "need_budget_positive"), reply_markup=menu_markup(lang))
        return
    set_budget(user_id, category, amount)
    await update.message.reply_text(t(lang, "budget_set_ok", category=category, amount=amount), reply_markup=menu_markup(lang))


async def budgets_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    budgets = get_budgets(user_id)
    if not budgets:
        await update.message.reply_text(t(lang, "budgets_empty"), reply_markup=menu_markup(lang))
        return
    lines = [t(lang, "budgets_title")]
    for cat, lim in sorted(budgets.items(), key=lambda x: x[0].lower()):
        spent = get_month_spent_by_category(user_id, cat)
        lines.append(f"• {cat}: <b>{spent:.2f}</b> / <b>{lim:.2f}</b>")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=menu_markup(lang))


async def start_psychological_test_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    extra = get_balance_questions(user_id)
    scales = build_scales(lang, extra)
    session = PsychologicalTestSession(user_id=user_id, lang=lang, scales=scales)
    context.user_data["psych_test"] = session.to_json()
    await update.message.reply_text(t(lang, "start_test") + "\n\n" + session.current_prompt())


async def balance_report_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    last = get_last_psychological_test(user_id)
    if not last:
        await update.message.reply_text(t(lang, "balance_last_empty"), reply_markup=menu_markup(lang))
        return
    taken_at, scores, avg = last
    lines = [t(lang, "balance_last_title"), f"<i>{taken_at}</i>", ""]
    for k, v in scores.items():
        bar = "█" * v + "░" * (10 - v)
        lines.append(f"• {k}: {v}/10  {bar}")
    lines.append("")
    lines.append(t(lang, "average", avg=avg))
    recs = make_recommendations(scores, lang)
    if recs:
        lines.append("")
        lines.append(t(lang, "recommendations"))
        for r in recs:
            lines.append(f"• {r}")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=menu_markup(lang))


async def add_balance_question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    raw = update.message.text.replace("/add_balance_question", "", 1).strip()
    if "|" not in raw:
        await update.message.reply_text(t(lang, "format_add_question"), reply_markup=menu_markup(lang))
        return
    sphere, prompt = [x.strip() for x in raw.split("|", 1)]
    if not sphere or not prompt:
        await update.message.reply_text(t(lang, "format_add_question"), reply_markup=menu_markup(lang))
        return
    set_balance_question(user_id, sphere, prompt)
    await update.message.reply_text(t(lang, "added_question_ok", sphere=sphere), reply_markup=menu_markup(lang))


async def balance_questions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    qs = get_balance_questions(user_id)
    if not qs:
        await update.message.reply_text(t(lang, "questions_empty"), parse_mode=ParseMode.HTML, reply_markup=menu_markup(lang))
        return
    lines = [t(lang, "questions_title")]
    for s, p in qs:
        lines.append(f"• <b>{s}</b>: {p}")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=menu_markup(lang))


async def charts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    days = 30
    if context.args:
        try:
            days = int(context.args[0])
        except ValueError:
            days = 30

    report = get_financial_report(user_id, days)
    exp = report.get("expense_by_category") or {}
    inc = report.get("income_by_category") or {}

    if not exp and not inc:
        await update.message.reply_text(t(lang, "charts_empty"), reply_markup=menu_markup(lang))
        return

    if exp:
        title_msg = t(lang, "charts_expense_title", days=days)
        title_plot = title_msg.replace("<b>", "").replace("</b>", "")
        bar, pie = build_charts(exp, title_plot)
        if bar and pie:
            await update.message.reply_text(title_msg, parse_mode=ParseMode.HTML, reply_markup=menu_markup(lang))
            await update.message.reply_photo(bar)
            await update.message.reply_photo(pie)

    if inc:
        title_msg = t(lang, "charts_income_title", days=days)
        title_plot = title_msg.replace("<b>", "").replace("</b>", "")
        bar, pie = build_charts(inc, title_plot)
        if bar and pie:
            await update.message.reply_text(title_msg, parse_mode=ParseMode.HTML, reply_markup=menu_markup(lang))
            await update.message.reply_photo(bar)
            await update.message.reply_photo(pie)

    records = []
    try:
        if sheets_is_enabled():
            records = sheets_fetch_finance_records(user_id=user_id, days=days)
        else:
            records = get_financial_records_raw(user_id, days)
    except Exception:
        records = get_financial_records_raw(user_id, days)

    html = build_plotly_html(records, title_prefix="")
    buf = io.BytesIO(html.encode("utf-8"))
    buf.name = f"charts_{days}d.html"
    await update.message.reply_document(InputFile(buf), filename=buf.name)


async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    days = 30
    if context.args:
        try:
            days = int(context.args[0])
        except ValueError:
            days = 30
    records = []
    try:
        if sheets_is_enabled():
            records = sheets_fetch_finance_records(user_id=user_id, days=days)
        else:
            records = get_financial_records_raw(user_id, days)
    except Exception:
        records = get_financial_records_raw(user_id, days)
    s = build_stats(records)
    inc = s["income"]
    exp = s["expense"]
    net = s["net"]["sum"]
    lines = [
        t(lang, "stats_title", days=days),
        t(lang, "stats_income_line", count=inc["count"], sum=inc["sum"], mean=inc["mean"], median=inc["median"]),
        t(lang, "stats_expense_line", count=exp["count"], sum=exp["sum"], mean=exp["mean"], median=exp["median"]),
        t(lang, "stats_net_line", net=net),
    ]
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=menu_markup(lang))


async def delete_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text(t(lang, "format_delete"), reply_markup=menu_markup(lang))
        return
    target = context.args[0].strip().lower()
    record_id = 0
    if target == "last":
        record_id = get_last_financial_record_id(user_id)
        if record_id <= 0:
            await update.message.reply_text(t(lang, "delete_none"), reply_markup=menu_markup(lang))
            return
    else:
        try:
            record_id = int(target)
        except ValueError:
            await update.message.reply_text(t(lang, "format_delete"), reply_markup=menu_markup(lang))
            return
    local_ok = delete_financial_record(user_id, record_id)
    sheets_ok = False
    if sheets_is_enabled():
        try:
            sheets_ok = sheets_delete_finance_record(record_id)
        except Exception:
            sheets_ok = False
    if not local_ok and not sheets_ok:
        await update.message.reply_text(t(lang, "delete_not_found", record_id=record_id), reply_markup=menu_markup(lang))
        return
    await update.message.reply_text(t(lang, "delete_done", record_id=record_id, local=int(local_ok), sheets=int(sheets_ok)), reply_markup=menu_markup(lang))


async def finish_psychological_test_from_text(update: Update, context: ContextTypes.DEFAULT_TYPE, scores: dict) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    avg = add_psychological_test(user_id, scores)
    sync_test(user_id, datetime.now(timezone.utc).replace(microsecond=0).isoformat(), scores, avg)
    lines = []
    for k, v in scores.items():
        bar = "█" * v + "░" * (10 - v)
        lines.append(f"• {k}: {v}/10  {bar}")
    lines.append("")
    lines.append(t(lang, "average", avg=avg))
    recs = make_recommendations(scores, lang)
    if recs:
        lines.append("")
        lines.append(t(lang, "recommendations"))
        for r in recs:
            lines.append(f"• {r}")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)
