"""
01_sorted_basics.py
===================
Step-by-step walkthrough of sorted() with key= and reverse=.

Run each section and read its output before moving to the next.
Live-coding suggestion: comment everything out, uncomment one section
at a time, run, discuss, then move on.
"""

print("=" * 60)
print("SECTION 1 — sorted() on simple lists")
print("=" * 60)

# sorted() takes any list and returns a NEW sorted list.
# It does NOT modify the original.
nums = [5, 2, 8, 1, 9]
print("Original:", nums)
print("Sorted ascending:", sorted(nums))
print("Sorted descending:", sorted(nums, reverse=True))
print("Original is unchanged:", nums)
print()


print("=" * 60)
print("SECTION 2 — sorted() on a list of tuples")
print("=" * 60)

# What if our data is pairs, like (name, score)?
# By default, sorted compares the FIRST element of each tuple.
scores = [
    ("Diya", 84),
    ("Aarav", 73),
    ("Priya", 95),
    ("Rohan", 80),
]
print("Default sort (by name, alphabetical):")
print(sorted(scores))
# Output: sorted alphabetically by name. But that's not what we want!
print()


print("=" * 60)
print("SECTION 3 — sorted() with key= to choose what to compare on")
print("=" * 60)

# We don't want to sort by name. We want to sort by SCORE (the 2nd element).
# We tell sorted() what to look at using key=
# key= takes a function. The function says "given this item, what should
# I compare on?"

# Way 1: Using lambda (a one-line anonymous function)
# pair[1] means "the second element of the tuple"
sorted_by_score = sorted(scores, key=lambda pair: pair[1])
print("Sorted by score (ascending):")
print(sorted_by_score)
print()

# Way 2: Same thing but descending — just add reverse=True
sorted_by_score_desc = sorted(scores, key=lambda pair: pair[1], reverse=True)
print("Sorted by score (descending — the highest scorers first):")
print(sorted_by_score_desc)
print()


print("=" * 60)
print("SECTION 4 — getting the TOP 3 with slicing [:3]")
print("=" * 60)

# Once the list is sorted with the highest scores first, the top 3
# are just the first 3 elements. Use slicing: [:3] means
# "from the start up to (but not including) index 3".
top_3 = sorted_by_score_desc[:3]
print("Top 3:")
print(top_3)
print()

# We can loop through with enumerate() to get a rank number.
# enumerate(list, start=1) gives (1, first_item), (2, second_item), ...
print("Top 3 with rank:")
for rank, (name, score) in enumerate(top_3, start=1):
    print(f"  {rank}. {name} — {score}")
print()


print("=" * 60)
print("SECTION 5 — putting it all together")
print("=" * 60)

# In one line: sort by score descending, take top 3, print with rank.
all_students = [
    ("Diya", 84),
    ("Aarav", 73),
    ("Priya", 95),
    ("Rohan", 80),
    ("Saanvi", 89),
    ("Ishaan", 77),
]

print("All students:")
for name, score in all_students:
    print(f"  {name}: {score}")

top_3 = sorted(all_students, key=lambda pair: pair[1], reverse=True)[:3]

print("\nTop 3:")
for rank, (name, score) in enumerate(top_3, start=1):
    print(f"  {rank}. {name} — {score}")


# ---------------------------------------------------------------------------
# What to remember
# ---------------------------------------------------------------------------
# 1. sorted(list)              -> ascending, by first element
# 2. sorted(list, reverse=True) -> descending
# 3. sorted(list, key=...)     -> sort by something other than the default
# 4. key= takes a FUNCTION that says "given an item, what should we
#    compare on?". `lambda pair: pair[1]` means "give me the 2nd element"
# 5. [:3] slices the first 3 elements
# 6. enumerate(list, start=1) gives you a rank number alongside each item
