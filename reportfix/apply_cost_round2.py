import os, sys
sys.stdout.reconfigure(encoding="utf-8")
SP = sys.argv[1]
DECK = os.path.join(SP, "deck")
RF = os.path.join(SP, "reportfix")
SENT = "Plan-team time is not in these 11 lines; we assume it sits in existing SG&A (team assumption, not costed)."

def rd(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return f.read()

def wr(p, t):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)

p = os.path.join(DECK, "specs", "slide_B3.json")
lines = rd(p).split("\n")
idx = [i for i, ln in enumerate(lines) if ln.startswith('  "notes": "')]
assert len(idx) == 1, ("notes lines", len(idx))
ln = lines[idx[0]].rstrip("\r")
if ln.endswith('",'):
    suffix = '",'
elif ln.endswith('"'):
    suffix = '"'
else:
    raise SystemExit("unexpected notes line ending")
if SENT not in ln:
    ln = ln[: -len(suffix)] + " " + SENT + suffix
lines[idx[0]] = ln
wr(p, "\n".join(lines))
print("ok  B3 notes: cost assumption")

p = os.path.join(RF, "review_loop.md")
out = []
done = False
for raw in rd(p).split("\n"):
    if raw.startswith("| 15 |"):
        cells = raw.split("|")
        cells[3] = " report 6.2; deck B3 notes "
        cells[4] = " applied: B3 notes say plan-team time is outside the 2,760m and sits in existing SG&A (team assumption) "
        raw = "|".join(cells)
        done = True
    out.append(raw)
t = "\n".join(out)
if "Item 15 needs a decision." in t:
    t = t.replace("Item 15 needs a decision.", "Round 2 (30 Oct): item 15 applied in the B3 notes, on your instruction.")
else:
    t = t.rstrip("\n") + "\nRound 2 (30 Oct): item 15 applied in the B3 notes, on your instruction.\n"
wr(p, t)
print("ok  tracker row 15:", done)
