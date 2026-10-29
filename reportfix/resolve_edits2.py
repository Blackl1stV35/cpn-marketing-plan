"""Round 2 of the resolution of the three open items: fixes adopted from the first Haiku verification round (29 Oct 2026).

Usage:
  python -I resolve_edits2.py SCRATCHPAD build DUMP.json    -> checks finds against the live dump, writes reportfix/req_resolve2.json
  python -I resolve_edits2.py SCRATCHPAD local [--write]    -> local mirrors + deck specs + outline + corrections log (dry run unless --write)
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
    ("R1a",
     "or 4.4 points at a 25% base, to be significant 8 times in 10. K1 is therefore read as a trend over the Q2 to Q4 waves, not as a single-wave pass test.",
     "or about 4.5 points at a 25% base, to be significant 8 times in 10. K1 is therefore read as a trend over the Q2 to Q4 waves and used as a warning trigger (risk 10), not as a pass test for any gate."),
    ("R1b",
     "as its contact, and whether The1 Central Limited is the data controller, and whether its aggregated outputs for members aged 18 and 19 raise the same guardian question as the survey, are left to the Thai-law reader below; until then the K2 figures for ages 18 and 19 are provisional.",
     "as its contact. Whether The1 Central Limited is the data controller, and whether its aggregated outputs for members aged 18 and 19 raise the same guardian question as the survey, are left to the Thai-law reader below, whose answer is due with S1 by the end of January 2027, before the baseline is built; until then the K2 figures for ages 18 and 19 are provisional."),
    ("R2",
     "ages 18 and 19 provisional until the Thai-law check (Section 4.5)",
     "ages 18 and 19 provisional until the Thai-law check, due by the end of January 2027 (Section 4.5)"),
    ("R3",
     "which only the active-member data in K2 cover (Section 4.5)",
     "which only the active-member data in K2 cover, provisionally (Section 4.5)"),
    ("R4",
     "base ฿328 million in FY2027E; G4 requires the tactics thresholds and reports the all-net-new ones (Table 6.2)",
     "base ฿328 million in FY2027E and ฿696 million in FY2028E; G4 requires the tactics thresholds and reports the all-net-new ones (Table 6.2)"),
    ("R5",
     "FY2028 repeat at or below the same ceiling (Chapter 5 assumes a repeat); the full ฿560 million need not be repaid for this release (that needs ฿933 million and 67%, K12)",
     "FY2028 repeat at or below the same ceilings (฿2,760 million gross, ฿560 million net-new; Chapter 5 assumes a repeat); the full ฿560 million need not be repaid for this release (that needs ฿933 million of uplift and 67% pass-through, K12)"),
    ("R6",
     "and K2 tests it for active members only while the row applies it to all visits by the band",
     "and K2 tests it for active members only while the row applies it to all visits by the band."),
]

DECK_EDITS = [
    ("specs/slide_B6.json",
     "Gate G4, but only in part. It requires the tactics break-even (฿400m uplift, pass-through above 29%); the full ฿560m needs ฿933m and 67%, reported at G4 but not required. A miss limits FY2028 to the tactics that passed.",
     "Gate G4, but only in part. It requires the tactics break-even (฿400m uplift, pass-through above 29%). The full ฿560m needs ฿933m uplift and 67% pass-through: reported at G4, not required, so a pass can release a repeat the base case does not repay (FY2028E uplift ฿696m). A miss limits FY2028 to the tactics that passed.", 1),
    ("specs/slide_B6.json",
     "The full 560 million needs 933 million and 67 percent, which G4 reports but does not require.",
     "The full 560 million needs 933 million of uplift and 67 percent pass-through. G4 reports that test but does not require it, so a pass can release a repeat that the base case does not repay; its FY2028E uplift is 696 million.", 1),
    ("specs/slide_B6.json",
     "the full 560m needs 933m and 67%, reported, not required\"",
     "the full 560m needs 933m uplift and 67% pass-through, reported, not required; the base case does not repay a repeat (FY2028E uplift 696m)\"", 1),
    ("specs/slide_B6.json",
     "The baseline and gates G2 to G4 test the frequency and lift; the 25% share is not measured directly, as K1 is the 20–29 share of visitors aged 20+.",
     "Gates G2 and G3 test the lift and the active-member frequency (at least +5% each) and G4 the uplift they produce; the 25% share is not measured directly, as K1 is the 20–29 share of visitors aged 20+.", 1),
    ("specs/slide_B6.json",
     "and the baseline and gates test the frequency and lift; the 25% share is not measured directly, because K1 is the 20 to 29 share of visitors aged 20 and over.",
     "and gates two and three test the lift and the active-member frequency, gate four the uplift they produce; the 25% share is not measured directly, because K1 is the 20 to 29 share of visitors aged 20 and over.", 1),
    ("specs/slide_B6.json",
     "\"on_slide\": \"Q4: The baseline and gates G2 to G4 test them\"",
     "\"on_slide\": \"Q4: Gates G2 and G3 test lift and active-member frequency; G4 tests the uplift they produce\"", 1),
    ("specs/slide_B5.json",
     "Gen Z visits per active member under +5% at G3; Q4 gain under 3.1 points",
     "Gen Z visits per active member under +5% at G3; K1 gain under 3.1 points at Q4", 1),
    ("specs/slide_10.json",
     "inside a ฿560 million net-new cap; a failed gate holds or cuts the next release.",
     "inside a ฿560 million net-new cap a year; a failed gate holds or cuts the next release.", 1),
    ("build_deck.py",
     "Keep caveats off the main slides; the only one (The Central Phaholyothin date) sits in the B2 footnote.",
     "Keep caveats off the main slides; they sit in the B2 footnote (The Central Phaholyothin date) and on the B6 cards.", 1),
    ("src/corrections.md",
     "those figures are provisional until the Thai-law reader confirms the consent basis.",
     "those figures are provisional until the Thai-law reader confirms the consent basis (due with S1 by the end of January 2027, before the baseline is built).", 1),
    ("src/corrections.md",
     "80% power needs 5.1 / 4.4 points, so K1 is read as a trend.",
     "80% power needs 5.1 / about 4.5 points, so K1 is read as a trend and used as a warning trigger (risk 10), not as a gate pass test.", 1),
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
    json.dump(reqs, open(os.path.join(RF, "req_resolve2.json"), "w", encoding="utf-8"), ensure_ascii=False)
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
