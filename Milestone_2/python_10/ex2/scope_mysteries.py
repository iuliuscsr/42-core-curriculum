#!/usr/bin/env python3
from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable[[], int]:
    count: int = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total_power = initial_power

    def accumulator(amount: int) -> int:
        nonlocal total_power
        total_power += amount
        return total_power

    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:

    def factory(item: str) -> str:
        return f"{enchantment_type} {item}"

    return factory


def memory_vault() -> dict[str, Callable[..., Any]]:
    vault: dict[str, Any] = {}

    def store(key: str, value: int) -> None:
        vault[key] = value

    def recall(key: str) -> Any:
        return vault.get(key, "Memory not found")

    return {
        "store": store,
        "recall": recall
    }


def main() -> None:
    print("==== Memory Depths Operations ====\n")

    initial_powers = [70, 30, 39]
    power_additions = [13, 6, 8, 7, 7]
    enchantment_types = ["Earthen", "Shocking", "Flaming"]
    items_to_enchant = ["Ring", "Wand", "Sword", "Shield"]

    print("Testing mage_counter:")
    counter_a = mage_counter()
    counter_b = mage_counter()

    print(f"  Counter A call 1: {counter_a()}")
    print(f"  Counter A call 2: {counter_a()}")
    print(f"  Counter B call 1: {counter_b()}")
    print(f"  Counter A call 3: {counter_a()}")

    print("\n---------------------------------")
    base_power = initial_powers[0]
    print(f"Testing spell_accumulator (Base {base_power}):")
    acc = spell_accumulator(base_power)
    for add in power_additions:
        res_int = acc(add)
        print(f"  Added {add:2} -> Total Power: {res_int}")

    print("\n---------------------------------")
    print("Testing enchantment_factory:")
    for ench, item in zip(enchantment_types, items_to_enchant):
        factory = enchantment_factory(ench)
        res_str: str = factory(item)
        print(f"  {item:6} + {ench:8} -> Result: {res_str}")

    print("\n---------------------------------")
    print("Testing memory_vault:")
    vault = memory_vault()
    store = vault["store"]
    recall = vault["recall"]

    print("  Storing 'initial_power' = 70...")
    store("initial_power", initial_powers[0])
    print(f"  Storing 'enchantment'   = '{enchantment_types[2]}'...\n")
    store("enchantment", enchantment_types[2])

    print(f"  Recall 'initial_power': {recall('initial_power')}")
    print(f"  Recall 'enchantment':   {recall('enchantment')}")
    print(f"  Recall 'unknown':       {recall('unknown')}")

    print("\n=================================")


if __name__ == "__main__":
    main()
