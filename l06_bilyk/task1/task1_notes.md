# Task 1 — Plugin Lifecycle

## Таблиця переходів

| State | Event | Next |
|---|---|---|
| Discovered | Load | Loaded |
| Loaded | Validate | Validated |
| Validated | Activate | Active |
| Active | Disable | Disabled |
| Active | Fail | Failed |
| Failed | Retry | Loaded |

Всього 6 переходів — усі присутні у Dictionary.

## Unknown policy: throw (fail-fast)

Обрав `throw InvalidOperationException` замість `return state`. Причини:

1. Плагін-система — це контракт з хостом. Якщо хтось викликає `Activate` напряму з `Discovered`, це баг у викликаючому коді, а не очікувана поведінка.
2. Тихий self-loop маскує помилки: тест може пройти, а в продакшені плагін зависне без діагностики.
3. Виняток містить інформативне повідомлення `Illegal transition: State + Event` — одразу видно, де зламалась логіка.

## Критерій готовності

Жодної неявної поведінки: будь-який вхід (state, evt) або повертає задокументований стан з таблиці, або кидає виняток із зрозумілим повідомленням. Перевірено на 4 валідних переходах і 1 невалідному.
