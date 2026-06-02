// Task4 — Duplication
// Before: sanitize-логіка повторюється у BuildInvoice і BuildReceipt.
// After: винесено у спільний helper.

using System;

// ===== BEFORE =====

class DocumentBuilderBefore
{
    public string BuildInvoice(string customer, decimal amount)
    {
        var clean = customer.Trim();
        if (clean.Length > 50) clean = clean.Substring(0, 50);
        clean = clean.Replace(";", "").Replace(",", "");
        return $"Invoice for {clean}: ${amount}";
    }

    public string BuildReceipt(string customer, decimal amount)
    {
        var clean = customer.Trim();                                // ← дублікат
        if (clean.Length > 50) clean = clean.Substring(0, 50);      // ← дублікат
        clean = clean.Replace(";", "").Replace(",", "");            // ← дублікат
        return $"Receipt for {clean}: ${amount}";
    }
}

// ===== AFTER =====

static class StringSanitizer
{
    public static string Sanitize(string input)
    {
        var clean = input.Trim();
        if (clean.Length > 50) clean = clean.Substring(0, 50);
        return clean.Replace(";", "").Replace(",", "");
    }
}

class DocumentBuilderAfter
{
    public string BuildInvoice(string customer, decimal amount) =>
        $"Invoice for {StringSanitizer.Sanitize(customer)}: ${amount}";

    public string BuildReceipt(string customer, decimal amount) =>
        $"Receipt for {StringSanitizer.Sanitize(customer)}: ${amount}";
}

// ===== Перевірка =====

var before = new DocumentBuilderBefore();
var after  = new DocumentBuilderAfter();

var customer = "  John; Smith, Jr.  ";

Console.WriteLine($"before invoice : {before.BuildInvoice(customer, 100)}");
Console.WriteLine($"after  invoice : {after.BuildInvoice(customer, 100)}");
Console.WriteLine($"before receipt : {before.BuildReceipt(customer, 100)}");
Console.WriteLine($"after  receipt : {after.BuildReceipt(customer, 100)}");
