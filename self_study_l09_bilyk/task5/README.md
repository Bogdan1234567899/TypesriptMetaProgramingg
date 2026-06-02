# Task 5 — fsmgen CLI

Універсальний CLI-генератор runtime і тестів з FSM DSL. Один інструмент для будь-якої моделі.

## Команди

```
fsmgen generate-runtime <modelPath> <outDir>
fsmgen generate-tests   <modelPath> <outDir>
fsmgen all              <modelPath> <outDir>
```

Перед генерацією виконується **semantic check**: перевірка наявності states, events, transitions, initial state і коректності всіх посилань. Якщо модель невалідна — генерація не відбувається, exit code 3.

## Збірка

```bash
cd task5
dotnet build
```

## Запуск для всіх 3 моделей

```bash
# Warehouse Flow
dotnet run -- all models/warehouse_flow_fsm.json generated/

# Support Ticket
dotnet run -- all models/support_ticket_fsm.json generated/

# Payment Retry
dotnet run -- all models/payment_retry_fsm.json generated/
```

Після запуску в `generated/` з'являються:

- `GeneratedWarehouseFlowRuntime.cs` + `GeneratedWarehouseFlowTests.cs`
- `GeneratedSupportTicketRuntime.cs` + `GeneratedSupportTicketTests.cs`
- `GeneratedPaymentRetryRuntime.cs` + `GeneratedPaymentRetryTests.cs`

## Тільки runtime або тільки тести

```bash
dotnet run -- generate-runtime models/warehouse_flow_fsm.json generated/
dotnet run -- generate-tests   models/warehouse_flow_fsm.json generated/
```

## Exit codes

- `0` — успіх
- `1` — неправильне використання CLI (показано usage)
- `2` — файл моделі не знайдено
- `3` — semantic check failed (помилки виведено у stderr)

## Що НЕ робити

- Не редагувати файли у `generated/` руками — наступний запуск їх перепише.
- Не робити окремий генератор під кожну модель — fsmgen працює з будь-якою моделлю, що відповідає схемі (states, events, initial, unknownPolicy, transitions).
