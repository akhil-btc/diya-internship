"""
assistant_template.py  —  Week 6 reference (Tuesday/Wednesday exercise)
=======================================================================
MENTOR REFERENCE. The "build a specialised assistant" exercise. This is
the seed of her capstone: a real, reusable mini-tool powered almost
entirely by a well-written system prompt.

THE LESSON
----------
You can turn a general model into a SPECIFIC tool without any new model
code -- just a carefully written system prompt. The two power moves here:

  - A strong ROLE + FORMAT system prompt (who it is, how it must answer)
  - FEW-SHOT examples: show it 1-2 finished examples so it copies the
    pattern instead of guessing. Examples beat instructions when you
    need a consistent format.

RUN IT
------
    python assistant_template.py "the water cycle"
    python assistant_template.py "what is an API"
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq


MODEL = "llama-3.3-70b-versatile"

# ROLE + FORMAT: this is what turns a generic model into a specific tool.
SYSTEM_PROMPT = (
    "You are 'Study Buddy', a friendly tutor for 10th-grade students. "
    "For any topic the student gives you, answer in EXACTLY this format:\n\n"
    "**In one line:** <a plain-English definition, no jargon>\n"
    "**Picture it:** <one everyday analogy>\n"
    "**Why it matters:** <one sentence on why a teenager should care>\n\n"
    "Never exceed 60 words total. Never break the format."
)

# FEW-SHOT: one finished example locks the pattern far better than
# instructions alone. The model will copy this shape.
FEW_SHOT = [
    {"role": "user", "content": "photosynthesis"},
    {"role": "assistant", "content": (
        "**In one line:** Plants turn sunlight, water, and air into food.\n"
        "**Picture it:** Like a tiny solar-powered kitchen inside every leaf.\n"
        "**Why it matters:** It's where almost all the food and oxygen you "
        "use actually comes from."
    )},
]


def load_client():
    """Load the API key and return a ready Groq client, or exit clearly."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Missing GROQ_API_KEY in .env. Add it and run again.")
        sys.exit(1)
    return Groq(api_key=key)


def study_buddy(client, topic):
    """Answer one topic in the Study Buddy format."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(FEW_SHOT)          # show it the example first
    messages.append({"role": "user", "content": topic})

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.5,
        max_tokens=150,
        messages=messages,
    )
    return response.choices[0].message.content.strip()


def main():
    topic = " ".join(sys.argv[1:]) or "recursion"
    client = load_client()
    print(study_buddy(client, topic))


if __name__ == "__main__":
    main()
