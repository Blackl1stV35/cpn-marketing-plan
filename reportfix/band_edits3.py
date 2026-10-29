"""Round 3 of the measurement-band change: fixes adopted from the second Haiku verification round (29 Oct 2026).

Usage:
  python -I band_edits3.py SCRATCHPAD build DUMP.json     -> checks every find against the live dump, writes reportfix/req_band3.json
  python -I band_edits3.py SCRATCHPAD local [--write]     -> local mirrors + deck specs (dry run unless --write)
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
    ("C1",
     "(a team definition, not CPN's) and measures them in two ways.",
     "(a team definition, not CPN's) and measures their visits in two ways."),
    ("C2",
     "so ages 18 and 19 are seen only there, and only as members.",
     "so ages 18 and 19 are seen only there, and only as members (their visits as non-members are not measured)."),
    ("C3",
     "whom the team treats as able to consent alone because s.20 asks for a guardian only for minors.",
     "whom the team treats as able to consent alone (the age of majority under the Civil and Commercial Code; s.20 asks for a guardian for minors)."),
    ("C4",
     "72-hour breach drill, surveys limited to respondents aged 20 and over (S1)",
     "72-hour breach drill, S4 survey limited to respondents aged 20 and over (S1)"),
    ("C5",
     "aggregated extracts only; surveys limited to respondents aged 20 and over; count-only counters",
     "aggregated extracts only; S4 survey limited to respondents aged 20 and over; count-only counters"),
]

DECK_EDITS = [
    ("specs/slide_07.json", "so it covers 20 to 29; member data cover active members 18 to 29.", "so it measures 20 to 29; member data cover active members 18 to 29.", 1),
    ("specs/slide_B6.json", "so it measures 20–29; member data cover members 18–29", "so it measures 20–29; member data cover active members 18–29", 2),
    ("specs/slide_B6.json",
     "The baseline and gates G2 to G4 test them; the 25% share itself is not measured directly, as K1 is the 20–29 share of visitors aged 20+.",
     "The baseline and gates G2 to G4 test the frequency and lift; the 25% share is not measured directly, as K1 is the 20–29 share of visitors aged 20+.", 1),
    ("specs/slide_B6.json",
     "and the baseline and gates test them; the 25% share itself is not measured directly, because our survey reads only the 20 to 29 share of visitors aged 20 and over.",
     "and the baseline and gates test the frequency and lift; the 25% share is not measured directly, because K1 is the 20 to 29 share of visitors aged 20 and over.", 1),
    ("specs/slide_11.json", "surveys ages 20+ only", "S4 survey ages 20+ only", 3),
    ("specs/slide_B5.json", "surveys ages 20+ only", "S4 survey ages 20+ only", 3),
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
            print("\nAFTER [%d-%d]: %s" % (p["start"], p["end"], t2.strip()))
    reqs = [{"replaceAllText": {"containsText": {"text": o, "matchCase": True}, "replaceText": n, "tabsCriteria": {"tabIds": [TAB_B]}}} for _k, o, n in EDITS_B]
    json.dump(reqs, open(os.path.join(RF, "req_band3.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("\nrequests:", len(reqs), "| problems:", problems if problems else "none")
elif MODE == "local":
    write = "--write" in sys.argv
    for rel in ("ch456/ch4.md", "ch456/ch6.md", "ch456/publish/final_tab.md"):
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
