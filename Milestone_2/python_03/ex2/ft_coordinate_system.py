#!/usr/bin/env python3
import math


def get_player_pos() -> tuple[float, float, float]:
    """Asks user to input pos."""

    while True:
        string = input("Enter new coordinates as floats in format 'x,y,z': ")
        split_str = string.split(',')

        if len(split_str) != 3:
            print("Invalid syntax")
            continue
        try:
            x: float = float(split_str[0])
            y: float = float(split_str[1])
            z: float = float(split_str[2])
            player_pos: tuple[float, float, float] = (x, y, z)
            return player_pos
        except ValueError as err:
            print(f"Error on parameter: {err}")


def display_pos1(pos1: tuple[float, float, float]) -> None:
    """Displays given pos1."""

    print(f"Got a first tuple: {pos1}\nIt includes: X={pos1[0]}, "
          f"Y={pos1[1]}, Z={pos1[2]}")
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    print(f"Distance to center: {calculate_pos(pos1, origin)}")


def display_pos2(pos1: tuple[float, float, float],
                 pos2: tuple[float, float, float]) -> None:
    """Displays given pos2."""

    res: float = calculate_pos(pos1, pos2)
    print(f"Distance between the 2 sets of coordinates: {res}")


def calculate_pos(pos1: tuple[float, float, float],
                  pos2: tuple[float, float, float]) -> float:
    """Calculates distance between two pos."""
    return round(math.sqrt((pos2[0]-pos1[0])**2 +
                           (pos2[1]-pos1[1])**2 + (pos2[2]-pos1[2])**2), 4)


def main() -> None:
    print("=== Game Coordinate System ===\n")
    print("Get a first set of coordinates")
    pos1: tuple[float, float, float] = get_player_pos()
    display_pos1(pos1)
    print("\nGet a second set of coordinates")
    pos2: tuple[float, float, float] = get_player_pos()
    display_pos2(pos1, pos2)


if __name__ == "__main__":
    main()
