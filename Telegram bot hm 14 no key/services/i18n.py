from typing import Dict

_TEXT: Dict[str, Dict[str, str]] = {
    "uk": {
        "bot_name": "FinanceBalanceBot",
        "welcome": "Привіт! Я бот для фінансів і тесту життєвого балансу.",
        "help": (
            "Команди:\n"
            "• /menu — меню\n"
            "• Додати витрати: /expense <сума> <категорія> <опис>\n"
            "  приклад: /expense 120 Їжа Обід\n"
            "• Додати доходи: /income <сума> <категорія> <опис>\n"
            "  приклад: /income 5000 Зарплата Аванс\n"
            "• (альтернатива) /add_financial_record <сума> <категорія> <опис>\n"
            "  витрати — сума зі знаком мінус: -120\n"
            "• /financial_report [днів] — звіт (за замовч. 30)\n"
            "• /budget_set <категорія> <сума> — встановити бюджет на місяць\n"
            "• /budgets — переглянути бюджети\n"
            "• /charts [днів] — графіки (витрати та/або доходи)\n"
            "• /start_psychological_test — тест «Колесо життєвого балансу»\n"
            "• /balance_report — останній результат тесту\n"
            "• /add_balance_question <сфера> | <питання> — додати питання\n"
            "• /balance_questions — список додаткових питань\n"
            "• /lang <uk|ru|en> — мова\n"
            "• /help — довідка"
                    + "• /stats [днів] — статистика\n• /delete last або /delete <id> — видалення\n• Фото з підписом: expense ... або income ...\n"
),
        "menu_title": "Меню:",
        "need_amount_number": "Сума має бути числом.",
        "need_amount_positive": "Сума має бути більше 0.",
        "need_budget_positive": "Сума бюджету має бути більше 0.",
        "record_added": "✅ Запис додано.",
        "expense_added": "✅ Витрати додано.",
        "income_added": "✅ Доходи додано.",
        "budget_over": "⚠️ Бюджет перевищено по категорії «{category}»: {spent:.2f} / {limit:.2f}",
        "budget_left": "Бюджет «{category}»: залишилось {left:.2f} з {limit:.2f}",
        "format_add_record": "Формат: /add_financial_record <сума> <категорія> <опис>",
        "format_expense": "Формат: /expense <сума> <категорія> <опис>",
        "format_income": "Формат: /income <сума> <категорія> <опис>",
        "format_set_budget": "Формат: /budget_set <категорія> <сума>",
        "budget_set_ok": "✅ Бюджет встановлено: {category} = {amount:.2f}",
        "budgets_empty": "Бюджетів немає. Додай: /budget_set <категорія> <сума>",
        "budgets_title": "📒 <b>Бюджети на цей місяць:</b>",
        "report_empty": "Немає записів за обраний період.",
        "report_title": "📊 <b>Фінансовий звіт за {days} дн.</b>",
        "income_total": "Доходи: <b>{income:.2f}</b>",
        "expense_total": "Витрати: <b>{expense:.2f}</b>",
        "net_total": "Баланс: <b>{net:.2f}</b>",
        "by_category_income": "Доходи за категоріями:",
        "by_category_expense": "Витрати за категоріями:",
        "start_test": "🧠 Починаємо тест «Колесо життєвого балансу».\nВідповідай числами від 1 до 10.",
        "enter_1_10": "Введи число від 1 до 10.",
        "balance_last_empty": "Ще немає результатів. Запусти: /start_psychological_test",
        "balance_last_title": "🧩 <b>Останній результат тесту:</b>",
        "average": "Середня оцінка: <b>{avg:.1f}</b>/10",
        "recommendations": "Рекомендації:",
        "added_question_ok": "✅ Питання додано для сфери «{sphere}».",
        "format_add_question": "Формат: /add_balance_question <сфера> | <питання>",
        "questions_empty": "Додаткових питань немає. Додай: /add_balance_question <сфера> | <питання>",
        "questions_title": "📝 <b>Додаткові питання:</b>",
        "charts_empty": "Немає даних для графіків за цей період.",
        "charts_expense_title": "📉 <b>Витрати за категоріями за {days} дн.</b>",
        "charts_income_title": "📈 <b>Доходи за категоріями за {days} дн.</b>",
        "ask_add_record": "Введи запис: <сума> <категорія> <опис> (витрати — мінус, доходи — плюс)",
        "ask_add_expense": "Введи витрати: <сума> <категорія> <опис> (сума без мінуса)",
        "ask_add_income": "Введи доходи: <сума> <категорія> <опис>",
        "ask_set_budget": "Введи бюджет: <категорія> <сума>",
        "ask_add_question": "Введи: <сфера> | <питання>",
        "choose_language": "Обери мову:",
        "lang_set": "✅ Мову змінено: {lang}",
        "unknown": "Я розумію команди. Напиши /menu або /help.",
        "menu_add_record": "➕ Запис",
        "menu_add_expense": "➖ Витрати",
        "menu_add_income": "➕ Доходи",
        "menu_report": "📊 Звіт",
        "menu_charts": "📈 Графіки",
        "menu_budgets": "📒 Мої бюджети",
        "menu_set_budget": "➕ Встановити бюджет",
        "menu_test": "🧠 Тест",
        "menu_questions": "📝 Питання",
        "menu_language": "🌐 Мова",
        "back_to_menu": "⬅️ Меню",
        "menu_stats": "📊 Статистика",
        "menu_delete_last": "🗑 Видалити останній",
        "format_delete": "Формат: /delete last або /delete <id>",
        "delete_none": "Немає записів для видалення.",
        "delete_not_found": "Не знайдено запис {record_id}.",
        "delete_done": "🗑 Видалено запис {record_id}. SQLite={local} Sheets={sheets}",
        "stats_title": "<b>Статистика за {days} днів</b>",
        "stats_income_line": "Доходи: к-сть={count}, сума={sum:.2f}, середнє={mean:.2f}, медіана={median:.2f}",
        "stats_expense_line": "Витрати: к-сть={count}, сума={sum:.2f}, середнє={mean:.2f}, медіана={median:.2f}",
        "stats_net_line": "Чистий результат: <b>{net:.2f}</b>",
        "photo_format": "Фото з підписом: expense <сума> <категорія> <опис> або income <сума> <категорія> <опис>",
    },
    "ru": {
        "bot_name": "FinanceBalanceBot",
        "welcome": "Привет! Я бот для финансов и теста жизненного баланса.",
        "help": (
            "Команды:\n"
            "• /menu — меню\n"
            "• Добавить расход: /expense <сумма> <категория> <описание>\n"
            "  пример: /expense 120 Еда Обед\n"
            "• Добавить доход: /income <сумма> <категория> <описание>\n"
            "  пример: /income 5000 Зарплата Аванс\n"
            "• (альтернатива) /add_financial_record <сумма> <категория> <описание>\n"
            "  расходы — сумма с минусом: -120\n"
            "• /financial_report [дней] — отчёт (по умолч. 30)\n"
            "• /budget_set <категория> <сумма> — установить бюджет на месяц\n"
            "• /budgets — посмотреть бюджеты\n"
            "• /charts [дней] — графики (расходы и/или доходы)\n"
            "• /start_psychological_test — тест «Колесо жизненного баланса»\n"
            "• /balance_report — последний результат теста\n"
            "• /add_balance_question <сфера> | <вопрос> — добавить вопрос\n"
            "• /balance_questions — список дополнительных вопросов\n"
            "• /lang <uk|ru|en> — язык\n"
            "• /help — справка"
                    + "• /stats [дней] — статистика\n• /delete last или /delete <id> — удаление\n• Фото с подписью: expense ... или income ...\n"
),
        "menu_title": "Меню:",
        "need_amount_number": "Сумма должна быть числом.",
        "need_amount_positive": "Сумма должна быть больше 0.",
        "need_budget_positive": "Сумма бюджета должна быть больше 0.",
        "record_added": "✅ Запись добавлена.",
        "expense_added": "✅ Расход добавлен.",
        "income_added": "✅ Доход добавлен.",
        "budget_over": "⚠️ Бюджет превышен по категории «{category}»: {spent:.2f} / {limit:.2f}",
        "budget_left": "Бюджет «{category}»: осталось {left:.2f} из {limit:.2f}",
        "format_add_record": "Формат: /add_financial_record <сумма> <категория> <описание>",
        "format_expense": "Формат: /expense <сумма> <категория> <описание>",
        "format_income": "Формат: /income <сумма> <категория> <описание>",
        "format_set_budget": "Формат: /budget_set <категория> <сумма>",
        "budget_set_ok": "✅ Бюджет установлен: {category} = {amount:.2f}",
        "budgets_empty": "Бюджетов нет. Добавь: /budget_set <категория> <сумма>",
        "budgets_title": "📒 <b>Бюджеты на этот месяц:</b>",
        "report_empty": "Нет записей за выбранный период.",
        "report_title": "📊 <b>Финансовый отчёт за {days} дн.</b>",
        "income_total": "Доходы: <b>{income:.2f}</b>",
        "expense_total": "Расходы: <b>{expense:.2f}</b>",
        "net_total": "Баланс: <b>{net:.2f}</b>",
        "by_category_income": "Доходы по категориям:",
        "by_category_expense": "Расходы по категориям:",
        "start_test": "🧠 Начинаем тест «Колесо жизненного баланса».\nОтвечай числами от 1 до 10.",
        "enter_1_10": "Введи число от 1 до 10.",
        "balance_last_empty": "Результатов ещё нет. Запусти: /start_psychological_test",
        "balance_last_title": "🧩 <b>Последний результат теста:</b>",
        "average": "Средняя оценка: <b>{avg:.1f}</b>/10",
        "recommendations": "Рекомендации:",
        "added_question_ok": "✅ Вопрос добавлен для сферы «{sphere}».",
        "format_add_question": "Формат: /add_balance_question <сфера> | <вопрос>",
        "questions_empty": "Дополнительных вопросов нет. Добавь: /add_balance_question <сфера> | <вопрос>",
        "questions_title": "📝 <b>Дополнительные вопросы:</b>",
        "charts_empty": "Нет данных для графиков за этот период.",
        "charts_expense_title": "📉 <b>Расходы по категориям за {days} дн.</b>",
        "charts_income_title": "📈 <b>Доходы по категориям за {days} дн.</b>",
        "ask_add_record": "Введи запись: <сумма> <категория> <описание> (расходы — минус, доходы — плюс)",
        "ask_add_expense": "Введи расход: <сумма> <категория> <описание> (сумма без минуса)",
        "ask_add_income": "Введи доход: <сумма> <категория> <описание>",
        "ask_set_budget": "Введи бюджет: <категория> <сумма>",
        "ask_add_question": "Введи: <сфера> | <вопрос>",
        "choose_language": "Выбери язык:",
        "lang_set": "✅ Язык изменён: {lang}",
        "unknown": "Я понимаю команды. Напиши /menu или /help.",
        "menu_add_record": "➕ Запись",
        "menu_add_expense": "➖ Расход",
        "menu_add_income": "➕ Доход",
        "menu_report": "📊 Отчёт",
        "menu_charts": "📈 Графики",
        "menu_budgets": "📒 Мои бюджеты",
        "menu_set_budget": "➕ Установить бюджет",
        "menu_test": "🧠 Тест",
        "menu_questions": "📝 Вопросы",
        "menu_language": "🌐 Язык",
        "back_to_menu": "⬅️ Меню",
        "menu_stats": "📊 Статистика",
        "menu_delete_last": "🗑 Удалить последнее",
        "format_delete": "Формат: /delete last или /delete <id>",
        "delete_none": "Нет записей для удаления.",
        "delete_not_found": "Запись {record_id} не найдена.",
        "delete_done": "🗑 Удалено {record_id}. SQLite={local} Sheets={sheets}",
        "stats_title": "<b>Статистика за {days} дней</b>",
        "stats_income_line": "Доходы: кол-во={count}, сумма={sum:.2f}, среднее={mean:.2f}, медиана={median:.2f}",
        "stats_expense_line": "Расходы: кол-во={count}, сумма={sum:.2f}, среднее={mean:.2f}, медиана={median:.2f}",
        "stats_net_line": "Итог: <b>{net:.2f}</b>",
        "photo_format": "Фото с подписью: expense <сумма> <категория> <описание> или income <сумма> <категория> <описание>",
    },
    "en": {
        "bot_name": "FinanceBalanceBot",
        "welcome": "Hi! I’m a bot for finance tracking and the life-balance test.",
        "help": (
            "Commands:\n"
            "• /menu — menu\n"
            "• Add expense: /expense <amount> <category> <description>\n"
            "  example: /expense 120 Food Lunch\n"
            "• Add income: /income <amount> <category> <description>\n"
            "  example: /income 5000 Salary Advance\n"
            "• (alternative) /add_financial_record <amount> <category> <description>\n"
            "  expenses use minus sign: -120\n"
            "• /financial_report [days] — report (default 30)\n"
            "• /budget_set <category> <amount> — set monthly budget\n"
            "• /budgets — view budgets\n"
            "• /charts [days] — charts (expenses and/or income)\n"
            "• /start_psychological_test — “Wheel of life balance” test\n"
            "• /balance_report — last test result\n"
            "• /add_balance_question <sphere> | <question> — add a question\n"
            "• /balance_questions — list extra questions\n"
            "• /lang <uk|ru|en> — language\n"
            "• /help — help"
                    + "• /stats [days] — stats\n• /delete last or /delete <id> — delete\n• Photo with caption: expense ... or income ...\n"
),
        "menu_title": "Menu:",
        "need_amount_number": "Amount must be a number.",
        "need_amount_positive": "Amount must be greater than 0.",
        "need_budget_positive": "Budget amount must be greater than 0.",
        "record_added": "✅ Record added.",
        "expense_added": "✅ Expense added.",
        "income_added": "✅ Income added.",
        "budget_over": "⚠️ Budget exceeded for “{category}”: {spent:.2f} / {limit:.2f}",
        "budget_left": "Budget “{category}”: {left:.2f} left of {limit:.2f}",
        "format_add_record": "Format: /add_financial_record <amount> <category> <description>",
        "format_expense": "Format: /expense <amount> <category> <description>",
        "format_income": "Format: /income <amount> <category> <description>",
        "format_set_budget": "Format: /budget_set <category> <amount>",
        "budget_set_ok": "✅ Budget set: {category} = {amount:.2f}",
        "budgets_empty": "No budgets yet. Add: /budget_set <category> <amount>",
        "budgets_title": "📒 <b>Budgets for this month:</b>",
        "report_empty": "No records for the selected period.",
        "report_title": "📊 <b>Financial report for {days} days</b>",
        "income_total": "Income: <b>{income:.2f}</b>",
        "expense_total": "Expenses: <b>{expense:.2f}</b>",
        "net_total": "Net: <b>{net:.2f}</b>",
        "by_category_income": "Income by category:",
        "by_category_expense": "Expenses by category:",
        "start_test": "🧠 Starting the “Wheel of life balance” test.\nReply with numbers from 1 to 10.",
        "enter_1_10": "Enter a number from 1 to 10.",
        "balance_last_empty": "No results yet. Run: /start_psychological_test",
        "balance_last_title": "🧩 <b>Last test result:</b>",
        "average": "Average score: <b>{avg:.1f}</b>/10",
        "recommendations": "Recommendations:",
        "added_question_ok": "✅ Question added for sphere “{sphere}”.",
        "format_add_question": "Format: /add_balance_question <sphere> | <question>",
        "questions_empty": "No extra questions. Add: /add_balance_question <sphere> | <question>",
        "questions_title": "📝 <b>Extra questions:</b>",
        "charts_empty": "No data for charts in this period.",
        "charts_expense_title": "📉 <b>Expenses by category for {days} days</b>",
        "charts_income_title": "📈 <b>Income by category for {days} days</b>",
        "ask_add_record": "Enter a record: <amount> <category> <description> (expenses use minus sign)",
        "ask_add_expense": "Enter an expense: <amount> <category> <description> (amount without minus)",
        "ask_add_income": "Enter an income: <amount> <category> <description>",
        "ask_set_budget": "Enter a budget: <category> <amount>",
        "ask_add_question": "Enter: <sphere> | <question>",
        "choose_language": "Choose a language:",
        "lang_set": "✅ Language set: {lang}",
        "unknown": "I understand commands. Type /menu or /help.",
        "menu_add_record": "➕ Record",
        "menu_add_expense": "➖ Expense",
        "menu_add_income": "➕ Income",
        "menu_report": "📊 Report",
        "menu_charts": "📈 Charts",
        "menu_budgets": "📒 Budgets",
        "menu_set_budget": "➕ Set budget",
        "menu_test": "🧠 Test",
        "menu_questions": "📝 Questions",
        "menu_language": "🌐 Language",
        "back_to_menu": "⬅️ Menu",
        "menu_stats": "📊 Stats",
        "menu_delete_last": "🗑 Delete last",
        "format_delete": "Format: /delete last or /delete <id>",
        "delete_none": "No records to delete.",
        "delete_not_found": "Record {record_id} not found.",
        "delete_done": "🗑 Deleted {record_id}. SQLite={local} Sheets={sheets}",
        "stats_title": "<b>Stats for {days} days</b>",
        "stats_income_line": "Income: count={count}, sum={sum:.2f}, mean={mean:.2f}, median={median:.2f}",
        "stats_expense_line": "Expense: count={count}, sum={sum:.2f}, mean={mean:.2f}, median={median:.2f}",
        "stats_net_line": "Net: <b>{net:.2f}</b>",
        "photo_format": "Photo caption: expense <amount> <category> <desc> or income <amount> <category> <desc>",
    },
}

_LANG_LABEL: Dict[str, str] = {"uk": "uk", "ru": "ru", "en": "en"}


def normalize_lang(code: str) -> str:
    if not code:
        return "uk"
    c = code.lower()
    if c.startswith("uk"):
        return "uk"
    if c.startswith("ru"):
        return "ru"
    if c.startswith("en"):
        return "en"
    return "uk"


def t(lang: str, key: str, **kwargs) -> str:
    l = normalize_lang(lang)
    template = _TEXT.get(l, _TEXT["uk"]).get(key, _TEXT["uk"].get(key, key))
    if kwargs:
        return template.format(**kwargs)
    return template


def lang_label(lang: str) -> str:
    return _LANG_LABEL.get(normalize_lang(lang), "uk")
