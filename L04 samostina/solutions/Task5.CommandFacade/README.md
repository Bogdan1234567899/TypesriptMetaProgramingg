# Task5 — Command + Facade: оркестрація

## Опис проблеми

Клієнт вручну викликає 4 окремих сервіси у конкретному порядку. Трансформації не фіксуються, тестувати послідовність виконання неможливо, а помилка в порядку викликів ламає пайплайн.

## Архітектурне рішення

Два патерни розподілили відповідальності:

- **Command** — кожна трансформація (`InlineConstantCommand`, `RenameSymbolCommand`) інкапсульована у клас з інтерфейсом `ICommand`. Команди передають стан через `PipelineContext`.
- **CommandBus** — виконує команди і веде журнал (`Log`) назв виконаних трансформацій.
- **Facade** (`AnalyzerFacade`) — єдина публічна точка входу `Run()`. Приховує оркестрацію від клієнта.

```
ICommand
  └── InlineConstantCommand
  └── RenameSymbolCommand

CommandBus
  └── Send(command, context) + Log

AnalyzerFacade
  └── Run(source)
        ├── CommandBus.Send(InlineConstant)
        ├── CommandBus.Send(RenameSymbol)
        ├── AstValidator.Validate()
        └── ReportGenerator.Generate()
```

## Інструкція запуску

```bash
cd self_study_projects/solutions/Task5.CommandFacade
dotnet run
```

Очікуваний вивід:
```
[Report] Source length: 42 chars
[Report] Content: function foo(100) { newName(); }

=== Command Log ===
  ✓ InlineConstants
  ✓ RenameSymbol(oldName→newName)
```

## Самоперевірка

**Критерій виконано.** Так, тому що клієнт викликає лише `facade.Run(source)` і не звертається до жодного внутрішнього сервісу напряму. Command Log після запуску підтверджує, що обидві трансформації виконано і зафіксовано.
