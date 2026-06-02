# Task 2 — Import Pipeline

## Що було не так у Before

В одному методі змішані дві unknown policy:
- Для `Draft` + будь-яка інша подія — `return state` (self-loop)
- Для `Parsing + Parse` — `throw` ("Already parsing")
- Для всього іншого — знову `return state`

Це означає, що поведінка системи залежить від порядку рядків у методі, а не від бізнес-правил. Розробник не може передбачити результат `Next(Mapped, Parse)` без читання коду.

## Обрана policy: Fail-Fast (throw)

Усі невідомі переходи кидають `InvalidOperationException`.

Чому fail-fast, а не self-loop:

1. Імпорт — бізнес-критична операція. Тихе ігнорування події означає втрату даних або непомітну розсинхронізацію.
2. Self-loop ховає помилки в коді що викликає FSM. У продакшені такий баг знайдуть тільки через скарги користувачів.
3. Виняток із повідомленням `Illegal import transition: State + Event` зразу показує, де проблема.

## Приклад

`Next(Mapped, Parse)` — у Before повертав `Mapped` (тихий self-loop). Після рефакторингу кидає виняток з повідомленням `Illegal import transition: Mapped + Parse`.

## Таблиця переходів

| State | Event | Next |
|---|---|---|
| Draft | Parse | Parsing |
| Parsing | Map | Mapped |
| Mapped | Save | Persisted |
| Draft | Reject | Rejected |
| Parsing | Reject | Rejected |
| Mapped | Reject | Rejected |

## Критерій готовності

Однакова передбачувана поведінка для будь-якого вхідного (state, event): або валідний перехід з таблиці, або виняток. Жодних винятків з правила.
