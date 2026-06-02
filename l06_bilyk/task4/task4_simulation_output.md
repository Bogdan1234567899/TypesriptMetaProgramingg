# Task 4 — Ticket SLA

## Таблиця переходів

| State | Event | Next |
|---|---|---|
| Open | Assign | InProgress |
| Open | Escalate | Escalated |
| Escalated | Assign | InProgress |
| InProgress | Resolve | Resolved |
| Resolved | Close | Closed |

Unknown policy: throw (fail-fast).

## Вивід симуляцій

**Normal flow:**
```
Open + Assign -> InProgress
InProgress + Resolve -> Resolved
Resolved + Close -> Closed
```

**Escalation flow:**
```
Open + Escalate -> Escalated
Escalated + Assign -> InProgress
InProgress + Resolve -> Resolved
Resolved + Close -> Closed
```

**Illegal transition (Closed + Assign):**
```
Caught: Illegal ticket transition: Closed + Assign
```

## Критерій готовності

Обидва сценарії (normal + escalation) проходять без нелегальних переходів. Кожен рядок виводу відповідає рядку у Dictionary — заглушки немає. Закритий тікет не можна перевідкрити — спроба `Closed + Assign` кидає виняток, як того вимагає бізнес-правило.
