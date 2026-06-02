// Task5 — Session Tests
// Before: 1 тест, Passed: 1/1, але це false confidence.
// After: реалізовано SessionFsm + 6 тестів (happy path + edge cases).

using System;
using System.Collections.Generic;

// ===== Тести (top-level) =====

int passed = 0, total = 0;

void Test(string name, Func<bool> check)
{
    total++;
    bool ok;
    try { ok = check(); }
    catch { ok = false; }

    if (ok) passed++;
    Console.WriteLine($"[{(ok ? "PASS" : "FAIL")}] {name}");
}

// 1. Базовий login
Test("New + Login -> Authenticated",
    () => SessionFsm.Next(SessionState.New, SessionEvent.Login) == SessionState.Authenticated);

// 2. Refresh-flow крок 1
Test("Authenticated + Refresh -> Refreshing",
    () => SessionFsm.Next(SessionState.Authenticated, SessionEvent.Refresh) == SessionState.Refreshing);

// 3. Refresh-flow крок 2
Test("Refreshing + Done -> Authenticated",
    () => SessionFsm.Next(SessionState.Refreshing, SessionEvent.Done) == SessionState.Authenticated);

// 4. Logout-flow
Test("Authenticated + Logout -> LoggedOut",
    () => SessionFsm.Next(SessionState.Authenticated, SessionEvent.Logout) == SessionState.LoggedOut);

// 5. Expire
Test("Authenticated + Expire -> Expired",
    () => SessionFsm.Next(SessionState.Authenticated, SessionEvent.Expire) == SessionState.Expired);

// 6. Unknown transition має кинути виняток
Test("New + Logout throws (unknown policy)",
    () =>
    {
        try
        {
            SessionFsm.Next(SessionState.New, SessionEvent.Logout);
            return false;
        }
        catch (InvalidOperationException) { return true; }
    });

Console.WriteLine($"\nPassed: {passed}/{total}");

// ===== Типи =====

enum SessionState { New, Authenticated, Refreshing, Expired, LoggedOut }
enum SessionEvent { Login, Refresh, Done, Expire, Logout }

static class SessionFsm
{
    private static readonly Dictionary<(SessionState, SessionEvent), SessionState> Transitions = new()
    {
        [(SessionState.New,           SessionEvent.Login)]   = SessionState.Authenticated,
        [(SessionState.Authenticated, SessionEvent.Refresh)] = SessionState.Refreshing,
        [(SessionState.Refreshing,    SessionEvent.Done)]    = SessionState.Authenticated,
        [(SessionState.Authenticated, SessionEvent.Expire)]  = SessionState.Expired,
        [(SessionState.Authenticated, SessionEvent.Logout)]  = SessionState.LoggedOut,
    };

    public static SessionState Next(SessionState state, SessionEvent evt)
    {
        if (Transitions.TryGetValue((state, evt), out var next))
            return next;

        throw new InvalidOperationException(
            $"Illegal session transition: {state} + {evt}");
    }
}
