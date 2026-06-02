# Task 1 — Complexity

## Метрики

| Метрика | Before | After | Поріг | Статус |
|---|---|---|---|---|
| Cyclomatic Complexity (Validate) | 10 | 5 | <= 5 | PASS |
| Cognitive Complexity (Validate) | 12 | 4 | <= 6 | PASS |

After рахував для головного `Validate`. Найскладніший helper — `HasValidDigitPositions`: Cyclomatic = 4, Cognitive = 4.

## Quality Gate

Поріг: Cognitive <= 6, Cyclomatic <= 5
Статус: **PASS**

## Висновок

Розбив великий метод на 4 маленькі: кожен перевіряє одну річ. Тепер легше читати і тестувати окремі правила. Поведінка не змінилась — перевірив на 9 тест-кейсах, всі результати збігаються з before-версією.
