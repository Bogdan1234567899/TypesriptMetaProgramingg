// Task1 — Plugin Lifecycle FSM
// Before: if-cascade з прихованим self-loop для будь-якого невідомого переходу.
// After: Dictionary-таблиця + явна unknown policy (throw).

using System;
using System.Collections.Generic;

// ===== Демонстрація (top-level) =====

Console.WriteLine("--- happy path ---");
var s = PluginState.Discovered;
foreach (var evt in new[] { PluginEvent.Load, PluginEvent.Validate, PluginEvent.Activate, PluginEvent.Disable })
{
    var next = PluginFlowAfter.Next(s, evt);
    Console.WriteLine($"{s} + {evt} -> {next}");
    s = next;
}

Console.WriteLine("\n--- illegal transition ---");
try
{
    PluginFlowAfter.Next(PluginState.Discovered, PluginEvent.Activate);
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"Caught: {ex.Message}");
}

// ===== Типи =====

enum PluginState { Discovered, Loaded, Validated, Active, Disabled, Failed }
enum PluginEvent { Load, Validate, Activate, Disable, Fail, Retry }

// ===== BEFORE =====

static class PluginFlowBefore
{
    public static PluginState Next(PluginState state, PluginEvent evt)
    {
        if (state == PluginState.Discovered && evt == PluginEvent.Load)     return PluginState.Loaded;
        if (state == PluginState.Loaded     && evt == PluginEvent.Validate) return PluginState.Validated;
        if (state == PluginState.Validated  && evt == PluginEvent.Activate) return PluginState.Active;
        if (state == PluginState.Active     && evt == PluginEvent.Disable)  return PluginState.Disabled;
        if (state == PluginState.Active     && evt == PluginEvent.Fail)     return PluginState.Failed;
        if (state == PluginState.Failed     && evt == PluginEvent.Retry)    return PluginState.Loaded;
        return state; // ← прихований self-loop
    }
}

// ===== AFTER =====

static class PluginFlowAfter
{
    private static readonly Dictionary<(PluginState, PluginEvent), PluginState> Transitions = new()
    {
        [(PluginState.Discovered, PluginEvent.Load)]     = PluginState.Loaded,
        [(PluginState.Loaded,     PluginEvent.Validate)] = PluginState.Validated,
        [(PluginState.Validated,  PluginEvent.Activate)] = PluginState.Active,
        [(PluginState.Active,     PluginEvent.Disable)]  = PluginState.Disabled,
        [(PluginState.Active,     PluginEvent.Fail)]     = PluginState.Failed,
        [(PluginState.Failed,     PluginEvent.Retry)]    = PluginState.Loaded,
    };

    public static PluginState Next(PluginState state, PluginEvent evt)
    {
        if (Transitions.TryGetValue((state, evt), out var next))
            return next;

        // Єдина unknown policy: fail-fast (throw)
        throw new InvalidOperationException(
            $"Illegal transition: {state} + {evt}");
    }
}
