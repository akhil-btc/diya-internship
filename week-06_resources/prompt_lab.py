"""
prompt_lab.py  —  Week 6 reference (Monday/Tuesday exercise)
============================================================
MENTOR REFERENCE. Diya should write her own; use this to unblock her
or to calibrate her version.

THE LESSON
----------
Same task, same model, same temperature. The ONLY thing that changes
is the prompt -- and the output quality changes dramatically. This is
the whole thesis of prompt engineering: a prompt is a SPEC, not a wish.

The "engineered" prompt below uses four levers Diya will learn Monday:
  1. ROLE        - tell it who to be (system message)
  2. CONTEXT     - tell it the situation and audience
  3. SPECIFICITY - say exactly what you want, not vaguely
  4. FORMAT      - dictate the shape of the answer
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq


MODEL = "llama-3.3-70b-versatile"

# Same task in both cases: help a student understand a tricky topic.
TASK_TOPIC = "Explain recursion in programming."

# ---- Version A: the lazy prompt (a wish) ----
LAZY_SYSTEM = "You are a helpful assistant."
LAZY_USER = TASK_TOPIC

# ---- Version B: the engineered prompt (a spec) ----
ENGINEERED_SYSTEM = (
    # ROLE
    "You are a patient computer-science tutor for high-school students. "
    # CONTEXT
    "Your student is 15, codes a little in Python, and gets lost when "
    "explanations use jargon or assume college math. "
    # SPECIFICITY + FORMAT
    "When explaining a concept, ALWAYS use exactly this structure:\n"
    "1. One plain-English sentence (no jargon).\n"
    "2. One everyday analogy.\n"
    "3. One tiny Python example, 5 lines max.\n"
    "4. One sentence on a common beginner mistake.\n"
    "Keep the whole thing under 150 words."
)
ENGINEERED_USER = TASK_TOPIC


def load_client():
    """Load the API key and return a ready Groq client, or exit clearly."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Missing GROQ_API_KEY in .env. Add it and run again.")
        sys.exit(1)
    return Groq(api_key=key)


def ask(client, system_prompt, user_prompt):
    """Same settings for both runs, so the PROMPT is the only variable."""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.4,
        max_tokens=300,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def main():
    client = load_client()

    print("################  VERSION A — lazy prompt (a wish)  ###########")
    print(ask(client, LAZY_SYSTEM, LAZY_USER))

    print("\n################  VERSION B — engineered prompt (a spec)  #####")
    print(ask(client, ENGINEERED_SYSTEM, ENGINEERED_USER))

    print("\n--------------------------------------------------------------")
    print("Same model. Same topic. Same temperature. The only thing that\n"
          "changed was the words in the prompt. Which answer would you\n"
          "actually want? That gap is the entire job.")


if __name__ == "__main__":
    main()
