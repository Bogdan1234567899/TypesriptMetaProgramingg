// AUTO-GENERATED from payment_retry_fsm_v1.json
// DO NOT EDIT MANUALLY.

using System;
using System.Collections.Generic;

public static class GeneratedPaymentTests
{
    static readonly Dictionary<(string, string), string> Transitions = new()
    {
        [("Initial", "Try")] = "Trying",
        [("Trying", "Success")] = "Succeeded",
        [("Trying", "Fail")] = "Failed",
        [("Failed", "Retry")] = "Trying",
        [("Failed", "GiveUp")] = "Abandoned",
    };

    static string Next(string state, string evt)
    {
        if (Transitions.TryGetValue((state, evt), out var next)) return next;
        throw new InvalidOperationException($"Illegal transition: {state} + {evt}");
    }

    public static int Run()
    {
        int passed = 0, total = 0;
        void Assert(string name, Func<bool> check)
        {
            total++;
            bool ok;
            try { ok = check(); } catch { ok = false; }
            if (ok) passed++;
            Console.WriteLine($"  [{(ok ? "PASS" : "FAIL")}] {name}");
        }

        // === Valid transition tests ===
        Console.WriteLine("-- Valid transitions --");
        Assert("Initial + Try -> Trying",
            () => Next("Initial", "Try") == "Trying");
        Assert("Trying + Success -> Succeeded",
            () => Next("Trying", "Success") == "Succeeded");
        Assert("Trying + Fail -> Failed",
            () => Next("Trying", "Fail") == "Failed");
        Assert("Failed + Retry -> Trying",
            () => Next("Failed", "Retry") == "Trying");
        Assert("Failed + GiveUp -> Abandoned",
            () => Next("Failed", "GiveUp") == "Abandoned");

        // === Invalid transition tests ===
        Console.WriteLine("-- Invalid transitions --");
        Assert("Initial + Success throws (invalid)",
            () => { try { Next("Initial", "Success"); return false; }
                    catch (InvalidOperationException) { return true; } });
        Assert("Initial + Fail throws (invalid)",
            () => { try { Next("Initial", "Fail"); return false; }
                    catch (InvalidOperationException) { return true; } });
        Assert("Initial + Retry throws (invalid)",
            () => { try { Next("Initial", "Retry"); return false; }
                    catch (InvalidOperationException) { return true; } });
        Assert("Initial + GiveUp throws (invalid)",
            () => { try { Next("Initial", "GiveUp"); return false; }
                    catch (InvalidOperationException) { return true; } });
        Assert("Trying + Try throws (invalid)",
            () => { try { Next("Trying", "Try"); return false; }
                    catch (InvalidOperationException) { return true; } });

        // === Policy tests ===
        Console.WriteLine("-- Policy behavior --");
        Assert("Unknown policy is 'throw' — throws on unknown",
            () => { try { Next("NonExistent", "WhoKnows"); return false; }
                    catch (InvalidOperationException) { return true; } });

        Console.WriteLine($"\nPassed: {passed}/{total}");
        return passed == total ? 0 : 1;
    }
}
