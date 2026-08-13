#!/usr/bin/env python3
from abc import ABC, abstractmethod
from .champions import Champion, BaseDarius, \
                       BaseGaren, EvolvedDarius, EvolvedGaren


class ChampionFactory(ABC):
    @abstractmethod
    def create_base(self) -> Champion:
        pass

    @abstractmethod
    def create_evolved(self) -> Champion:
        pass


class DemaciaFactory(ChampionFactory):
    def create_base(self) -> Champion:
        return BaseGaren()

    def create_evolved(self) -> Champion:
        return EvolvedGaren()


class NoxusFactory(ChampionFactory):
    def create_base(self) -> Champion:
        return BaseDarius()

    def create_evolved(self) -> Champion:
        return EvolvedDarius()
