#!/usr/bin/env python3
from ex0.factories import DemaciaFactory, NoxusFactory, ChampionFactory
from ex0.champions import Champion
from ex1.factories import TargonFactory, ShadowIslesFactory
from ex2.battlestrategy import (
    BattleStrategy, NormalStrategy, AgressiveStrategy,
    DefensiveStrategy, InvalidStrategyError)


def battle(opponents: list[tuple[ChampionFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    fighter: list[tuple[Champion, BattleStrategy]] = []
    for factory, strategy in opponents:
        fighter.append((factory.create_base(), strategy))

    for i in range(len(fighter)):
        for j in range(i + 1, len(fighter)):
            champ1, strat1 = fighter[i]
            champ2, strat2 = fighter[j]

            print("\n* Battle *")
            print(champ1.describe())
            print("< VS >")
            print(champ2.describe())
            print("now fight!")
            try:
                print(strat1.act(champ1).strip())
                print(strat2.act(champ2).strip())
            except InvalidStrategyError as err:
                print(f"Battle error, aborting tournament: {err}")
                return


def main() -> None:
    demacia = DemaciaFactory()
    noxus = NoxusFactory()
    targon = TargonFactory()
    shadow_isles = ShadowIslesFactory()

    normal_strat = NormalStrategy()
    defensive_strat = DefensiveStrategy()
    aggressive_strat = AgressiveStrategy()

    print("Tournament 0 (basic)")
    battle([
        (demacia, normal_strat),
        (targon, defensive_strat)
    ])
    print()

    print("Tournament 1 (error)")
    battle([
        (demacia, aggressive_strat),
        (targon, defensive_strat)
    ])
    print()

    print("Tournament 2 (multiple)")
    battle([
        (noxus, normal_strat),
        (targon, defensive_strat),
        (shadow_isles, aggressive_strat)
    ])


if __name__ == "__main__":
    main()
