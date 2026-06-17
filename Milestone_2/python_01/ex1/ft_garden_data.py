#!/usr/bin/env python3
class Plant:
    """this is a class of a plant"""
    def __init__(self, name: str, height: int, age: int) -> None:
        """initializes a new plant"""
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> str:
        """formats data output-ready"""
        return (f"{self.name}: "
                f"{self.height}cm, "
                f"{self.age} days old")


if __name__ == "__main__":
    # executes as main program if not imported
    plant1 = Plant("Rose", 25, 30)
    plant2 = Plant("Sunflower", 80, 45)
    plant3 = Plant("Cactus", 15, 120)

    print("=== Garden Plant Registry ===")
    print(plant1.show())
    print(plant2.show())
    print(plant3.show())
