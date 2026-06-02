// HANDWRITTEN — runtime layer on top of generated FSM.
// Це приклад ручного шару, який використовує generated runtime.
// Безпечно редагувати: викликає GeneratedExampleRuntime через публічний API.

using System;

public class ExampleService
{
    private string _state = "Idle";

    // Ручна логіка: додає логування і метрики поверх generated Next().
    public void HandleEvent(string evt)
    {
        Console.WriteLine($"[Service] received event '{evt}' in state '{_state}'");

        try
        {
            _state = GeneratedExampleRuntime.Next(_state, evt);
            Console.WriteLine($"[Service] transitioned to '{_state}'");
        }
        catch (InvalidOperationException ex)
        {
            Console.WriteLine($"[Service] rejected: {ex.Message}");
            throw;
        }
    }

    public string CurrentState => _state;
}
