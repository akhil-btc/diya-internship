"""
grounded_qa.py  —  Week 6 reference (Thursday exercise)
=======================================================
MENTOR REFERENCE. The single most important reference of the program,
because it's the brain of her capstone in miniature.

THE TECHNIQUE — "grounding"
---------------------------
A normal LLM call asks the model from its TRAINING. That's where
hallucinations live: it guesses when it doesn't know.

A *grounded* call PUTS THE SOURCE TEXT INSIDE THE PROMPT, then INSTRUCTS
the model to answer ONLY from that text. Two consequences:

  - The model has nothing to "guess from" — the source is right there.
  - When the answer isn't in the source, it's allowed (in fact REQUIRED)
    to say so. That kills hallucination at the root.

This is the entire idea behind every "ChatGPT with my docs" / "AI search"
/ RAG product on earth. Diya's link-summarizer capstone is exactly this
pattern, just with a URL fetcher bolted onto the front. Week 7 adds the
URL fetcher. THIS week proves the brain works.
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq


MODEL = "llama-3.3-70b-versatile"

# A short, self-contained "article". Deliberately fictional so it CAN'T
# be in the model's training data — any correct answer must come from
# the prompt itself. That's the cleanest possible demo of grounding.
ARTICLE = """
On 12 March 2024, the Riverside High School robotics team won the
Greenfield Regional Championship with their robot, codenamed "Marigold".
The team was captained by 11th-grader Priya Menon and coached by Mr.
Daniel Okafor. Marigold scored 142 points in the final round, narrowly
beating the defending champions, Hillcrest Academy, who scored 138. The
team will compete in the State Finals in Bengaluru on 4 May 2024.
Funding for the trip was provided by the school's PTA and a local
sponsor, Apex Engineering.
"""

# The grounded system prompt has FOUR jobs:
#   1. ROLE        - who the model is being
#   2. SOURCE      - hand it the article as the only source of truth
#   3. CONSTRAINT  - "answer ONLY from this text"
#   4. REFUSAL     - "if not in the text, say so plainly"
SYSTEM_PROMPT = f"""You are a careful research assistant for a student.

You will be given a SOURCE ARTICLE and a QUESTION. Follow these rules
without exception:
  - Answer using ONLY information from the SOURCE ARTICLE below.
  - If the answer is not in the article, reply EXACTLY:
    "That isn't in this article."
  - Do not use outside knowledge, do not guess, do not invent details.
  - Keep answers to two sentences or fewer.

SOURCE ARTICLE:
\"\"\"
{ARTICLE.strip()}
\"\"\"
"""

# Three test questions designed to exercise the grounding:
QUESTIONS = [
    "Who captained the Riverside robotics team?",          # IN the article
    "What is Priya Menon's favourite subject?",            # NOT in the article
    "How many points did Hillcrest score in the final?",   # IN the article
]


def load_client():
    """Load the API key and return a ready Groq client, or exit clearly."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Missing GROQ_API_KEY in .env. Add it and run again.")
        sys.exit(1)
    return Groq(api_key=key)


def ask(client, question):
    """Same low temperature for every question — we want the GROUNDING
    to be doing the work, not randomness."""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.1,
        max_tokens=120,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content.strip()


def main():
    client = load_client()
    for question in QUESTIONS:
        print(f"\nQ: {question}")
        print(f"A: {ask(client, question)}")

    print("\n--------------------------------------------------------")
    print("Notice: the questions IN the article are answered crisply.\n"
          "The question NOT in the article gets refused with the exact\n"
          "phrase we asked for. No hallucination. The model didn't get\n"
          "smarter -- we gave it a source and a rule. That's grounding.")


if __name__ == "__main__":
    main()
