#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    """Converts input string into an integer and checks if it is valid."""
    temperature = int(temp_str)
    if temperature < 0:
        raise ValueError(f"{temperature}°C is too cold for plants (min 0°C)")
    elif temperature > 40:
        raise ValueError(f"{temperature}°C is too hot for plants (max 40°C)")
    return temperature


def test_temperature() -> None:
    """Checks test cases."""
    test_cases = ["25", "abc", "100", "-50"]
    for val in test_cases:
        try:
            print(f"\nInput data is '{val}'")
            temperature = input_temperature(val)
            print(f"Temperature is now {temperature}°C")
        except ValueError as err:
            print(f"Caught input_temperature error: {err}\n")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===")
    test_temperature()
    print("All tests completed - program didn't crash!")
