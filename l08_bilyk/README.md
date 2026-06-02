# L08 Self Study — FSM DSL у C# (5 задач)

## Що зроблено

| Задача | Домен | Артефакти |
|---|---|---|
| Task 1 | Кавомат | coffee_machine_fsm.json + Program.cs + run_output.txt |
| Task 2 | Пропускна система | access_control_fsm.json + Program.cs (валідатор) |
| Task 3 | Модерація контенту | content_moderation_fsm.json + Program.cs + scenarios_output.txt |
| Task 4 | Сесія іспиту | broken/fixed JSON + Program.cs + fix_report.md |
| Task 5 | Universal Runner | 3 моделі + 3 events + Program.cs + run_all_output.txt + README.md |

## Рефлексія

### 1. Що було найскладнішим

Task 5 — універсальний runner. Спочатку був спокус прив'язати логіку до конкретних state/event enum-ів кожної моделі. Довелося свідомо тримати все на рядкових значеннях зі словника, а не на типах. Так само непросто було коректно описати reachability як ітеративний fixed-point (множина розширюється поки змінюється), а не одним обходом.

Task 4 — додати рівно 3 помилки різних типів (reference, determinism, reachability), щоб кожна перевірка валідатора відпрацювала. Reference був простим (просто event з опечаткою), conflict — теж, але unreachable state треба було видумати — додав стан Limbo і не зробив переходу до нього.

### 2. Яку unknownPolicy обирав і чому

У всіх 5 задачах обрав `throw` (fail-fast). Причини однакові для всіх доменів:

- **Task 1 (кавомат)** — якщо викликати Brew з Idle, користувач отримає каву без оплати. Тихий self-loop приховає логічну помилку у викликаючому коді.
- **Task 2 (пропуск)** — security-критичний домен. Невідомий перехід може означати спробу атаки, тихо ігнорувати не можна.
- **Task 3 (модерація)** — критерій явно вимагає fail-fast для unknown event (третій сценарій).
- **Task 4 (іспит)** — фіксація стану студента не може мовчки втратити подію.
- **Task 5 (runner)** — універсальний код, але всі три моделі мають `"unknownPolicy": "throw"`. Runner поважає це поле з моделі і кидає при невідомому переході.

Self-loop розглядав, але відмовився: він зручний для прототипу, але у продакшені приховує баги до моменту, коли їх знайдуть користувачі. Краще зразу побачити помилку в логах.

### 3. Які інваріанти найчастіше порушувалися

Під час складання моделей найчастіше ловив себе на двох помилках:

- **Reachability** — додавав стан у список states, забував додати до нього transition. Так з'явився Limbo в task4 broken — це не вигадка, це справжня моя помилка, яку я зафіксував як приклад.
- **Reference** — описки в назвах подій між списком events і transitions (StartReview vs StartRewiew). Валідатор з task2/task5 ловив це одразу.

Determinism порушував рідко — конфлікт переходів важче випадково створити, але task4 broken містить штучний приклад для повноти.

## Структура

```
self_study_l08_bilyk/
├── README.md
├── task1/  (JSON модель + Program.cs + output + csproj)
├── task2/  (JSON модель + Program.cs валідатор + csproj)
├── task3/  (JSON модель + Program.cs + 3 сценарії output + csproj)
├── task4/  (broken JSON + fixed JSON + Program.cs + fix_report + csproj)
└── task5/  (3 JSON моделі + 3 events JSON + Program.cs + run_all_output + README + csproj)
```
