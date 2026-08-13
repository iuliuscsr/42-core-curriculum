#!/usr/bin/env python3
from ex0.champions import Champion
from .capabilities import HealCapability, TransformCapability


class BaseSoraka(Champion, HealCapability):
    def __init__(self) -> None:
        super().__init__("Soraka", "Targon")

    def attack(self) -> str:
        return f"{self.name} casts Starcall!"

    def heal(self) -> str:
        return f"{self.name} casts Astral Infusion and restores health!"


class EvolvedSoraka(Champion, HealCapability):
    def __init__(self) -> None:
        super().__init__("Soraka (Star Guardian)", "Targon")

    def attack(self) -> str:
        return f"{self.name} casts Equinox, silencing enemies inside!"

    def heal(self) -> str:
        return f"{self.name} casts Wish and heals all allies!"


class BaseElise(Champion, TransformCapability):
    def __init__(self) -> None:
        Champion.__init__(self, "Elise", "Shadow Isles")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.is_transformed:
            return f"{self.name} executes venemous bite!"
        return f"{self.name} injects neurotoxin in Human Form!"

    def transform(self) -> str:
        self.is_transformed = True
        return f"{self.name} transforms into a menacing Spider!"

    def revert(self) -> str:
        self.is_transformed = False
        return f"{self.name} reverts back to Human form!"


class EvolvedElise(Champion, TransformCapability):
    def __init__(self) -> None:
        Champion.__init__(self, "Elise (Spider Queen)", "Shadow Isles")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.is_transformed:
            return f"{self.name} unleashes Frenzied Arachnid in Spider Form!"
        return f"{self.name} casts Volatile Spiderling in Human Form!"

    def transform(self) -> str:
        self.is_transformed = True
        return f"{self.name} transforms into a menacing Spider!"

    def revert(self) -> str:
        self.is_transformed = False
        return f"{self.name} reverts back to Human form!"
