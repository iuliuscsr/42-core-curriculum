"""Constrained greedy decoding on top of the provided LLM SDK."""

from typing import Any

import numpy as np
from pydantic import BaseModel, ConfigDict

from src.constraints import ValueConstraint
from src.vocabulary import TokenVocabulary


class ConstrainedDecoder(BaseModel):
    """Runs the model token by token while a constraint masks the logits."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    llm: Any
    vocabulary: TokenVocabulary
    model_calls: int = 0

    def encode(self, text: str) -> list[int]:
        """Tokenize text into a flat list of ids."""
        if not text:
            return []
        rows: Any = self.llm.encode(text).tolist()
        return [int(token_id) for token_id in rows[0]]

    def append_text(self, input_ids: list[int], text: str) -> None:
        """Append fixed text (no choice involved) to the context."""
        input_ids.extend(self.encode(text))

    def next_token(self, input_ids: list[int],
                   constraint: ValueConstraint) -> int | None:
        """Pick the most likely allowed token, None if nothing is allowed."""
        logits = np.asarray(self.llm.get_logits_from_input_ids(input_ids),
                            dtype=np.float32)
        self.model_calls += 1
        mask = constraint.allowed_mask()
        if logits.shape[0] < mask.shape[0]:
            mask = mask[:logits.shape[0]]
        elif logits.shape[0] > mask.shape[0]:
            mask = np.pad(mask, (0, logits.shape[0] - mask.shape[0]))
        if not mask.any():
            return None
        masked = np.where(mask, logits, -np.inf)
        return int(np.argmax(masked))

    def generate(self, input_ids: list[int],
                 constraint: ValueConstraint) -> None:
        """Generate one value in place until the constraint is complete."""
        while not constraint.is_complete():
            text = constraint.forced_text()
            token_id: int | None = None
            if text is None and constraint.tokens_used < constraint.max_tokens:
                token_id = self.next_token(input_ids, constraint)
            if token_id is not None:
                input_ids.append(token_id)
                constraint.tokens_used += 1
                constraint.advance(self.vocabulary.text(token_id))
                continue
            if text is None:
                text = constraint.finish_text()
            self.append_text(input_ids, text)
            constraint.advance(text)
