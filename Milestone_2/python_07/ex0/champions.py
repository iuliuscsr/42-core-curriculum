#!/usr/bin/env python3
from abc import ABC, abstractmethod


class Champion(ABC):
    def __init__(self, name: str, region: str):
        self.name = name
        self.region = region

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self.name} is a Champion from {self.region}"


class BaseGaren(Champion):
    def __init__(self) -> None:
        super().__init__("Garen", "Demacia")

    def attack(self) -> str:
        return f"{self.name} uses Decisive Strike!"


class EvolvedGaren(Champion):
    def __init__(self) -> None:
        super().__init__("Garen (Might of Demacia)", "Demacia")

    def attack(self) -> str:
        return f"{self.name} uses Demacian Justice!"


class BaseDarius(Champion):
    def __init__(self) -> None:
        super().__init__("Darius", "Noxus")

    def attack(self) -> str:
        return f"{self.name} uses Decimate!"


class EvolvedDarius(Champion):
    def __init__(self) -> None:
        super().__init__("Darius (Hand of Noxus)", "Noxus")

    def attack(self) -> str:
        return f"{self.name} uses Noxian Guillotine!"
