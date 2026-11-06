import enum
import json
import re
from typing import Any, Dict, List, Optional, Set

import numpy as np
from pydantic import BaseModel, Field

from llm_sdk import Small_LLM_Model


class JSONState(str, enum.Enum):
    """Expliziter Lebenszyklus für das Constrained Decoding."""

    EXPECT_PROMPT: str = "EXPECT_PROMPT"
    EXPECT_FUNCTION_NAME: str = "EXPECT_FUNCTION_NAME"
    EXPECT_PARAMS_OPEN: str = "EXPECT_PARAMS_OPEN"
    EXPECT_PARAM_KEY: str = "EXPECT_PARAM_KEY"
    EXPECT_PARAM_COLON: str = "EXPECT_PARAM_COLON"
    EXPECT_PARAM_VALUE: str = "EXPECT_PARAM_VALUE"
    EXPECT_PARAMS_CLOSE: str = "EXPECT_PARAMS_CLOSE"
    EXPECT_CLOSE_BRACKET: str = "EXPECT_CLOSE_BRACKET"
    END: str = "END"


class Vocabulary(BaseModel):
    """Contains two sets of token_ids, for numbers and strings."""
    text_of: Dict[int, str]
    string_ids: Set[int]
    number_ids: Set[int]

    @classmethod
    def load(cls, model: Small_LLM_Model) -> "Vocabulary":
        """Creates an Vocabulary object."""

        vocab_path: str = model.get_path_to_vocabulary_json()
        with open(vocab_path, "r", encoding="utf-8") as f:
            raw_vocab: Dict[str, int] = json.load(f)

        reversed_vocab: dict[int, str] = {
            token_id: token_str for token_str, token_id in raw_vocab.items()
        }

        string_ids: set[int] = {
            tok_id
            for tok_id, tok_text in reversed_vocab.items()
            if tok_text and not any(char in tok_text for char in '"\\\n')
        }
        number_ids: Set[int] = {
            tok_id
            for tok_id, tok_text in reversed_vocab.items()
            if tok_text and all(char in "0123456789.-eE" for char in tok_text)
        }

        return cls(
            text_of=text_of, string_ids=string_ids, number_ids=number_ids
        )


