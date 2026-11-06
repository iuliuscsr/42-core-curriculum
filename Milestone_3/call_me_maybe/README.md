*This project has been created as part of the 42 curriculum by jmalsam.*

# call me maybe

## Description

`call me maybe` turns natural-language requests into structured function
calls. Given the request *"What is the sum of 2 and 3?"* and a list of
available functions, the program does not answer `5`; it outputs

```json
{"prompt": "What is the sum of 2 and 3?", "name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}
```

The model used is the small **Qwen/Qwen3-0.6B**. On its own, such a model
often produces broken or off-schema JSON. This project makes the output
reliable with **constrained decoding**: at every generation step, all
tokens that would break the JSON syntax or the function schema are removed
before the next token is picked. The model still makes every real decision
(which function, which argument values); the decoder only guarantees that
the result is valid.

## Instructions

Requirements: Python ≥ 3.10 and [uv](https://docs.astral.sh/uv/).

```bash
make install        # uv sync: creates .venv with numpy, pydantic and the SDK deps
make run            # uv run python -m src with the default paths
make debug          # same, under pdb
make lint           # flake8 + mypy with the mandatory flags
make lint-strict    # flake8 + mypy --strict
make test           # pytest (offline, uses fake models)
make clean          # remove caches and data/output
```

The first run downloads the model from the Hugging Face Hub.

## Example usage

```bash
uv run python -m src
uv run python -m src \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calling_results.json
make run ARGS="--input my_prompts.json"
```

| option | default |
|---|---|
| `--functions_definition` | `data/input/functions_definition.json` |
| `--input` | `data/input/function_calling_tests.json` |
| `--output` | `data/output/function_calling_results.json` |
| `--model` | `Qwen/Qwen3-0.6B` |

Progress and warnings go to stderr, the results to the output file:

```
[1/11] 'What is the sum of 2 and 3?' -> fn_add_numbers({'a': 2.0, 'b': 3.0})
...
Wrote 11 result(s) to data/output/function_calling_results.json
```

## Algorithm explanation

### 1. Tokens as text

`vocab.json` (path from `Small_LLM_Model.get_path_to_vocab_file()`) maps
byte-level BPE token strings to ids. Every byte is stored as a printable
character (`Ġ` = space, `Ċ` = newline). `vocabulary.py` inverts the GPT-2
`bytes_to_unicode` table, so each token id is known by the exact text it
adds. Tokens that are only half of a multi-byte UTF-8 character, and
special tokens (`<|im_end|>`, ...) get no text and are never allowed.

At start-up the vocabulary also precomputes the token groups the
constraints need: a boolean mask of "plain" tokens that can appear inside
a JSON string unchanged, the few tokens containing `"` or `\`, tokens made
only of number characters, and tokens grouped by first character.

### 2. Skeleton + generated holes

The answer is built from fixed parts and generated parts:

```
{"name": "<CHOICE>", "parameters": {"a": <NUMBER>, "b": <NUMBER>}}
```

Fixed parts (braces, keys, separators) are appended to the context
directly, without asking the model - there is nothing to decide there.
Only the holes are generated, each by a constraint for its type
(`constraints.py`):

| constraint | used for | allowed tokens |
|---|---|---|
| `ChoiceConstraint` | function name | text so far + token must be a prefix of one of the options |
| `NumberConstraint` | `number`, `integer` | must keep a valid JSON-number prefix (state machine); may end only in an accepting state |
| `StringConstraint` | `string` | no raw control chars, only valid escapes (`\\`, `\"`, `\n`, `\uXXXX`, ...); ends at the first unescaped `"` |
| `BooleanConstraint` | `boolean` | `true` / `false` |

### 3. One decoding step

```
logits = llm.get_logits_from_input_ids(context)
mask   = constraint.allowed_mask()          # True = token allowed
token  = argmax(where(mask, logits, -inf))  # greedy among valid tokens
context.append(token); constraint.advance(text(token))
```

Setting disallowed logits to `-inf` is exactly "remove them before
choosing". Greedy decoding keeps the result deterministic.

### 4. Details that matter

* **Merged tokens.** The tokenizer likes tokens such as `",` or `"}}`.
  Every value knows the fixed text that follows it (`follow`), and a token
  may continue into that text. The swallowed part is reported as
  `consumed` and not written a second time. Without this the model would
  be forced away from its preferred ending and could keep writing.
* **Forced text.** If a choice has only one possible continuation (e.g.
  the common prefix `fn_` of all names, or the rest of the last remaining
  name) it is appended without a model call.
* **Guaranteed termination.** Each value has a token budget. When it is
  used up, `finish_text()` closes the value with the shortest valid
  completion (e.g. `"` for a string, `0` + separator for `1.`).
