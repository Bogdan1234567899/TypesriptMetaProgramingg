// AUTO-GENERATED from payment_retry_fsm_v1.json
// DO NOT EDIT MANUALLY.

using System;
using System.Collections.Generic;

public static class GeneratedPaymentRuntime
{
    public const string InitialState = "Initial";

    public static readonly Dictionary<(string, string), string> Transitions = new()
    {
        [("Initial", "Try")] = "Trying",
        [("Trying", "Success")] = "Succeeded",
        [("Trying", "Fail")] = "Failed",
        [("Failed", "Retry")] = "Trying",
        [("Failed", "GiveUp")] = "Abandoned",
    };

    public static string Next(string state, string evt)
    {
        if (Transitions.TryGetValue((state, evt), out var next))
            return next;

        // Unknown policy from DSL: throw
        throw new InvalidOperationException(
            $"Illegal transition: {state} + {evt}");
    }
}
