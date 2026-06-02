// Task5 — Universal FSM Runner
// Один Program.cs для будь-якої моделі.
// Usage:
//   dotnet run -- <model.json> <events.json>
// Якщо аргументів немає — прогоняє всі 3 моделі послідовно.

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;

if (args.Length == 2)
{
    RunOne(args[0], args[1]);
}
else
{
    // Прогін усіх трьох моделей
    var pairs = new[]
    {
        ("warehouse_robot_fsm.json", "events_warehouse_robot.json"),
        ("support_ticket_fsm.json",  "events_support_ticket.json"),
        ("payment_retry_fsm.json",   "events_payment_retry.json"),
    };

    foreach (var (model, events) in pairs)
    {
        RunOne(model, events);
        Console.WriteLine();
    }
}

static void RunOne(string modelPath, string eventsPath)
{
    Console.WriteLine($"=== {modelPath} ===");

    var model = JsonSerializer.Deserialize<FsmModel>(File.ReadAllText(modelPath),
        new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
        ?? throw new InvalidOperationException("Failed to parse model");

    // 1. Semantic validation
    var errors = new List<string>();
    CheckReferences(model, errors);
    CheckDeterminism(model, errors);
    CheckReachability(model, errors);

    if (errors.Count > 0)
    {
        Console.WriteLine($"Validation FAILED — {errors.Count} error(s):");
        errors.ForEach(e => Console.WriteLine($"  [ERROR] {e}"));
        return;
    }

    Console.WriteLine("Validation OK");

    // 2. Execute scenario
    var script = JsonSerializer.Deserialize<EventScript>(File.ReadAllText(eventsPath),
        new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
        ?? throw new InvalidOperationException("Failed to parse events");

    var table = new Dictionary<(string, string), string>();
    foreach (var t in model.Transitions)
        table[(t.From, t.Event)] = t.To;

    var state = model.Initial;
    Console.WriteLine($"Initial: {state}");
    foreach (var evt in script.Events)
    {
        if (table.TryGetValue((state, evt), out var next))
        {
            Console.WriteLine($"  {state} + {evt} -> {next}");
            state = next;
        }
        else
        {
            // unknownPolicy = throw (fail-fast)
            Console.WriteLine($"  [FAIL-FAST] Illegal: {state} + {evt}");
            return;
        }
    }
    Console.WriteLine($"Final: {state}");
}

// ===== Перевірки інваріантів =====

static void CheckReferences(FsmModel m, List<string> errors)
{
    var statesSet = new HashSet<string>(m.States);
    var eventsSet = new HashSet<string>(m.Events);

    if (!statesSet.Contains(m.Initial))
        errors.Add($"Reference: initial '{m.Initial}' not in states");

    foreach (var t in m.Transitions)
    {
        if (!statesSet.Contains(t.From))
            errors.Add($"Reference: from '{t.From}' not in states");
        if (!statesSet.Contains(t.To))
            errors.Add($"Reference: to '{t.To}' not in states");
        if (!eventsSet.Contains(t.Event))
            errors.Add($"Reference: event '{t.Event}' not in events");
    }
}

static void CheckDeterminism(FsmModel m, List<string> errors)
{
    var seen = new Dictionary<(string, string), string>();
    foreach (var t in m.Transitions)
    {
        var key = (t.From, t.Event);
        if (seen.TryGetValue(key, out var existing) && existing != t.To)
            errors.Add($"Determinism: conflict for ({t.From}, {t.Event}) → '{existing}' and '{t.To}'");
        else
            seen[key] = t.To;
    }
}

static void CheckReachability(FsmModel m, List<string> errors)
{
    var reachable = new HashSet<string> { m.Initial };
    bool changed = true;
    while (changed)
    {
        changed = false;
        foreach (var t in m.Transitions)
            if (reachable.Contains(t.From) && reachable.Add(t.To))
                changed = true;
    }
    foreach (var s in m.States.Where(s => !reachable.Contains(s)))
        errors.Add($"Reachability: state '{s}' unreachable from '{m.Initial}'");
}

// ===== Типи =====

record FsmModel(
    string Name,
    string Initial,
    string UnknownPolicy,
    List<string> States,
    List<string> Events,
    List<Transition> Transitions);

record Transition(string From, string Event, string To);

record EventScript(List<string> Events);
