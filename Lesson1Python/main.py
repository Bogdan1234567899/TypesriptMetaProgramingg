

import runpy


def run(title: str, module_file: str) -> None:
    print("\n" + title)
    runpy.run_path(module_file, run_name="__main__")


if __name__ == "__main__":
    run("TASK 1: decorator log_call", "task1_decorators.py")
    run("TASK 2: dataclass User", "task2_dataclass.py")
    run("TASK 3: Product validation", "task3_product_manual.py")
    run("TASK 4: inspect utils functions", "inspect_demo.py")
    run("TASK 5: ast parse demo", "ast_demo.py")


