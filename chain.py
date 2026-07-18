"""
chain.py — runs the multi-step reasoning chain.
Pure logic, no Streamlit imports, so it can be tested or reused
(e.g. from a CLI or a future API endpoint) independently of the UI.
"""

from groq import Groq
from config import MODEL, TEMPERATURE


def run_chain(api_key: str, raw_input: str, steps: list, on_progress=None) -> list[str]:
    """
    Runs each step in `steps` sequentially, feeding each output forward
    as context into the next step. Returns a list of outputs, one per step,
    in the same order as `steps`.

    on_progress(i, total, step_title) is called before each step starts,
    if provided — used to drive a UI progress bar.
    """
    client = Groq(api_key=api_key)
    context = raw_input
    outputs = []

    for i, step in enumerate(steps):
        if on_progress:
            on_progress(i, len(steps), step["title"])

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": step["system"]},
                {"role": "user", "content": context},
            ],
            temperature=TEMPERATURE,
        )
        result = response.choices[0].message.content
        outputs.append(result)
        context = context + "\n\n---\n\n" + result  # chain forward

    return outputs
