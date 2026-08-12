#!/usr/bin/env python3
def main() -> None:
    print("=== Kaboom 1 ===")
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    from alchemy.grimoire.dark_spellbook import dark_spell_record
    print(f"Testing record light spell: "
          f"{dark_spell_record('Fantasy', 'Earth, wind and fire')}")


if __name__ == "__main__":
    main()