* **Types.** `number` values are emitted as floats (`2.0`), `integer` as
  ints, and the final record is validated by a pydantic model with strict
  types before it is written.

## Design decisions

* **One module per responsibility:** `models.py` (pydantic schemas),
  `file_io.py` (reading/validating/writing), `vocabulary.py` (token
  texts), `constraints.py` (what may come next), `decoder.py` (the
  decoding loop), `prompt_builder.py` (context text),
  `function_caller.py` (skeleton for one prompt), `cli.py` (entry point).
* **Skeleton instead of a full JSON grammar.** The output format is
  fixed, so a general JSON parser state machine is not needed. Generating
  only the holes is simpler to explain and saves most model calls.
* **The LLM chooses the function**, via `ChoiceConstraint`; no keyword
  heuristics.
* **No torch in `src/`.** Logits are converted to a numpy array;
  `llm_sdk` is only used through its public methods.
* **All classes are pydantic models**, including the constraints and the
  decoder (`arbitrary_types_allowed` for numpy arrays and the SDK model).
* **Errors never crash the program.** Missing/invalid input files give a
  clear message and exit code 1; invalid entries (missing `prompt`,
  unsupported parameter type, duplicate function names) are skipped with
  a warning; a failing prompt is skipped and reported.

## Performance analysis

* **Validity:** 100 % parseable, schema-compliant JSON by construction.
  The test suite drives the pipeline with a model returning pure random
  logits: every record still has the right keys and argument types.
* **Accuracy:** depends on the model's choices; constraints only remove
  invalid options. With Qwen3-0.6B the function choice and simple
  arguments are reliable; regex arguments are the weakest point.
* **Speed:** the SDK recomputes the whole context at each call (no KV
  cache), so the number of model calls dominates. Fixed text costs no
  calls, so a prompt needs roughly one call per generated value token
  (≈ 5-20 per prompt). Mask building is vectorised for the large
  "plain string" group; only small token groups are checked in Python.

## Challenges faced

* **Byte-level tokens:** the vocabulary does not contain readable text;
  solved with the inverse `bytes_to_unicode` table.
* **Tokens spanning value and syntax** (`",`, `}}`): handled with the
  `follow`/`consumed` mechanism described above.
* **Regular expressions in JSON:** `\d` is not a valid JSON escape; the
  string constraint only allows valid escapes, so the model has to write
  `\\d`, which decodes to the regex `\d`.
* **Ambiguous prefixes** like `fn_add` / `fn_add_numbers`: the closing
  quote is part of each option, so no option is a prefix of another.

## Testing strategy

`tests/` runs fully offline (`make test`):

* unit tests for the byte decoding, the number/string/choice constraints
  and the input file error handling (missing file, invalid JSON, wrong
  top-level type, invalid entries);
* a *scripted* fake model that "wants" to write the expected answer -
  checks that the pipeline reproduces all example calls exactly
  (including `\\d+` escaping and `1.44e2` → `144.0`);
* a *random* fake model - checks that even nonsense logits always yield
  valid, schema-compliant output and that decoding terminates;
* integer/boolean parameters, functions without parameters and the CLI.

The fake models use a small byte-level vocabulary with merged tokens like
`",` and `}}`, so token-boundary cases are covered.

## Resources

* https://huggingface.co/learn/nlp-course/chapter6/5
* Willard & Louf, *Efficient Guided Generation for Large Language Models* (2023)
* https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/
* https://huggingface.co/Qwen/Qwen3-0.6B

### Use of AI

An AI assistant was used to understand how AI works, to explain specific vocabulary
and help with optimizing the architecture as well as debug.
