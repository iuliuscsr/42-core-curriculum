#!/usr/bin/env python3

class GardenError(Exception):
    """Defines new Error class inheriting from Exception."""
    def __init__(self, err: str = "Unknown garden error") -> None:
        super().__init__(err)


class PlantError(GardenError):
    """Defines new Error class inheriting from GardenError."""
    def __init__(self, err: str = "Unknown plant error") -> None:
        super().__init__(err)


def water_plant(plant_name: str) -> None:
    """Waters a plant."""
    if plant_name == plant_name.capitalize():
        print(f"Watering {plant_name}: [OK]")
    else:
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")


def test_watering_system() -> None:
    """Tests different valid and invalid plant-names."""
    print("Testing valid plants...")
    print("Opening watering system")
    try:
        water_plant("Tomato")
        water_plant("Lettuce")
        water_plant("Carrots")
    except PlantError as err:
        print(f"Caught PlantError: {err}")
        print(".. ending tests and returning to main")
    finally:
        print("Closing watering system\n")

    print("Testing invalid plants...")
    print("Opening watering system")
    try:
        water_plant("Tomato")
        water_plant("lettuce")
    except PlantError as err:
        print(f"Caught PlantError: {err}")
        print(".. ending tests and returning to main")
    finally:
        print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===\n")
    test_watering_system()
    print("\n Cleanup always happens, even with errors!")
