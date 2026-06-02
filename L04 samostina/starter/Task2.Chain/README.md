# Task2 — Chain of Responsibility: валідація

## Опис проблеми

Клас `RuleEngine` містить усі правила валідації в одному методі. Додати нове правило без зміни цього класу неможливо. Логіка `fail-fast` і `accumulate` вручну вбудована в метод, а не винесена як окрема стратегія.

## Архітектурне рішення

Кожне правило виділено в окремий клас-обробник, що успадковує абстрактний `ValidationHandler`. Обробники з'єднані у ланцюг через метод `SetNext()`. Стратегія зупинки (`FailFast` / `Accumulate`) передається як параметр і обробляється централізовано у базовому класі.

```
ValidationHandler (abstract)
  └── UsernameHandler
  └── EmailHandler
  └── AgeHandler

RuleEngine
  └── будує ланцюг: Username → Email → Age
  └── приймає ValidationPolicy (enum)
  └── публічна точка входу: Handle()
```

## Інструкція запуску

```bash
cd self_study_projects/solutions/Task2.Chain
dotnet run
```

Очікуваний вивід:
```
=== FailFast ===
Valid: False
  - Username is required.

=== Accumulate ===
Valid: False
  - Username is required.
  - Email is invalid.
  - Age must be >= 18.
```

## Самоперевірка

**Критерій виконано.** Так, тому що додавання нового правила (наприклад, `PasswordHandler`) вимагає лише створення нового класу та підключення його до ланцюга в `RuleEngine` — жоден з існуючих обробників не змінюється.
