// Task2 — Import Pipeline FSM
// Before: змішані дві unknown policy (self-loop + throw) в одному методі.
// After: Dictionary + єдина policy throw (fail-fast).

using System;
using System.Collections.Generic;

// ===== Демонстрація =====

Console.WriteLine("--- happy path ---");
var s = ImportState.Draft;
foreach (var evt in new[] { ImportEvent.Parse, ImportEvent.Map, ImportEvent.Save })
{
    var next = ImportFlowAfter.Next(s, evt);
    Console.WriteLine($"{s} + {evt} -> {next}");
    s = next;
}

Console.WriteLine("\n--- reject path ---");
var r = ImportFlowAfter.Next(ImportState.Parsing, ImportEvent.Reject);
Console.WriteLine($"Parsing + Reject -> {r}");

Console.WriteLine("\n--- illegal transition ---");
try { ImportFlowAfter.Next(ImportState.Mapped, ImportEvent.Parse); }
catch (InvalidOperationException ex) { Console.WriteLine($"Caught: {ex.Message}"); }

// ===== Типи =====

enum ImportState { Draft, Parsing, Mapped, Persisted, Rejected }
enum ImportEvent { Parse, Map, Save, Reject }

// ===== BEFORE — змішані policy =====

static class ImportFlowBefore
{
    public static ImportState Next(ImportState state, ImportEvent evt)
    {
        if (state == ImportState.Draft   && evt == ImportEvent.Parse) return ImportState.Parsing;
        if (state == ImportState.Parsing && evt == ImportEvent.Map)   return ImportState.Mapped;
        if (state == ImportState.Mapped  && evt == ImportEvent.Save)  return ImportState.Persisted;

        if (state == ImportState.Draft) return state; // ← policy A: self-loop

        if (state == ImportState.Parsing && evt == ImportEvent.Parse)
            throw new Exception("Already parsing"); // ← policy B: throw

        return state; // ← знову policy A
    }
}

// ===== AFTER — єдина policy (fail-fast) =====

static class ImportFlowAfter
{
    private static readonly Dictionary<(ImportState, ImportEvent), ImportState> Transitions = new()
    {
        [(ImportState.Draft,   ImportEvent.Parse)]  = ImportState.Parsing,
        [(ImportState.Parsing, ImportEvent.Map)]    = ImportState.Mapped,
        [(ImportState.Mapped,  ImportEvent.Save)]   = ImportState.Persisted,
        [(ImportState.Draft,   ImportEvent.Reject)] = ImportState.Rejected,
        [(ImportState.Parsing, ImportEvent.Reject)] = ImportState.Rejected,
        [(ImportState.Mapped,  ImportEvent.Reject)] = ImportState.Rejected,
    };

    public static ImportState Next(ImportState state, ImportEvent evt)
    {
        if (Transitions.TryGetValue((state, evt), out var next))
            return next;

        throw new InvalidOperationException(
            $"Illegal import transition: {state} + {evt}");
    }
}
