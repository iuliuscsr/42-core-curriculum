"""Turns one natural-language prompt into one function call.

The JSON answer is assembled from fixed parts and generated parts:

    {"name": "<CHOICE>", "parameters": {"a": <NUMBER>, "s": "<STRING>"}}

Fixed parts (braces, keys, separators) are appended directly. Each
generated part is decoded by the model under a constraint for its type,
so the result always parses and always matches the function's schema.
"""

from pydantic import BaseModel, ConfigDict

from src.constraints import (
    ChoiceConstraint,
    JsonValue,
    make_value_constraint,
)
from src.decoder import ConstrainedDecoder
from src.models import FunctionCall, FunctionDefinition
from src.prompt_builder import build_context, json_key


class FunctionCaller(BaseModel):
    """Chooses a function and its arguments with the LLM."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    decoder: ConstrainedDecoder
    functions: list[FunctionDefinition]

    def _choose_function(self, input_ids: list[int]) -> tuple[
            FunctionDefinition, str]:
        """Let the model pick a function name among the defined ones.

        Returns the function and the part of the following JSON text
        that is still to be written.
        """
        self.decoder.append_text(input_ids, '{"name": "')
        choice = ChoiceConstraint(
            vocabulary=self.decoder.vocabulary,
            options=[function.name for function in self.functions],
            suffix='"',
            follow=', "parameters": {',
        )
        self.decoder.generate(input_ids, choice)
        chosen = choice.selected()
        function = next(fn for fn in self.functions if fn.name == chosen)
        return function, choice.remaining_follow()

    def _fill_parameters(self, input_ids: list[int],
                         function: FunctionDefinition,
                         pending: str) -> dict[str, JsonValue]:
        """Generate every parameter value in definition order."""
        values: dict[str, JsonValue] = {}
        names = list(function.parameters)
        for index, name in enumerate(names):
            param_type = function.parameters[name].type
            is_last = index == len(names) - 1
            opening = '"' if param_type == "string" else ""
            self.decoder.append_text(
                input_ids, pending + json_key(name) + ": " + opening
            )
            constraint = make_value_constraint(
                param_type, self.decoder.vocabulary,
                follow="}}" if is_last else ", ",
            )
            self.decoder.generate(input_ids, constraint)
            values[name] = constraint.value()
            pending = constraint.remaining_follow()
        return values

    def call(self, prompt: str) -> FunctionCall:
        """Translate prompt into a validated function call record."""
        input_ids = self.decoder.encode(build_context(self.functions, prompt))
        function, pending = self._choose_function(input_ids)
        parameters = self._fill_parameters(input_ids, function, pending)
        return FunctionCall(prompt=prompt, name=function.name,
                            parameters=parameters)
