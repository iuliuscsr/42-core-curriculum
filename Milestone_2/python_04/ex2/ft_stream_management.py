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
        print(f"[STDERR] Error opening file '{sys.argv[1]}': {err}",
              file=sys.stderr)
        sys.exit(1)
    finally:
        if file is not None:
            file.close()
            print(f"File '{sys.argv[1]}' closed.")


def transform_file(content: str) -> None:
    """Edits and reads user given file."""

    lines: list[str] = content.splitlines()
    new_content: str = "\n".join(line + "#" for line in lines)
    print("\nTransform data:")
    print("---\n")
    print(new_content)
    print("\n---")

    file: typing.IO[str] | None = None
    print("Enter new file name (or empty): ", end="", flush=True)
    file_name: str = sys.stdin.readline().strip()
    if not file_name:
        print("Not saving data.")
        return
    try:
        print(f"Saving data to '{file_name}'")
        file = open(file_name, "w")
        file.write(new_content)
        print(f"Data saved in file '{file_name}'.")
    except Exception as err:
        print(f"[STDERR] Error opening file '{file_name}': {err}",
              file=sys.stderr)
        print("Data not saved.")
    finally:
        if file is not None:
            file.close()


def main() -> None:
    """Displays file operations."""

    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>", file=sys.stderr)
        sys.exit(1)

    print("=== Cyber Archives Recovery & Preservation ===")
    content = open_file()
    transform_file(content)


if __name__ == "__main__":
    main()
