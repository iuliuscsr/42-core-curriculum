#!/usr/bin/env python3
class Plant:
    """this is a class of a plant"""
    def __init__(self, name: str, height: float, _age: int) -> None:
        """initializes a new plant"""
        self.name = name
        self.height = height
        self._age = _age

    def show(self) -> str:
        """formats data output-ready"""
        return (f"Created: {self.name}: "
                f"{self.height}cm, "
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
