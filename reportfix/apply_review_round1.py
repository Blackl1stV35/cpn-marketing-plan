"""Round 1 of the 30 Oct 2026 review: applies the deck fixes and updates the loop tracker.

Usage: python -I apply_review_round1.py SCRATCHPAD
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
SP = sys.argv[1]
DECK = os.path.join(SP, "deck")
RF = os.path.join(SP, "reportfix")


def rd(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return f.read()


def wr(p, t):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


# 1. B4 notes: the international-row assumption (item 16)
p = os.path.join(DECK, "specs", "slide_B4.json")
t = rd(p)
old = "which is defined as target-met, passes."
new = old + " The international row applies the 13.7% visit share to revenue, which assumes a foreign visit earns the same as a Thai visit (team assumption, not tested)."
assert t.count(old) == 1, ("B4", t.count(old))
wr(p, t.replace(old, new))
print("ok  B4 notes (item 16)")

# 2. Outline checklist sentence (review status)
p = os.path.join(DECK, "build_deck.py")
t = rd(p)
old = "and the report was aligned with the deck. B6 sources outside Chapters 4 to 6"
new = "and the report was aligned with the deck. Re-checked 30 Oct 2026 (32 points): deck points applied, report points open. B6 sources outside Chapters 4 to 6"
assert t.count(old) == 1, ("outline", t.count(old))
wr(p, t.replace(old, new))
print("ok  outline checklist sentence")

# 3. Loop tracker: status column per item
STATUS = {
    1: "report, after reset (deck keys already match the Sections 2-3 list)",
    2: "report, after reset",
    3: "consistent: deck says 23M everywhere; no change",
    4: "not in the new deck (the 200 figure is in the frozen presented deck); report after reset",
    5: "deck has no growth column, nothing to change; report appendix table vs bullet, after reset",
    6: "not in the new deck (no 5.3% there); report 5.2 after reset",
    7: "deck consistent ('four business lines' in B2); report 2.4 after reset",
    8: "deck uses the MD&A NLA (about 100,000 sq m) only; reconciliation in report after reset",
    9: "deck consistent (S4, B3 say team proposal, not CPN guidance); report Ch3 after reset",
    10: "report after reset; deck facts cite the budget as Section 4.5 (internal), fix then",
    11: "deck consistent (S2 defines F1, S4 lists the objectives); report Ch3 after reset",
    12: "deck facts cite Wikipedia (internal); needs a primary source, after reset",
    13: "not in the new deck; report after reset",
    14: "fixed in deck (S3, 33.55% y/y in 2025); report fixed 29 Oct",
    15: "DECISION NEEDED: state that plan-team time sits in existing SG&A (team assumption)?",
    16: "applied: B4 notes state the foreign-visit assumption; 32.97m year not used in deck",
    17: "not cited in the new deck; report after reset",
    18: "deck consistent (35.5% team floor; CPN figures explained in B6 Q12)",
    19: "not in the new deck; report after reset",
    20: "deck consistent with appendix (presented deck differs and is frozen)",
}
for n in range(21, 33):
    STATUS[n] = "report ch4, after reset"

p = os.path.join(RF, "review_loop.md")
done = 0
out = []
for ln in rd(p).split("\n"):
    if ln.startswith("| ") and ln.count("|") >= 5:
        cells = ln.split("|")
        try:
            n = int(cells[1].strip())
        except ValueError:
            out.append(ln)
            continue
        cells[4] = " " + STATUS[n] + " "
        ln = "|".join(cells)
        done += 1
    out.append(ln)
t = "\n".join(out).rstrip("\n") + "\n\nRound 1 (30 Oct): deck fixes applied (item 16 in B4, outline checklist line). Item 15 needs a decision. The rest waits for the reset.\n"
wr(p, t)
print("ok  tracker rows updated:", done)
