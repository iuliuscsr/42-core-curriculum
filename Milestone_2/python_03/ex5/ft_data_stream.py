#!/usr/bin/env python3
import random
import typing


PLAYER: list[str] = ['bob', 'alice', 'dylan', 'charlie']
ACTION: list[str] = ['run', 'eat', 'sleep', 'grab',
                     'move', 'climb', 'swim', 'release']


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    """Generates a player and their action."""

    while True:
        event: tuple[str, str] = random.choice(PLAYER), random.choice(ACTION)
        yield event


def consume_event(custom_list: list[tuple[str, str]]
                  ) -> typing.Generator[tuple[str, str], None, None]:
    """Erases a random event from a created list of tuples."""
    while custom_list:
        index: int = random.randrange(len(custom_list))
        event: tuple[str, str] = custom_list[index]
        custom_list[:] = custom_list[:index] + custom_list[index + 1:]
        yield event


def main() -> None:
    """Displays events and event-stats."""

    print("=== Game Data Stream Processor ===")

    stream = gen_event()
    for i in range(1000):
        player, action = next(stream)
        print(f"Event {i}: Player {player} did action {action}")
    custom_list: list[tuple[str, str]] = []

    for _ in range(10):
        custom_list += [next(stream)]
    print(f"Built list of 10 events: {custom_list}")

    stream = consume_event(custom_list)
    for _ in range(10):
        del_event: tuple[str, str] = next(stream)
        print(f"Got event from list: {del_event}")
        print(f"Remains in list: {custom_list}")


if __name__ == "__main__":
    main()
