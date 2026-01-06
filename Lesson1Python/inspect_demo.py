import inspect
import utils


if __name__ == "__main__":
    functions = inspect.getmembers(utils, inspect.isfunction)

    print("Функції в utils.py:")
    for name, _ in functions:
        print("-", name)
