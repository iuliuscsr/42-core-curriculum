"""Token vocabulary: maps token ids to the text they produce.

Qwen uses a byte-level BPE tokenizer (like GPT-2). In ``vocab.json`` every
byte is written as a printable unicode character, e.g. a space becomes
'Ġ' and a newline 'Ċ'. This module reverses that mapping so each token id
is known by the exact text it adds to the output, and precomputes the
token groups the constraints need at every decoding step.
"""

import json
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel, ConfigDict, PrivateAttr

BoolMask = npt.NDArray[np.bool_]

NUMBER_CHARS = frozenset("0123456789+-.eE")


def bytes_to_unicode() -> dict[int, str]:
    """Return the GPT-2 byte -> printable character table.

    Printable bytes keep their own character, all others (space, control
    bytes, ...) are shifted to code points above 255.
    """
    printable = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    table: dict[int, str] = {byte: chr(byte) for byte in printable}
    shift = 0
    for byte in range(256):
        if byte not in table:
            table[byte] = chr(256 + shift)
            shift += 1
    return table


def decode_token(token: str, char_to_byte: dict[str, int]) -> str | None:
    """Turn a vocab.json token string into the text it stands for.

    Returns None when the token is not a complete UTF-8 sequence (a
    fragment of a multi-byte character); such tokens are never allowed.
    """
    try:
        raw = bytes(char_to_byte[char] for char in token)
        text = raw.decode("utf-8")
    except (KeyError, UnicodeDecodeError):
        return None
    return text or None


def _is_plain_string_text(text: str) -> bool:
    """True if text can appear unchanged inside a JSON string."""
    return all(char not in '"\\' and ord(char) >= 0x20 for char in text)


class TokenVocabulary(BaseModel):
    """Decoded vocabulary plus precomputed token groups."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    texts: list[str | None]
    text_to_id: dict[str, int]
    plain_string_mask: BoolMask
    string_special_ids: list[int]
    number_ids: list[int]
    ids_by_first_char: dict[str, list[int]]
    _substring_cache: dict[tuple[str, ...], list[int]] = PrivateAttr(
        default_factory=dict
    )

    @classmethod
    def from_token_map(cls, token_map: dict[str, int],
                       size: int) -> "TokenVocabulary":
        """Build the vocabulary from a {token: id} map (vocab.json format).

        Args:
            token_map: byte-level token strings and their ids.
            size: number of logits the model returns; ids outside the map
                (special tokens) stay unusable.
        """
        char_to_byte = {char: byte
                        for byte, char in bytes_to_unicode().items()}
        texts: list[str | None] = [None] * size
        text_to_id: dict[str, int] = {}
        for token, token_id in token_map.items():
            if not 0 <= token_id < size:
                continue
            text = decode_token(token, char_to_byte)
            texts[token_id] = text
            if text is not None:
                text_to_id.setdefault(text, token_id)

        plain = np.zeros(size, dtype=np.bool_)
        special: list[int] = []
        numbers: list[int] = []
        by_first: dict[str, list[int]] = {}
        for token_id, text in enumerate(texts):
            if text is None:
                continue
            by_first.setdefault(text[0], []).append(token_id)
            if _is_plain_string_text(text):
                plain[token_id] = True
            elif all(ord(char) >= 0x20 for char in text):
                special.append(token_id)
            if all(char in NUMBER_CHARS for char in text):
                numbers.append(token_id)
        return cls(texts=texts, text_to_id=text_to_id,
                   plain_string_mask=plain, string_special_ids=special,
                   number_ids=numbers, ids_by_first_char=by_first)

    @classmethod
    def from_vocab_file(cls, path: Path, size: int) -> "TokenVocabulary":
        """Load a vocab.json file.

        Raises:
            ValueError: if the file cannot be read or has the wrong shape.
        """
        try:
            with path.open("r", encoding="utf-8") as handle:
                data: Any = json.load(handle)
        except (OSError, json.JSONDecodeError) as err:
            raise ValueError(f"cannot load vocabulary {path}: {err}") from None
        if not isinstance(data, dict) or not all(
            isinstance(key, str) and isinstance(value, int)
            for key, value in data.items()
        ):
            raise ValueError(f"unexpected vocabulary format in {path}")
        return cls.from_token_map(data, size)

    @property
    def size(self) -> int:
        """Number of token ids (= number of logits)."""
        return len(self.texts)

    def text(self, token_id: int) -> str:
        """Text of a usable token id."""
        text = self.texts[token_id]
        if text is None:
            raise ValueError(f"token {token_id} has no text")
        return text

    def empty_mask(self) -> BoolMask:
        """A mask that allows no token."""
        return np.zeros(self.size, dtype=np.bool_)

    def ids_inside(self, targets: tuple[str, ...]) -> list[int]:
        """Ids of all tokens whose text occurs inside one of targets.

        Only those tokens can ever help to spell one of the targets, so a
        choice constraint checks this short list instead of the whole
        vocabulary. Results are cached per target tuple.
        """
        if targets not in self._substring_cache:
            self._substring_cache[targets] = [
                token_id for token_id, text in enumerate(self.texts)
                if text is not None
                and any(text in target for target in targets)
            ]
        return self._substring_cache[targets]
