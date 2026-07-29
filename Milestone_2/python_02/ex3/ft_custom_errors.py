#!/usr/bin/env python3

class GardenError(Exception):
    """Defines new Error class inheriting from Exception."""
    def __init__(self, err: str = "Unknown garden error") -> None:
        super().__init__(err)


class PlantError(GardenError):
    """Defines new Error class inheriting from GardenError."""
    def __init__(self, err: str = "Unknown plant error") -> None:
        super().__init__(err)


class WaterError(GardenError):
    """Defines new Error class inheriting from GardenError."""
    def __init__(self, err: str = "Unknown water error") -> None:
        super().__init__(err)


def raise_plant_error() -> None:
    """Raises plant error."""
    raise PlantError("The tomato plant is wilting!")


def raise_water_error() -> None:
    """Raises water error."""
    raise WaterError("Not enough water in the tank!")


def test_custom_error_types() -> None:
    """Checks custom errors."""
    print("Testing PlantError...")
    try:
        raise_plant_error()
    except PlantError as err:
        print(f"Caught PlantError: {err}")

    print("\nTesting WaterError...")
    try:
        raise_water_error()
    except WaterError as err:
        print(f"Caught WaterError: {err}")

    print("\nTesting catching all garden errors...")
    try:
        raise_plant_error()
    except GardenError as err:
        print(f"Caught GardenError: {err}")
    try:
        raise_water_error()
    except GardenError as err:
        print(f"Caught GardenError: {err}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===\n")
    test_custom_error_types()
    print("\nAll custom error types work correctly!")
