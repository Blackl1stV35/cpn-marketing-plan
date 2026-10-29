"""Round 2 of the measurement-band change: wording fixes after the Haiku verification round (29 Oct 2026).

Usage:
  python -I band_edits2.py SCRATCHPAD build DUMP.json     -> checks every find against the live dump, writes reportfix/req_band2.json
  python -I band_edits2.py SCRATCHPAD local [--write]     -> local mirrors + deck specs (dry run unless --write)
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
    ("B1",
     "s.20), so it measures ages 20 to 29.",
     "s.20), so the plan uses it for ages 20 to 29."),
    ("B2",
     "borrowed for illustration from the team's assumed 18–29 share of visits in Table 5.2 row C1 and not an estimate of K1",
     "borrowed for illustration from the team's assumed 18 to 29 share of visits in Table 5.2 row C1 and not an estimate of K1"),
    ("B3",
     "(the survey part of the 18–29 Gen Z and young-adult band)",
     "(the part of the 18–29 Gen Z and young-adult band that the survey reaches)"),
    ("B4",
     ", and only respondents aged 20 and over are surveyed, in every wave (the team treats them as able to consent alone under s.20).",
     ". The intercept survey reaches only respondents aged 20 and over, in every wave, whom the team treats as able to consent alone because s.20 asks for a guardian only for minors."),
    ("B5",
     "respondents aged 20 and over only, in every wave of the S4 intercept survey",
     "the S4 intercept survey limited to respondents aged 20 and over, in every wave"),
]

S7_NOTES_OLD = "We define Gen Z and young adults as ages 18 to 29. Our survey reaches only people aged 20 and over, the age of majority, so it covers 20 to 29; member data cover members 18 to 29. We found no CPN age split of visits, so we set a baseline by 31 March 2027. The only published comparator, 14.7 percent for ages 13 to 24, is a different band. Four indicators track proposed targets."
S7_NOTES_NEW = "We define Gen Z and young adults as ages 18 to 29. Our survey reaches only people aged 20 and over, the age of majority, so it covers 20 to 29; member data cover active members 18 to 29. We found no CPN age split of visits, so we set a baseline by 31 March 2027. The only published comparator, 14.7 percent for ages 13 to 24, is another band. Four indicators track proposed targets."

DECK_EDITS = [
    ("specs/slide_07.json", S7_NOTES_OLD, S7_NOTES_NEW, 1),
    ("specs/slide_B6.json",
     "The baseline and gates G2 to G4 test them; the visit share only by proxy (K1 is ages 20–29).",
     "The baseline and gates G2 to G4 test them; the 25% share itself is not measured directly, as K1 is the 20–29 share of visitors aged 20+.", 1),
    ("specs/slide_B6.json",
     "and the baseline and gates test them, the visit share only by proxy because our survey measures 20 to 29.",
     "and the baseline and gates test them; the 25% share itself is not measured directly, because our survey reads only the 20 to 29 share of visitors aged 20 and over.", 1),
    ("specs/slide_B6.json",
     "(age of majority; younger need a guardian, PDPA s.20)",
     "(age of majority; younger people would need a guardian on our reading of PDPA s.20)", 2),
    ("specs/slide_B6.json",
     "Gen Z and young adults means ages 18–29; our survey reaches only respondents aged 20 and over, the age of majority, so it measures 20 to 29, and member data cover members 18 to 29; younger respondents would need a guardian under the PDPA.",
     "Gen Z and young adults means ages 18 to 29; our survey reaches only respondents aged 20 and over, the age of majority, so it measures 20 to 29, and member data cover active members 18 to 29; younger respondents would need a guardian under the PDPA, which a Thai-law reader should confirm.", 1),
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
    json.dump(reqs, open(os.path.join(RF, "req_band2.json"), "w", encoding="utf-8"), ensure_ascii=False)
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
