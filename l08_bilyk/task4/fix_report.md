# Task 4 — Exam Session Fix Report

## Помилки у broken-моделі

Валідатор знайшов 3 помилки (по одній з кожного типу).

### 1. Reference: невідомий event

**Було:**
```json
{ "from": "NotStarted", "event": "Pause", "to": "InProgress" }
```

Подія `Pause` використовується у transition, але відсутня у списку `events` моделі.

**Стало:** transition видалено. Якщо потрібен Pause — спочатку додавати в events.

### 2. Reachability: недосяжний стан

**Було:** стан `Limbo` оголошений у списку states, але немає жодного transition, що веде до нього.

**Стало:** стан видалено зі списку states. Якщо потрібен — додавати разом з transition.

### 3. Determinism: конфлікт переходів

**Було:**
```json
{ "from": "InProgress", "event": "Submit", "to": "Submitted" }
{ "from": "InProgress", "event": "Submit", "to": "Cancelled" }
```

Два різних `to` для однієї пари `(InProgress, Submit)`.

**Стало:** залишив перший transition (Submit → Submitted). Для cancel-сценарію є окрема подія Cancel: `{ "from": "InProgress", "event": "Cancel", "to": "Cancelled" }`.

## Вивід валідатора

**Broken:**
```
=== Validating: exam_session_broken.json ===
Validation FAILED — 3 error(s):
  [ERROR] Reference: transition.event 'Pause' not in events
  [ERROR] Determinism: conflict for (InProgress, Submit) → 'Submitted' and 'Cancelled'
  [ERROR] Reachability: state 'Limbo' is unreachable from initial 'NotStarted'
```

**Fixed:**
```
=== Validating: exam_session_fixed.json ===
Validation OK — all invariants hold.
```

## Висновок

Валідатор спрацював fail-early: помилки виявлено до запуску FSM, без падіння в рантаймі. Усі три типи інваріантів (reference, determinism, reachability) перевіряються окремими функціями — додати нову перевірку можна без зміни існуючих.
