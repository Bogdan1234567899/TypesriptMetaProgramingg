// Task4 — Exam Session Validator
// Запускає валідатор послідовно на broken і fixed моделях,
// демонструє різницю: помилки → Validation OK.

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;

ValidateFile("exam_session_broken.json");
Console.WriteLine();
ValidateFile("exam_session_fixed.json");

static void ValidateFile(string path)
{
    Console.WriteLine($"=== Validating: {path} ===");

    var model = JsonSerializer.Deserialize<FsmModel>(File.ReadAllText(path),
        new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
        ?? throw new InvalidOperationException("Failed to parse model");

    var errors = new List<string>();
    CheckReferences(model, errors);
    CheckDeterminism(model, errors);
    CheckReachability(model, errors);

    if (errors.Count == 0)
    {
        Console.WriteLine("Validation OK — all invariants hold.");
    }
    else
    {
        Console.WriteLine($"Validation FAILED — {errors.Count} error(s):");
        errors.ForEach(e => Console.WriteLine($"  [ERROR] {e}"));
    }
}

static void CheckReferences(FsmModel m, List<string> errors)
{
    var statesSet = new HashSet<string>(m.States);
    var eventsSet = new HashSet<string>(m.Events);

    if (!statesSet.Contains(m.Initial))
        errors.Add($"Reference: initial state '{m.Initial}' not declared in states");

    foreach (var t in m.Transitions)
    {
        if (!statesSet.Contains(t.From))
            errors.Add($"Reference: transition.from '{t.From}' not in states");
        if (!statesSet.Contains(t.To))
            errors.Add($"Reference: transition.to '{t.To}' not in states");
        if (!eventsSet.Contains(t.Event))
            errors.Add($"Reference: transition.event '{t.Event}' not in events");
    }
}

static void CheckDeterminism(FsmModel m, List<string> errors)
{
    var seen = new Dictionary<(string, string), string>();
    foreach (var t in m.Transitions)
    {
        var key = (t.From, t.Event);
        if (seen.TryGetValue(key, out var existing))
        {
            if (existing != t.To)
                errors.Add($"Determinism: conflict for ({t.From}, {t.Event}) → '{existing}' and '{t.To}'");
        }
        else
        {
            seen[key] = t.To;
        }
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
        {
            if (reachable.Contains(t.From) && reachable.Add(t.To))
                changed = true;
        }
    }
    foreach (var s in m.States.Where(s => !reachable.Contains(s)))
        errors.Add($"Reachability: state '{s}' is unreachable from initial '{m.Initial}'");
}

record FsmModel(
    string Name,
    string Initial,
    string UnknownPolicy,
    List<string> States,
    List<string> Events,
    List<Transition> Transitions);

record Transition(string From, string Event, string To);
