#!/usr/bin/env python3
from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(artifacts, key=lambda item: item["power"], reverse=True)


def power_filter(
    mages: list[dict[str, Any]],
    min_power: int
                ) -> list[dict[str, Any]]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"*{spell}*", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    power_levels = list(map(lambda mage: mage["power"], mages))
    max_power = max(power_levels)
    min_power = min(power_levels)
    avg_power = round(sum(power_levels) / len(mages), 2)

    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": avg_power
    }


def main() -> None:
    print("==== Lambda Spells Operations ====\n")

    provided_artifacts = [
        {'name': 'Lightning Rod', 'power': 79, 'type': 'focus'},
        {'name': 'Ice Wand', 'power': 117, 'type': 'focus'},
        {'name': 'Earth Shield', 'power': 115, 'type': 'armor'},
        {'name': 'Ice Wand', 'power': 89, 'type': 'accessory'}
        ]

    provided_mages = [
        {'name': 'River', 'power': 85, 'element': 'fire'},
        {'name': 'Riley', 'power': 83, 'element': 'light'},
        {'name': 'Ash', 'power': 65, 'element': 'lightning'},
        {'name': 'Jordan', 'power': 86, 'element': 'light'},
        {'name': 'Morgan', 'power': 54, 'element': 'fire'}
        ]

    provided_spells = ['lightning', 'meteor', 'darkness', 'fireball']

    sorted_res = artifact_sorter(provided_artifacts)
    print("Testing artifact sorter (power_level descending):")
    print(f"  All Artifacts: {[a['power'] for a in provided_artifacts]}")
    print(f"  Sorted Res:    {[a['power'] for a in sorted_res]}")

    print("\n---------------------------------")
    min_power = 75
    filtered_res = power_filter(provided_mages, min_power)
    print(f"Testing power filter (min_power >= {min_power}):")
    print(f"  All Mages:      {[m['power'] for m in provided_mages]}")
    print(f"  Filtered Mages: {[m['power'] for m in filtered_res]}")

    print("\n---------------------------------")
    transformed_res = spell_transformer(provided_spells)
    print("Testing spell transformer:")
    print(f"  Original:    {provided_spells}")
    print(f"  Transformed: {transformed_res}")

    print("\n---------------------------------")
    stats_res = mage_stats(provided_mages)
    print("Testing mage stats:")
    print(f"  Max Power: {stats_res['max_power']}")
    print(f"  Min Power: {stats_res['min_power']}")
    print(f"  Avg Power: {stats_res['avg_power']}")

    print("\n=================================")


if __name__ == "__main__":
    main()
