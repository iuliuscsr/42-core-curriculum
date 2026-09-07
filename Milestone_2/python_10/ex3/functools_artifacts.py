#!/usr/bin/env python3
from collections.abc import Callable
from typing import Any
import functools
import operator


def spell_reducer(spells: list[int], operation: str) -> int:

    if not spells:
        return 0
    ops: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min
    }
    if operation not in ops:
        raise ValueError(f"Unknown operation: {operation}")
    return functools.reduce(ops[operation], spells)


def partial_enchanter(
        base_enchantment: Callable[[int, str, str], str]
        ) -> dict[str, Callable[[str], str]]:

    return {
        "fire": functools.partial(base_enchantment, 50, "fire"),
        "water": functools.partial(base_enchantment, 50, "water"),
        "air": functools.partial(base_enchantment, 50, "air"),
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:

    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n in (0, 1):
        return n

    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:

    @functools.singledispatch
    def dispatch(spell: Any) -> str:
        return "Unknown spell type"

    @dispatch.register(int)
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @dispatch.register(str)
    def _(entchantment: str) -> str:
        return f"Enchantment: {entchantment}"

    @dispatch.register(list)
    def _(multi_cast: list[str]) -> str:
        return f"Multi-cast {len(multi_cast)} spells"

    return dispatch


def base_enchant_spell(power: int, element: str, target: str) -> str:
    """Helper base enchantment function for testing."""
    return f"Enchanted {target} with {power} {element} power!"


def main() -> None:
    print("==== Ancient Library Operations ====\n")

    spell_powers = [35, 47, 22, 38, 45, 45]
    operations = ['add', 'multiply', 'max', 'min']
    fibonacci_tests = [19, 17, 16]

    print("Testing spell_reducer:")
    print(f"  Base Powers: {spell_powers}")
    for op in operations:
        res_int: int = spell_reducer(spell_powers, op)
        print(f"  Operation '{op:<8}': {res_int}")
    print(f"  Empty List Test : {spell_reducer([], 'add')}")

    print("\n---------------------------------")
    print("Testing partial_enchanter:")
    enchanters = partial_enchanter(base_enchant_spell)
    for elem, ench_func in enchanters.items():
        res_str: str = ench_func("Dragon")
        print(f"  {elem.capitalize():9} Enchanter -> {res_str}")

    print("\n---------------------------------")
    print("Testing memoized_fibonacci:")
    for n in fibonacci_tests:
        res_int = memoized_fibonacci(n)
        print(f"  Fib({n:<2}): {res_int}")
    print(f"  Cache Info: {memoized_fibonacci.cache_info()}")

    print("\n---------------------------------")
    print("Testing spell_dispatcher:")
    dispatcher = spell_dispatcher()
    dispatcher_tests = [
        42,
        "Fireball",
        ["fireball", "heal", "shield"],
        3.14
    ]
    for test in dispatcher_tests:
        res = dispatcher(test)
        print(f"  Input ({type(test).__name__:<4}): {res}")

    print("\n=================================")


if __name__ == "__main__":
    main()
