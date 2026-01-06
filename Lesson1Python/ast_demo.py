import ast


code = """
def foo(x):
    return x * 2

print("Hello")
m = max(1, 5, 3)
y = foo(10)
print(m, y)
"""

if __name__ == "__main__":
    tree = ast.parse(code)

    print(tree)
    print("-" * 30)

    print(ast.dump(tree, indent=2))
