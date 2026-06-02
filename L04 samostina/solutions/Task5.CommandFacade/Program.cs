// Task5.CommandFacade — SOLUTION
// Command інкапсулює AST-трансформації з підтримкою логування.
// Facade приховує складну оркестрацію за одним методом виклику.

using System;
using System.Collections.Generic;

// --- Сервіси трансформацій (не змінюємо) ---

class ConstantInliner
{
    public string Inline(string source)
    {
        return source.Replace("MAX_SIZE", "100");
    }
}

class SymbolRenamer
{
    public string Rename(string source, string from, string to) =>
        source.Replace(from, to);
}

class AstValidator
{
    public void Validate(string source)
    {
        if (source.Contains("???"))
            throw new InvalidOperationException("Invalid token found.");
    }
}

class ReportGenerator
{
    public void Generate(string source)
    {
        Console.WriteLine($"[Report] Source length: {source.Length} chars");
        Console.WriteLine($"[Report] Content: {source}");
    }
}

// --- Контекст, що передається між командами ---

class PipelineContext
{
    public string Source { get; set; } = "";
    public PipelineContext(string source) => Source = source;
}

// --- Інтерфейс Command ---

interface ICommand
{
    string Name { get; }
    void Execute(PipelineContext context);
}

// --- Конкретні команди ---

class InlineConstantCommand : ICommand
{
    private readonly ConstantInliner _inliner = new();
    public string Name => "InlineConstants";

    public void Execute(PipelineContext context)
    {
        context.Source = _inliner.Inline(context.Source);
    }
}

class RenameSymbolCommand : ICommand
{
    private readonly SymbolRenamer _renamer = new();
    private readonly string _from;
    private readonly string _to;

    public string Name => $"RenameSymbol({_from}→{_to})";

    public RenameSymbolCommand(string from, string to)
    {
        _from = from;
        _to   = to;
    }

    public void Execute(PipelineContext context)
    {
        context.Source = _renamer.Rename(context.Source, _from, _to);
    }
}

// --- CommandBus з журналом ---

class CommandBus
{
    private readonly List<string> _log = new();

    public IReadOnlyList<string> Log => _log;

    public void Send(ICommand command, PipelineContext context)
    {
        command.Execute(context);
        _log.Add(command.Name);
    }
}

// --- Facade ---

class AnalyzerFacade
{
    private readonly CommandBus      _bus       = new();
    private readonly AstValidator    _validator  = new();
    private readonly ReportGenerator _reporter   = new();

    public void Run(string source)
    {
        var context = new PipelineContext(source);

        _bus.Send(new InlineConstantCommand(),              context);
        _bus.Send(new RenameSymbolCommand("oldName", "newName"), context);

        _validator.Validate(context.Source);
        _reporter.Generate(context.Source);

        Console.WriteLine("\n=== Command Log ===");
        foreach (var entry in _bus.Log)
            Console.WriteLine($"  ✓ {entry}");
    }
}

// --- Клієнт: тільки через фасад ---

var facade = new AnalyzerFacade();
facade.Run("function foo(MAX_SIZE) { oldName(); }");
