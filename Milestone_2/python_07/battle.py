#!/usr/bin/env python3
from ex0 import ChampionFactory, DemaciaFactory, NoxusFactory
from ex0.champions import Champion


def test_factory(factory: ChampionFactory) -> None:
    print("==Testing factory==")
    base = factory.create_base()
    evolved = factory.create_evolved()

    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack(), "\n")


def test_battle(base1: Champion, base2: Champion) -> None:
    print("==Testing battle==")
    print(f"{base1.describe()}\n < VS > \n{base2.describe()}\n fight!\n")
    print(base1.attack())
    print(base2.attack())


def main() -> None:
    factory1 = DemaciaFactory()
    factory2 = NoxusFactory()
    test_factory(factory1)
    test_factory(factory2)
    portalmaster1 = factory1.create_base()
    portalmaster2 = factory2.create_base()
    test_battle(portalmaster1, portalmaster2)


if __name__ == "__main__":
    main()
