// Task2.Chain — SOLUTION
// Патерн Chain of Responsibility: нове правило — новий handler-клас,
// існуючі обробники не змінюються. Підтримка двох стратегій: FailFast і Accumulate.

using System;
using System.Collections.Generic;

// --- Модель запиту та результату ---

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

// --- Стратегія зупинки ---

enum ValidationPolicy { FailFast, Accumulate }

// --- Базовий абстрактний обробник ---

abstract class ValidationHandler
{
    protected ValidationHandler? Next { get; private set; }

    public ValidationHandler SetNext(ValidationHandler next)
    {
        Next = next;
        return next;
    }

    public void Handle(ValidationRequest request, ValidationResult result, ValidationPolicy policy)
    {
        Validate(request, result);

        if (policy == ValidationPolicy.FailFast && !result.IsValid)
            return;

        Next?.Handle(request, result, policy);
    }

    protected abstract void Validate(ValidationRequest request, ValidationResult result);
}

// --- Обробники ---

class UsernameHandler : ValidationHandler
{
    protected override void Validate(ValidationRequest request, ValidationResult result)
    {
        if (string.IsNullOrWhiteSpace(request.Username))
            result.Errors.Add("Username is required.");
    }
}

class EmailHandler : ValidationHandler
{
    protected override void Validate(ValidationRequest request, ValidationResult result)
    {
        if (!request.Email.Contains('@'))
            result.Errors.Add("Email is invalid.");
    }
}

class AgeHandler : ValidationHandler
{
    protected override void Validate(ValidationRequest request, ValidationResult result)
    {
        if (request.Age < 18)
            result.Errors.Add("Age must be >= 18.");
    }
}

// --- Точка входу через Handle() ---

class RuleEngine
{
    private readonly ValidationHandler _chain;
    private readonly ValidationPolicy  _policy;

    public RuleEngine(ValidationPolicy policy)
    {
        _policy = policy;

        var username = new UsernameHandler();
        var email    = new EmailHandler();
        var age      = new AgeHandler();

        username.SetNext(email).SetNext(age);
        _chain = username;
    }

    public ValidationResult Handle(ValidationRequest request)
    {
        var result = new ValidationResult();
        _chain.Handle(request, result, _policy);
        return result;
    }
}

// --- Демонстрація ---

var request = new ValidationRequest { Username = "", Email = "notanemail", Age = 15 };

Console.WriteLine("=== FailFast ===");
var ffEngine = new RuleEngine(ValidationPolicy.FailFast);
var ffResult = ffEngine.Handle(request);
Console.WriteLine($"Valid: {ffResult.IsValid}");
foreach (var e in ffResult.Errors) Console.WriteLine($"  - {e}");

Console.WriteLine("\n=== Accumulate ===");
var accEngine = new RuleEngine(ValidationPolicy.Accumulate);
var accResult = accEngine.Handle(request);
Console.WriteLine($"Valid: {accResult.IsValid}");
foreach (var e in accResult.Errors) Console.WriteLine($"  - {e}");
