#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import TypeGuard, Protocol
from ex1.capabilities import HealCapability, TransformCapability
from ex0.champions import Champion


class InvalidStrategyError(Exception):
    pass


class AgressiveChampion(Protocol):
    def attack(self) -> str:
        ...

    def transform(self) -> str:
        ...

    def revert(self) -> str:
        ...


class DefensiveChampion(Protocol):
    def attack(self) -> str:
        ...

    def heal(self) -> str:
        ...


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, champion: Champion) -> bool:
        pass

    @abstractmethod
    def act(self, champion: Champion) -> str:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, champion: Champion) -> bool:
        return isinstance(champion, Champion)

    def act(self, champion: Champion) -> str:
        if not self.is_valid(champion):
            raise InvalidStrategyError(
                f"Battle error, aborting tournament: "
                f"Invalid Champion '{champion.name}' for this normal strategy."
                )
        return champion.attack()


class AgressiveStrategy(BattleStrategy):
    def is_valid(self, champion: Champion) -> TypeGuard[AgressiveChampion]:
        return isinstance(champion, TransformCapability)

    def act(self, champion: Champion) -> str:
        if not self.is_valid(champion):
            raise InvalidStrategyError(
                f"Battle error, aborting tournament: "
                f"Invalid Champion '{champion.name}' for "
                f"this agressive strategy."
                )
        return (
            champion.transform() + "\n" +
            champion.attack() + "\n" +
            champion.revert() + "\n"
        )


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, champion: Champion) -> TypeGuard[DefensiveChampion]:
        return isinstance(champion, HealCapability)

    def act(self, champion: Champion) -> str:
        if not self.is_valid(champion):
            raise InvalidStrategyError(
                f"Battle error, aborting tournament: "
                f"Invalid Champion '{champion.name}' for this "
                f"defensive strategy."
                )
        return (
            champion.attack() + "\n" +
            champion.heal() + "\n"
        )
