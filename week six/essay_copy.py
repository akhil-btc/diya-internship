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
When I began thinking seriously about college, I was drawn to Texas A&M University. The more I learned about the university, the more I saw a community that values leadership, service, and personal growth. Those qualities are what I hope to develop throughout my college experience.
My academic experiences have reinforced that interest. In Precalculus, I have spent hours working through problems that did not make sense the first time I looked at them. I remember filling an entire sheet of paper with calculations only to realize I had made a mistake near the beginning. Instead of starting over with frustration, I learned to carefully retrace my steps and find where things went wrong. In Spanish, I often found myself hesitant to speak because I was afraid of making mistakes in front of my classmates. Over time, I became more comfortable participating, even when I knew I might not say everything perfectly.
These experiences have shaped the type of student I want to become. I enjoy being challenged because challenges force me to grow. Whether I am practicing a difficult piece on the violin, solving a math problem, or speaking Spanish in class, I have learned that improvement rarely happens all at once. It comes from showing up consistently and putting in the effort each day
That mindset is one of the reasons Texas A&M appeals to me. I am excited by the idea of joining a university where students are encouraged to become leaders and contribute to something larger than themselves. I want to be part of a community that values hard work, service, and continuous improvement.When I think about what would make my application incomplete, I do not think about a single accomplishment or activity. I think about the habits I have built through years of practice, learning, and perseverance. Those experiences have influenced how I approach challenges and opportunities. As I look toward Texas A&M and the future beyond college, I hope to continue growing as a student, a leader, and a member of my community.
"""

# The RUBRIC is the system prompt. This is where the whole intelligence
# of the tool lives. The five criteria are the ones admissions readers
# actually care about.
RUBRIC_SYSTEM_PROMPT = """ You are a blunt english teacher. You have taught this kid all year on college levell writing skills. you want the best for your sttudents, but by no means are you going to be lenient with their mistakes. you want them to survive in the 
real world. Your job is to give brutally honest feedback on the essay draft they give you, based on the following rubric. You will give a score of 1-5 for each criterion, and a short comment about what was done well or could be improved. Then you will ask three revision questions that push the student to sharpen the single weakest point, add a concrete scene or moment, and find their unique voice.
The student will give you  their DRAFT response. You will evaluate the draft against the
rubric below.

RUBRIC (score each 1-5 and give one short comment about improvement of what was done well):
  1. SPECIFICITY: does the draft have vived and specific details that let the reader know about their life? or is it boring and filler ("you would benefit so much by having me go to yur college. i can bring a lot to your campus.")
  2. VOICE: Does it sound like a real, distinctive teenager — or like AI-generated blandness with no emotions behind the writing? remember, you have seen this kid grow all year. you know about their life, and when it sound lie they are lying
  3. STRUCTURE: Is there a clear arc — an opening hook, development,
     and a meaningful insight or turn? Or does it list things?
  4. SHOW, DON'T TELL: Does the draft DRAMATISE moments, or just CLAIM
     things ("music taught me discipline") without showing them? the best example would be the book thief- narrated by death itself.
  5. STAKES: After reading, does the reader understand something
     specific about THIS person? Or could this essay have been written
     by anyone? does it have a clear "so what?" about why the reader should care about this person? 
  6. GRAMMAR AND STYLE: is the writing clear and easy to read? or are there mistakes that distract the reader and make it hard to understand? remember, this is a college-level essay, so it should be polished and well-written.
     Does it use basic vocabulary, like "cool" or "good" instead of more precise and vivid words? does it have awkward phrasing or run-on sentences that make it hard to read? does it have spelling mistakes or typos that show a lack of care? these things matter, because they can make the reader think the student is lazy or careless, even if they have a good story to tell.

OUTPUT FORMAT (use exactly this; do not deviate):

**Rubric scores**
1. Specificity: <score>/5 — <one-sentence comment quoting a line from
   the draft when relevant>
2. Voice: <score>/5 — <comment>
3. Structure: <score>/5 — <comment>
4. Show, don't tell: <score>/5 — <comment>
5. Stakes: <score>/5 — <comment>
6. Grammar and Style: <score>/5 — <comment>


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

if __name__ == "__main__":
    main()
