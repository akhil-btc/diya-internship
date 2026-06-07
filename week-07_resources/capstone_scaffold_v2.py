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
<Diya's sharpened v3 rubric goes here — role + 6 criteria +
OUTPUT FORMAT section + ABSOLUTE RULES section, all in one block.>
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
    label, prompt_text = pick_essay_prompt()
    print(f"\nWorking on: {label}")

    scores1 = run_one_round(client, prompt_text, "round-1")
    input("\nRevise your draft using the questions above. Save as a new "
          ".txt file. Press ENTER when ready...")
    scores2 = run_one_round(client, prompt_text, "round-2")

    compare_rounds(scores1, scores2)


if __name__ == "__main__":
    main()
