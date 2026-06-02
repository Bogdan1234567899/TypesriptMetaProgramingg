// Task3.Template — SOLUTION
// Патерн Template Method: порядок фаз фіксований в одному місці (AnalyzerTemplate.Analyze()).
// Підкласи перевизначають лише варіативні hook-методи.

using System;

// --- Абстрактний базовий клас ---

abstract class AnalyzerTemplate
{
    // Template method — порядок фіксований тут і лише тут
    public void Analyze(string source)
    {
        var tokens = Parse(source);
        Validate(tokens);
        Report(tokens);
    }

    // Спільна фаза: parse
    protected string[] Parse(string source)
    {
        Console.WriteLine($"[{Label}] Parsing source...");
        return source.Split(' ');
    }

    // Hook: варіативна фаза
    protected abstract void Validate(string[] tokens);

    // Спільна фаза: report
    protected void Report(string[] tokens)
    {
        Console.WriteLine($"[{Label}] Generating report...");
        Console.WriteLine($"[{Label}] Total tokens: {tokens.Length}");
    }

    protected abstract string Label { get; }
}

// --- Конкретні аналізатори ---

class StrictAnalyzer : AnalyzerTemplate
{
    protected override string Label => "Strict";

    protected override void Validate(string[] tokens)
    {
        Console.WriteLine($"[{Label}] Validating (strict mode)...");
        foreach (var token in tokens)
            if (token.Length > 10)
                Console.WriteLine($"[{Label}] WARNING: long token '{token}'");
    }
}

class RelaxedAnalyzer : AnalyzerTemplate
{
    protected override string Label => "Relaxed";

    protected override void Validate(string[] tokens)
    {
        Console.WriteLine($"[{Label}] Validating (relaxed mode — skipping warnings)...");
    }
}

// --- Демонстрація ---

var code = "int longVariableName = foo bar baz";

new StrictAnalyzer().Analyze(code);
Console.WriteLine();
new RelaxedAnalyzer().Analyze(code);
