"""Builds the text context the model sees before it writes the call.

The prompt only helps the model to choose well; the structure of the
output is guaranteed by constrained decoding, not by these instructions.
"""

import json

from src.models import FunctionDefinition

# Qwen3 chat markers. The empty <think> block switches off the
# "thinking" mode so the answer starts right away.
_SYSTEM_START = "<|im_start|>system\n"
_USER_START = "<|im_start|>user\n"
_ASSISTANT_START = "<|im_start|>assistant\n<think>\n\n</think>\n\n"
_TURN_END = "<|im_end|>\n"

_INSTRUCTIONS = """\
You translate a user request into exactly one function call.
Pick the function that best matches the request and fill in its \
arguments with values taken from the request.
Answer with a JSON object: {"name": <function name>, \
"parameters": {<argument name>: <value>, ...}}.
Rules:
- numbers are written as JSON numbers, e.g. 42 or 3.5
- string arguments copy the text from the request without the \
surrounding quotes
- regular expressions are written in JSON string syntax, e.g. "[0-9]+"

Example: for the function fn_multiply(x: number, y: number) and the \
request "Multiply 7 by 6" the answer is \
{"name": "fn_multiply", "parameters": {"x": 7, "y": 6}}

Available functions:
"""


def function_signature(function: FunctionDefinition) -> str:
    """One-line description, e.g. 'fn_greet(name: string) -> string'."""
    params = ", ".join(f"{name}: {spec.type}"
                       for name, spec in function.parameters.items())
    line = f"- {function.name}({params})"
    if function.returns is not None:
        line += f" -> {function.returns.type}"
    if function.description:
        line += f": {function.description}"
    return line


def build_context(functions: list[FunctionDefinition], prompt: str) -> str:
    """Chat-formatted context ending where the JSON answer begins."""
    signatures = "\n".join(function_signature(fn) for fn in functions)
    return (
        _SYSTEM_START + _INSTRUCTIONS + signatures + "\n" + _TURN_END
        + _USER_START + prompt + "\n" + _TURN_END
        + _ASSISTANT_START
    )


def json_key(name: str) -> str:
    """A parameter name as a JSON object key, quotes escaped."""
    return json.dumps(name, ensure_ascii=False)
