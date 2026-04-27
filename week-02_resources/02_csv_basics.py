"""
02_csv_basics.py
================
Step-by-step walkthrough of csv.DictReader — the easiest, most reliable
way to read a CSV file in Python.

Make sure messy_marks.csv is in the same folder as this script before running.
"""

import csv


print("=" * 60)
print("SECTION 1 — reading the file the 'school way' (the painful way)")
print("=" * 60)

# This is what most beginners try first.
# It works, but you have to manually split commas and remember
# which column is which by counting positions. Easy to mess up.
with open("messy_marks.csv") as f:
    for line in f:
        parts = line.strip().split(",")
        # parts is now a list of strings: ["Arjun", "72", "88", "76", "69"]
        # And we'd have to remember "math is index 1, science is 2, ..."
        print(parts)
print()


print("=" * 60)
print("SECTION 2 — the real way: csv.DictReader")
print("=" * 60)

# DictReader treats the first row as column headers, and gives you
# every following row as a DICTIONARY. So instead of indexing by number,
# you access columns by NAME.
with open("messy_marks.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # row is a dict like {"student_name": "Arjun", "math": "72", ...}
        print(row)
        # Note: All values are strings! "72" not 72.
print()


print("=" * 60)
print("SECTION 3 — accessing columns by name")
print("=" * 60)

with open("messy_marks.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Pull out specific columns by their name
        name = row["student_name"]
        math_score = row["math"]
        print(f"{name} got {math_score} in math")
print()


print("=" * 60)
print("SECTION 4 — what columns does the file actually have?")
print("=" * 60)

# DictReader gives you the column headers in `reader.fieldnames`.
# This is useful when you don't want to hardcode column names.
with open("messy_marks.csv") as f:
    reader = csv.DictReader(f)
    print("Columns found in file:")
    for col in reader.fieldnames:
        # Notice anything weird?
        # The 'english' column has spaces around it: ' english '
        # That's because someone made the CSV sloppily. We have
        # to deal with this.
        print(f"  -> {col!r}")    # !r shows quotes around the string
print()


print("=" * 60)
print("SECTION 5 — cleaning up the messy column headers")
print("=" * 60)

# We can fix the whitespace by stripping each header.
with open("messy_marks.csv") as f:
    reader = csv.DictReader(f)
    # IMPORTANT: this only works if you read fieldnames first
    cleaned_headers = [h.strip() for h in reader.fieldnames]
    reader.fieldnames = cleaned_headers
    print("Cleaned columns:", reader.fieldnames)
    # Now you can use row["english"] without spaces
    for row in reader:
        print(f"{row['student_name']}'s english score: {row['english']}")
        break  # just show one row
print()


print("=" * 60)
print("SECTION 6 — skipping blank rows")
print("=" * 60)

# Some rows in our CSV are completely empty.
# Let's filter them out.
def is_blank(row):
    """Return True if every value in the row is empty/whitespace."""
    return all(value.strip() == "" for value in row.values())


with open("messy_marks.csv") as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [h.strip() for h in reader.fieldnames]
    valid_rows = [row for row in reader if not is_blank(row)]

print(f"Got {len(valid_rows)} non-blank rows")
print("First valid row:", valid_rows[0])


# ---------------------------------------------------------------------------
# What to remember
# ---------------------------------------------------------------------------
# 1. import csv  — built into Python, no install needed
# 2. csv.DictReader(file) gives each row as a dict, keyed by column name
# 3. reader.fieldnames = list of column names from the header row
# 4. ALL values from a CSV are strings — convert with int() or float() yourself
# 5. Always use `with open(...) as f:` so the file closes properly
# 6. Strip whitespace from headers if the CSV is messy
