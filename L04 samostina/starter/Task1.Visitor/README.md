# Task1 — Visitor: AST-метрики

## Опис проблеми

Стартовий код обходить AST через ланцюг `if/else` всередині одного методу `Collect()`. Кожна нова операція над деревом (наприклад, вивід дерева або підрахунок глибини) вимагає зміни вже існуючого класу — це порушення принципу Open/Closed.

## Архітектурне рішення

Введено два інтерфейси:
- `IAstNode` — кожен вузол реалізує `Accept(IAstVisitor)`, делегуючи диспетчеризацію паттерну (double dispatch).
- `IAstVisitor` — кожна нова операція реалізується як окремий клас.

Класи вузлів (`FunctionNode`, `CallNode`, `LiteralNode`) більше не містять жодної умовної логіки.

```
IAstVisitor
  └── MetricsVisitor  (збирає лічильники)

PrintVisitor          (новий клас — обходить дерево рекурсивно, вузли не змінені)

IAstNode
  └── FunctionNode.Accept(v) → v.Visit(this)
  └── CallNode.Accept(v)     → v.Visit(this)
  └── LiteralNode.Accept(v)  → v.Visit(this)
```

## Інструкція запуску

```bash
cd self_study_projects/solutions/Task1.Visitor
dotnet run
```

Очікуваний вивід:
```
=== Метрики ===
Functions : 2
Calls     : 2
Literals  : 2

=== Дерево ===
[Function] main
  [Call] print
  [Literal] 42
  [Literal] hello
  [Function] helper
    [Call] log
```

## Самоперевірка

**Критерій виконано.** Так, тому що клас `PrintVisitor` доданий як нова операція над AST без жодних змін у `FunctionNode`, `CallNode` або `LiteralNode`. Вузли залишились закритими для змін, поведінка розширена ззовні.
