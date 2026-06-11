# Diya — what you built, what you learned, what's next

*A document for after the program. Print it, save it, dog-ear it. Re-read
it in a year. Some of this won't make sense yet — that's fine.*

---

## 1. What you actually built

You built a college essay practice tool that gives rubric-based
feedback on your drafts and refuses to write the essay for you. It has
a menu of Common App prompts, a real iteration loop (round 1 → revise →
round 2), a score comparison table, input validation, retry logic on
API failure, and graceful degradation when the parser doesn't find
scores. It's three hundred lines of code with a fifty-line rubric that
is the actual product.

You did this at fifteen. Most people who get paid to build AI tools
build less interesting things.

---

## 2. The arc you went through (so you can see it from outside)

**Weeks 1–3 — foundations.** Python you already knew got cleaner.
You learned to read and write CSVs and JSON. You met your first APIs.
You learned about secrets and `.env` files — which is not a small
thing; most adult engineers learn it the embarrassing way.

**Week 4 — your first LLM calls.** Hello world. A news brief. The
moment a real model talked back to your code. You felt the difference
between "I read about AI" and "I'm using AI."

**Week 5 — under the hood.** Tokens, the context window, hallucination,
temperature. You ran experiments on each one. You proved with your own
hands that Hindi takes more tokens than English (and you found out why).
You learned the model isn't a search engine.

**Week 6 — the craft.** Prompt engineering as a discipline. Role,
context, specificity, format, examples, iteration. You learned to
write *systems* in English. You learned the prompt-as-rubric move —
asking the model to JUDGE instead of GENERATE.

**Weeks 7–8 — the capstone.** You designed the brain, built the body,
hardened it, and now you can demo it. You went from spec to ship in
two weeks. You discovered that your own tool was more honest than your
revision, which is the kind of lesson you can't get anywhere else.

---

## 3. The lessons that outlive the code

These are the things you can re-use everywhere. Bookmark them.

**A prompt is a spec, not a wish.** Amateurs wish. Pros specify —
who, what, for whom, in what shape. This applies to people too.

**The rubric is the soul of the tool.** When the rubric is vague, the
feedback is vague. The same is true of any judgement — by a teacher, a
boss, a friend. The clearer the standard, the sharper the verdict.

**Hallucination is what happens when "plausible" and "true" come
apart.** The model picks what's likely to come next, not what's likely
to be true. Confidence is not proof. *Trust it for shape, verify it
for facts.*

**Revision is restructuring, not appending.** When you read feedback,
the temptation is to *add words around* the problem. The work is to
*cut the problem* and put something different in its place. This
applies to essays, code, designs, presentations, and arguments.

**Cut claim, replace with scene.** When your writing is generic, the
fix is almost never a better-sounding claim. The fix is a specific
moment — a place, a time, a single thing that happened. You internalised
this on the last call. It will make you a better writer for the rest
of your life.

**Fail loudly, recover gracefully.** When something breaks, tell the
user clearly what happened and what to do. Never crash silently. Never
crash with a traceback in someone's face. This is true of software,
and also of being a person.

**Models are teammates, not oracles.** The first prompt is a draft.
The first answer is a draft. The first version is a draft. Iterate.
You do this with humans too — your best collaborators are the ones who
take a sketch and improve it, not the ones who refuse to start unless
the request is perfect.

---

## 4. What to do in the next 30 days

**Use your own tool on a real essay.** When you write something for
school in the next month — an English essay, a history paper, a
personal statement — run it through your tool. See what your tool
flags. Practice the claim → scene move. The tool gets useful only when
you use it.

**Keep an "I wish something existed" notebook.** Every time you think
"I wish a thing could do X for me," write it down. You will be ten
times better at noticing problems than your peers because you now
*know what's buildable.* The note doesn't have to lead anywhere — it's
the practice of noticing.

**Read one prompt a week.** Find a real AI tool you use — Anthropic and
OpenAI publish their system prompts; many open-source tools have theirs
on GitHub. Read them. Notice the levers. Notice the rules. Notice the
structure. You'll learn faster by reading good prompts than by writing
mediocre ones.

**Write code once a week, even if it's tiny.** Twenty lines is enough.
The muscle goes soft fast. A small script for your schedule, a parser
for your music library, a thing that fetches something. Don't lose the
keyboard.

---

## 5. What to do in the next year

**Build one more small thing.** Pick one entry from your "I wish"
notebook. Build a v0. Show it to someone. The second project will go
twice as fast because you already know the shape.

**When you write your real college essays, use the tool.** That's the
test. You built it for a future version of yourself. In about a year,
that version of yourself will exist. Use it.

**Don't lose Python.** Codecademy or freeCodeCamp for thirty minutes a
week is enough. Don't let the muscle go.

**Watch Karpathy when you're ready.** Andrej Karpathy has a series of
free videos called "Neural Networks: Zero to Hero." It will be over
your head right now. In about a year it won't be. When you're ready,
start with "Let's build GPT from scratch." It will change how you
think about all of this.

**Try Claude / ChatGPT for actual schoolwork — but as a teammate, not
an autocompleter.** Brainstorm with it. Have it critique your drafts.
Ask it to explain things you don't understand. Never let it write
something *for* you that someone thinks *you* wrote. That's the same
rule your essay tool has, and it's right.

---

## 6. When to message me

- When you ship a v1 of something new. Even if it's tiny. I want to see.
- When you get into your college of choice and you used the tool to
  write the essay. That is the success metric of this whole program.
- When you hit a bug you can't beat and you've been stuck on it for
  more than a day. That's information, not failure.
- When something you build helps someone else. Tell me who, and how.
- When you're nineteen and you're picking what to study next. We can
  talk.

You don't need permission to message me before any of that. The door is
open.

---

## 7. One last thing

The thing that surprised me about working with you is how much you
*kept noticing on your own*. The skateboarding tangent in your memory
test. The temperature drift in your scores. The "rucurrung" typo your
tool let through. The hallucinated "resturaunts" in feedback you didn't
mention — but I bet you saw it. That noticing is the real engineering
skill. The code is just the way you write it down.

Keep noticing.

— Akhil
