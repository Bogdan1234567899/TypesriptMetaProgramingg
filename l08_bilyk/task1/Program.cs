// Task1 — Coffee Machine FSM runner
// Читає coffee_machine_fsm.json, виконує сценарій, виводить лог у консоль і run_output.txt.

using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

var modelPath = "coffee_machine_fsm.json";
var outputPath = "run_output.txt";

var json = File.ReadAllText(modelPath);
var model = JsonSerializer.Deserialize<FsmModel>(json,
    new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
    ?? throw new InvalidOperationException("Failed to parse model");

// Будуємо таблицю переходів
var table = new Dictionary<(string, string), string>();
foreach (var t in model.Transitions)
    table[(t.From, t.Event)] = t.To;

var log = new StringBuilder();
void Print(string line)
{
    Console.WriteLine(line);
    log.AppendLine(line);
}

Print($"Loaded model: {model.Name}");
Print($"Initial state: {model.Initial}");
Print($"Unknown policy: {model.UnknownPolicy}");
Print("");

// Сценарій: normal flow + Fault
var script = new[]
{
    "InsertCoin", "SelectDrink", "StartBrew", "Serve", "Reset",
    "Fault",
    "Reset"
};

var state = model.Initial;
Print($"=== Scenario start ({script.Length} events) ===");
foreach (var evt in script)
{
    if (table.TryGetValue((state, evt), out var next))
    {
        Print($"{state} + {evt} -> {next}");
        state = next;
    }
    else
    {
        // Єдина unknown policy: fail-fast
        Print($"[ILLEGAL] {state} + {evt} — no transition");
        throw new InvalidOperationException($"Illegal transition: {state} + {evt}");
    }
}
Print($"=== End: final state = {state} ===");

File.WriteAllText(outputPath, log.ToString());
Console.WriteLine($"\nOutput written to {outputPath}");

// ===== Типи =====

record FsmModel(
    string Name,
    string Initial,
    string UnknownPolicy,
    List<string> States,
    List<string> Events,
    List<Transition> Transitions);

record Transition(string From, string Event, string To);
