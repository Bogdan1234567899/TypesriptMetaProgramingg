// Task4 — Ticket SLA FSM
// Before: заглушка Next завжди повертала state — переходи фіктивні.
// After: реальна таблиця + дві симуляції (normal + escalation).

using System;
using System.Collections.Generic;

// ===== Симуляції =====

// Сценарій 1: звичайний flow
Simulate("Normal flow", TicketState.Open, new[]
{
    TicketEvent.Assign,
    TicketEvent.Resolve,
    TicketEvent.Close,
});

// Сценарій 2: ескалація
Simulate("Escalation flow", TicketState.Open, new[]
{
    TicketEvent.Escalate,
    TicketEvent.Assign,
    TicketEvent.Resolve,
    TicketEvent.Close,
});

// Сценарій 3: нелегальний перехід
Console.WriteLine("\n--- illegal transition test ---");
try
{
    TicketFlowAfter.Next(TicketState.Closed, TicketEvent.Assign);
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"Caught: {ex.Message}");
}

// ===== Локальна функція =====

static void Simulate(string name, TicketState start, TicketEvent[] events)
{
    Console.WriteLine($"\n--- {name} ---");
    var state = start;
    foreach (var evt in events)
    {
        var next = TicketFlowAfter.Next(state, evt);
        Console.WriteLine($"{state} + {evt} -> {next}");
        state = next;
    }
}

// ===== Типи =====

enum TicketState { Open, InProgress, Escalated, Resolved, Closed }
enum TicketEvent { Assign, Escalate, Resolve, Close }

static class TicketFlowAfter
{
    private static readonly Dictionary<(TicketState, TicketEvent), TicketState> Transitions = new()
    {
        [(TicketState.Open,        TicketEvent.Assign)]   = TicketState.InProgress,
        [(TicketState.Open,        TicketEvent.Escalate)] = TicketState.Escalated,
        [(TicketState.Escalated,   TicketEvent.Assign)]   = TicketState.InProgress,
        [(TicketState.InProgress,  TicketEvent.Resolve)]  = TicketState.Resolved,
        [(TicketState.Resolved,    TicketEvent.Close)]    = TicketState.Closed,
    };

    public static TicketState Next(TicketState state, TicketEvent evt)
    {
        if (Transitions.TryGetValue((state, evt), out var next))
            return next;

        throw new InvalidOperationException(
            $"Illegal ticket transition: {state} + {evt}");
    }
}
