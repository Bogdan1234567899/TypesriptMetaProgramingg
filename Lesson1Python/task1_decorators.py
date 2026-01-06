from typing import Any, Callable


def log_call(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"[LOG] Виклик: {func.__name__}")
        print(f"[LOG] args={args}, kwargs={kwargs}")

        result = func(*args, **kwargs)

        print(f"[LOG] Результат: {result}")
        print("-" * 30)
        return result

    return wrapper


@log_call
def add(a: int, b: int) -> int:
    return a + b


@log_call
def multiply(a: int, b: int, c: int = 1) -> int:
    return a * b * c


@log_call
def make_greeting(name: str, city: str = "Kyiv") -> str:
    return f"Привіт, {name}! Місто: {city}"


if __name__ == "__main__":
    add(2, 3)
    multiply(2, 5)
    multiply(2, 5, c=3)
    make_greeting("Олег")
    make_greeting("Іра", city="Львів")
