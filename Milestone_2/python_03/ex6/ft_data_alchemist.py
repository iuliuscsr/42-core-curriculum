#!/usr/bin/env python3
import random


PLAYERS: list[str] = ['Alice', 'bob', 'Charlie', 'dylan',
                      'Emma', 'Gregory', 'john', 'kevin', 'Liam']


def main() -> None:

    cap_names: list[str] = [name.capitalize() for name in PLAYERS]
    cap_names_only: list[str] = [name for name in PLAYERS if name.istitle()]
    cap_names_dic: dict[str, int] = {
        name: random.randint(0, 1000) for name in cap_names}
    avg_score: float = sum(
        cap_names_dic[name] for name in cap_names_dic) / len(cap_names)
    cap_names_dic_avg: dict[str, int] = {
        name: cap_names_dic[name] for name in cap_names_dic
        if cap_names_dic[name] > avg_score}

    print("=== Game Data Alchemist ===\n")
    print(f"Initial list of players: {PLAYERS}")
    print(f"New list with all names capitalized: {cap_names}")
    print(f"New list of capitalized names only: {cap_names_only}")
    print(f"Score dict: {cap_names_dic}")
    print(f"Score average is {round(avg_score, 2)}")
    print(f"High scores: {cap_names_dic_avg}")


if __name__ == "__main__":
    main()
