// Task4.Adapter — SOLUTION
// Патерн Adapter: клієнт працює з одним контрактом IAstProvider.
// Маппінг зовнішнього формату — відповідальність адаптера, не клієнта.

using System;
using System.Collections.Generic;

// --- Внутрішній контракт і модель ---

class AstDocument
{
    public string RootName { get; set; } = "";
    public List<string> NodeNames { get; set; } = new();
}

interface IAstProvider
{
    AstDocument Parse(string source);
}

// --- Внутрішній провайдер ---

class InternalParser : IAstProvider
{
    public AstDocument Parse(string source) =>
        new AstDocument
        {
            RootName  = "root",
            NodeNames = new List<string>(source.Split(' '))
        };
}

// --- Зовнішня бібліотека (не змінюємо) ---

class ExternalLibraryParser
{
    public ExternalTree BuildTree(string input)
    {
        var tree = new ExternalTree { Title = "external-root" };
        foreach (var w in input.Split(' '))
            tree.Items.Add(new ExternalItem { Tag = w });
        return tree;
    }
}

class ExternalTree
{
    public string Title { get; set; } = "";
    public List<ExternalItem> Items { get; set; } = new();
}

class ExternalItem
{
    public string Tag { get; set; } = "";
}

// --- Адаптер ---

class ExternalParserAdapter : IAstProvider
{
    private readonly ExternalLibraryParser _library = new();

    public AstDocument Parse(string source)
    {
        var tree = _library.BuildTree(source);

        // Маппінг — відповідальність адаптера
        return new AstDocument
        {
            RootName  = tree.Title,
            NodeNames = tree.Items.ConvertAll(item => item.Tag)
        };
    }
}

// --- Клієнт: один контракт, без розгалужень і приведень типів ---

void RunAnalysis(IAstProvider provider, string label, string source)
{
    var doc = provider.Parse(source);
    Console.WriteLine($"[{label}] Root: {doc.RootName}");
    Console.WriteLine($"[{label}] Nodes: {string.Join(", ", doc.NodeNames)}");
}

var source = "function call literal";

RunAnalysis(new InternalParser(),       "Internal", source);
Console.WriteLine();
RunAnalysis(new ExternalParserAdapter(), "External", source);
