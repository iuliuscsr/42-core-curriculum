#!/usr/bin/env python3
from ex0.champions import Champion
from ex0.factories import ChampionFactory
from .champions import BaseSoraka, BaseElise, EvolvedSoraka, EvolvedElise


class TargonFactory(ChampionFactory):
    def create_base(self) -> Champion:
        return BaseSoraka()

    def create_evolved(self) -> Champion:
        return EvolvedSoraka()


class ShadowIslesFactory(ChampionFactory):
    def create_base(self) -> Champion:
        return BaseElise()

    def create_evolved(self) -> Champion:
        return EvolvedElise()
