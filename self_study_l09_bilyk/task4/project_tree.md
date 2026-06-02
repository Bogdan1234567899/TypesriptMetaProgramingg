# Task 4 — Project Tree

Структура проєкту з розведенням generated/handwritten:

```
project/
├── models/                    # DSL-вхід (handwritten)
│   ├── warehouse_flow_fsm.json
│   ├── support_ticket_fsm.json
│   └── payment_retry_fsm.json
│
├── codegen/                   # Генератори (handwritten)
│   ├── Codegen.cs
│   └── TestCodegen.cs
│
├── generated/                 # ВИВІД ГЕНЕРАТОРА — DO NOT EDIT
│   ├── GeneratedWarehouseRuntime.cs
│   ├── GeneratedSupportTests.cs
│   ├── GeneratedPaymentRuntime.cs
│   └── GeneratedPaymentTests.cs
│
├── runtime/                   # Ручний шар поверх generated (handwritten)
│   ├── WarehouseService.cs       # бізнес-логіка, що викликає GeneratedWarehouseRuntime
│   ├── TicketService.cs
│   └── PaymentService.cs
│
├── reports/                   # Документація і звіти (handwritten)
│   ├── boundary_rules.md
│   └── regeneration_report.md
│
└── README.md                  # Інструкція (handwritten)
```

## Принцип розведення

- **`generated/`** — власність генератора. Перезаписується при кожному запуску codegen. Тут ніколи нічого не редагується руками.
- **`runtime/`** — ручні розширення (бізнес-логіка, інтеграція з БД, логування). Викликає generated runtime, але не змінює його.
- **`models/`** — джерело правди для всього в `generated/`. Зміна моделі = causes регенерація.
- **`codegen/`** — самі генератори. Змінюються лише коли потрібно змінити стратегію генерації (наприклад, додати новий тип тестів).
- **`reports/`** — звіти і документація. Не впливає на компіляцію, але є частиною інженерної дисципліни.
