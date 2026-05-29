"""
temperature_lab.py  —  Week 5 reference (Thursday exercise)
===========================================================

SETUP
-----
Same .env as Week 4 (GROQ_API_KEY). Same Groq client.
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq


MODEL = "llama-3.3-70b-versatile"

# One prompt, reused at every temperature. A slightly "creative" prompt
# shows the effect more dramatically than a factual one.
PROMPT = "Give me a one-sentence name and tagline for a new ice-cream shop."

# The dial, from 'locked down' to 'wild'. 2.0 is near the max Groq allows.
TEMPERATURES = [0.0, 0.7, 1.5]

# Run each temperature a few times so the pattern is obvious:
# low temp barely changes between runs; high temp changes a lot.
RUNS_PER_TEMP = 3


def load_client():
    """Load the API key and return a ready Groq client, or exit clearly."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Missing GROQ_API_KEY in .env. Add it and run again.")
        sys.exit(1)
    return Groq(api_key=key)


def ask(client, prompt, temperature):
    """Send one prompt at one temperature. Return the text answer."""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=temperature,
        max_tokens=60,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


def main():
    client = load_client()

    print(f"Prompt: {PROMPT}\n")
    for temp in TEMPERATURES:
        print(f"================  temperature = {temp}  ================")
        for run in range(1, RUNS_PER_TEMP + 1):
            answer = ask(client, PROMPT, temp)
            print(f"  run {run}: {answer}")
        print()

    print("Notice: at 0.0 the runs are nearly identical. As temperature\n"
          "climbs, the runs drift apart and get more inventive (and\n"
          "sometimes weirder). That's the dial.")


if __name__ == "__main__":
    main()
