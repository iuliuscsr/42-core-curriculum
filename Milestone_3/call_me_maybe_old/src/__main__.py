import torch
from llm_sdk import Small_LLM_Model
from .parse_input import read_calling_tests


def generate_unconstrained(
    model: Small_LLM_Model, prompt: str, max_new_tokens: int = 100
) -> str:
    raw_encoded = model.encode(prompt)
    input_ids: list[int] = raw_encoded.flatten().tolist()

    for _ in range(max_new_tokens):
        raw_logits = model.get_logits_from_input_ids(input_ids)
        logits = torch.as_tensor(raw_logits)
        next_token_id = int(torch.argmax(logits).item())
        input_ids.append(next_token_id)

    return model.decode(input_ids)


def run_unconstrained() -> None:
    model = Small_LLM_Model()
    tests: list[dict[str, str]] = read_calling_tests()
    sample_prompt: str = tests[0]["prompt"]
    raw_output = generate_unconstrained(model, sample_prompt, max_new_tokens=80)

    print("===PROMPT===")
    print(sample_prompt)
    print("result without constrained decoding:")
    print(raw_output)


def main() -> None:
    run_unconstrained()


if __name__ == "__main__":
    main()
