// Task3.Template — STARTER
// Проблема: StrictAnalyzer і RelaxedAnalyzer дублюють логіку фаз
// parse → validate → report. Зміна порядку в одному не відображається в іншому.

// TODO: Створити абстрактний клас AnalyzerTemplate з методом Analyze()
// TODO: Виділити abstract hook-методи для варіативних фаз
// TODO: Реалізувати StrictAnalyzer і RelaxedAnalyzer як підкласи
// TODO: Спільну логіку перенести у базовий клас, різну — у hook-и

using System;

// --- Антипатерн: дублювання фаз ---

class StrictAnalyzer
{
    public void Analyze(string source)
    {
        // Фаза 1: parse
        Console.WriteLine("[Strict] Parsing source...");
        var tokens = source.Split(' ');

        // Фаза 2: validate (сувора перевірка)
        Console.WriteLine("[Strict] Validating (strict mode)...");
        foreach (var token in tokens)
            if (token.Length > 10)
                Console.WriteLine($"[Strict] WARNING: long token '{token}'");

        // Фаза 3: report
        Console.WriteLine("[Strict] Generating report...");
        Console.WriteLine($"[Strict] Total tokens: {tokens.Length}");
    }
}

class RelaxedAnalyzer
{
    public void Analyze(string source)
    {
        // Фаза 1: parse  ← дублювання
        Console.WriteLine("[Relaxed] Parsing source...");
        var tokens = source.Split(' ');

        // Фаза 2: validate (м'яка перевірка)
        Console.WriteLine("[Relaxed] Validating (relaxed mode)...");
        // Пропускаємо попередження

        // Фаза 3: report  ← дублювання
        Console.WriteLine("[Relaxed] Generating report...");
        Console.WriteLine($"[Relaxed] Total tokens: {tokens.Length}");
    }
}

// --- Демонстрація ---

var code = "int longVariableName = foo bar baz";

new StrictAnalyzer().Analyze(code);
Console.WriteLine();
new RelaxedAnalyzer().Analyze(code);
