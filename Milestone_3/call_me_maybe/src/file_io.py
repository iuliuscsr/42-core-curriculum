"""Loading and validating the input files, writing the output file."""

import json
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from src.models import FunctionCall, FunctionDefinition, PromptItem


def warn(message: str) -> None:
    """Print a warning to stderr."""
    print(f"[warning] {message}", file=sys.stderr)


def read_json_list(path: Path, label: str) -> list[Any]:
    """Read a JSON file whose top-level value must be an array.

    Raises:
        ValueError: if the file is missing, unreadable, not valid JSON
            or not a JSON array. The message is meant for the user.
    """
    try:
        with path.open("r", encoding="utf-8") as handle:
            data: Any = json.load(handle)
    except FileNotFoundError:
        raise ValueError(f"{label} file not found: {path}") from None
    except IsADirectoryError:
        raise ValueError(f"{label} path is a directory: {path}") from None
    except PermissionError:
        raise ValueError(f"no permission to read {label} file: {path}") \
            from None
    except UnicodeDecodeError:
        raise ValueError(f"{label} file is not valid UTF-8: {path}") from None
    except json.JSONDecodeError as err:
        raise ValueError(
            f"{label} file contains invalid JSON ({path}, line {err.lineno},"
            f" column {err.colno}): {err.msg}"
        ) from None
    except OSError as err:
        raise ValueError(f"cannot read {label} file {path}: {err}") from None
    if not isinstance(data, list):
        raise ValueError(f"{label} file must contain a JSON array: {path}")
    return data


def _short_error(err: ValidationError) -> str:
    """Condense a pydantic error into a single readable line."""
    first = err.errors()[0]
    location = ".".join(str(part) for part in first["loc"]) or "entry"
    return f"{location}: {first['msg']}"


def load_functions(path: Path) -> list[FunctionDefinition]:
    """Load function definitions, skipping invalid or duplicate entries.

    Raises:
        ValueError: if the file is unusable or holds no valid function.
    """
    functions: list[FunctionDefinition] = []
    seen: set[str] = set()
    for index, raw in enumerate(read_json_list(path, "functions definition")):
        try:
            function = FunctionDefinition.model_validate(raw)
        except ValidationError as err:
            warn(f"skipping function #{index}: {_short_error(err)}")
            continue
        if function.name in seen:
            warn(f"skipping duplicate function '{function.name}'")
            continue
        seen.add(function.name)
        functions.append(function)
    if not functions:
        raise ValueError(f"no valid function definition found in {path}")
    return functions


def load_prompts(path: Path) -> list[PromptItem]:
    """Load the prompts to process, skipping invalid entries.

    Raises:
        ValueError: if the file itself is unusable.
    """
    prompts: list[PromptItem] = []
    for index, raw in enumerate(read_json_list(path, "input")):
        try:
            prompts.append(PromptItem.model_validate(raw))
        except ValidationError as err:
            warn(f"skipping prompt #{index}: {_short_error(err)}")
    return prompts


def write_results(path: Path, results: list[FunctionCall]) -> None:
    """Write the results as a JSON array, creating parent directories.

    Raises:
        ValueError: if the file cannot be written.
    """
    payload = [result.model_dump() for result in results]
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False,
                      allow_nan=False)
            handle.write("\n")
    except (OSError, ValueError) as err:
        raise ValueError(f"cannot write output file {path}: {err}") from None
