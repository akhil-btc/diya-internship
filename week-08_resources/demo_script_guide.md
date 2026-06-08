# Capstone Demo — The Three-Part Structure

The biggest mistake students make demoing a capstone is the same as
the biggest mistake they make writing a college essay: they *explain*
when they should *show*. A demo is a tiny piece of theatre — it has a
hook, a body, and a takeaway. Five minutes total. Three parts.

---

## Part 1 — The 30-second hook  (why this exists)

The opening 30 seconds answer **three questions** in one breath:

1. **What does it do?** — One sentence, no jargon.
2. **Who's it for?** — Name them concretely. The more specific, the better.
3. **Why does it matter to *you*?** — The personal hook is the strongest possible motivator. *You are the user.*

If the audience tunes out anywhere in a demo, it's here. The hook
earns the next four minutes.

**Example shape (NOT the final version — she writes hers in her own
voice):**

> "This is a college essay practice tool. It gives high-schoolers
> rubric-based feedback on their drafts — *without* writing the essay
> for them. I built it because in eighteen months I'm going to be
> writing those essays for real, and the tool I wished existed didn't.
> So I made it."

That's 35 words. Three sentences. Done.

---

## Part 2 — The live walkthrough  (what it does)

Run the tool on a real draft. Narrate as you go. **3 to 3.5 minutes max.**

What to show, in this order:

- **Pick a Common App prompt** (5 seconds — "I'm working on prompt 1.")
- **Round 1 feedback** (45 seconds — scroll through it briefly, point at *one* sharp comment and *one* place the model quoted her actual line).
- **The revision** (60 seconds — show her round-1 draft and round-2 draft side by side, point at the *one specific sentence* she cut and the scene she replaced it with — say it explicitly: *"watch what changes — I replaced this CLAIM with this SCENE"*).
- **Round 2 feedback + the comparison table** (60 seconds — the number that moved. That's the punchline of the entire demo. The score table is her tool's *receipts.*).
- **One robustness moment** (30 seconds — feed it an empty file or a 3-word draft, show the friendly refusal. *"It doesn't crash. It tells you what to fix."*)

**What to skip:**
- The code. Nobody wants to see the code in a 5-minute demo. Mention the architecture in one sentence if asked, otherwise the code is for follow-up.
- Long pauses while you read the screen silently. Always narrate.
- The setup (env vars, API keys). Have it pre-loaded.

**Demo trick:** if the model does something weird live — a glitch, a
typo, a hallucinated detail — **name it.** "Watch — the model just
flagged a typo that isn't actually in the draft. That's called
hallucination; it happens even with the source in the prompt. It's
also exactly why my tool only flags things for the writer instead of
editing for them — because *I* can't fully trust it, but the *writer*
can verify." Owning the imperfection is more impressive than hiding it.

---

## Part 3 — The "what I learned" close  (why this matters)

The last 60 seconds. Not "thanks for watching." Two beats:

**Beat 1 — the one technical insight.** What did building this teach
her about prompts, or AI, or the gap between intention and behavior?
One sentence. Concrete.

> "The biggest thing I learned: the rubric is the soul of the tool.
> When the rubric is vague the feedback is vague — the same way a
> vague teacher gives vague comments. Most of my time wasn't writing
> code, it was writing the rubric better."

**Beat 2 — the one personal insight.** What did using her own tool on
her own writing teach her about *writing*? This is the unexpected one,
and it's what makes the demo memorable.

> "The other thing I learned wasn't about AI. My tool told me my
> essay's opening was generic — and I tried to fix it by writing a
> better-sounding sentence. The tool told me again. Three times. The
> real fix wasn't a better sentence — it was a scene. That distinction
> between *claims* and *scenes* I'm going to use the rest of my life."

That second beat is the line the audience walks out remembering.

---

## The total budget

| Part                | Time          |
| ------------------- | ------------- |
| Hook                | 30 seconds    |
| Live walkthrough    | 3 – 3.5 min   |
| What I learned      | 60 seconds    |
| Q&A buffer          | 30 seconds    |
| **Total**           | **~5 min**    |

If it's running long, the live walkthrough is what to cut from. The
hook and the close are non-negotiable.

---

## Three rules for the demo prep this week

1. **Practice it out loud, alone, at least three times.** Once silent
   in your head doesn't count. The first time you hear yourself say a
   sentence, you find the rough words.
2. **Practice it once with a non-technical adult** (a parent, a
   sibling, anyone). If they understand the hook, the hook is right.
3. **Have a "if it breaks live" plan.** API down? Talk through the
   architecture using the code on screen. Tool gives weird output?
   Name it and explain why. *Never apologize for the model's behavior
   as if it's your fault* — narrate it as a researcher would.
