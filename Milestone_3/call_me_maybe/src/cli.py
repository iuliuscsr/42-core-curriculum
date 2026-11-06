"""Command line entry point: read inputs, run the model, write results."""

import argparse
import sys
import time
from pathlib import Path

from src.decoder import ConstrainedDecoder
from src.file_io import load_functions, load_prompts, warn, write_results
from src.function_caller import FunctionCaller
from src.models import FunctionCall
from src.vocabulary import TokenVocabulary

DEFAULT_FUNCTIONS = Path("data/input/functions_definition.json")
DEFAULT_INPUT = Path("data/input/function_calling_tests.json")
DEFAULT_OUTPUT = Path("data/output/function_calling_results.json")
DEFAULT_MODEL = "Qwen/Qwen3-0.6B"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the command line options."""
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Translate prompts into function calls with an LLM.",
    )
    parser.add_argument("--functions_definition", type=Path,
                        default=DEFAULT_FUNCTIONS,
                        help="JSON file with the available functions")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                        help="JSON file with the prompts to process")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="where to write the resulting JSON array")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Hugging Face model id (default: %(default)s)")
    return parser.parse_args(argv)


def load_decoder(model_name: str) -> ConstrainedDecoder:
    """Load the LLM and its vocabulary.

    Raises:
        ValueError: if the SDK, the model or the vocabulary cannot be
            loaded (missing packages, no network, unknown model, ...).
    """
    try:
        from llm_sdk import Small_LLM_Model
        llm = Small_LLM_Model(model_name)
        vocab_path = Path(llm.get_path_to_vocab_file())
        # One forward pass tells how many logits (token ids) exist.
        vocab_size = len(llm.get_logits_from_input_ids(
            [int(i) for i in llm.encode("{").tolist()[0]]))
    except Exception as err:  # the SDK may raise almost anything
        raise ValueError(
            f"cannot load model '{model_name}': "
            f"{type(err).__name__}: {err}"
        ) from None
    vocabulary = TokenVocabulary.from_vocab_file(vocab_path, vocab_size)
    return ConstrainedDecoder(llm=llm, vocabulary=vocabulary)


def run(args: argparse.Namespace) -> int:
    """Process every prompt and return the process exit code."""
    functions = load_functions(args.functions_definition)
    prompts = load_prompts(args.input)
    if not prompts:
        warn("no valid prompt to process, writing an empty result")

    print(f"Loading model {args.model} ...", file=sys.stderr)
    caller = FunctionCaller(decoder=load_decoder(args.model),
                            functions=functions)

    results: list[FunctionCall] = []
    start = time.perf_counter()
    for index, item in enumerate(prompts, start=1):
        try:
            result = caller.call(item.prompt)
        except (ValueError, RuntimeError) as err:
            warn(f"prompt #{index} failed and is skipped: {err}")
            continue
        results.append(result)
        print(f"[{index}/{len(prompts)}] {item.prompt!r} -> "
              f"{result.name}({result.parameters})", file=sys.stderr)

    write_results(args.output, results)
    elapsed = time.perf_counter() - start
    print(f"Wrote {len(results)} result(s) to {args.output} "
          f"in {elapsed:.1f}s ({caller.decoder.model_calls} model calls)",
          file=sys.stderr)
    return 0 if len(results) == len(prompts) else 1


def main(argv: list[str] | None = None) -> int:
    """Run the program and turn every error into a clear message."""
    args = parse_args(argv)
    try:
        return run(args)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
    return 1
