// Task3 — Deployment Validation
// Before: список required має 4 переходи, transitions — тільки 2.
// After: дописано відсутні переходи, валідатор показує Errors: 0.

using System;
using System.Collections.Generic;

// ===== Top-level код =====

// Список обов'язкових переходів
var required = new List<(DeployState, DeployEvent)>
{
    (DeployState.Planned,   DeployEvent.Build),
    (DeployState.Building,  DeployEvent.Test),
    (DeployState.Testing,   DeployEvent.Deploy),
    (DeployState.Deploying, DeployEvent.Done),
};

// ===== BEFORE — неповна таблиця =====

Console.WriteLine("=== BEFORE validation ===");

var transitionsBefore = new Dictionary<(DeployState, DeployEvent), DeployState>
{
    [(DeployState.Planned,  DeployEvent.Build)] = DeployState.Building,
    [(DeployState.Building, DeployEvent.Test)]  = DeployState.Testing,
};

Validate(required, transitionsBefore);

// ===== AFTER — повна таблиця =====

Console.WriteLine("\n=== AFTER validation ===");

var transitionsAfter = new Dictionary<(DeployState, DeployEvent), DeployState>
{
    [(DeployState.Planned,   DeployEvent.Build)]  = DeployState.Building,
    [(DeployState.Building,  DeployEvent.Test)]   = DeployState.Testing,
    [(DeployState.Testing,   DeployEvent.Deploy)] = DeployState.Deploying,
    [(DeployState.Deploying, DeployEvent.Done)]   = DeployState.Done,
};

Validate(required, transitionsAfter);

// ===== FSM walkthrough =====

Console.WriteLine("\n=== FSM walkthrough (after) ===");
var st = DeployState.Planned;
foreach (var evt in new[] { DeployEvent.Build, DeployEvent.Test, DeployEvent.Deploy, DeployEvent.Done })
{
    if (transitionsAfter.TryGetValue((st, evt), out var next))
    {
        Console.WriteLine($"{st} + {evt} -> {next}");
        st = next;
    }
    else
    {
        throw new InvalidOperationException($"Illegal: {st} + {evt}");
    }
}

// ===== Локальна функція-валідатор =====

static void Validate(
    List<(DeployState, DeployEvent)> req,
    Dictionary<(DeployState, DeployEvent), DeployState> table)
{
    var errors = new List<string>();
    foreach (var pair in req)
    {
        if (!table.ContainsKey(pair))
            errors.Add($"Missing transition: {pair.Item1} + {pair.Item2}");
    }

    if (errors.Count == 0)
    {
        Console.WriteLine("Validation OK — Errors: 0");
    }
    else
    {
        Console.WriteLine($"Errors: {errors.Count}");
        errors.ForEach(e => Console.WriteLine($"  [ERROR] {e}"));
    }
}

// ===== Типи =====

enum DeployState { Planned, Building, Testing, Deploying, Done }
enum DeployEvent { Build, Test, Deploy, Done }
