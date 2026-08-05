#!/usr/bin/env python3
import sys


def main() -> None:
    """Testing user arguments and argument count."""

    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")

    count: int = 1
    if len(sys.argv) < 2:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(sys.argv) - 1}")
        for arg in sys.argv[1:]:
            print(f"Argument {count}: {arg}")
            count += 1

    print(f"Total arguments: {count}")


if __name__ == "__main__":
    main()
