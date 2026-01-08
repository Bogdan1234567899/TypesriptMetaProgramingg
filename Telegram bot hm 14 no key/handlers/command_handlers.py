from telegram import Update
from telegram.ext import ContextTypes

from handlers.common import ensure_user
from handlers.menu_handlers import lang_markup, menu_markup
from services.database_service import set_user_language
from services.i18n import lang_label, normalize_lang, t


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    await update.message.reply_text(t(lang, "welcome"))
    await update.message.reply_text(t(lang, "menu_title"), reply_markup=menu_markup(lang))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    await update.message.reply_text(t(lang, "help"), reply_markup=menu_markup(lang))


async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = ensure_user(update)
    if not context.args:
        await update.message.reply_text(t(lang, "choose_language"), reply_markup=lang_markup(lang))
        return
    new_lang = normalize_lang(context.args[0])
    set_user_language(update.effective_user.id, new_lang)
    text = t(new_lang, "lang_set", lang=lang_label(new_lang))
    await update.message.reply_text(text + "\n\n" + t(new_lang, "menu_title"), reply_markup=menu_markup(new_lang))
