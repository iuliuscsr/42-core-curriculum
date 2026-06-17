#!/usr/bin/env python3
class Plant:
    """this is a class of a plant"""
    def __init__(self, name: str, height: float, age: int) -> None:
        """initializes a new plant"""
        self.name = name
        self.set_height(height, flag=True)
        self.set_age(age, flag=True)

    def set_height(self, height: float, flag: bool = False) -> None:
        """protects data from wrong parameters"""

        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
            if flag:
                self._height = 15.0
        else:
            self._height = height
            if not flag:
                print(f"Height updated: {round(self._height)}cm")

    def set_age(self, age: int, flag: bool = False) -> None:
        """protects data from wrong parameters"""
        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
            print("Age update rejected")
            if flag:
                self._age = 10
        else:
            self._age = age
            if not flag:
                print(f"Age updated: {round(self._age)} days")

    def get_height(self) -> float:
        """returns protected value"""
        return self._height

    def get_age(self) -> int:
        """returns protected value"""
        return self._age

    def show(self) -> str:
        """formats data output-ready"""
        return (f"{self.name}: "
                f"{self._height:.1f}cm, "
                f"{self._age} days old")


if __name__ == "__main__":
    # executes as main program if not imported

    print("=== Garden security system ===")
    plant = Plant("Rose", 10, 10)
    print(f"Plant created: {plant.show()}")
    plant.set_age(30)
    plant.set_age(-5)
    print(f"Current state: {plant.show()}")
