import fitz, re, sys
sys.stdout.reconfigure(encoding="utf-8")
pdf = fitz.open(sys.argv[1])
bad = 0
for i, pg in enumerate(pdf, 1):
    t = re.sub(r"\s+", " ", pg.get_text())
    for pat in ("detectable", "detection limit", "reviewed, not required", "G2 to G4 test", "wave 1", "adults only", "footfall share gain"):
        if re.search(pat, t):
            print("page", i, "still has:", pat)
            bad += 1
print("deck leftovers:", bad)
