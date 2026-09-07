#!/usr/bin/env python3
from collections.abc import Callable
import functools
import time
from typing import Any


def spell_timer(func: Callable[[], str]) -> Callable[[], str]:

    @functools.wraps(func)
    def wrapper() -> str:
        print(f"Casting {func.__name__}...")
        start_time: float = time.time()
        result: str = func()
        elapsed_time: float = time.time() - start_time
        print(f"Spell completed in {elapsed_time:.3f} seconds")
        return result
    return wrapper


def power_validator(
        min_power: int
        ) -> Callable[[Callable[..., str]], Callable[..., str]]:

    def decorator(func: Callable[..., str]) -> Callable[..., str]:

        @functools.wraps(func)
        def wrapper(*args: Any) -> str:

            if len(args) > 1 and not isinstance(args[0], int):
                power = args[1]
            else:
                power = args[0]

            if power >= min_power:
                return func(*args)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(
        max_attempts: int
        ) -> Callable[[Callable[..., str]], Callable[..., str]]:

    def decorator(func: Callable[..., str]) -> Callable[..., str]:

        @functools.wraps(func)
        def wrapper(*args: Any) -> str:

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args)
                except Exception:
                    if attempt < max_attempts:
                        print(
                            f"Spell failed, retrying... "
                            f"(attempt {attempt}/{max_attempts})"
                            )
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(c.isalpha() or c.isspace() for c in name)

    @power_validator(min_power=10)
    def cast_spell(self, power: int, spell_name: str) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball() -> str:
    time.sleep(3)
    return "Fireball cast!"


@retry_spell(max_attempts=3)
def unstable_spell(should_fail: bool) -> str:
    if should_fail:
        raise ValueError("Magic overload!")
    return "Wingardium Leviosa!!"


def main() -> None:

    test_powers = [14, 26, 19, 28]
    spell_names = ['fireball', 'freeze', 'heal', 'blizzard']
    mage_names = ['Morgan', 'River', 'Ash', 'Kai', 'Ember', 'Rowan']
    invalid_names = ['Jo', 'A', 'Alex123', 'Test@Name']

    print("==== Master's Tower Operations ====\n")

    print("--- 1. Testing spell_timer ---")
    timer_result: str = fireball()
    print(f"Result: {timer_result}\n")

    print("--- 2. Testing retry_spell ---")
    print("Testing failing spell:")
    print(unstable_spell(True))
    print("\nTesting successful spell:")
    print(unstable_spell(False))
    print()

    print("--- 3. Testing validate_mage_name ---")
    print("Valid Mage Names:")
    for name in mage_names:
        is_valid: bool = MageGuild.validate_mage_name(name)
        print(f"  '{name:6}': {is_valid}")

    print("\nInvalid Mage Names:")
    for name in invalid_names:
        is_valid = MageGuild.validate_mage_name(name)
        print(f"  '{name:9}': {is_valid}")
    print()

    print("--- 4. Testing cast_spell with power_validator (min_power=20) ---")
    guild: MageGuild = MageGuild()
    for power, spell in zip(test_powers, spell_names):
        result: str = guild.cast_spell(power, spell)
        print(f"  Power {power} for '{spell:8}': {result}")

    print("\n=================================")


if __name__ == "__main__":
    main()
