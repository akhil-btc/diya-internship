"""
  1. A MENU of essay prompts (not one hardcoded prompt)
  2. FILE-BASED draft input (she edits her essay in a real doc,
     the tool reads from disk -- pasting essays into a terminal is
     misery and she'll never use the tool if it's painful)
  3. FUNCTIONS, not a top-level script. Each step is its own function
     so she can swap, debug, and reuse them.
  4. AN ITERATION LOOP: round 1 feedback -> she revises in her doc ->
     round 2 feedback. This is what makes it a TOOL.
  5. SCORE EXTRACTION + COMPARISON: pull the rubric scores out of each
     round's feedback so she can SEE whether her revision worked. This
     is the closest thing to a "did it improve" signal she'll get.
"""

import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


MODEL = "llama-3.3-70b-versatile"

# MENU: a small starter set of Common App prompts. She can add more.
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

# PLACEHOLDER -- Diya pastes her sharpened rubric in here. The rest of
# the file does NOT change. This is the whole reason it's separated.
RUBRIC_SYSTEM_PROMPT = """\
Your job is to give brutally honest feedback on the essay draft they give you, based on the following rubric. You will give a score of 1-5 for each criterion, and a short comment about what was done well or could be improved. Then you will ask three revision questions that push the student to sharpen the single weakest point, add a concrete scene or moment, and find their unique voice.
The student will give you  their DRAFT response. You will evaluate the draft against the
rubric below. do NOT rewerite, or provide sample sentences. do NOT rewrite the essay.

RUBRIC (score each 1-5 and give one short comment about improvement of what was done well):
  1. SPECIFICITY: does the draft have vived and specific details that let the reader know about their life? or is it boring and filler ("you would benefit so much by having me go to yur college. i can bring a lot to your campus.")
  2. VOICE: Does the writing have a distinctive teenage voice — concrete word choices, sentence-length variety, surprising images? Or does it sound generic and textbook-like (abstract nouns, 'I learned that...' summaries, no personality)? Score 1–5 and quote one line from the draft as evidence.
  3. STRUCTURE: Is there a clear arc — an opening hook, development,
     and a meaningful insight or turn? Or does it list things?
  4. SHOW, DON'T TELL: Does the draft DRAMATISE moments, or just CLAIM
     things ("music taught me discipline") without showing them? the best example would be the book thief- narrated by death itself.
  5. STAKES: After reading, does the reader understand something
     specific about THIS person? Or could this essay have been written
     by anyone? ("It would be an honor for me to be here. i work hard, submit my work on timee, and am always willing to connect with others") things that anyone could say about themselves is not valuable in an essay.
     
     does it have a clear "so what?" about why the reader should care about this person? 
  6. GRAMMAR AND STYLE: is the writing clear and easy to read? or are there mistakes that distract the reader and make it hard to understand? remember, this is a college-level essay, so it should be polished and well-written.
     Does it use basic vocabulary, like "cool" or "good" instead of more precise and vivid words? does it have awkward phrasing or run-on sentences that make it hard to read? does it have spelling mistakes or typos that show a lack of care? these things matter, because they can make the reader think the student is lazy or careless, even if they have a good story to tell.

Must enforce output format:
  1. Specificity: N/5 -- does the draft have vived and specific details that let the reader know about their life? or is it boring and filler ("you would benefit so much by having me go to yur college. i can bring a lot to your campus.")
  2. Voice: N/5 -- Does the writing have a distinctive teenage voice — concrete word choices, sentence-length variety, surprising images? Or does it sound generic and textbook-like (abstract nouns, 'I learned that...' summaries, no personality)? Score 1–5 and quote one line from the draft as evidence.
  3. Structure: N/5 -- Is there a clear arc — an opening hook, development,
     and a meaningful insight or turn? Or does it list things?
  4. Show, don't tell: N/5 -- Does the draft DRAMATISE moments, or just CLAIM
     things ("music taught me discipline") without showing them? the best example would be the book thief- narrated by death itself.
  5. Stakes: N/5 -- After reading, does the reader understand something
     specific about THIS person? Or could this essay have been written
     by anyone? ("It would be an honor for me to be here. i work hard, submit my work on timee, and am always willing to connect with others") things that anyone could say about themselves is not valuable in an essay.
followed by three revision questions.
Must include the absolute rule: do NOT rewrite the essay.>
"""


