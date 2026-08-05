#!/usr/bin/env python3
import sys


def get_inventory() -> dict[str, int]:
    """Parses input into an inventory dictionary."""

    inventory: dict[str, int] = {}
    for argc in sys.argv[1:]:
        if ':' not in argc:
            print(f"Error - invalid parameter '{argc}'")
            continue
        string: list[str] = argc.split(':', 1)
        item: str = string[0].strip()
        amount_str: str = string[1].strip()
        if item in inventory:
            print(f"Redundant item '{item}' - discarding")
            continue
        try:
            amount = int(amount_str)
            inventory[item] = amount
        except ValueError as err:
            print(f"Quantity error for '{item}': {err}")
    return inventory


def display_inventory_information(inv: dict[str, int]) -> None:
    """Displays multiple inventory stats."""

    if not inv:
        print("Inventory is empty.")
    else:
        print(f"Got inventory: {inv}")
        inv_list: list[str] = list(inv.keys())
        print(f"Item list: {inv_list}")
        print(f"Total quantity of the {len(inv)} items: {sum(inv.values())}")

        name_max = inv_list[0]
        name_min = inv_list[0]
        tot_items = sum(inv.values())

        for item in inv.keys():
            if tot_items > 0:
                percentage: float = round(inv[item] / tot_items * 100, 1)
            else:
                percentage = 0.0
            print(f"Item {item} represents {percentage}%")
            if inv[name_max] < inv[item]:
                name_max = item
            if inv[name_min] > inv[item]:
                name_min = item

        print(f"Item most abundant: {name_max} with quantity {inv[name_max]}")
        print(f"Item least abundant: {name_min} with quantity {inv[name_min]}")
    inv.update({"magic_item": 1})
    print(f"Updated inventory: {inv}")


def main() -> None:
    """Creates and displays inventory."""
    print("=== Inventory System Analysis ===")
    inventory = get_inventory()
    display_inventory_information(inventory)


if __name__ == "__main__":
    main()
