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


if __name__ == "__main__":
    # executes as main program if not imported

    plant1 = Plant("Rose", 25.0, 30)
    plant2 = Plant("Oak", 200.0, 365)
    plant3 = Plant("Cactus", 5.0, 90)
    plant4 = Plant("Sunflower", 80.0, 45)
    plant5 = Plant("Fern", 15.0, 120)

    print("=== Plant Factory Output ===")
    print(plant1.show())
    print(plant2.show())
    print(plant3.show())
    print(plant4.show())
    print(plant5.show())
