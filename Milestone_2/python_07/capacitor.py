#!/usr/bin/env python3
from ex0 import ChampionFactory
from ex1 import TargonFactory, ShadowIslesFactory
from ex1.capabilities import HealCapability, TransformCapability


def test_healing_factory(factory: ChampionFactory) -> None:
    print("==Testing Champion with healing capability==")
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, HealCapability):
        print(base.heal())
    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, HealCapability):
        print(evolved.heal(), "\n")


def test_transforming_factory(factory: ChampionFactory) -> None:
    print("==Testing Champion with transform capability==")
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, TransformCapability):
        print(base.transform())
        print(base.attack())
        print(base.revert())

    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, TransformCapability):
        print(evolved.transform())
        print(evolved.attack())
        print(evolved.revert(), "\n")


def main() -> None:
    factory1 = TargonFactory()
    factory2 = ShadowIslesFactory()
    test_healing_factory(factory1)
    test_transforming_factory(factory2)


if __name__ == "__main__":
    main()
