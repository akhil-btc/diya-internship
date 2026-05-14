"""
compare_prompts.py
==================
Reference solution for Week 4 Wednesday exercise.

Asks the same question with 4 different system messages and saves
the four answers to compare_prompts_output.md.

The teaching point: the user message is identical across all 4 runs.
Only the *system message* changes — and the answers come back
completely different in tone, vocabulary, length, and structure.
That's the power of a system message.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


QUESTION = "Why do we sleep?"

SYSTEM_PROMPTS = {
    "poet":       "You are a poet. Answer in 4 lines of rhyming verse.",
    "5_year_old": "You are a 5-year-old. Use only short, simple words.",
    "wikipedia":  "You are a Wikipedia editor. Be neutral and factual.",
    "teacher":    "You are an enthusiastic teacher. Use analogies "
                  "and exclamation points.",
}


def load_key():
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Missing GROQ_API_KEY. Add it to .env first.")
        sys.exit(1)
    return key


def ask(client, system_message, user_message):
    """Send a system + user message pair and return the response text."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user",   "content": user_message},
        ],
    )
    return response.choices[0].message.content


def main():
    client = Groq(api_key=load_key())

    output_lines = [
        "# Same question, four different system prompts",
        "",
        f"**Question:** {QUESTION}",
        "",
        "---",
        "",
    ]

    for label, system_message in SYSTEM_PROMPTS.items():
        print(f"\n=== {label.upper()} ===")
        print(f"System: {system_message}\n")

        answer = ask(client, system_message, QUESTION)
        print(answer)

        output_lines.append(f"## {label}")
        output_lines.append("")
        output_lines.append(f"_System: {system_message}_")
        output_lines.append("")
        output_lines.append(answer)
        output_lines.append("")
        output_lines.append("---")
        output_lines.append("")

    Path("compare_prompts_output.md").write_text("\n".join(output_lines))
    print("\nSaved all four answers to compare_prompts_output.md")


if __name__ == "__main__":
    main()
