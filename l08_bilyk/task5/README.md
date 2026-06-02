# Task 5 — Universal FSM Runner

Один `Program.cs` працює для трьох незалежних моделей без переписування логіки.

## Файли

- `Program.cs` — універсальний runner
- `warehouse_robot_fsm.json` + `events_warehouse_robot.json`
- `support_ticket_fsm.json` + `events_support_ticket.json`
- `payment_retry_fsm.json` + `events_payment_retry.json`
- `run_all_output.txt` — результат прогону всіх трьох моделей

## Запуск

**Прогін усіх трьох моделей одразу (без аргументів):**

```bash
dotnet run
```

**Прогін конкретної моделі (з аргументами):**

```bash
dotnet run -- warehouse_robot_fsm.json events_warehouse_robot.json
dotnet run -- support_ticket_fsm.json  events_support_ticket.json
dotnet run -- payment_retry_fsm.json   events_payment_retry.json
```

## Як це працює

1. Завантажує модель з JSON.
2. Проводить семантичну валідацію (reference, determinism, reachability).
3. Якщо `Validation OK` — завантажує сценарій подій і виконує його по таблиці переходів.
4. Невідомий перехід → fail-fast з повідомленням.

Жодного коду, специфічного для конкретної моделі. Структура `FsmModel` універсальна.
