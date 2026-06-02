# Task 2 — Coupling

## Метрики

| Метрика | Before | After | Поріг | Статус |
|---|---|---|---|---|
| Direct instantiations у Register | 2 | 0 | = 0 | PASS |
| Fan-out (UserService) | 2 (конкретні класи) | 2 (інтерфейси) | — | — |
| Abstraction ratio | 0.0 | 1.0 | >= 0.7 | PASS |

Abstraction ratio = (залежності на інтерфейси) / (всі залежності). Before: 0/2 = 0. After: 2/2 = 1.0.

## Quality Gate

Поріг: Direct instantiations = 0 і Abstraction ratio >= 0.7
Статус: **PASS**

## Висновок

UserService більше не створює залежності сам — отримує їх через конструктор. Тепер можна підставити mock-репозиторій і mock-сендер для тестів. Зв'язування з конкретними реалізаціями зникло.
