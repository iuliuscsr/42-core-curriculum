#!/usr/bin/env python3
import sys
import typing


def open_file() -> None:
    """Opens and reads user given file."""

    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return
    file: typing.Optional[typing.IO[str]] = None
    try:
        file = open(sys.argv[1], "r")
        print(f"Accessing file '{sys.argv[1]}'")
        print("---\n")
        print(file.read())
        print("\n---")
    except Exception as err:
        print(f"Error opening file '{sys.argv[1]}': {err}")
    finally:
        if file is not None:
            file.close()
            print(f"File '{sys.argv[1]}' closed.")


def main() -> None:
    print("=== Cyber Archives Recovery ===")
    open_file()



if __name__ == "__main__":
    main()
