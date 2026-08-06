#!/usr/bin/env python3
import sys
import typing


def edit_file() -> None:
    """Opens and reads user given file."""

    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return
    file: typing.Optional[typing.IO[str]] = None
    content: str = ""
    try:
        file = open(sys.argv[1], "r")
        print(f"Accessing file '{sys.argv[1]}'")
        content = file.read()
        print("---\n")
        print(content)
        print("\n---")
    except Exception as err:
        print(f"Error opening file '{sys.argv[1]}': {err}")
        return
    finally:
        if file is not None:
            file.close()
            print(f"File '{sys.argv[1]}' closed.\n")
    transform_file(content)


def transform_file(content: str) -> None:
    """Edits and reads user given file."""

    lines: list[str] = content.splitlines()
    new_content: str = "\n".join(line + "#" for line in lines) + "\n"
    print("Transform data:")
    print("---\n")
    print(new_content)
    print("---")

    file: typing.Optional[typing.IO[str]] = None
    file_name: str = input("Enter new file name (or empty): ")
    if not file_name:
        print("Not saving data.")
        return

    try:
        print(f"Saving data to '{file_name}'")
        file = open(file_name, "w")
        file.write(new_content)
        print(f"Data saved in file '{file_name}'.")
    except Exception as err:
        print(f"Error saving file '{file_name}': {err}")
    finally:
        if file is not None:
            file.close()


def main() -> None:
    print("=== Cyber Archives Recovery & Preservation ===")
    edit_file()


if __name__ == "__main__":
    main()
