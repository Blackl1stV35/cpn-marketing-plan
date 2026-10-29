"""Round 4 (last) of the resolution of the three open items: small fixes from the third Haiku round (29 Oct 2026).

Usage:
  python -I resolve_edits4.py SCRATCHPAD build DUMP.json    -> checks finds against the live dump, writes reportfix/req_resolve4.json
  python -I resolve_edits4.py SCRATCHPAD local [--write]    -> local mirrors + deck specs + corrections log (dry run unless --write)
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
    ("V1",
     "The 1 member data cover active members aged 18 to 29, so ages 18 and 19 are seen only there, and only as members",
     "The 1 member data, once The1 Central Limited supplies the extract by age band, cover active members aged 18 to 29, so ages 18 and 19 are seen only there, and only as members"),
    ("V2",
     "K1 is therefore read as a trend over the Q2 to Q4 waves and used as a warning trigger (risk 10), not as a pass test for any gate.",
     "K1 is therefore read across the Q2 to Q4 waves and used only as a warning trigger (risk 10), never as a pass test for any gate."),
    ("V3",
     "K1 gain (the 20–29 share of visitors aged 20 and over) below the significance threshold at the Q4 wave (about 3.1 points at a 25% base share, 3.6 at 50%)",
     "K1 gain from the baseline to the Q4 wave (the 20–29 share of visitors aged 20 and over) below the significance threshold (about 3.1 points at a 25% base share, 3.6 at 50%)"),
]

DECK_EDITS = [
    ("specs/slide_B5.json",
     "K1 gain under its threshold (3.1 points at a 25% base) at Q4",
     "K1 gain under its threshold (3.1 points at a 25% base, 3.6 at 50%) at Q4", 1),
    ("specs/slide_B5.json",
     "K1 gain (the 20–29 share of visitors aged 20 and over) below the significance threshold at the Q4 wave (about 3.1 points at a 25% base share, 3.6 at 50%)",
     "K1 gain from the baseline to the Q4 wave (the 20–29 share of visitors aged 20 and over) below the significance threshold (about 3.1 points at a 25% base share, 3.6 at 50%)", 1),
    ("src/corrections.md",
     "so K1 is read as a trend and used as a warning trigger (risk 10), not as a gate pass test.",
     "so K1 is read across the waves and used only as a warning trigger (risk 10), never as a gate pass test.", 1),
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
    reqs = [{"replaceAllText": {"containsText": {"text": o, "matchCase": True}, "replaceText": n, "tabsCriteria": {"tabIds": [TAB_B]}}} for _k, o, n in EDITS_B]
    json.dump(reqs, open(os.path.join(RF, "req_resolve4.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("requests:", len(reqs), "| problems:", problems if problems else "none")
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
