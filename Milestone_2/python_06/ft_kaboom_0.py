#!/usr/bin/env python3
import alchemy.grimoire


def main() -> None:
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")
    print(
        "Testing record light spell: "
        + alchemy.grimoire.light_spell_record(
         "Fantasy", "Earth, wind and fire")
    )


if __name__ == "__main__":
    main()
