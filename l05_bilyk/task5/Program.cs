// Task5 — Hotspot
// Обчислюємо hotspot = churn × defects для кожного модуля,
// знаходимо top-1 ризик і даємо перший крок рефакторингу.

using System;
using System.Linq;

class Module
{
    public string Name { get; set; } = "";
    public int    Churn { get; set; }
    public int    Defects { get; set; }
    public int    Hotspot => Churn * Defects;
}

var modules = new[]
{
    new Module { Name = "AuthService",     Churn = 12, Defects = 5 },
    new Module { Name = "PaymentGateway",  Churn = 8,  Defects = 9 },
    new Module { Name = "Logger",          Churn = 3,  Defects = 1 },
    new Module { Name = "ReportBuilder",   Churn = 6,  Defects = 2 },
    new Module { Name = "NotificationHub", Churn = 4,  Defects = 3 },
};

Console.WriteLine("Module           | Churn | Defects | Hotspot");
Console.WriteLine("-----------------|-------|---------|--------");
foreach (var m in modules.OrderByDescending(m => m.Hotspot))
    Console.WriteLine($"{m.Name,-16} | {m.Churn,5} | {m.Defects,7} | {m.Hotspot,7}");

var top = modules.OrderByDescending(m => m.Hotspot).First();
int maxHotspot = top.Hotspot;

Console.WriteLine($"\nTop risk: {top.Name} (hotspot = {maxHotspot})");

// Quality Gate
int threshold = 80;   // власний поріг — обґрунтований у звіті
string status = maxHotspot <= threshold ? "PASS" : "FAIL";
Console.WriteLine($"Gate: max hotspot ({maxHotspot}) <= {threshold} → {status}");

Console.WriteLine($"\nNext step: розбити {top.Name} на менші модулі за відповідальностями");
Console.WriteLine("і покрити критичні гілки тестами — це знизить і churn, і defects.");
