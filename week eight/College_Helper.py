"""
capstone_scaffold_v2.py  —  Week 7 reference (Thursday → Sunday)
================================================================
MENTOR REFERENCE. The v1 scaffold from Monday, hardened.

THE LESSON
----------
v1 was the spreadsheet — it worked when everything went right. v2 is
the tool that survives weird inputs and a flaky network. Three patterns
added, each one a real production move:

  1. INPUT VALIDATION (fail fast, fail clear). Check the draft before
     spending an API call on it. Empty? Too short? Tell the user, don't
     send garbage.

  2. TRY / EXCEPT around the API call (with ONE retry). Networks blip.
     Rate limits hit. The tool tells the user what happened, in plain
     English, instead of dumping a Python traceback at them.

  3. PARSER GRACEFUL DEGRADATION. If the model breaks format and the
     score regex(regular expressions) finds nothing, the tool says "couldn't parse scores"
     instead of silently showing an empty table.

THE PHILOSOPHY
--------------
**Fail loudly, recover gracefully.** When something goes wrong, the
tool tells the user clearly what happened AND what to do next. Never
crash with a traceback if you can help it. That's the difference
between a script someone wrote for themselves and a tool a friend can
use.

You should not copy this whole file. You should look at the three
NEW patterns and add the matching ones to your tool, keeping your style.
"""

import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


MODEL = "llama-3.3-70b-versatile"
MIN_DRAFT_WORDS = 50            # below this, the rubric has nothing to grade
MAX_DRAFT_WORDS = 1200          # above this, we're past most essay limits
RETRIES_ON_API_FAILURE = 1      # one extra try before giving up

ESSAY_PROMPTS = [
    ("Common App #1",
     "Some students have a background, identity, interest, or talent "
     "that is so meaningful they believe their application would be "
     "incomplete without it. If this sounds like you, share your story."),
    ("Common App #2",
     "The lessons we take from obstacles we encounter can be fundamental "
     "to later success. Recount a time when you faced a challenge, "
     "setback, or failure. How did it affect you, and what did you "
     "learn from the experience?"),
    ("Common App #5",
     "Discuss an accomplishment, event, or realization that sparked a "
     "period of personal growth and a new understanding of yourself or "
     "others."),
]

RUBRIC_SYSTEM_PROMPT = """\
Role: essay grader
Your job is to give brutally honest feedback on the essay draft they give you, based on the following rubric. You will give a score of 1-5 for each criterion, and a short comment about what was done well or could be improved. Then you will ask three revision questions that push the student to sharpen the single weakest point, add a concrete scene or moment, and find their unique voice.
The student will give you  their DRAFT response. You will evaluate the draft against the
rubric below. do NOT rewerite, or provide sample sentences. do NOT rewrite the essay.

Rubric and format. use this, do not deviate:
  1. SPECIFICITY N/5: does the draft have vived and specific details that let the reader know about their life? or is it boring and filler ("you would benefit so much by having me go to yur college. i can bring a lot to your campus.")
  2. VOICE N/5: Does the writing have a distinctive teenage voice — concrete word choices, sentence-length variety, surprising images? Or does it sound generic and textbook-like (abstract nouns, 'I learned that...' summaries, no personality)? Score 1–5 and quote one line from the draft as evidence.
  3. STRUCTURE N/5: Is there a clear arc — an opening hook, development,
     and a meaningful insight or turn? Or does it list things?
  4. SHOW, DON'T TELL N/5: Does the draft DRAMATISE moments, or just CLAIM
     things ("music taught me discipline") without showing them? the best example would be the book thief- narrated by death itself.
  5. STAKES N/5: After reading, does the reader understand something
     specific about THIS person? Or could this essay have been written
     by anyone? ("It would be an honor for me to be here. i work hard, submit my work on timee, and am always willing to connect with others") things that anyone could say about themselves is not valuable in an essay.
     
     does it have a clear "so what?" about why the reader should care about this person? 
  6. GRAMMAR AND STYLE N/5: is the writing clear and easy to read? and are all the words spelled correctly, no errors, at all? remember, this is a college-level essay, so it should be polished and well-written.
     Does it use basic vocabulary, like "cool" or "good" instead of more precise and vivid words? does it have awkward phrasing or run-on sentences that make it hard to read? does it have spelling mistakes or typos that show a lack of care? these things matter, because they 
     can make the reader think the student is lazy or careless, even if they have a good story to tell.
ABSOLUTE RULES — DO NOT BREAK:
  - Do NOT rewrite the essay or any portion of it.
  - Do NOT provide example replacement sentences for the student.
  - Do NOT add a "here's how I'd say it" or a model answer.
  - When you quote the draft, quote it EXACTLY in quotation marks.
  - Your job is to ask questions and point at things. The student writes.



"""


