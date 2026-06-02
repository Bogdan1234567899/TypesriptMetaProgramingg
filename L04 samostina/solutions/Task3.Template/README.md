# Task3 — Template Method: аналіз коду

## Опис проблеми

`StrictAnalyzer` і `RelaxedAnalyzer` незалежно реалізують однакові фази `parse → validate → report`. Якщо порядок фаз потрібно змінити, правку доводиться робити в обох класах — це дублювання і порушення принципу єдиної відповідальності.

## Архітектурне рішення

Введено абстрактний клас `AnalyzerTemplate` з методом `Analyze()` (template method), що фіксує порядок фаз. Спільні фази (`Parse`, `Report`) реалізовані у базовому класі. Варіативна фаза `Validate` оголошена як `abstract` — підкласи зобов'язані її реалізувати.

```
AnalyzerTemplate (abstract)
  ├── Analyze()       ← template method, порядок незмінний
  ├── Parse()         ← спільна реалізація у базовому класі
  ├── Validate()      ← abstract hook, різна у підкласах
  └── Report()        ← спільна реалізація у базовому класі

  └── StrictAnalyzer  : override Validate()
  └── RelaxedAnalyzer : override Validate()
```

## Інструкція запуску

```bash
cd self_study_projects/solutions/Task3.Template
dotnet run
```

Очікуваний вивід:
```
[Strict] Parsing source...
[Strict] Validating (strict mode)...
[Strict] WARNING: long token 'longVariableName'
[Strict] Generating report...
[Strict] Total tokens: 6

[Relaxed] Parsing source...
[Relaxed] Validating (relaxed mode — skipping warnings)...
[Relaxed] Generating report...
[Relaxed] Total tokens: 6
```

## Самоперевірка

**Критерій виконано.** Так, тому що порядок фаз `Parse → Validate → Report` закодований виключно в методі `AnalyzerTemplate.Analyze()`. Щоб змінити порядок, достатньо правки в одному місці — підкласи при цьому не чіпаються.
