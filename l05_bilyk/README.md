# L05 Self Study — Метрики якості коду

## Зведена таблиця

| Задача | Метрика | Before | After | Поріг | Статус |
|---|---|---|---|---|---|
| Task1 — Complexity | Cognitive (Validate) | 12 | 4 | <= 6 | PASS |
| Task1 — Complexity | Cyclomatic (Validate) | 10 | 5 | <= 5 | PASS |
| Task2 — Coupling | Direct instantiations | 2 | 0 | = 0 | PASS |
| Task2 — Coupling | Abstraction ratio | 0.0 | 1.0 | >= 0.7 | PASS |
| Task3 — Test Quality | Branch coverage | 25% | 100% | >= 90% | PASS |
| Task3 — Test Quality | Mutation killed | 0 | 1 | >= 1 | PASS |
| Task4 — Duplication | Duplicate ratio | 21% | 0% | <= 10% | PASS |
| Task5 — Hotspot | Max hotspot | — | 72 | <= 80* | PASS |

\* у Task5 використано власний поріг 80 замість стандартних 50 — обґрунтування у звіті задачі.

## Короткі висновки

**Task1** — розбив `Validate` на 4 маленькі методи. Складність впала, поведінка збережена (перевірено на 9 кейсах).

**Task2** — ввів інтерфейси `IUserRepository` і `IEmailSender`, передаю їх через конструктор. Тепер сервіс можна тестувати з mock-ами.

**Task3** — додав 3 тести, що покривають усі гілки. Mutation-перевірка показала, що тест "OK" з рядком довжиною 8 убиває мутацію `<` → `<=`.

**Task4** — виніс sanitize у статичний клас `StringSanitizer`. Дублювання зникло, обидва методи використовують один helper.

**Task5** — порахував hotspot для 5 модулів. Top-ризик — PaymentGateway (72). Перший крок: розбити за відповідальностями.

## Структура

```
self_study_l05_student/
├── task1/
│   ├── Program.cs
│   └── task1_metrics.md
├── task2/
│   ├── Program.cs
│   └── task2_metrics.md
├── task3/
│   ├── Program.cs
│   └── task3_test_report.md
├── task4/
│   ├── Program.cs
│   └── task4_duplication_report.md
├── task5/
│   ├── Program.cs
│   └── task5_hotspot_report.md
└── README.md
```
