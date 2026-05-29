"""
essay_feedback.py  —  Week 6 reference (Thursday exercise)
==========================================================

THE NEW TECHNIQUE — "prompting to EVALUATE, not GENERATE"
---------------------------------------------------------
This prompt asks it to *judge* something — to apply a rubric to
text the user supplied. That's a fundamentally different kind of
cognitive work, and it unlocks a whole class of tools (essay feedback,
code review, study-quiz grading).

The three moves that make this work:

  1. RUBRIC AS SYSTEM PROMPT. Spell out the criteria the model should
     judge against. Without a rubric the model gives vague platitudes
     ("nice voice, good job"). With a rubric it gives surgical feedback.

  2. THE "DON'T WRITE IT FOR HER" CONSTRAINT. This is the integrity
     line. The model must NOT rewrite her essay or provide replacement
     sentences. If it does, the tool stops being a practice tool and
     becomes a cheating tool. Strict refusal language is required.

  3. STRUCTURED OUTPUT. The model returns scored feedback per criterion
     plus 3 revision questions. Same shape every time, which makes the
     tool feel like a real product and makes iteration measurable.

WHAT GOOD LOOKS LIKE
--------------------
ideally a quick stab at one
of the Common App prompts — and writes 3 sentences on (a) whether the
feedback was useful, (b) where it was generic, and (c) what she'd
sharpen in the rubric to make next round better. The tool itself isn't
the deliverable; the *iteration on the rubric* is.
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq


MODEL = "llama-3.3-70b-versatile"

# A real Common App prompt (option 1). Hardcoded for the demo; in her
# v0 she'll pick from a small list.
ESSAY_PROMPT = (
    "Some students have a background, identity, interest, or talent "
    "that is so meaningful they believe their application would be "
    "incomplete without it. If this sounds like you, share your story."
)

# A deliberately MEDIOCRE first draft — earnest but generic, tells-not-
# shows, no scenes. A good rubric should catch all of that. This is the
# kind of draft Diya's tool will see on Day 1.
SAMPLE_DRAFT = """
I have always loved music. Ever since I was young, I would listen to my
parents' old records and try to sing along. In middle school I joined
the choir and learned how to read music. I made many friends in choir
and we had a lot of fun performing at concerts. Music has taught me a
lot of things, like how to work with others and how to be patient. It
has also taught me discipline, because you have to practice every day
to get better. I think music will continue to be a big part of my life
in college and beyond.
"""

# The RUBRIC is the system prompt. This is where the whole intelligence
# of the tool lives. The five criteria are the ones admissions readers
# actually care about.
RUBRIC_SYSTEM_PROMPT = """You are a thoughtful college essay coach for a
10th-grade student. The student will give you (a) an essay PROMPT and
(b) their DRAFT response. You will evaluate the draft against the
rubric below.

RUBRIC (score each 1-5 and give one short comment):
  1. SPECIFICITY: Does the draft contain concrete scenes, real moments,
     sensory detail, specific names/places? Or is it abstract and
     general?
  2. VOICE: Does it sound like a real, distinctive teenager — or like a
     textbook / a generic application essay?
  3. STRUCTURE: Is there a clear arc — an opening hook, development,
     and a meaningful insight or turn? Or does it list things?
  4. SHOW, DON'T TELL: Does the draft DRAMATISE moments, or just CLAIM
     things ("music taught me discipline") without showing them?
  5. STAKES: After reading, does the reader understand something
     specific about THIS person? Or could this essay have been written
     by anyone?

OUTPUT FORMAT (use exactly this; do not deviate):

**Rubric scores**
1. Specificity: <score>/5 — <one-sentence comment quoting a line from
   the draft when relevant>
2. Voice: <score>/5 — <comment>
3. Structure: <score>/5 — <comment>
4. Show, don't tell: <score>/5 — <comment>
5. Stakes: <score>/5 — <comment>

**Three revision questions for the student**
- <a question that points at the single weakest point>
- <a question that pushes for a concrete scene or moment>
- <a question that asks 'what would only YOU say here?'>

ABSOLUTE RULES — DO NOT BREAK:
  - Do NOT rewrite the essay or any portion of it.
  - Do NOT provide example replacement sentences for the student.
  - Do NOT add a "here's how I'd say it" or a model answer.
  - When you quote the draft, quote it EXACTLY in quotation marks.
  - Your job is to ask questions and point at things. The student writes.
"""


def load_client():
    """Load the API key and return a ready Groq client, or exit clearly."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Missing GROQ_API_KEY in .env. Add it and run again.")
        sys.exit(1)
    return Groq(api_key=key)


def get_feedback(client, essay_prompt, draft):
    """Run one round of feedback. Low temperature so the rubric does the
    work, not randomness — we want feedback to be CONSISTENT across runs
    on the same draft."""
    user_message = (
        f"ESSAY PROMPT:\n{essay_prompt}\n\n"
        f"DRAFT:\n\"\"\"\n{draft.strip()}\n\"\"\""
    )
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        max_tokens=600,
        messages=[
            {"role": "system", "content": RUBRIC_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content.strip()


def main():
    client = load_client()
    print(f"ESSAY PROMPT:\n{ESSAY_PROMPT}\n")
    print(f"DRAFT (Diya's first try):\n{SAMPLE_DRAFT.strip()}\n")
    print("=" * 60)
    print("FEEDBACK:\n")
    print(get_feedback(client, ESSAY_PROMPT, SAMPLE_DRAFT))
    print("\n" + "=" * 60)
    print("Notice: the model did not rewrite a single sentence of the\n"
          "draft. It judged it against a rubric, scored each criterion,\n"
          "and ended with three questions for the student. That's the\n"
          "whole tool. The rubric IS the product.")


if __name__ == "__main__":
    main()
