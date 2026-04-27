"""
03_combined.py
==============
Putting csv.DictReader + sorted() together to solve the actual exercise:
  - Read the messy CSV
  - Compute each student's total score across all subjects
  - Print the top 3

This is a SIMPLER version of the full assignment — for now, we treat
missing/invalid scores as 0 instead of properly ignoring them.
That's fine for learning the structure today. On Wednesday you'll
add try/except to handle invalid scores properly.
"""

import csv


def is_blank(row):
    """Return True if every value in the row is empty/whitespace."""
    return all(value.strip() == "" for value in row.values())


def to_score(value):
    """
    Convert a CSV cell to an integer.
    Returns 0 if the cell is missing or not a number.
    (We'll improve this on Wednesday with try/except.)
    """
    cleaned = value.strip()
    if cleaned == "" or cleaned in ("N/A", "absent"):
        return 0
    if cleaned.isdigit():
        return int(cleaned)
    return 0


# ---------------------------------------------------------------------------
# Step 1 — read the CSV using DictReader
# ---------------------------------------------------------------------------
with open("messy_marks.csv") as f:
    reader = csv.DictReader(f)
    # Clean up sloppy whitespace in headers (' english ' -> 'english')
    reader.fieldnames = [h.strip() for h in reader.fieldnames]
    rows = [row for row in reader if not is_blank(row)]

# Figure out which columns are subjects (everything except 'student_name')
subject_columns = [col for col in reader.fieldnames if col != "student_name"]
print(f"Found {len(rows)} students, subjects: {subject_columns}\n")


# ---------------------------------------------------------------------------
# Step 2 — for each student, compute total score
# ---------------------------------------------------------------------------
students = []   # will become a list of (name, total) tuples
for row in rows:
    name = row["student_name"].strip()
    if not name:
        continue
    total = 0
    for subject in subject_columns:
        total += to_score(row[subject])
    students.append((name, total))

print("All students with their totals:")
for name, total in students:
    print(f"  {name}: {total}")
print()


# ---------------------------------------------------------------------------
# Step 3 — sort the list, descending by total, and take the top 3
# ---------------------------------------------------------------------------
# Remember from 01_sorted_basics.py:
#   key=lambda pair: pair[1]   ->   "compare on the second element (total)"
#   reverse=True               ->   "highest first"
#   [:3]                       ->   "first 3 only"
top_3 = sorted(students, key=lambda pair: pair[1], reverse=True)[:3]


# ---------------------------------------------------------------------------
# Step 4 — print the final report
# ---------------------------------------------------------------------------
print("=== Top 3 students ===")
for rank, (name, total) in enumerate(top_3, start=1):
    print(f"  {rank}. {name} — {total}")


# ---------------------------------------------------------------------------
# What to take from this script
# ---------------------------------------------------------------------------
# 1. Read CSV with DictReader -> each row is a dict
# 2. Build a list of (key, value) tuples that you can sort
# 3. Use sorted(..., key=..., reverse=True)[:N] to get the top N
# 4. enumerate(..., start=1) is the cleanest way to add ranks
#
# Things you'll improve later this week:
# - Wednesday: replace to_score() with proper try/except
# - Wednesday: also compute averages per subject (ignoring invalid)
# - Wednesday: report which students had missing data (and which subjects)
