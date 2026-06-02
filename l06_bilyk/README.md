# L06 Self Study — FSM у C#: 5 задач

## Що зроблено

| Задача | Домен | Артефакти |
|---|---|---|
| Task 1 | Plugin Lifecycle | Program.cs + task1_notes.md |
| Task 2 | Import Pipeline | Program.cs + task2_policy.md |
| Task 3 | Deployment Validation | Program.cs + task3_validation_report.md |
| Task 4 | Ticket SLA | Program.cs + task4_simulation_output.md |
| Task 5 | Session Tests | Program.cs + task5_test_results.md |

## Спільні інженерні принципи

У всіх 5 задачах застосовано однакову дисципліну:

1. **Dictionary замість if-cascade** — таблиця переходів `Dictionary<(State, Event), State>` явно описує всі дозволені пари. Жодних прихованих гілок.
2. **Єдина unknown policy: throw (fail-fast)** — будь-який невідомий перехід кидає `InvalidOperationException` з повідомленням `Illegal transition: State + Event`. Однаково в усіх 5 задачах.
3. **Перевірка інваріантів** — у Task 3 додано окремий валідатор, що порівнює список обов'язкових переходів з фактичною таблицею до запуску FSM.
4. **Тестованість** — кожна задача має ізольовану реалізацію без побічних ефектів. У Task 4 — дві симуляції, у Task 5 — 6 тестів покривають happy path + edge cases.

## Чому скрізь throw, а не self-loop

Self-loop тихо ховає помилки виклику FSM. У всіх п'яти доменах (плагіни, імпорт, деплой, тікети, сесії) — це бізнес-критичні операції, де "тихо нічого не сталось" гірше за "видно зразу, що зламалось". Виняток із зрозумілим повідомленням — простіше для дебагу.

## Найскладніше

Task 2 — там було спокусливо залишити частину переходів self-loop "для зручності". Але це повертає до старої проблеми змішаних policy. Прийняв принципове рішення: одна стратегія на весь автомат.

## Що дізнався нового

FSM-підхід не залежить від домену. Plugin lifecycle, import pipeline, deployment, tickets, sessions — всі мають різні стани і події, але структура коду майже ідентична. Це і є цінність патерну: одного разу зрозумів — застосовуєш скрізь.

## Структура

```
self_study_l06_bilyk/
├── README.md
├── task1/  (Program.cs + task1_notes.md + task1.csproj)
├── task2/  (Program.cs + task2_policy.md + task2.csproj)
├── task3/  (Program.cs + task3_validation_report.md + task3.csproj)
├── task4/  (Program.cs + task4_simulation_output.md + task4.csproj)
└── task5/  (Program.cs + task5_test_results.md + task5.csproj)
```
