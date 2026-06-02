// Task1.Visitor — SOLUTION
// Патерн Visitor: нова операція над AST — новий клас-visitor,
// вузли не змінюються. Реалізація принципу Open/Closed.

using System;
using System.Collections.Generic;

// --- Інтерфейс Visitor ---

interface IAstVisitor
{
    void Visit(FunctionNode node);
    void Visit(CallNode node);
    void Visit(LiteralNode node);
}

// --- Інтерфейс вузла AST ---

interface IAstNode
{
    void Accept(IAstVisitor visitor);
}

// --- Вузли AST ---

class FunctionNode : IAstNode
{
    public string Name { get; }
    public List<IAstNode> Body { get; } = new();
    public FunctionNode(string name) => Name = name;

    public void Accept(IAstVisitor visitor)
    {
        visitor.Visit(this);
        foreach (var child in Body)
            child.Accept(visitor);
    }
}

class CallNode : IAstNode
{
    public string TargetName { get; }
    public CallNode(string targetName) => TargetName = targetName;

    public void Accept(IAstVisitor visitor) => visitor.Visit(this);
}

class LiteralNode : IAstNode
{
    public object Value { get; }
    public LiteralNode(object value) => Value = value;

    public void Accept(IAstVisitor visitor) => visitor.Visit(this);
}

// --- Visitor: збір метрик ---

class MetricsVisitor : IAstVisitor
{
    public int FunctionCount { get; private set; }
    public int CallCount { get; private set; }
    public int LiteralCount { get; private set; }

    public void Visit(FunctionNode node) => FunctionCount++;
    public void Visit(CallNode node)     => CallCount++;
    public void Visit(LiteralNode node)  => LiteralCount++;
}

// --- Демонстрація: нова операція — новий Visitor, вузли не змінені ---
// PrintVisitor обходить дерево самостійно через рекурсію,
// щоб коректно керувати глибиною відступу.

class PrintVisitor
{
    public void Print(IAstNode node, int depth = 0)
    {
        var pad = new string(' ', depth * 2);
        switch (node)
        {
            case FunctionNode fn:
                Console.WriteLine($"{pad}[Function] {fn.Name}");
                foreach (var child in fn.Body)
                    Print(child, depth + 1);
                break;
            case CallNode cn:
                Console.WriteLine($"{pad}[Call] {cn.TargetName}");
                break;
            case LiteralNode ln:
                Console.WriteLine($"{pad}[Literal] {ln.Value}");
                break;
        }
    }
}

// --- Точка входу ---

var root = new FunctionNode("main");
root.Body.Add(new CallNode("print"));
root.Body.Add(new LiteralNode(42));
root.Body.Add(new LiteralNode("hello"));

var inner = new FunctionNode("helper");
inner.Body.Add(new CallNode("log"));
root.Body.Add(inner);

var metrics = new MetricsVisitor();
root.Accept(metrics);

Console.WriteLine("=== Метрики ===");
Console.WriteLine($"Functions : {metrics.FunctionCount}");
Console.WriteLine($"Calls     : {metrics.CallCount}");
Console.WriteLine($"Literals  : {metrics.LiteralCount}");

Console.WriteLine("\n=== Дерево ===");
new PrintVisitor().Print(root);
