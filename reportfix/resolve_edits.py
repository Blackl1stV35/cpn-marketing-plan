"""Resolves the three items left open on 29 Oct 2026: gate G4, consent for 18-19 year-old members, and the significance-threshold wording.

Decisions:
 1. G4 keeps the tactics break-even test (tightening to 933m/67% would fail the base case, FY2028E uplift 696m, and force a re-run of FY2028E);
    the report and deck now say that the full 560m is reported at G4, not required.
 2. The 1 data for ages 18-19 are provisional until the Thai-law reader confirms the consent basis.
 3. 3.6 / 3.1 / 6.9 points are the smallest SIGNIFICANT change between waves (5%, two-sided); a true +4 is significant about 6 times in 10 at a 50% base
    and 7 in 10 at a 25% base; 80% power needs 5.1 / 4.4 points; K1 is read as a trend over waves Q2-Q4.
 Plus: C1 applies +10% to all visits by the band while K2 tests members only; K15 fragment.

Usage:
  python -I resolve_edits.py SCRATCHPAD build DUMP.json    -> checks finds against the live dump, writes reportfix/req_resolve.json
  python -I resolve_edits.py SCRATCHPAD local [--write]    -> local mirrors + deck specs + corrections log (dry run unless --write)
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
    # ---- item 1: G4 (text only; the rule stays)
    ("G1",
     "FY2028 repeat at or below the same ceiling (Chapter 5 assumes a repeat)",
     "FY2028 repeat at or below the same ceiling (Chapter 5 assumes a repeat); the full ฿560 million need not be repaid for this release (that needs ฿933 million and 67%, K12)"),
    ("G2",
     "against the 50% assumed in Table 5.2 row C5 (Section 5.1); base ฿328 million in FY2027E",
     "against the 50% assumed in Table 5.2 row C5 (Section 5.1); base ฿328 million in FY2027E; G4 requires the tactics thresholds and reports the all-net-new ones (Table 6.2)"),
    # ---- item 2: consent for ages 18 and 19 in The 1 data
    ("M1",
     "and whether The1 Central Limited is the data controller is left to the Thai-law reader below.",
     "and whether The1 Central Limited is the data controller, and whether its aggregated outputs for members aged 18 and 19 raise the same guardian question as the survey, are left to the Thai-law reader below; until then the K2 figures for ages 18 and 19 are provisional."),
    ("M2",
     "(the plan band; K1 covers only its 20–29 part, and the 13–24 comparator is a different band), per quarter (S2)",
     "(the plan band; K1 covers only its 20–29 part, and the 13–24 comparator is a different band), per quarter (S2); ages 18 and 19 provisional until the Thai-law check (Section 4.5)"),
    # ---- C1 applies +10% to all visits; K2 tests members only
    ("C1",
     "adopts the +10% frequency as a [Proposed] target (K2); it is set equal to the assumption and is not evidence for it",
     "adopts the +10% frequency as a [Proposed] target (K2); it is set equal to the assumption and is not evidence for it, and K2 tests it for active members only while the row applies it to all visits by the band"),
    # ---- K15 fragment
    ("K15",
     "(S1); confirmed breaches",
     "(S1); count of confirmed breaches"),
    # ---- item 3: significance wording and power
    ("S1",
     "the smallest detectable change between waves is about 3.6 points at a 50% base share and about 3.1 points at a 25% base share, borrowed for illustration from the team's assumed 18 to 29 share of visits in Table 5.2 row C1 and not an estimate of K1 (team calculation, simple random sampling, so minimums).",
     "the smallest significant change between waves (5% level, two-sided) is about 3.6 points at a 50% base share and about 3.1 points at a 25% base share, borrowed for illustration from the team's assumed 18 to 29 share of visits in Table 5.2 row C1 and not an estimate of K1 (team calculation, simple random sampling, so minimums). A true gain of 4 points would be significant about 6 times in 10 at a 50% base and 7 times in 10 at a 25% base; it takes a true gain of about 5.1 points at a 50% base, or 4.4 points at a 25% base, to be significant 8 times in 10. K1 is therefore read as a trend over the Q2 to Q4 waves, not as a single-wave pass test."),
    ("S2",
     "detects 3.6 points at a 50% base share and 3.1 points at an illustrative 25% base share (team calculation)",
     "significant change 3.6 points at a 50% base share and 3.1 points at an illustrative 25% base share (team calculation)"),
    ("S3",
     "smallest detectable change 3.6 points at a 50% base and 3.1 points at a 25% base share, borrowed for illustration from the team's assumed 18–29 share of visits in Table 5.2 row C1 (team calculation, n = 1,500)",
     "smallest significant change between waves 3.6 points at a 50% base and 3.1 points at a 25% base share, borrowed for illustration from the team's assumed 18–29 share of visits in Table 5.2 row C1 (team calculation, n = 1,500); a true +4 is significant about 6 to 7 times in 10"),
    ("S4",
     "the smallest detectable wave-to-wave change is 6.9 points",
     "the smallest significant wave-to-wave change is 6.9 points"),
    ("S5",
     "above the detection limit of 6.9 points at a 50% base",
     "above the significance threshold of 6.9 points at a 50% base"),
    ("S6",
     "M1, M2 and M5 targets confirmed above the detection limits",
     "M1, M2 and M5 targets confirmed above the significance thresholds"),
    ("S7",
     "below the 3.1-point detection limit at the Q4 wave",
     "below the 3.1-point significance threshold at the Q4 wave"),
]

Q7_CARD_OLD = "G4 requires ฿400m uplift and pass-through above 29% (tactics break-even); a miss limits FY2028 to tactics that passed. The full ฿560m needs ฿933m and 67%: reviewed, not required."
Q7_CARD_NEW = "Gate G4, but only in part. It requires the tactics break-even (฿400m uplift, pass-through above 29%); the full ฿560m needs ฿933m and 67%, reported at G4 but not required. A miss limits FY2028 to the tactics that passed."

DECK_EDITS = [
    ("specs/slide_B6.json", Q7_CARD_OLD, Q7_CARD_NEW, 1),
    ("specs/slide_B6.json",
     "G4 requires the tactics break-even, 400 million of uplift and pass-through above 29 percent; below that FY2028 is limited to the tactics that passed. The full 560 million needs 933 million and 67 percent, which G4 reviews but does not require.",
     "Gate G4, but only in part. It requires the tactics break-even, 400 million of uplift and pass-through above 29 percent; below that FY2028 is limited to the tactics that passed. The full 560 million needs 933 million and 67 percent, which G4 reports but does not require.", 1),
    ("specs/slide_B6.json",
     '"on_slide": "Q7: G4 requires 400m uplift and pass-through above 29%; the full 560m needs 933m and 67%"',
     '"on_slide": "Q7: Gate G4 only in part: tactics break-even (400m uplift, pass-through above 29%); the full 560m needs 933m and 67%, reported, not required"', 1),
    ("specs/slide_B6.json",
     "which G4 reviews with all Table 6.3 KPIs but does not require",
     "which G4 reports beside the tactics test but does not require (Table 6.2 row G4 and K12 now say so; tightening to 933 million and 67% would fail the base case, whose FY2028E uplift is 696 million, and force a re-run of FY2028E)", 1),
    ("specs/slide_B6.json",
     "member data cover active members 18–29",
     "member data cover active members 18–29 (18–19 provisional)", 2),
    ("specs/slide_B6.json",
     "which a Thai-law reader should confirm.",
     "which a Thai-law reader should confirm; The 1 data for ages 18 and 19 are aggregated and provisional until then.", 1),
    ("specs/slide_B5.json",
     "below the 3.1-point detection limit at the Q4 wave",
     "below the 3.1-point significance threshold at the Q4 wave", 1),
    ("src/corrections.md",
     "Surveys reach respondents aged 20 and over, so the survey band is 20-29 and ages 18-19 are seen only in The 1 member data (decided 29 Oct 2026).",
     "Surveys reach respondents aged 20 and over, so the survey band is 20-29 and ages 18-19 are seen only in The 1 member data (decided 29 Oct 2026); those figures are provisional until the Thai-law reader confirms the consent basis. G4 (decided 29 Oct 2026): the pass test stays the tactics break-even (400m uplift, pass-through above 29%); a 933m/67% test would fail the base case (FY2028E uplift 696m) and force a re-run of FY2028E, so Table 6.2, K12 and B6 Q7 state that the full 560m is reported at G4, not required. Survey precision: 3.6 / 3.1 / 6.9 points are the smallest significant change between waves (5% level); a true +4 is significant about 6 times in 10 at a 50% base and 7 in 10 at a 25% base, and 80% power needs 5.1 / 4.4 points, so K1 is read as a trend.", 1),
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
    json.dump(reqs, open(os.path.join(RF, "req_resolve.json"), "w", encoding="utf-8"), ensure_ascii=False)
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
    ft = rd(os.path.join(SP, "ch456", "publish", "final_tab.md"))
    for key, old, new in EDITS_B:
        # after --write the new text must be present once in final_tab.md (dry run: old present once)
        present = (ft.count(new) if write else ft.count(old))
        print("  final_tab.md %s %s x%d" % (key, "new" if write else "old", present))
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
