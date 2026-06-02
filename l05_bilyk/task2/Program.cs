// Task2 — Coupling
// Before: UserService створює залежності через new — жорстке зв'язування.
// After: інтерфейси + constructor injection.

using System;

// ===== BEFORE =====

class UserRepositoryBefore
{
    public void Save(string email) => Console.WriteLine($"[Repo] saved {email}");
}

class EmailSenderBefore
{
    public void Send(string to, string msg) => Console.WriteLine($"[Mail] {to}: {msg}");
}

class UserServiceBefore
{
    public void Register(string email)
    {
        var repo   = new UserRepositoryBefore();   // direct instantiation #1
        var sender = new EmailSenderBefore();      // direct instantiation #2
        repo.Save(email);
        sender.Send(email, "Welcome");
    }
}

// ===== AFTER =====

interface IUserRepository
{
    void Save(string email);
}

interface IEmailSender
{
    void Send(string to, string msg);
}

class UserRepository : IUserRepository
{
    public void Save(string email) => Console.WriteLine($"[Repo] saved {email}");
}

class EmailSender : IEmailSender
{
    public void Send(string to, string msg) => Console.WriteLine($"[Mail] {to}: {msg}");
}

class UserServiceAfter
{
    private readonly IUserRepository _repo;
    private readonly IEmailSender    _sender;

    public UserServiceAfter(IUserRepository repo, IEmailSender sender)
    {
        _repo   = repo;
        _sender = sender;
    }

    public void Register(string email)
    {
        _repo.Save(email);
        _sender.Send(email, "Welcome");
    }
}

// ===== Перевірка =====

Console.WriteLine("--- before ---");
new UserServiceBefore().Register("a@b.com");

Console.WriteLine("--- after ---");
var service = new UserServiceAfter(new UserRepository(), new EmailSender());
service.Register("a@b.com");
