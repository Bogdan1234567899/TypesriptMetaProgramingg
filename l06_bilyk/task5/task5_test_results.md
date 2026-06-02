# Task 5 — Session Tests

## Таблиця переходів SessionFsm

| State | Event | Next |
|---|---|---|
| New | Login | Authenticated |
| Authenticated | Refresh | Refreshing |
| Refreshing | Done | Authenticated |
| Authenticated | Expire | Expired |
| Authenticated | Logout | LoggedOut |

Unknown policy: throw (fail-fast).

## Тести (6 шт)

1. `New + Login -> Authenticated` — базовий login
2. `Authenticated + Refresh -> Refreshing` — refresh, крок 1
3. `Refreshing + Done -> Authenticated` — refresh, крок 2
4. `Authenticated + Logout -> LoggedOut` — нормальний logout
5. `Authenticated + Expire -> Expired` — таймаут сесії
6. `New + Logout throws` — перевірка unknown policy

## Вивід

```
[PASS] New + Login -> Authenticated
[PASS] Authenticated + Refresh -> Refreshing
[PASS] Refreshing + Done -> Authenticated
[PASS] Authenticated + Logout -> LoggedOut
[PASS] Authenticated + Expire -> Expired
[PASS] New + Logout throws (unknown policy)

Passed: 6/6
```

## Чому Before з Passed: 1/1 — небезпечно

Один тест `New + Login -> Authenticated` не покриває:
- refresh-flow (2 переходи)
- expire / logout
- поведінку при нелегальному переході

З цим тестом FSM могла би повертати завжди `Authenticated` для будь-якого входу — і тест би пройшов. Це false positive.

## Критерій готовності

Passed: 6/6 (N >= 5). Покриті: happy path login, повний refresh cycle, два варіанти завершення сесії (expire і logout), і edge case з невідомим переходом. Будь-яка регресія в таблиці (наприклад, забути додати `Refreshing + Done`) одразу вилетить як FAIL.
