"""Token-level constraints for the values the model has to generate.

Each constraint describes one JSON value that is still being written
(the function name, a number, a string, ...). At every decoding step it
answers two questions:

* which tokens may come next (``allowed_mask``), and
* how its state changes once a token was chosen (``advance``).

Every value is followed by a fixed piece of JSON (its ``follow`` text,
e.g. ``", "`` or ``"}}"``). A token may already contain the beginning of
that text - the tokenizer often merges ``"`` and ``,`` into one token -
so constraints accept it and report the part they swallowed in
``consumed``.
"""

import json
import math
import sys
from abc import ABC, abstractmethod
from string import hexdigits
from typing import Iterable

from pydantic import BaseModel, ConfigDict, field_validator

from src.vocabulary import NUMBER_CHARS, BoolMask, TokenVocabulary

JsonValue = bool | int | float | str


class ValueConstraint(BaseModel, ABC):
    """Common state and interface of all value constraints."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    vocabulary: TokenVocabulary
    follow: str
    max_tokens: int = 48
    tokens_used: int = 0
    consumed: str = ""

    @abstractmethod
    def candidate_ids(self) -> Iterable[int]:
        """Token ids worth checking with ``accepts`` at the current step."""

    @abstractmethod
    def accepts(self, text: str) -> bool:
        """True if a token with this text may be appended now."""

    @abstractmethod
    def advance(self, text: str) -> None:
        """Append text (a chosen token or forced text) to the value."""

    @abstractmethod
    def is_complete(self) -> bool:
        """True once the value is finished."""

    @abstractmethod
    def finish_text(self) -> str:
        """Shortest text that turns the current state into a valid value."""

    @abstractmethod
    def value(self) -> JsonValue:
        """The generated value as a Python object."""

    def forced_text(self) -> str | None:
        """Text that is certain to come next, so no model call is needed."""
        return None

    def allowed_mask(self) -> BoolMask:
        """Boolean mask over the vocabulary of the tokens allowed next."""
        mask = self.vocabulary.empty_mask()
        for token_id in self.candidate_ids():
            if self.accepts(self.vocabulary.text(token_id)):
                mask[token_id] = True
        return mask

    def remaining_follow(self) -> str:
        """Part of the follow text that still has to be written."""
        return self.follow[len(self.consumed):]

    def _is_follow_start(self, rest: str) -> bool:
        """True if rest is a non-empty beginning of the follow text."""
        return bool(rest) and self.follow.startswith(rest)


class ChoiceConstraint(ValueConstraint):
    """Value that must be exactly one of a few fixed options.

    Used for the function name (options end with the closing quote) and
    for booleans.
    """

    options: list[str]
    suffix: str = ""
    generated: str = ""

    def _targets(self) -> tuple[str, ...]:
        return tuple(opt + self.suffix + self.follow for opt in self.options)

    def _alive(self) -> list[str]:
        """Options (with suffix) still compatible with the text so far."""
        return [opt + self.suffix for opt in self.options
                if (opt + self.suffix).startswith(self.generated)]

    def _match(self) -> str | None:
        for option in self.options:
            if self.generated.startswith(option + self.suffix):
                return option
        return None

    def candidate_ids(self) -> Iterable[int]:
        return self.vocabulary.ids_inside(self._targets())

    def accepts(self, text: str) -> bool:
        candidate = self.generated + text
        return any(target.startswith(candidate)
                   for target in self._targets())

    def advance(self, text: str) -> None:
        self.generated += text
        option = self._match()
        if option is not None:
            self.consumed = self.generated[len(option + self.suffix):]

    def is_complete(self) -> bool:
        return self._match() is not None

    def forced_text(self) -> str | None:
        """Common prefix of all remaining options, e.g. 'fn_'.

        With a single option left this is the whole rest of it, so the
        model is only asked where the options really differ.
        """
        remainders = [alive[len(self.generated):] for alive in self._alive()]
        if not remainders:
            return None
        prefix = remainders[0]
        for remainder in remainders[1:]:
            while not remainder.startswith(prefix):
                prefix = prefix[:-1]
        return prefix or None

    def finish_text(self) -> str:
        alive = self._alive()
        if alive:
            return alive[0][len(self.generated):]
        raise ValueError("choice constraint reached an impossible state")

    def selected(self) -> str:
        """The chosen option."""
        option = self._match()
        if option is None:
            raise ValueError("choice is not complete yet")
        return option

    def value(self) -> JsonValue:
        return self.selected()


class BooleanConstraint(ChoiceConstraint):
    """JSON boolean: the literal true or false."""

    options: list[str] = ["true", "false"]

    def value(self) -> JsonValue:
        return self.selected() == "true"


# JSON number grammar as a small state machine.
# 0 start, 1 after '-', 2 integer digits, 3 single '0', 4 after '.',
# 5 fraction digits, 6 after 'e', 7 after exponent sign, 8 exponent digits
_NUMBER_ACCEPTING = frozenset({2, 3, 5, 8})


def _number_step(state: int, char: str, integer: bool) -> int | None:
    """Next number-grammar state, or None if char is not allowed here."""
    digit = char.isdigit()
    if state in (0, 1):
        if char == "-" and state == 0:
            return 1
        if digit:
            return 3 if char == "0" else 2
        return None
    if state in (2, 3):
        if digit and state == 2:
            return 2
        if not integer and char == ".":
            return 4
        if not integer and char in "eE":
            return 6
        return None
    if state in (4, 5):
        if digit:
            return 5
        if state == 5 and char in "eE":
            return 6
        return None
    if state == 6 and char in "+-":
        return 7
    if state in (6, 7, 8) and digit:
        return 8
    return None


class NumberConstraint(ValueConstraint):
    """JSON number; ``integer`` forbids fraction and exponent."""

    integer: bool = False
    text: str = ""
    state: int = 0
    done: bool = False

    @field_validator("follow")
    @classmethod
    def _follow_not_empty(cls, follow: str) -> str:
        if not follow:
            raise ValueError("a number needs a follow text to end it")
        return follow

    def _simulate(self, text: str) -> tuple[int, str] | None:
        """Run the grammar over text.

        Returns the new state and the non-number rest of text, or None if
        text breaks the grammar.
        """
        state = self.state
        for index, char in enumerate(text):
            if char not in NUMBER_CHARS:
                return state, text[index:]
            next_state = _number_step(state, char, self.integer)
            if next_state is None:
                return None
            state = next_state
        return state, ""

    def candidate_ids(self) -> Iterable[int]:
        yield from self.vocabulary.number_ids
        for end in range(1, len(self.follow) + 1):
            token_id = self.vocabulary.text_to_id.get(self.follow[:end])
            if token_id is not None:
                yield token_id

    def accepts(self, text: str) -> bool:
        result = self._simulate(text)
        if result is None:
            return False
        state, rest = result
        if not rest:
            return True
        return state in _NUMBER_ACCEPTING and self._is_follow_start(rest)

    def advance(self, text: str) -> None:
        result = self._simulate(text)
        if result is None:
            raise ValueError(f"invalid number continuation {text!r}")
        self.state, rest = result
        self.text += text[:len(text) - len(rest)]
        if rest:
            self.done = True
            self.consumed = rest

    def is_complete(self) -> bool:
        return self.done

    def finish_text(self) -> str:
        padding = "" if self.state in _NUMBER_ACCEPTING else "0"
        return padding + self.follow[0]

    def value(self) -> JsonValue:
        if self.integer:
            return int(self.text)
        number = float(self.text)
        if not math.isfinite(number):
            number = math.copysign(sys.float_info.max, number)
        return number


# String escape states: 0 normal, -1 right after a backslash,
# n > 0 still n hex digits of a \uXXXX escape to read.
_SIMPLE_ESCAPES = frozenset('"\\/bfnrt')


def _string_step(state: int, char: str) -> int | None:
    """Next escape state inside a JSON string, None if invalid."""
    if state == -1:
        if char in _SIMPLE_ESCAPES:
            return 0
        return 4 if char == "u" else None
    if state > 0:
        return state - 1 if char in hexdigits else None
    if char == "\\":
        return -1
    return None if ord(char) < 0x20 else 0


class StringConstraint(ValueConstraint):
    """Content of a JSON string; the opening quote is already written.

    The value ends with the first unescaped quote.
    """

    max_tokens: int = 96
    content: str = ""
    state: int = 0
    done: bool = False

    def _simulate(self, text: str) -> tuple[int, int | None] | None:
        """Run text through the string grammar.

        Returns the new escape state and the index of the closing quote
        (None if the string stays open), or None if text is invalid.
        """
        state = self.state
        for index, char in enumerate(text):
            if state == 0 and char == '"':
                return state, index
            next_state = _string_step(state, char)
            if next_state is None:
                return None
            state = next_state
        return state, None

    def candidate_ids(self) -> Iterable[int]:
        if self.state == 0:
            return self.vocabulary.string_special_ids
        starts = _SIMPLE_ESCAPES | {"u"} if self.state == -1 \
            else frozenset(hexdigits)
        return [token_id for char in starts
                for token_id in self.vocabulary.ids_by_first_char.get(char,
                                                                      [])]

    def accepts(self, text: str) -> bool:
        result = self._simulate(text)
        if result is None:
            return False
        _, close = result
        return close is None or text[close + 1:] == "" \
            or self._is_follow_start(text[close + 1:])

    def allowed_mask(self) -> BoolMask:
        """Plain text tokens come from a precomputed mask (fast path)."""
        mask = super().allowed_mask()
        if self.state == 0:
            mask |= self.vocabulary.plain_string_mask
        return mask

    def advance(self, text: str) -> None:
        result = self._simulate(text)
        if result is None:
            raise ValueError(f"invalid string continuation {text!r}")
        self.state, close = result
        if close is None:
            self.content += text
            return
        self.content += text[:close]
        self.consumed = text[close + 1:]
        self.done = True

    def is_complete(self) -> bool:
        return self.done

    def finish_text(self) -> str:
        if self.state == -1:
            return '\\"'
        return "0" * max(self.state, 0) + '"'

    def value(self) -> JsonValue:
        decoded: str = json.loads('"' + self.content + '"')
        return decoded


def make_value_constraint(param_type: str, vocabulary: TokenVocabulary,
                          follow: str) -> ValueConstraint:
    """Create the constraint that generates a value of param_type."""
    if param_type in ("number", "integer"):
        return NumberConstraint(vocabulary=vocabulary, follow=follow,
                                integer=param_type == "integer")
    if param_type == "boolean":
        return BooleanConstraint(vocabulary=vocabulary, follow=follow)
    if param_type == "string":
        return StringConstraint(vocabulary=vocabulary, follow=follow)
    raise ValueError(f"unsupported parameter type '{param_type}'")
