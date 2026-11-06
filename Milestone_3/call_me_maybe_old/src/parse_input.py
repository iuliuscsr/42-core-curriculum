import json
from pathlib import Path
from typing import Any
from pydantic import BaseModel


class FunctionsDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]


def read_allowed_functions() -> list[dict[str, Any]]:
    file_path = Path("data/input/functions_definition.json")
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    else:
        raise FileNotFoundError(f"Allowed functions file not found.: {file_path}")


def read_calling_tests() -> list[dict[str, str]]:
    file_path = Path("data/input/function_calling_tests.json")
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    else:
        raise FileNotFoundError(f"Test input file not found: {file_path}")  


def convert_functions() -> list[FunctionsDefinition]:
    data = read_allowed_functions()
    functions: list[FunctionsDefinition] = [
        FunctionsDefinition.model_validate(item) for item in data
    ]
    return functions

