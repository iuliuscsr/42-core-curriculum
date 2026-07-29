#!/usr/bin/env python3

def garden_operations(operation_number: int) -> None:
    """Selects various error types with the indizes 0-3"""
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        5 / 0
    elif operation_number == 2:
        open('/non/existent/file')
    elif operation_number == 3:
        "abc" + 42


def test_error_types() -> None:
    """Checks test cases."""
    for case in range(5):
        print(f"Testing operation {case}...")
        try:
            garden_operations(case)
            print("Operation completed succesfully")
        except ValueError as err:
            print(f"Caught ValueError: {err}")
        except ZeroDivisionError as err:
            print(f"Caught ZeroDivisionError: {err}")
        except FileNotFoundError as err:
            print(f"Caught FileNotFoundError: {err}")
        except TypeError as err:
            print(f"Caught TypeError: {err}")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===")
    test_error_types()
    print("\nAll error types tested successfully!")
