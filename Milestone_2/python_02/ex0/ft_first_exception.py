#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    """Converts input string into an integer."""
    return (int(temp_str))


def test_temperature() -> None:
    """Checks test cases."""
    test_cases = ["25", "abc"]
    for index in test_cases:
        try:
            print(f"\nInput data is '{index}'")
            temperature = input_temperature(index)
            print(f"Temperature is now {temperature}°C")
        except ValueError as err:
            print(f"Caught input_temperature error: {err}\n")


if __name__ == "__main__":
    print("=== Garden Temperature ===")
    test_temperature()
    print("All tests completed - program didn't crash!")
