"""Round 3 of the resolution of the three open items: fixes adopted from the second Haiku verification round (29 Oct 2026).

Usage:
  python -I resolve_edits3.py SCRATCHPAD build DUMP.json    -> checks finds against the live dump, writes reportfix/req_resolve3.json
  python -I resolve_edits3.py SCRATCHPAD local [--write]    -> local mirrors + deck specs + corrections log (dry run unless --write)
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
SP = sys.argv[1]
MODE = sys.argv[2]
RF = os.path.join(SP, "reportfix")
DECK = os.path.join(SP, "deck")
TAB_B = "t.8nyhv8rr5vec"

EDITS_B = [
    ("T1",
     "whose answer is due with S1 by the end of January 2027, before the baseline is built; until then",
     "whose answer is due with S1 by the end of January 2027, before any 18 or 19 figure is used; until then"),
    ("T2",
     "smallest significant change between waves 3.6 points at a 50% base and 3.1 points at a 25% base share, borrowed",
     "smallest significant change between waves 3.6 points at a 50% base share and 3.1 points at a 25% base share, borrowed"),
    ("T3",
     "below the 3.1-point significance threshold at the Q4 wave",
     "below the significance threshold at the Q4 wave (about 3.1 points at a 25% base share, 3.6 at 50%)"),
    ("T4",
     "and the smallest significant wave-to-wave change is 6.9 points (team calculation)",
     "and the smallest significant wave-to-wave change (5% level, two-sided) is 6.9 points at a 50% base (team calculation)"),
    ("T5",
     "significant change 3.6 points at a 50% base share and 3.1 points at an illustrative 25% base share (team calculation)",
     "smallest significant change between waves (5%, two-sided) 3.6 points at a 50% base share and 3.1 points at an illustrative 25% base share (team calculation)"),
]

DECK_EDITS = [
    ("specs/slide_B6.json",
     "The full ฿560m needs ฿933m uplift and 67% pass-through: reported at G4, not required, so a pass can release a repeat the base case does not repay (FY2028E uplift ฿696m).",
     "The full ฿560m needs ฿933m uplift and 67% pass-through; G4 reports that test but does not require it, so a pass can release a repeat the base case does not repay (FY2028E uplift ฿696m).", 1),
    ("specs/slide_B6.json",
     "It requires the tactics break-even, 400 million of uplift and pass-through above 29 percent; below that FY2028 is limited to the tactics that passed.",
     "It requires the tactics break-even, 400 million of uplift and pass-through above 29 percent. If it is missed, FY2028 is limited to the tactics that passed.", 1),
    ("specs/slide_B5.json",
     "Gen Z visits per active member under +5% at G3; K1 gain under 3.1 points at Q4",
     "Gen Z visits per active member under +5% at G3; K1 gain under its threshold (3.1 points at a 25% base) at Q4", 1),
    ("specs/slide_B5.json",
     "below the 3.1-point significance threshold at the Q4 wave",
     "below the significance threshold at the Q4 wave (about 3.1 points at a 25% base share, 3.6 at 50%)", 1),
    ("src/corrections.md",
     "before the baseline is built).",
     "before any 18 or 19 figure is used).", 1),
]


def rd(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return f.read()


def wr(p, t):
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


problems = []
if MODE == "build":
    sys.path.insert(0, RF)
    import docparse
    d = docparse.load(sys.argv[3])
    tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
    ps = docparse.paragraphs(tabs[TAB_B])
    print("revision:", d["revisionId"])
    for key, old, new in EDITS_B:
        hits = [p for p in ps if old in p["text"]]
        n = sum(p["text"].count(old) for p in hits)
        print("%s %s: %d hit(s) [%s]" % ("OK " if n == 1 else "BAD", key, n, ", ".join(str(p["start"]) for p in hits)))
        if n != 1:
            problems.append((key, n))
    for p in ps:
        t2 = p["text"]
        for _k, o, n in EDITS_B:
            t2 = t2.replace(o, n)
        if t2 != p["text"]:
            print("\nAFTER [%d-%d]: %s" % (p["start"], p["end"], t2.strip()[:600]))
    reqs = [{"replaceAllText": {"containsText": {"text": o, "matchCase": True}, "replaceText": n, "tabsCriteria": {"tabIds": [TAB_B]}}} for _k, o, n in EDITS_B]
    json.dump(reqs, open(os.path.join(RF, "req_resolve3.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("\nrequests:", len(reqs), "| problems:", problems if problems else "none")
elif MODE == "local":
    write = "--write" in sys.argv
    for rel in ("ch456/ch4.md", "ch456/ch5.md", "ch456/ch6.md", "ch456/publish/final_tab.md"):
        p = os.path.join(SP, rel.replace("/", os.sep))
        t = rd(p)
        out = t
        for key, old, new in EDITS_B:
            n = out.count(old)
            if n:
                print("  %s %s x%d" % (rel, key, n))
            out = out.replace(old, new)
        if write and out != t:
            wr(p, out)
    for rel, old, new, want in DECK_EDITS:
        p = os.path.join(DECK, rel.replace("/", os.sep))
        t = rd(p)
        n = t.count(old)
        ok = n == want
        if not ok:
            problems.append((rel, old[:50], n))
        print("  %s %s x%d (want %d): %s" % ("ok " if ok else "BAD", rel, n, want, old[:60]))
        if write and ok:
            wr(p, t.replace(old, new))
    print("PROBLEMS:", problems if problems else "none", "| WRITE" if write else "| DRY RUN")
