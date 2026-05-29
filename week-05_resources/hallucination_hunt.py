"""
hallucination_hunt.py  —  Week 5 reference (Friday exercise)
============================================================
MENTOR REFERENCE. This is the bridge from "how LLMs work" into
"prompt engineering" (Week 6). Diya makes the model lie, then fixes
it with nothing but better instructions.

GOAL FOR DIYA
-------------
Two stages:

  STAGE 1 — Catch it lying.
    Ask the model something it will confidently get wrong: a made-up
    book, a fake person, an obscure "fact". Watch it invent details
    with total confidence. This is hallucination, live.

  STAGE 2 — Reduce the lying with the prompt alone.
    Add a system message that gives it PERMISSION to say "I don't
    know." Re-ask the same question. Watch the behaviour change.
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq


MODEL = "llama-3.3-70b-versatile"

# Questions engineered to tempt a confident wrong answer. The model has
# no such facts, so a "helpful" model tends to invent them.
TRAP_QUESTIONS = [
    "Summarise the plot of the 2019 novel 'The Glass Lighthouse' "
    "by Aria Whitfield.",
    "What were the three main findings of the 2021 Hargrove-Stein "
    "study on teenage sleep and memory?",
]

# Stage 1: no guardrails. We don't tell it that 'I don't know' is allowed.
SYSTEM_NO_GUARDRAIL = "You are a helpful assistant. Answer the question."

# Stage 2: same task, but we explicitly license uncertainty.
SYSTEM_WITH_GUARDRAIL = (
    "You are a careful assistant. If you are not sure something is real "
    "or you don't have reliable information about it, say so plainly "
    "instead of guessing. Never invent titles, authors, dates, or "
    "study findings. It is better to say 'I don't know' than to make "
    "something up."
)


def load_client():
    """Load the API key and return a ready Groq client, or exit clearly."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Missing GROQ_API_KEY in .env. Add it and run again.")
        sys.exit(1)
    return Groq(api_key=key)


def ask(client, system_prompt, user_prompt):
    """Send one system+user pair. Low temperature so the only variable
    we're testing is the SYSTEM PROMPT, not randomness."""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        max_tokens=200,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def run_stage(client, label, system_prompt):
    print(f"\n############  {label}  ############")
    for question in TRAP_QUESTIONS:
        print(f"\nQ: {question}")
        answer = ask(client, system_prompt, question)
        print(f"A: {answer}")


def main():
    client = load_client()

    # Stage 1: watch it confidently invent.
    run_stage(client, "STAGE 1  (no guardrail)", SYSTEM_NO_GUARDRAIL)

    # Stage 2: same questions, one extra paragraph of instruction.
    run_stage(client, "STAGE 2  (with guardrail)", SYSTEM_WITH_GUARDRAIL)

    print("\n----------------------------------------------------------")
    print("Compare the two stages. Same questions, same model, same\n"
          "temperature. The ONLY thing that changed was the system\n"
          "prompt -- and the honesty of the answers changed with it.\n"
          "That's prompt engineering. More on it Monday.")


if __name__ == "__main__":
    main()
