#!/usr/bin/env python3
class Plant:
    """This is a class of a plant."""
    def __init__(self, name: str, height: float, age: int) -> None:
        """Initializes a new plant"""
        self.name = name
        self._height = height
        self._age = age

    def grow(self, cm: float) -> None:
        """Adds plant growth."""
        self._height += cm

    def age(self, days: int = 1) -> None:
        """Adds plant age."""
        self._age += days

    def show(self) -> str:
        """Formats data output-ready."""
        return (f"{self.name}: "
                f"{self._height:.1f}cm, "
                f"{self._age} days old")


def simulate_growth(plant: Plant, days: int, growth: float) -> None:
    """Simulates the growth of a plant."""
    i: int = 0

    print("=== Garden Plant Growth ===")
    while (i < days):
        print(f"=== Day {i + 1} ===")
        print(plant.show())
        plant.grow(growth)
        plant.age()
        print(f"{plant._height:.1f}\n"
              f"{plant._age}")
        i += 1
    print(f"Growth this week: {round(i * growth)}cm")


if __name__ == "__main__":
    # executes as main program if not imported
    plant = Plant("Rose", 25, 30)
    days: int = 7
    growth: float = 0.8

    simulate_growth(plant, days, growth)
