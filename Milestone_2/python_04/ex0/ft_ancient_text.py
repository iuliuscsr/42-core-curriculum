#!/usr/bin/env python3
import sys
import typing


def open_file() -> str:
    """Opens and reads user given file."""

    file: typing.IO[str] | None = None
    try:
        print(f"Accessing file '{sys.argv[1]}'")
        file = open(sys.argv[1], "r")
        content = file.read()
        print("---\n")
        print(content)
        print("\n---")
        return content
    except Exception as err:
        print(f"Error opening file '{sys.argv[1]}': {err}")
        sys.exit(1)
    finally:
        if file is not None:
            file.close()
            print(f"File '{sys.argv[1]}' closed.")


def main() -> None:
    """Displays file operations."""

    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        sys.exit(1)

    print("=== Cyber Archives Recovery ===")
    open_file()


if __name__ == "__main__":
    main()
