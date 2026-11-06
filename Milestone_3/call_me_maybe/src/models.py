"""Pydantic data models for the input files and the output records."""

from typing import Literal, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
)

ParamType = Literal["number", "integer", "string", "boolean"]

# A generated argument value. Strict types keep pydantic from coercing
# e.g. True into 1 or 2.0 into "2.0" when the result is validated.
ArgValue = Union[StrictBool, StrictInt, StrictFloat, StrictStr]


class ParameterSpec(BaseModel):
    """Type description of one function parameter or return value."""

    model_config = ConfigDict(extra="ignore")

    type: ParamType


class FunctionDefinition(BaseModel):
    """One callable function as described in the definitions file."""

    model_config = ConfigDict(extra="ignore")

    name: str = Field(min_length=1, pattern=r'^[^"\\\x00-\x1f]+$')
    description: str = ""
    parameters: dict[str, ParameterSpec] = Field(default_factory=dict)
    returns: ParameterSpec | None = None


class PromptItem(BaseModel):
    """One natural-language request from the tests file."""

    model_config = ConfigDict(extra="ignore")

    prompt: str


class FunctionCall(BaseModel):
    """One output record: the prompt and the function call chosen for it."""

    model_config = ConfigDict(extra="forbid")

    prompt: str
    name: str
    parameters: dict[str, ArgValue]
