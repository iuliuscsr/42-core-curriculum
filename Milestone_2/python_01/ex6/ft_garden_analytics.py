#!/usr/bin/env python3
class Plant:
    """This is a class of a plant."""

    class Stats:
        """Internal log."""
        def __init__(self) -> None:
            self._grow_count: int = 0
            self._age_count: int = 0
            self._show_count: int = 0
            self._shadow_count: int = 0

        def set_grow_count(self) -> None:
            self._grow_count += 1

        def set_age_count(self) -> None:
            self._age_count += 1

        def set_show_count(self) -> None:
            self._show_count += 1

        def set_shadow_count(self) -> None:
            self._shadow_count += 1

    def __init__(self, name: str, height: float, age: int) -> None:
        """Initializes a new plant."""
        self.name = name
        self.set_height(height, flag=True)
        self.set_age(age, flag=True)
        self._log = self.Stats()

    @staticmethod
    def check_age_is_year(days: int) -> bool:
        """Checks, if given age is older than a year."""
        return (365 < days)

    @classmethod
    def anonymous(cls) -> "Plant":
        """Creates an anonymous plant."""
        return (cls("Unknown Plant", 0.0, 0))

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
        return (self._height)

    def get_age(self) -> int:
        """Returns protected value."""
        return (self._age)

    def grow(self, cm: float) -> None:
        """Adds plant growth."""
        self._height += cm
        self._log.set_grow_count()

    def age(self, days: int = 1) -> None:
        """Adds plant age."""
        self._age += days
        self._log.set_age_count()

    def show_log(self) -> str:
        """Formats stats output-ready."""
        return (f"Stats: {self._log._grow_count} "
                f"grow, {self._log._age_count} age, "
                f"{self._log._show_count} show")

    def show(self) -> str:
        """Formats data output-ready."""
        self._log.set_show_count()
        return (f"{self.name}: "
                f"{self.get_height():.1f}cm, "
                f"{self.get_age()} days old")


class Flower(Plant):
    """This is a class of a flower."""
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        """Initializes a new flower."""
        super().__init__(name, height, age)
        self.color = color
        self.flag: bool = False

    def bloom(self) -> None:
        """Lets flower bloom."""
        self.flag = True

    def show(self) -> str:
        """Formats data output-ready."""
        plant_info = super().show()
        flower_info = f"\nColor: {self.color}\n"
        if self.flag:
            flower_info += f"{self.name} is blooming beautifully!"
        else:
            flower_info += f"{self.name} has not bloomed yet"
        return (plant_info + flower_info)


class Seed(Flower):
    """This is a class for the seeds of a flower."""
    def __init__(self, name: str, height: float,
                 age: int, color: str, seed_amount: int = 0) -> None:
        super().__init__(name, height, age, color)
        self._seed_amount = seed_amount

    def set_seed_amount(self) -> None:
        """Calculates seed amount."""
        seed_constant = 0.00587
        self._seed_amount = round(self.get_height()
                                  * self.get_age() * seed_constant)

    def get_seed_amount(self) -> int:
        """Returns protected value."""
        if self.flag:
            self.set_seed_amount()
        return (self._seed_amount)

    def show(self) -> str:
        """Formats data output-ready."""
        flower_info = super().show()
        seed_info = f"\nSeeds: {self.get_seed_amount()}"
        return (flower_info + seed_info)


class Tree(Plant):
    """This is a class of a tree."""
    def __init__(self, name: str, height: float,
                 age: int, trunk_diameter: float) -> None:
        """Initializes a new tree."""
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter
        self.flag: bool = False

    def produce_shade(self) -> None:
        """Produces shade of a tree with its height and trunk_diameter."""
        self.flag = True
        self._log.set_shadow_count()
        print(f"Tree {self.name} now produces a shade of "
              f"{self._height:.1f}cm long and {self.trunk_diameter}cm wide.")

    def show_log(self) -> str:
        """Formats stats output-ready."""
        stats_info = super().show_log()
        tree_addition = f"\n{self._log._shadow_count} shade"
        return (stats_info + tree_addition)

    def show(self) -> str:
        """Formats data output-ready."""
        flower_info = super().show()
        tree_info = f"\nTrunk diameter: {self.trunk_diameter:.1f}cm"
        return (flower_info + tree_info)


class Vegetable(Plant):
    """This is a class of a Vegetable."""
    def __init__(self, name: str, height: float, age: int,
                 harvest_season: str, nutritional_value: int = 0) -> None:
        """Initializes a new vegetable."""
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def grow(self, cm: float) -> None:
        """Calculates nutritional value and grows the plant."""
        super().grow(cm)
        self.nutritional_value += 1

    def show(self) -> str:
        """Formats data output-ready."""
        plant_info = super().show()
        vegetable_info = (f"\nHarvest season: {self.harvest_season}\n"
                          f"Nutritional value: {self.nutritional_value}")
        return (plant_info + vegetable_info)


def show_log(Plant: Plant) -> None:
    print(Plant.show_log())


if __name__ == "__main__":
    # Executes as main program if not imported.

    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.check_age_is_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.check_age_is_year(400)}")

    print("\n=== Flower")
    Pflanze1 = Flower("Rose", 15.0, 10, "red")
    print(Pflanze1.show())
    print(f"[statistics for {Pflanze1.name}]")
    print(f"{Pflanze1.show_log()}")
    print(f"[asking the {Pflanze1.name} to grow and bloom]")
    Pflanze1.grow(23)
    Pflanze1.bloom()
    print(Pflanze1.show())
    print(f"[statistics for {Pflanze1.name}]")
    print(Pflanze1.show_log())

    print("\n=== Tree")
    Pflanze2 = Tree("Oak", 200.0, 365, 5.0)
    print(Pflanze2.show())
    print(f"[statistics for {Pflanze2.name}]")
    print(Pflanze2.show_log())
    print(f"[asking the {Pflanze2.name} to produce shadow]")
    Pflanze2.produce_shade()
    print(f"[statistics for {Pflanze2.name}]")
    print(Pflanze2.show_log())

    print("\n=== Seed")
    Pflanze3 = Seed("Sunflower", 80.0, 45, "yellow")
    print(Pflanze3.show())
    print(f"[make {Pflanze3.name} grow, age and bloom]")
    Pflanze3.grow(30)
    Pflanze3.age(20)
    Pflanze3.bloom()
    print(Pflanze3.show())
    print(f"[statistics for {Pflanze3.name}]")
    print(Pflanze3.show_log())

    print("\n=== Anonmymous")
    Pflanze4 = Plant.anonymous()
    print(f"{Pflanze4.show()}")
    print(f"[statistics for {Pflanze4.name}]")
    show_log(Pflanze4)
