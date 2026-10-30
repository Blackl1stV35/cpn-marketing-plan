"""Applies the 30 Oct 2026 text fixes to deck specs and the outline builder (exact match, counts checked).

Usage: python -I apply_deck_edits_30oct.py SCRATCHPAD
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
SP = sys.argv[1]
DECK = os.path.join(SP, "deck")
EDITS = [
    ("specs/slide_B2.json",
     '"cite": "The Story Thailand, 2025; Wikipedia, 2026"',
     '"cite": "The Story Thailand, 2025; Central Pattana Investor Relations, 2026"', 1),
    ("specs/slide_B6.json",
     '"cite": "Central Retail Corporation, 2026 (Sections 2-3 reference list)"',
     '"cite": "Central Retail Corporation, 2026 (reference list, Chapters 2 to 6)"', 1),
    ("specs/slide_B6.json",
     '"cite": "S&P Global, 2026 (Sections 2-3 reference list)"',
     '"cite": "S&P Global, 2026 (reference list, Chapters 2 to 6)"', 1),
    ("build_deck.py",
     "are in the Sections 2–3 list.",
     "are in the merged reference list.", 1),
]
problems = []
for rel, old, new, want in EDITS:
    p = os.path.join(DECK, rel.replace("/", os.sep))
    with open(p, encoding="utf-8-sig", newline="") as f:
        t = f.read()
    n = t.count(old)
    print("%s %s x%d (want %d): %s" % ("ok " if n == want else "BAD", rel, n, want, old[:60]))
    if n != want:
        problems.append(rel)
        continue
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t.replace(old, new))
print("problems:", problems or "none")