class GrammarControl(BaseModel):
    """Grammar Control Engine basierend auf einer datengetriebenen State Machine."""

    prompt: str
    allowed_functions: List[Dict[str, Any]]
    vocab: Vocabulary
    state: JSONState = JSONState.EXPECT_PROMPT

    selected_function: Optional[Dict[str, Any]] = None
    remaining_params: List[str] = Field(default_factory=list)
    current_param: Optional[str] = None

    # Laufzeit-Speicher für Multi-Token-Abläufe
    pending_tokens: Optional[List[int]] = None
    candidate_tokens: Optional[Dict[str, List[int]]] = None
    generated_value_text: str = ""

    model_config: Dict[str, bool] = {"arbitrary_types_allowed": True}


    def _encode(self, model: Small_LLM_Model, text: str) -> List[int]:
        """Kodiert einen String in eine reine Liste von Token-IDs."""
        return model.encode(text)

    def _get_current_param_type(self) -> str:
        """Gibt den JSON-Schema-Typ des aktuell verarbeiteten Parameters zurück."""
        if not self.selected_function or not self.current_param:
            return ""
        params_schema: Dict[str, Any] = self.selected_function.get(
            "parameters", {}
        )
        spec: Dict[str, Any] = params_schema.get(self.current_param, {})
        return str(spec.get("type", "string"))

    def _is_candidate_state(self) -> bool:
        """Prüft, ob im aktuellen State aus diskreten Strings gewählt werden muss."""
        if self.state == JSONState.EXPECT_FUNCTION_NAME:
            return True
        if (
            self.state == JSONState.EXPECT_PARAM_VALUE
            and self._get_current_param_type() == "boolean"
        ):
            return True
        return False

    def _get_literal_text(self) -> str:
        is_string_val: bool = self._get_current_param_type() == "string"
        closing_quote: str = '"' if is_string_val else ""

        if self.state == JSONState.EXPECT_PROMPT:
            return f'{{\n  "prompt": {json.dumps(self.prompt)},\n'

        if self.state == JSONState.EXPECT_PARAMS_OPEN:
            return '  "parameters": {'

        if self.state == JSONState.EXPECT_PARAM_KEY:
            has_prev_param: bool = self.current_param is not None
            comma_prefix: str = "," if has_prev_param else ""
            next_key: str = json.dumps(self.remaining_params[0])
            return f"{closing_quote}{comma_prefix}\n    {next_key}"

        if self.state == JSONState.EXPECT_PARAM_COLON:
            return ': "' if is_string_val else ": "

        if self.state == JSONState.EXPECT_PARAMS_CLOSE:
            return f"{closing_quote}\n  }}"

        return "\n}"  # EXPECT_CLOSE_BRACKET

    def _determine_next_param_state(self) -> JSONState:
        """Entscheidet, ob noch weitere Parameter folgen oder geschlossen wird."""
        if self.remaining_params:
            return JSONState.EXPECT_PARAM_KEY
        return JSONState.EXPECT_PARAMS_CLOSE


    def get_allowed_token_ids(self, model: Small_LLM_Model) -> Set[int]:
        """Hauptmethode: Liefert alle im aktuellen State gültigen Token-IDs."""
        if self.state == JSONState.END:
            return set()

        if self._is_candidate_state():
            candidates: Dict[str, List[int]] = self._get_candidates(model)
            return {token_ids[0] for token_ids in candidates.values()}

        if self.state == JSONState.EXPECT_PARAM_VALUE:
            return self._get_allowed_value_token_ids(model)

        pending: List[int] = self._get_pending_tokens(model)
        return {pending[0]}

    def _get_pending_tokens(self, model: Small_LLM_Model) -> List[int]:
        """Initialisiert oder liefert die verbleibende Token-Liste eines Literals."""
        if self.pending_tokens is None:
            literal_str: str = self._get_literal_text()
            self.pending_tokens = self._encode(model, literal_str)
        return self.pending_tokens

    def _get_candidates(
        self, model: Small_LLM_Model
    ) -> Dict[str, List[int]]:
        """Initialisiert oder liefert Token-Bäume für Auswahl-Entscheidungen."""
        if self.candidate_tokens is None:
            candidate_texts: Dict[str, str] = {"true": "true", "false": "false"}

            if self.state == JSONState.EXPECT_FUNCTION_NAME:
                candidate_texts = {
                    fn["name"]: f'  "name": {json.dumps(fn["name"])}'
                    for fn in self.allowed_functions
                }

            self.candidate_tokens = {
                name: self._encode(model, text)
                for name, text in candidate_texts.items()
            }
        return self.candidate_tokens

    def _get_allowed_value_token_ids(self, model: Small_LLM_Model) -> Set[int]:
        """Berechnet gültige Token für freie Parameterwerte (String, Number)."""
        p_type: str = self._get_current_param_type()

        if p_type == "string":
            allowed: Set[int] = set(self.vocab.string_ids)
        else:
            regex_pattern: str = (
                r"-?\d*" if p_type == "integer" else r"-?\d*\.?\d*"
            )
            allowed = {
                tok_id
                for tok_id in self.vocab.number_ids
                if re.fullmatch(
                    regex_pattern,
                    self.generated_value_text + self.vocab.text_of[tok_id],
                )
            }

        if self._can_value_generation_stop(p_type):
            allowed.add(self._get_stop_token_id(model))

        return allowed

    def _can_value_generation_stop(self, p_type: str) -> bool:
        if p_type == "string":
            return True
        regex_pattern: str = (
            r"-?\d+" if p_type == "integer" else r"-?\d+(\.\d+)?"
        )
        return (
            re.fullmatch(regex_pattern, self.generated_value_text) is not None
        )

    def _get_stop_token_id(self, model: Small_LLM_Model) -> int:
        """Ermittelt das erste Token des nächsten Zustands als Stopp-Signal."""
        target_state: JSONState = self._determine_next_param_state()
        old_state: JSONState = self.state
        self.state = target_state
        next_text: str = self._get_literal_text()
        self.state = old_state

        return self._encode(model, next_text)[0]


    def update_state(self, chosen_token_id: int, model: Small_LLM_Model) -> None:
        """Verarbeitet das gewählte Token und schaltet die State Machine weiter."""
        if self.state == JSONState.END:
            return

        if self._is_candidate_state():
            # Kandidaten filtern, die mit dem gewählten Token übereinstimmen
            current_candidates: Dict[str, List[int]] = self._get_candidates(model)
            self.candidate_tokens = {
                name: ids[1:]
                for name, ids in current_candidates.items()
                if ids[0] == chosen_token_id
            }
            # Wenn ein Kandidat vollständig gewählt wurde -> State wechseln
            finished: List[str] = [
                name
                for name, ids in self.candidate_tokens.items()
                if not ids
            ]
            if finished:
                if self.state == JSONState.EXPECT_FUNCTION_NAME:
                    self._on_function_selected(finished[0])
                self._transition_to_next_state(model)

        elif self.state == JSONState.EXPECT_PARAM_VALUE:
            if chosen_token_id == self._get_stop_token_id(model):
                # Modell hat das Stopp-Token gewählt -> Transition auslösen
                self._transition_to_next_state(model, is_stop_token_consumed=True)
            else:
                self.generated_value_text += self.vocab.text_of[chosen_token_id]

        else:  # Synchroner Literal-State
            pending: List[int] = self._get_pending_tokens(model)
            pending.pop(0)
            if not pending:
                self._transition_to_next_state(model)

    def _on_function_selected(self, function_name: str) -> None:
        """Setzt die gewählte Funktion und lädt deren Parameterliste."""
        for fn in self.allowed_functions:
            if fn["name"] == function_name:
                self.selected_function = fn
                self.remaining_params = list(
                    fn.get("parameters", {}).keys()
                )
                break

    def _transition_to_next_state(
        self, model: Small_LLM_Model, is_stop_token_consumed: bool = False
    ) -> None:
        """Führt den eigentlichen Zustandsübergang durch und reinigt Puffer."""
        if self.state == JSONState.EXPECT_PROMPT:
            next_state: JSONState = JSONState.EXPECT_FUNCTION_NAME

        elif self.state == JSONState.EXPECT_FUNCTION_NAME:
            next_state = JSONState.EXPECT_PARAMS_OPEN

        elif self.state in (
            JSONState.EXPECT_PARAMS_OPEN,
            JSONState.EXPECT_PARAM_VALUE,
        ):
            next_state = self._determine_next_param_state()

        elif self.state == JSONState.EXPECT_PARAM_KEY:
            self.current_param = self.remaining_params.pop(0)
            next_state = JSONState.EXPECT_PARAM_COLON

        elif self.state == JSONState.EXPECT_PARAM_COLON:
            next_state = JSONState.EXPECT_PARAM_VALUE

        elif self.state == JSONState.EXPECT_PARAMS_CLOSE:
            next_state = JSONState.EXPECT_CLOSE_BRACKET

        else:
            next_state = JSONState.END

        # State aktualisieren und Puffer zurücksetzen
        self.state = next_state
        self.pending_tokens = None
        self.candidate_tokens = None
        self.generated_value_text = ""

        # Spezialfall: Falls das Stopp-Token bereits das 1. Token des neuen Literals war
        if is_stop_token_consumed:
            new_literal: str = self._get_literal_text()
            full_ids: List[int] = self._encode(model, new_literal)
            self.pending_tokens = full_ids[1:]  # Erstes Token abziehen
            if not self.pending_tokens:
                self._transition_to_next_state(model)

    # =========================================================================
    # 4. LOGIT MASKING (PYTORCH-FREI MIT NUMPY)
    # =========================================================================

    def mask_logits(self, raw_logits: Any, model: Small_LLM_Model) -> np.ndarray:
        """Maskiert unzulässige Logits rein mit NumPy auf -inf (Kapitel V.3.3)."""
        logits: np.ndarray = np.asarray(raw_logits, dtype=np.float32)
        if logits.ndim > 1:
            logits = logits[-1]  # Nur die letzte Token-Position nutzen

        masked_logits: np.ndarray = np.full_like(logits, fill_value=-np.inf)
        allowed_token_ids: Set[int] = self.get_allowed_token_ids(model)

        for token_id in allowed_token_ids:
            masked_logits[token_id] = logits[token_id]

        return masked_logits