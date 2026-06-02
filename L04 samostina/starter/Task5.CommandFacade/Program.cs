// Task5.CommandFacade — STARTER
// Проблема: клієнт вручну викликає 4-5 сервісів у довільному порядку.
// Трансформації не логуються, код крихкий і важко тестується.

// TODO: Реалізувати мінімум 2 команди (InlineConstantCommand, RenameSymbolCommand)
// TODO: Створити CommandBus з журналом виконаних команд
// TODO: Реалізувати AnalyzerFacade з одним методом запуску пайплайну

using System;
using System.Collections.Generic;

// --- Сервіси трансформацій ---

class ConstantInliner
{
    public string Inline(string source)
    {
        Console.WriteLine("[ConstantInliner] Inlining constants...");
        return source.Replace("MAX_SIZE", "100");
    }
}

class SymbolRenamer
{
    public string Rename(string source, string from, string to)
    {
        Console.WriteLine($"[SymbolRenamer] Renaming '{from}' → '{to}'...");
        return source.Replace(from, to);
    }
}

class AstValidator
{
    public void Validate(string source)
    {
        Console.WriteLine("[AstValidator] Validating AST...");
        if (source.Contains("???"))
            throw new InvalidOperationException("Invalid token found.");
    }
}

class ReportGenerator
{
    public void Generate(string source)
    {
        Console.WriteLine("[ReportGenerator] Generating report...");
        Console.WriteLine($"  Source length: {source.Length} chars");
    }
}

// --- Антипатерн: клієнт напряму викликає всі сервіси ---

var source = "function foo(MAX_SIZE) { oldName(); }";

var inliner   = new ConstantInliner();
var renamer   = new SymbolRenamer();
var validator = new AstValidator();
var reporter  = new ReportGenerator();

// Клієнт знає про всі сервіси і порядок викликів — крихкий код
source = inliner.Inline(source);
source = renamer.Rename(source, "oldName", "newName");
validator.Validate(source);
reporter.Generate(source);

Console.WriteLine($"\nResult: {source}");
// Немає журналу виконаних трансформацій
