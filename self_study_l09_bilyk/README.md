# L09 Self Study — Генерація FSM Runtime і тестів

## Структура

```
self_study_l09_bilyk/
├── README.md
├── task1/  Codegen.cs + warehouse_flow_fsm.json + GeneratedWarehouseRuntime.cs
├── task2/  TestCodegen.cs + support_ticket_fsm.json + GeneratedSupportTests.cs
├── task3/  v1.json, v2.json + generated_before/, generated_after/ + regeneration_report.md
├── task4/  project_tree.md + boundary_rules.md + example_files/
└── task5/  FsmGenCli.csproj + Program.cs + models/ + generated/ + README.md
```

## Рефлексія

### Що було найскладнішим у codegen

Екранування рядків. Codegen пише C#-код як рядок, тому коли треба згенерувати `$"Illegal: {state}"` — у вихідному коді доводиться писати `"$\"Illegal: {state}\""` і не заплутатись. Особливо у task5, де всередині генерованого тестового коду є тернарний оператор з лапками.

### Де найчастіше виникали розсинхрони

При зміні назв подій у моделі. Generated код перегенерується коректно, але якщо хтось у ручному шарі викликав `Next(state, "Submit")` по старій назві — runtime падає у fail-fast. Компілятор цього не ловить, бо події — рядки.

### Які правила регенерації критичні для команди

1. Generated файли — read-only поза codegen. Будь-яка ручна правка зникне при наступному запуску.
2. Semantic check перед генерацією — обов'язково, інакше генератор видасть валідний C# з логічно зламаної моделі.
3. Один генератор на всі моделі (task5) — окремі генератори під кожну модель не масштабуються.