def load_client():
    """Load the API key, return a ready Groq client, exit cleanly if missing."""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Missing GROQ_API_KEY in .env.")
        sys.exit(1)
    return Groq(api_key=key)


def pick_essay_prompt():
    """Show the menu, return the (label, text) the user picked."""
    print("\nWhich essay prompt are you working on?\n")
    for i, (label, _) in enumerate(ESSAY_PROMPTS, 1):
        print(f"  {i}. {label}")
    choice = input("\nEnter number: ").strip()
    return ESSAY_PROMPTS[int(choice) - 1]


def read_draft(path):
    """Read a draft from a .txt file the student wrote in their doc app."""
    p = Path(path)
    if not p.exists():
        print(f"No file found at: {path}")
        sys.exit(1)
    return p.read_text()


def get_feedback(client, essay_prompt_text, draft):
    """Run the rubric on a draft. Same low temperature both rounds so the
    rubric (not randomness) is what's grading."""
    user_message = (
        f"ESSAY PROMPT:\n{essay_prompt_text}\n\n"
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


def extract_scores(feedback_text):
    """Pull '<criterion>: N/5' patterns from the feedback. Returns
    {criterion -> int}. Depends on the rubric enforcing the exact format
    -- which is why the system prompt's FORMAT section matters."""
    pattern = re.compile(
        r"^\s*\d+\.\s*([A-Za-z, '\-]+?):\s*(\d)\s*/\s*5", re.MULTILINE
    )
    return {m.group(1).strip(): int(m.group(2))
            for m in pattern.finditer(feedback_text)}


def compare_rounds(r1, r2):
    """Print a small table of round-1 vs round-2 scores per criterion."""
    print("\nIteration comparison:")
    print(f"  {'Criterion':<22} {'Round 1':>8} {'Round 2':>8}   change")
    for k in r1:
        if k not in r2:
            continue
        diff = r2[k] - r1[k]
        arrow = "up" if diff > 0 else ("down" if diff < 0 else "same")
        print(f"  {k:<22} {r1[k]:>8} {r2[k]:>8}   {arrow}")


def save(path, text):
    """Write feedback to disk so she can read it carefully, not skim it."""
    Path(path).write_text(text)
    print(f"  saved -> {path}")


def main():
    client = load_client()
    label, prompt_text = pick_essay_prompt()
    print(f"\nWorking on: {label}")

    # --- ROUND 1 ---
    path1 = input("\nPath to your round-1 draft (.txt): ").strip()
    draft1 = read_draft(path1)
    feedback1 = get_feedback(client, prompt_text, draft1)
    print("\n========== ROUND 1 FEEDBACK ==========\n")
    print(feedback1)
    save("feedback_round1.txt", feedback1)
    scores1 = extract_scores(feedback1)

    # --- REVISE OFFLINE ---
    input(
        "\nRevise your draft in your doc, using the questions above. "
        "Save it as a new .txt file. Press ENTER when ready..."
    )

    # --- ROUND 2 ---
    path2 = input("Path to your round-2 draft (.txt): ").strip()
    draft2 = read_draft(path2)
    feedback2 = get_feedback(client, prompt_text, draft2)
    print("\n========== ROUND 2 FEEDBACK ==========\n")
    print(feedback2)
    save("feedback_round2.txt", feedback2)
    scores2 = extract_scores(feedback2)

    # --- DID IT IMPROVE? ---
    compare_rounds(scores1, scores2)


if __name__ == "__main__":
    main()