def load_client():
    """Load API key + return Groq client, or exit with a helpful message."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Missing GROQ_API_KEY in .env.")
        sys.exit(1)
    return Groq(api_key=key)


def pick_essay_prompt():
    print("\nWhich essay prompt are you working on?\n")
    for i, (label, _) in enumerate(ESSAY_PROMPTS, 1):
        print(f"  {i}. {label}")
    choice = input("\nEnter number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(ESSAY_PROMPTS)):
        print(f"  Pick a number between 1 and {len(ESSAY_PROMPTS)}.")
        sys.exit(1)
    return ESSAY_PROMPTS[int(choice) - 1]


# ---------- NEW PATTERN 1: INPUT VALIDATION ----------
def validate_draft(text):
    """Return (ok, message). The tool stops before wasting an API call
    on a draft that's too short, too long, or empty."""
    words = len(text.split())
    if words == 0:
        return False, "Your draft file is empty. Write something in it first."
    if words < MIN_DRAFT_WORDS:
        return False, (f"Your draft is {words} words — too short for the "
                       f"rubric to grade. Aim for at least "
                       f"{MIN_DRAFT_WORDS} words.")
    if words > MAX_DRAFT_WORDS:
        return False, (f"Your draft is {words} words — that's longer than "
                       f"most college essay limits. Trim to under "
                       f"{MAX_DRAFT_WORDS} before grading.")
    return True, f"Draft looks fine ({words} words). Grading now..."


def read_draft(path):
    p = Path(path)
    if not p.exists():
        print(f"No file found at: {path}")
        sys.exit(1)
    return p.read_text()


# ---------- NEW PATTERN 2: TRY/EXCEPT AROUND THE API ----------
def get_feedback(client, essay_prompt_text, draft):
    """Run the rubric on a draft. Retries once on API failure, then gives
    up with a clear message instead of a traceback."""
    user_message = (
        f"ESSAY PROMPT:\n{essay_prompt_text}\n\n"
        f"DRAFT:\n\"\"\"\n{draft.strip()}\n\"\"\""
    )
    last_error = None
    for attempt in range(RETRIES_ON_API_FAILURE + 1):
        try:
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
        except Exception as err:    # network blip, rate limit, etc.
            last_error = err
            if attempt < RETRIES_ON_API_FAILURE:
                print(f"  API call failed ({err}). Retrying once...")
                time.sleep(2)
    # Both tries failed. Tell the user something useful, not a traceback.
    print(f"\nCouldn't reach the model after {RETRIES_ON_API_FAILURE + 1} "
          f"tries. Last error: {last_error}")
    print("Check your internet, and that GROQ_API_KEY is still valid.")
    sys.exit(1)


# ---------- NEW PATTERN 3: PARSER GRACEFUL DEGRADATION ---------- Ignore this part
def extract_scores(feedback_text):
    """Pull '<criterion>: N/5' patterns. Returns a dict (possibly empty).
    The CALLER checks whether anything was parsed and responds."""
    pattern = re.compile(
        r"^\s*\d+\.\s*([A-Za-z, '\-]+?):\s*(\d)\s*/\s*5", re.MULTILINE
    )
    return {m.group(1).strip(): int(m.group(2))
            for m in pattern.finditer(feedback_text)}


def compare_rounds(r1, r2):
    """Tolerates missing criteria in either round (model broke format)."""
    if not r1 or not r2:
        print("\nCouldn't extract scores from one of the rounds, so no "
              "comparison table this run. The feedback is still above — "
              "your rubric's OUTPUT FORMAT section probably needs to be "
              "stricter.")
        return
    print("\nIteration comparison:")
    print(f"  {'Criterion':<22} {'Round 1':>8} {'Round 2':>8}   change")
    all_keys = set(r1) | set(r2)
    for k in sorted(all_keys):
        v1 = r1.get(k, "-")
        v2 = r2.get(k, "-")
        if isinstance(v1, int) and isinstance(v2, int):
            diff = v2 - v1
            arrow = "up" if diff > 0 else ("down" if diff < 0 else "same")
        else:
            arrow = "?"
        print(f"  {k:<22} {str(v1):>8} {str(v2):>8}   {arrow}")


def save(path, text):
    Path(path).write_text(text)
    print(f"  saved -> {path}")


def run_one_round(client, prompt_text, round_label):
    """One full round: read draft, validate, get feedback, save, parse."""
    path = input(f"\nPath to your {round_label} draft (.txt): ").strip()
    draft = read_draft(path)

    ok, message = validate_draft(draft)
    print(f"  {message}")
    if not ok:
        sys.exit(1)

    feedback = get_feedback(client, prompt_text, draft)
    print(f"\n========== {round_label.upper()} FEEDBACK ==========\n")
    print(feedback)
    save(f"feedback_{round_label.replace('-', '_')}.txt", feedback)
    return extract_scores(feedback)


def main():
    client = load_client()
    print("Welcome to the college essay helper!")
    print("This tool will give you feedback on your essay based on a prompt and a rubric.")
    print("You'll do two rounds of feedback, with a revision step in between.  ")
    print("Lets get started!")
    print("")
    print("")
    print("")
    print("Help: each score is graded out of five, from specificity, voice, structure, language use, and grammar.")
    label, prompt_text = pick_essay_prompt()
    print(f"\nWorking on: {label}")

    scores1 = run_one_round(client, prompt_text, "round-1")
    input("\nRevise your draft using the questions above. Save as a new "
          ".txt file. Press ENTER when ready...")
    scores2 = run_one_round(client, prompt_text, "round-2")

    compare_rounds(scores1, scores2)


if __name__ == "__main__":
    main()
