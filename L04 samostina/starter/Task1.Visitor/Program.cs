// Task1.Visitor — STARTER
// Проблема: обхід AST реалізований через if/else всередині одного методу.
// Кожна нова операція вимагає змін у існуючому коді — порушення OCP.

// TODO: Ввести інтерфейс IAstNode з методом Accept(IAstVisitor)
// TODO: Ввести інтерфейс IAstVisitor з методами Visit для кожного типу вузла
// TODO: Реалізувати MetricsVisitor, що збирає метрики
// TODO: Прибрати всі умовні конструкції з логіки обходу

using System;
using System.Collections.Generic;

// --- Вузли AST (без інтерфейсів) ---

class FunctionNode
{
    public string Name { get; }
    public List<object> Body { get; } = new();
    public FunctionNode(string name) => Name = name;
}

class CallNode
{
    public string TargetName { get; }
    public CallNode(string targetName) => TargetName = targetName;
}

class LiteralNode
{
    public object Value { get; }
    public LiteralNode(object value) => Value = value;
}

// --- Антипатерн: обхід через if/else ---

class AstMetricsCollector
{
    public int FunctionCount { get; private set; }
    public int CallCount { get; private set; }
    public int LiteralCount { get; private set; }

    public void Collect(object node)
    {
        if (node is FunctionNode fn)
        {
            FunctionCount++;
            foreach (var child in fn.Body)
                Collect(child);
        }
        else if (node is CallNode)
        {
            CallCount++;
        }
        else if (node is LiteralNode)
        {
            LiteralCount++;
        }
        // Кожна нова операція або новий тип вузла — зміна цього методу
    }
}

// --- Демонстрація проблеми ---

var root = new FunctionNode("main");
root.Body.Add(new CallNode("print"));
root.Body.Add(new LiteralNode(42));
root.Body.Add(new LiteralNode("hello"));

var inner = new FunctionNode("helper");
inner.Body.Add(new CallNode("log"));
root.Body.Add(inner);

var collector = new AstMetricsCollector();
collector.Collect(root);

Console.WriteLine($"Functions : {collector.FunctionCount}");
Console.WriteLine($"Calls     : {collector.CallCount}");
Console.WriteLine($"Literals  : {collector.LiteralCount}");
