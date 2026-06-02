// Task4.Adapter — STARTER
// Проблема: зовнішня бібліотека повертає власний формат дерева,
// несумісний із внутрішнім AstDocument. Клієнт знає про обидва формати.

// TODO: Реалізувати ExternalParserAdapter : IAstProvider
// TODO: Виконати маппінг зовнішнього дерева у внутрішній AstDocument
// TODO: Запустити систему з двома провайдерами через один контракт IAstProvider

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
    public AstDocument Parse(string source)
    {
        return new AstDocument
        {
            RootName  = "root",
            NodeNames = new List<string>(source.Split(' '))
        };
    }
}

// --- Зовнішня бібліотека (чужий код, не змінюємо) ---

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

// --- Антипатерн: клієнт знає про зовнішній формат ---

var source = "function call literal";

var internalParser  = new InternalParser();
var externalLibrary = new ExternalLibraryParser();

// Клієнт сам робить маппінг — це неправильно
var internalDoc = internalParser.Parse(source);
Console.WriteLine($"[Internal] Root: {internalDoc.RootName}, Nodes: {string.Join(", ", internalDoc.NodeNames)}");

var externalTree = externalLibrary.BuildTree(source);
// Клієнт знає про ExternalTree і ExternalItem — порушення мети Adapter
var mapped = new AstDocument
{
    RootName  = externalTree.Title,
    NodeNames = externalTree.Items.ConvertAll(i => i.Tag)
};
Console.WriteLine($"[External] Root: {mapped.RootName}, Nodes: {string.Join(", ", mapped.NodeNames)}");
