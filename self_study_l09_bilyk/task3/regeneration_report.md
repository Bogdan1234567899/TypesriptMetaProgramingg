# Task 3 — Regeneration Report

## Зміна у DSL (v1 → v2)

| | v1 | v2 |
|---|---|---|
| events | 5 (Try, Success, Fail, Retry, GiveUp) | 6 (+ **Cancel**) |
| transitions | 5 | 6 (+ **Trying + Cancel → Abandoned**) |
| states | 5 | 5 (без змін) |

**Конкретна зміна:** додано подію `Cancel` і перехід `{ "from": "Trying", "event": "Cancel", "to": "Abandoned" }`.

## Які файли змінилися після регенерації

Порівняння `generated_before/` і `generated_after/`:

### GeneratedPaymentRuntime.cs

| Файл | Зміна |
|---|---|
| `before/` | Transitions містить 5 пар |
| `after/`  | Transitions містить 6 пар — додано `[("Trying", "Cancel")] = "Abandoned"` |

Один рядок різниці. Метод `Next()` і обробка unknownPolicy не змінились.

### GeneratedPaymentTests.cs

| Файл | Зміна |
|---|---|
| `before/` | 5 valid tests, 5 invalid tests |
| `after/`  | 6 valid tests (+ `Trying + Cancel -> Abandoned`), 5 invalid tests (тепер `Initial + Cancel` замість `Trying + Try` у списку invalid) |

Уточнення: множина invalid-пар змінилась, тому що один з раніше невалідних transition `Trying + Cancel` тепер став валідним. Генератор бере перші 5 з невалідних — порядок інший, але загальне покриття валідне.

## Чому саме ці файли змінилися

Причинно-наслідковий ланцюг:

1. **Нова подія `Cancel` у списку events DSL** → нічого не змінюється у самому списку у generated коді, тому що list of events як такий не з'являється в runtime (тільки в transition map).
2. **Новий transition `(Trying, Cancel) → Abandoned`** → рядок у Dictionary `Transitions` у `GeneratedPaymentRuntime.cs` та `GeneratedPaymentTests.cs`.
3. **Один новий valid-тест** у `GeneratedPaymentTests.cs` — генератор створює по одному тесту на кожен transition у моделі.
4. **Зміни у списку invalid-тестів** — генератор перебирає всі пари (state, event), фільтрує валідні. Оскільки набір валідних змінився, набір невалідних теж.

Жодного ручного дописування. Кожна зміна простежується назад до конкретного рядка у DSL.

## Висновок

Регенерація — це детерміністична функція від моделі: `regenerate(v2.json) == diff(v1.json, v2.json)` застосований до generated артефактів. Якщо у майбутньому хтось зробить ручні зміни у generated коді — регенерація їх знищить. Тому правило: generated файли — read-only поза codegen.
