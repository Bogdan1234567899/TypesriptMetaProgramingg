// Task3 — Content Moderation FSM
// Прогон 3 сценаріїв: normal flow, reject→revise→review, unknown event (fail-fast).

using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;

var modelPath  = "content_moderation_fsm.json";
var outputPath = "scenarios_output.txt";

var model = JsonSerializer.Deserialize<FsmModel>(File.ReadAllText(modelPath),
    new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
    ?? throw new InvalidOperationException("Failed to parse model");

var table = new Dictionary<(string, string), string>();
foreach (var t in model.Transitions)
    table[(t.From, t.Event)] = t.To;

var log = new StringBuilder();
void Print(string s) { Console.WriteLine(s); log.AppendLine(s); }

string Run(string state, string evt)
{
    if (table.TryGetValue((state, evt), out var next))
        return next;
    // unknownPolicy = throw
    throw new InvalidOperationException($"Illegal transition: {state} + {evt}");
}

void Scenario(string title, string[] events)
{
    Print($"=== {title} ===");
    var state = model.Initial;
    foreach (var evt in events)
    {
        try
        {
            var next = Run(state, evt);
            Print($"{state} + {evt} -> {next}");
            state = next;
        }
        catch (InvalidOperationException ex)
        {
            Print($"[FAIL-FAST] {ex.Message}");
            break;
        }
    }
    Print($"Final state: {state}");
    Print("");
}

// Сценарій 1: normal flow до Published
Scenario("Scenario 1: Normal flow to Published", new[]
{
    "Submit", "StartReview", "Approve", "Publish"
});

// Сценарій 2: reject → revise → повторний review → publish
Scenario("Scenario 2: Reject -> Revise -> Review again", new[]
{
    "Submit", "StartReview", "Reject", "Revise",
    "Submit", "StartReview", "Approve", "Publish"
});

// Сценарій 3: unknown event (Publish з Draft) — має кинути fail-fast
Scenario("Scenario 3: Unknown event (fail-fast)", new[]
{
    "Publish"
});

File.WriteAllText(outputPath, log.ToString());
Console.WriteLine($"Output written to {outputPath}");

// ===== Типи =====

record FsmModel(
    string Name,
    string Initial,
    string UnknownPolicy,
    List<string> States,
    List<string> Events,
    List<Transition> Transitions);

record Transition(string From, string Event, string To);
