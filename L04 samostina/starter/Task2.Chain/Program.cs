// Task2.Chain — STARTER
// Проблема: монолітний RuleEngine — всі перевірки в одному методі.
// Неможливо додати нове правило без зміни класу.

// TODO: Виділити окремі класи-обробники для кожного правила
// TODO: Побудувати ланцюг мінімум з 3 обробників
// TODO: Реалізувати перемикач політики: FailFast або Accumulate
// TODO: Зберегти єдину точку входу через метод Handle()

using System;
using System.Collections.Generic;

class ValidationRequest
{
    public string Username { get; set; } = "";
    public string Email    { get; set; } = "";
    public int    Age      { get; set; }
}

class ValidationResult
{
    public bool IsValid => Errors.Count == 0;
    public List<string> Errors { get; } = new();
}

// --- Антипатерн: монолітний RuleEngine ---

class RuleEngine
{
    public ValidationResult Validate(ValidationRequest request)
    {
        var result = new ValidationResult();

        // Правило 1: Username не порожній
        if (string.IsNullOrWhiteSpace(request.Username))
            result.Errors.Add("Username is required.");

        // Правило 2: Email містить @
        if (!request.Email.Contains('@'))
            result.Errors.Add("Email is invalid.");

        // Правило 3: Вік >= 18
        if (request.Age < 18)
            result.Errors.Add("Age must be >= 18.");

        // Нове правило — обов'язкова зміна цього методу

        return result;
    }
}

// --- Демонстрація ---

var engine = new RuleEngine();

var badRequest = new ValidationRequest { Username = "", Email = "notanemail", Age = 15 };
var result = engine.Validate(badRequest);

Console.WriteLine($"Valid: {result.IsValid}");
foreach (var e in result.Errors)
    Console.WriteLine($"  - {e}");
