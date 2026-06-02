// Task1 — Complexity
// Before: один метод з купою вкладених перевірок.
// After: декомпозиція на маленькі методи.

using System;

// ===== BEFORE =====

class TextCheckerBefore
{
    public bool Validate(string text)
    {
        if (text == null) return false;
        if (text.Length == 0) return false;
        if (text.Length < 3) return false;
        if (text.Length > 50) return false;

        for (int i = 0; i < text.Length; i++)
        {
            if (char.IsDigit(text[i]))
            {
                if (i == 0) return false;
                if (i == text.Length - 1) return false;
            }
        }

        if (text.StartsWith(" ")) return false;
        if (text.EndsWith(" ")) return false;

        return true;
    }
}

// ===== AFTER =====

class TextCheckerAfter
{
    public bool Validate(string text)
    {
        if (!HasContent(text)) return false;
        if (!HasValidLength(text)) return false;
        if (!HasValidDigitPositions(text)) return false;
        if (HasEdgeWhitespace(text)) return false;
        return true;
    }

    private bool HasContent(string text) => !string.IsNullOrEmpty(text);

    private bool HasValidLength(string text) =>
        text.Length >= 3 && text.Length <= 50;

    private bool HasValidDigitPositions(string text)
    {
        for (int i = 0; i < text.Length; i++)
        {
            if (char.IsDigit(text[i]) && (i == 0 || i == text.Length - 1))
                return false;
        }
        return true;
    }

    private bool HasEdgeWhitespace(string text) =>
        text.StartsWith(" ") || text.EndsWith(" ");
}

// ===== Перевірка що поведінка не змінилась =====

var before = new TextCheckerBefore();
var after  = new TextCheckerAfter();

string[] cases =
{
    "abc",
    "ab",
    "1abc",
    "abc1",
    " abc",
    "abc ",
    "valid text",
    "",
    new string('x', 60)
};

foreach (var c in cases)
{
    bool b = before.Validate(c);
    bool a = after.Validate(c);
    Console.WriteLine($"'{c}': before={b}, after={a}, equal={b == a}");
}
