#!/usr/bin/env python3
from collections.abc import Callable


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage."


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} hitpoints."


def is_strong_enough(target: str, power: int) -> bool:
    return power >= 15


def spell_combiner(
        spell1: Callable[[str, int], str],
        spell2: Callable[[str, int], str]
        ) -> Callable[[str, int], tuple[str, str]]:
    def combined_spell(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combined_spell


def power_amplifier(
        base_spell: Callable[[str, int], str],
        multiplier: int
        ) -> Callable[[str, int], str]:

    def amplified_spell(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified_spell


def conditional_caster(
        condition: Callable[[str, int], bool],
        spell: Callable[[str, int], str]
        ) -> Callable[[str, int], str]:
    def conditional_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return conditional_spell


def spell_sequence(
        spells: list[Callable[[str, int], str]]
        ) -> Callable[[str, int], list[str]]:
    def cast_spells(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return cast_spells


def main() -> None:
    print("==== Higher Realm Magic Operations ====\n")

    test_values = [12, 8, 20]
    test_targets = ["Dragon", "Goblin", "Wizard", "Knight"]

    print("Testing spell_combiner:")
    combined = spell_combiner(fireball, heal)
    for target in test_targets:
        res_tuple = combined(target, test_values[0])
        print(f"  {target} (Power {test_values[0]}): {res_tuple}")

    print("\n---------------------------------")
    print("Testing power_amplifier (Multiplier x3):")
    mega_fireball = power_amplifier(fireball, 3)
    target = test_targets[0]
    for val in test_values:
        print(f"  {target} (Base {val}): {mega_fireball(target, val)}")

    print("\n---------------------------------")
    print("Testing conditional_caster (Condition: power >= 15):")
    guarded_spell = conditional_caster(is_strong_enough, fireball)
    for target, val in zip(test_targets, test_values + [18]):
        res_str = guarded_spell(target, val)
        print(f"  {target:<8} (Power {val:<2}): {res_str}")

    print("\n---------------------------------")
    print("Testing spell_sequence:")
    spell_chain = spell_sequence([fireball, heal])
    for target in test_targets:
        seq_res = spell_chain(target, test_values[1])
        print(f"  {target:<8}: {seq_res}")

    print("\n=================================")


if __name__ == "__main__":
    main()
