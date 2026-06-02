// Task3 — Test Quality
// Before: лише 1 позитивний тест, інші гілки не покриті.
// After: покрив усі 4 гілки + mutation-перевірка.

using System;

class PasswordValidator
{
    public string Check(string pwd)
    {
        if (string.IsNullOrEmpty(pwd)) return "Empty";       // branch 1
        if (pwd.Length < 8)             return "Too short";  // branch 2
        foreach (var c in pwd)
            if (char.IsDigit(c))        return "Has digits"; // branch 3
        return "OK";                                          // branch 4
    }
}

// ===== BEFORE: тільки 1 тест =====

Console.WriteLine("=== BEFORE ===");
var v1 = new PasswordValidator();
Console.WriteLine($"OK case: {v1.Check("password") == "OK"}");
// branch coverage: 1/4 = 25%

// ===== AFTER: всі гілки + mutation check =====

Console.WriteLine("\n=== AFTER ===");
var v = new PasswordValidator();
int passed = 0, total = 0;

void Test(string desc, bool ok)
{
    total++;
    if (ok) passed++;
    Console.WriteLine($"  [{(ok ? "PASS" : "FAIL")}] {desc}");
}

Test("Empty input → 'Empty'",       v.Check("")          == "Empty");
Test("Short input → 'Too short'",   v.Check("ab")        == "Too short");
Test("Digits inside → 'Has digits'", v.Check("abc12345")  == "Has digits");
Test("Valid → 'OK'",                v.Check("password")  == "OK");

Console.WriteLine($"\nResult: {passed}/{total} passed");

// ===== Mutation check =====
// Уявна мутація: < замінили на <= у "pwd.Length < 8".
// Тоді для "password" (довжина 8) метод поверне "Too short" замість "OK" — тест OK впаде.
// Тобто мутант killed тестом "Valid → 'OK'". Mutation killed >= 1.
Console.WriteLine("Mutation < → <= у Length < 8: killed by 'Valid → OK' test");
