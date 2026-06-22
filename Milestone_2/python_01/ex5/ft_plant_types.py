#!/usr/bin/env python3
class Plant:
    """This is a class of a plant."""
    def __init__(self, name: str, height: float, age: int) -> None:
        """Initializes a new plant."""
        self.name = name
        self.set_height(height, flag=True)
        self.set_age(age, flag=True)

    def set_height(self, height: float, flag: bool = False) -> None:
        """Protects data from wrong parameters."""

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
        """Protects data from wrong parameters."""
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
        """Returns protected value."""
        return self._height

    def get_age(self) -> int:
        """Returns protected value."""
        return self._age

    def grow(self, cm: float) -> None:
        """Adds plant growth."""
        self._height += cm

    def age(self, days: int = 1) -> None:
        """Adds plant age."""
        self._age += days

    def show(self) -> None:
        """Formats data output-ready."""
        print(f"{self.name}: "
              f"{self._height:.1f}cm, "
              f"{self._age} days old")


class Flower(Plant):
    """This is a class of a flower."""
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        """Initializes a new flower."""
        super().__init__(name, height, age)
        self.color = color
        self.flag: bool = False

    def bloom(self) -> None:
        self.flag = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self.color}")
        if self.flag:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    """This is a class of a tree."""
    def __init__(self, name: str, height: float,
                 age: int, trunk_diameter: float) -> None:
        """Initializes a new tree."""
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter
        self.flag: bool = False

    def produce_shade(self) -> None:
        self.flag = True
        print(f"Tree {self.name} now produces a shade of "
              f"{self._height:.1f}cm long and {self.trunk_diameter}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self.trunk_diameter:.1f}cm")


class Vegetable(Plant):
    """This is a class of a Vegetable."""
    def __init__(self, name: str, height: float, age: int,
                 harvest_season: str, nutritional_value: int = 0) -> None:
        """Initializes a new vegetable."""
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def grow(self, cm: float) -> None:
        super().grow(cm)
        self.nutritional_value += 1

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self.harvest_season}\n"
              f"Nutritional value: {self.nutritional_value}")


if __name__ == "__main__":
    # Executes as main program if not imported.

    print("=== Garden Plant Types ===")
    plant1 = Flower("Rose", 10, 10, "red")
    print("=== Flower ===")
    plant1.show()
    print(f"[asking the {plant1.name} to bloom]")
    plant1.bloom()
    plant1.show()
    print("")

    plant2 = Tree("Oak", 200.0, 365, 5.0)
    print("=== Tree ===")
    plant2.show()
    print(f"[asking the {plant2.name} to produce shade]")
    plant2.produce_shade()
    print("")

    plant3 = Vegetable("Tomato", 5.0, 10, "April")
    print("=== Vegetable ===")
    plant3.show()
    print(f"[make {plant3.name} grow and age for 20 days]")
    for x in range(20):
        plant3.grow(2.1)
        plant3.age(1)
    plant3.show()
    print("")
