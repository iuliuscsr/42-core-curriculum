#!/usr/bin/env python3
class Plant:
    """this is a class of a plant"""
    def __init__(self, name: str, height: float, _age: int) -> None:
        """initializes a new plant"""
        self.name = name
        self.height = height
        self._age = _age

    def grow(self, cm: float) -> float:
        """adds plant growth"""
        self.height += cm
        return self.height

    def age(self, days: int = 1) -> int:
        """adds plant age"""
        self._age += days
        return self._age

    def show(self) -> str:
        """formats data output-ready"""
        return (f"{self.name}: "
                f"{self.height:.1f}cm, "
                f"{self._age} days old")


def simulate_growth(plant: Plant, days: int, growth: float) -> None:
    """simulates the growth of a plant"""
    i: int = 0

    print("=== Garden Plant Growth ===")
    while (i < days):
        print(f"=== Day {i + 1} ===")
        print(plant.show())
        plant.grow(growth)
        plant.age()
        i += 1
    print(f"Growth this week: {round(i * growth)}cm")


if __name__ == "__main__":
    # executes as main program if not imported
    plant = Plant("Rose", 25, 30)
    days: int = 7
    growth: float = 0.8

    simulate_growth(plant, days, growth)
