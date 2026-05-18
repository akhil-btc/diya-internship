"""
hello_llm.py
============
Reference solution for Week 4 Tuesday exercise.

Diya's first solo LLM call. Loads the API key from .env, sends a
single user message, prints the response.

Run it three times in a row and you will get slightly different
answers each time — that variation is the topic for Thursday.
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq


PROMPT = (
    "In 3 sentences, explain to me what a Large Language Model is, "
    "like I'm a 10th grader."
)


def load_key():
    """Load GROQ_API_KEY from .env or exit with a friendly message."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print(
            "Missing GROQ_API_KEY.\n"
            "1. Get a free key at https://console.groq.com\n"
            "2. Create a .env file with: GROQ_API_KEY=your_key_here\n"
            "3. Make sure .env is in your .gitignore"
        )
        sys.exit(1)
    return key


def ask(client, user_message):
    """Send a single user message and return the response text."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": user_message}],
    )
    return response.choices[0].message.content


def main():
    client = Groq(api_key=load_key())
    answer = ask(client, PROMPT)
    print(answer)


if __name__ == "__main__":
    main()
