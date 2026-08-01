#!/usr/bin/env python3
import random


TOTAL_ACHIEV: list[str] = [
    'Crafting Genius', 'World Savior', 'Boss Slayer',
    'Collector Supreme', 'Untouchable', 'Strategist',
    'Speed Runner', 'First Steps', 'Treasure Hunter',
    'Unstoppable', 'Master Explorer', 'Sharp Mind',
    'Hidden Path Finder', 'Survivor']


def gen_player_achievements() -> set[str]:
    """Generates an achievement set for a player."""
    return set(random.sample(TOTAL_ACHIEV, random.randint(5, 9)))


def main() -> None:
    """Displays achievements of different players and their stats."""

    alice: set[str] = gen_player_achievements()
    bob: set[str] = gen_player_achievements()
    charlie: set[str] = gen_player_achievements()
    dylan: set[str] = gen_player_achievements()

    print("=== Achievement Tracker System ===\n")
    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Charlie: {charlie}")
    print(f"Player Dylan: {dylan}\n")

    distinct_achiev: set[str] = set().union(alice, bob, charlie, dylan)
    print(f"All distinct achievements: {distinct_achiev}\n")

    common_achiev: set[str] = set().intersection(alice, bob, charlie, dylan)
    print(f"Common achievements: {common_achiev}\n")

    print(f"Only Alice has: {alice.difference(bob, charlie, dylan)}")
    print(f"Only Bob has: {bob.difference(alice, charlie, dylan)}")
    print(f"Only Charlie has: {charlie.difference(bob, alice, dylan)}")
    print(f"Only Dylan has: {dylan.difference(bob, charlie, alice)}\n")

    print(f"Alice is missing: {distinct_achiev.difference(alice)}")
    print(f"Bob is missing: {distinct_achiev.difference(bob)}")
    print(f"Charlie is missing: {distinct_achiev.difference(charlie)}")
    print(f"Dylan is missing: {distinct_achiev.difference(dylan)}")


if __name__ == "__main__":
    main()
