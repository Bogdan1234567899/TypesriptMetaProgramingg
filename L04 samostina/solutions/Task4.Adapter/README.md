# Task4 — Adapter: зовнішній парсер

## Опис проблеми

Зовнішня бібліотека повертає `ExternalTree` з власним форматом. У стартовому коді клієнт сам виконував маппінг: знав про `ExternalTree`, `ExternalItem` і вручну перетворював їх у `AstDocument`. Це порушує мету патерну — клієнт не повинен залежати від зовнішніх деталей.

## Архітектурне рішення

Реалізовано `ExternalParserAdapter`, що реалізує внутрішній контракт `IAstProvider`. Весь маппінг виконується всередині адаптера. Клієнт не знає про `ExternalLibraryParser`, `ExternalTree` або `ExternalItem` взагалі.

```
IAstProvider
  └── InternalParser           (внутрішня реалізація)
  └── ExternalParserAdapter    (адаптер)
        └── ExternalLibraryParser  (зовнішня бібліотека, лише тут)
              └── маппінг ExternalTree → AstDocument
```

## Інструкція запуску

```bash
cd self_study_projects/solutions/Task4.Adapter
dotnet run
```

Очікуваний вивід:
```
[Internal] Root: root
[Internal] Nodes: function, call, literal

[External] Root: external-root
[External] Nodes: function, call, literal
```

## Самоперевірка

**Критерій виконано.** Так, тому що клієнтський метод `RunAnalysis` приймає `IAstProvider` і однаково обробляє обидва провайдери — без розгалужень, без `is`/`as`, без знань про зовнішню бібліотеку.
