from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from config.config import Config
from handlers.command_handlers import help_command, lang_command, start_command
from handlers.menu_handlers import menu_callback_handler, menu_command
from handlers.text_handlers import handle_text_message
from handlers.photo_handlers import photo_message_handler
from handlers.user_handlers import (
    add_balance_question_handler,
    add_financial_record_handler,
    balance_questions_handler,
    balance_report_handler,
    budget_set_handler,
    budgets_handler,
    charts_handler,
    stats_handler,
    delete_handler,
    expense_handler,
    financial_report_handler,
    income_handler,
    start_psychological_test_handler,
)
from services.database_service import init_db
from services.sheets_service import is_enabled as sheets_is_enabled, update_summary_24h
import asyncio


def main() -> None:
    init_db()
    if not Config.TELEGRAM_TOKEN:
        raise SystemExit("TELEGRAM_TOKEN не заданий.")
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("lang", lang_command))

    application.add_handler(CommandHandler("expense", expense_handler))
    application.add_handler(CommandHandler("income", income_handler))

    application.add_handler(CommandHandler("add_financial_record", add_financial_record_handler))
    application.add_handler(CommandHandler("financial_report", financial_report_handler))

    application.add_handler(CommandHandler("budget_set", budget_set_handler))
    application.add_handler(CommandHandler("set_budget", budget_set_handler))
    application.add_handler(CommandHandler("budgets", budgets_handler))

    application.add_handler(CommandHandler("charts", charts_handler))
    application.add_handler(CommandHandler("stats", stats_handler))
    application.add_handler(CommandHandler("delete", delete_handler))

    application.add_handler(CommandHandler("start_psychological_test", start_psychological_test_handler))
    application.add_handler(CommandHandler("balance_report", balance_report_handler))
    application.add_handler(CommandHandler("add_balance_question", add_balance_question_handler))
    application.add_handler(CommandHandler("balance_questions", balance_questions_handler))

    application.add_handler(CallbackQueryHandler(menu_callback_handler))
    application.add_handler(MessageHandler(filters.PHOTO, photo_message_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    async def _summary_job(context):
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, update_summary_24h)
        except Exception:
            return

    if Config.SUMMARY_ENABLED and sheets_is_enabled():
        interval = max(5, int(Config.SUMMARY_INTERVAL_MINUTES)) * 60
        if application.job_queue is not None:
            application.job_queue.run_repeating(_summary_job, interval=interval, first=60)
        else:
            print('JobQueue недоступний. Встанови: pip install "python-telegram-bot[job-queue]" (summary вимкнено).')

    application.run_polling()


if __name__ == "__main__":
    main()
