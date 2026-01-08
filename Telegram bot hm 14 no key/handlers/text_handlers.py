from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from handlers.common import ensure_user
from handlers.menu_handlers import back_markup, menu_markup
from services.database_service import (
    add_financial_data,
    get_budgets,
    get_financial_record_by_id,
    get_month_spent_by_category,
    set_balance_question,
    set_budget,
)
from services.sync_service import sync_finance_record
from services.i18n import t
from services.psychological_test_service import PsychologicalTestSession, parse_score
from handlers.user_handlers import finish_psychological_test_from_text


async def _restore_menu(context: ContextTypes.DEFAULT_TYPE, chat_id: Optional[int], message_id: Optional[int], lang: str, fallback_message=None) -> None:
    if chat_id is not None and message_id is not None:
        try:
            await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=t(lang, "menu_title"), reply_markup=menu_markup(lang))
            return
        except Exception:
            pass
    if fallback_message is not None:
        await fallback_message.reply_text(t(lang, "menu_title"), reply_markup=menu_markup(lang))


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    user_id = update.effective_user.id
    text = (update.message.text or "").strip()

    if "psych_test" in context.user_data:
        session = PsychologicalTestSession.from_json(context.user_data["psych_test"])
        value = parse_score(text)
        if value is None:
            await update.message.reply_text(t(lang, "enter_1_10"))
            return
        session.record_score(value)
        msg_ref = context.user_data.get("psych_test_msg") or {}
        chat_id = msg_ref.get("chat_id")
        message_id = msg_ref.get("message_id")
        if session.is_active():
            context.user_data["psych_test"] = session.to_json()
            if chat_id is not None and message_id is not None:
                try:
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=session.current_prompt(), reply_markup=back_markup(lang))
                except Exception:
                    await update.message.reply_text(session.current_prompt())
            else:
                await update.message.reply_text(session.current_prompt())
            return
        scores = session.scores
        context.user_data.pop("psych_test", None)
        context.user_data.pop("psych_test_msg", None)
        await finish_psychological_test_from_text(update, context, scores)
        await _restore_menu(context, chat_id, message_id, lang, update.message)
        return

    awaiting = context.user_data.get("awaiting")
    if awaiting:
        kind = awaiting.get("type")
        chat_id = awaiting.get("chat_id")
        message_id = awaiting.get("message_id")

        if kind in {"add_record", "add_expense", "add_income"}:
            parts = text.split()
            if len(parts) < 3:
                key = "ask_add_record"
                if kind == "add_expense":
                    key = "ask_add_expense"
                if kind == "add_income":
                    key = "ask_add_income"
                await update.message.reply_text(t(lang, key))
                return
            try:
                amount = float(parts[0].replace(",", "."))
            except ValueError:
                await update.message.reply_text(t(lang, "need_amount_number"))
                return
            category = parts[1].strip()
            description = " ".join(parts[2:]).strip()

            if kind == "add_income":
                amount = abs(amount)
                if amount <= 0:
                    await update.message.reply_text(t(lang, "need_amount_positive"))
                    return
                record_id = add_financial_data(user_id, amount, category, description)
                record = get_financial_record_by_id(user_id, record_id)
                if record:
                    sync_finance_record(record)
                context.user_data.pop("awaiting", None)
                await update.message.reply_text(t(lang, "income_added"))
                await _restore_menu(context, chat_id, message_id, lang, update.message)
                return

            if kind == "add_expense":
                amount = abs(amount)
                if amount <= 0:
                    await update.message.reply_text(t(lang, "need_amount_positive"))
                    return
                record_id = add_financial_data(user_id, -amount, category, description)
                record = get_financial_record_by_id(user_id, record_id)
                if record:
                    sync_finance_record(record)
                context.user_data.pop("awaiting", None)
                msg = t(lang, "expense_added")
                budgets = get_budgets(user_id)
                if category in budgets:
                    spent = get_month_spent_by_category(user_id, category)
                    limit = budgets[category]
                    if spent > limit:
                        msg += "\n" + t(lang, "budget_over", category=category, spent=spent, limit=limit)
                    else:
                        left = limit - spent
                        msg += "\n" + t(lang, "budget_left", category=category, left=left, limit=limit)
                await update.message.reply_text(msg)
                await _restore_menu(context, chat_id, message_id, lang, update.message)
                return
                record_id = add_financial_data(user_id, amount, category, description)
                record = get_financial_record_by_id(user_id, record_id)
                if record:
                    sync_finance_record(record)
            context.user_data.pop("awaiting", None)
            await update.message.reply_text(t(lang, "record_added"))
            await _restore_menu(context, chat_id, message_id, lang, update.message)
            return

        if kind == "set_budget":
            parts = text.split()
            if len(parts) < 2:
                await update.message.reply_text(t(lang, "ask_set_budget"))
                return
            category = " ".join(parts[:-1]).strip()
            try:
                amount = float(parts[-1].replace(",", "."))
            except ValueError:
                await update.message.reply_text(t(lang, "need_amount_number"))
                return
            if amount <= 0:
                await update.message.reply_text(t(lang, "need_budget_positive"))
                return
            set_budget(user_id, category, amount)
            context.user_data.pop("awaiting", None)
            await update.message.reply_text(t(lang, "budget_set_ok", category=category, amount=amount))
            await _restore_menu(context, chat_id, message_id, lang, update.message)
            return

        if kind == "add_question":
            if "|" not in text:
                await update.message.reply_text(t(lang, "ask_add_question"))
                return
            sphere, prompt = [x.strip() for x in text.split("|", 1)]
            if not sphere or not prompt:
                await update.message.reply_text(t(lang, "ask_add_question"))
                return
            set_balance_question(user_id, sphere, prompt)
            context.user_data.pop("awaiting", None)
            await update.message.reply_text(t(lang, "added_question_ok", sphere=sphere))
            await _restore_menu(context, chat_id, message_id, lang, update.message)
            return

        context.user_data.pop("awaiting", None)

    await update.message.reply_text(t(lang, "unknown"), reply_markup=menu_markup(lang))
