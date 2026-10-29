"""Measurement-band change (29 Oct 2026): survey indicator K1 = ages 20-29 (share of visitors aged 20+); The 1 member data (K2) keep 18-29.
Revised after the Haiku design critique (member data = active members only; 25% is an illustrative base, not a K1 estimate; 20+ rule in every wave).

Usage:
  python -I band_edits.py SCRATCHPAD build DUMP.json      -> checks every find string against the live dump, writes reportfix/req_band.json
  python -I band_edits.py SCRATCHPAD local [--write]      -> local mirrors (ch4/ch6/final_tab) + deck specs + corrections log (dry run unless --write)
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

# ------------------------------------------------------------------ report edits (Chapters 4-6 tab); en dashes as in the live text
EDITS_B = [
    ("A1",
     "The plan measures Gen Z and young adults as ages 18 to 29 (a team definition, not CPN's); the surveys reach only respondents aged 20 and over, whom the team treats as able to consent alone under the PDPA, and younger respondents would need a guardian (s.20).",
     "The plan defines Gen Z and young adults as ages 18 to 29 (a team definition, not CPN's) and measures them in two ways. The intercept survey reaches only respondents aged 20 and over (the age of majority), whom the team treats as able to consent alone under the PDPA (younger respondents would need a guardian, s.20), so it measures ages 20 to 29. The 1 member data cover active members aged 18 to 29, so ages 18 and 19 are seen only there, and only as members."),
    ("A2",
     "S2, S4 and Chapter 6 indicators K1 and K2 use this band, and age bands above 29 are read beside it as a comparison.",
     "Research row S2 and Chapter 6 indicator K2 use the 18 to 29 band; research row S4 and indicator K1 use its 20 to 29 part, as a share of visitors aged 20 and over. Age bands above 29 are read beside both as a comparison."),
    ("A3",
     "the share that Table 5.2 row C1 assumes for the 18–29 band (team calculation, simple random sampling, so minimums)",
     "borrowed for illustration from the team's assumed 18–29 share of visits in Table 5.2 row C1 and not an estimate of K1 (team calculation, simple random sampling, so minimums)"),
    ("A4",
     "weighted to footfall, reporting the 18–29 band; repeated quarterly",
     "weighted to footfall, reporting the 20–29 band; repeated quarterly"),
    ("A5",
     "K1 Gen Z and young-adult (18–29) share of footfall; the plan measures this band as a team definition (Section 4.5); surveys reach respondents aged 20 and over",
     "K1 Share of visitors aged 20 and over who are aged 20–29 (the survey part of the 18–29 Gen Z and young-adult band); the survey does not reach ages 18 and 19, which only the active-member data in K2 cover (Section 4.5)"),
    ("A6",
     "+4 points by the Q4 wave [Proposed]; smallest detectable change 3.6 points at a 50% base and 3.1 points at a 25% base share, the team assumption for the 18–29 band's share of visits in Table 5.2 row C1 (team calculation, n = 1,500)",
     "+4 points by the Q4 wave [Proposed; to be re-checked on the 20–29 baseline]; smallest detectable change 3.6 points at a 50% base and 3.1 points at a 25% base share, borrowed for illustration from the team's assumed 18–29 share of visits in Table 5.2 row C1 (team calculation, n = 1,500)"),
    ("A7",
     "(the same band as K1; the 13–24 comparator is a different band)",
     "(the plan band; K1 covers only its 20–29 part, and the 13–24 comparator is a different band)"),
    ("A8",
     "detects 3.6 points at a 50% base share and 3.1 points at a 25% base share (team calculation)",
     "detects 3.6 points at a 50% base share and 3.1 points at an illustrative 25% base share (team calculation)"),
    ("W1",
     "and only respondents aged 20 and over are surveyed in wave 1 (the team treats them as able to consent alone under s.20)",
     "and only respondents aged 20 and over are surveyed, in every wave (the team treats them as able to consent alone under s.20)"),
    ("W2",
     "respondents aged 20 and over only in wave 1 of the S4 intercept survey",
     "respondents aged 20 and over only, in every wave of the S4 intercept survey"),
    ("W3",
     "72-hour breach drill, wave 1 limited to respondents aged 20 and over (S1)",
     "72-hour breach drill, surveys limited to respondents aged 20 and over (S1)"),
    ("W4",
     "aggregated extracts only; wave 1 limited to respondents aged 20 and over; count-only counters",
     "aggregated extracts only; surveys limited to respondents aged 20 and over; count-only counters"),
]

# ------------------------------------------------------------------ deck edits: (file, old, new, expected count)
S7_HEAD_OLD = "We propose to measure Gen Z and young adults as ages 18–29 and to set the baseline by 31 March 2027, so each Gen Z target is set against our own data."
S7_HEAD_NEW = "We propose to measure Gen Z and young adults by survey (ages 20–29) and member data (18–29), with baselines by 31 March 2027 to set targets against our data."
S7_NOTES_OLD = "We propose to measure Gen Z and young adults as ages 18 to 29. Surveys reach only respondents aged 20 and over, who can consent alone. In what we reviewed, CPN gives no age split of visits. Our baseline, January to March 2027, uses member analytics, a survey, tourist research and sustainability tracking. The only published comparator, 14.7 percent for ages 13 to 24, is a different band. Four indicators track proposed targets."
S7_NOTES_NEW = "We define Gen Z and young adults as ages 18 to 29. Our survey reaches only people aged 20 and over, the age of majority, so it covers 20 to 29; member data cover members 18 to 29. We found no CPN age split of visits, so we set a baseline by 31 March 2027. The only published comparator, 14.7 percent for ages 13 to 24, is a different band. Four indicators track proposed targets."

DECK_EDITS = [
    ("specs/slide_07.json", S7_HEAD_OLD, S7_HEAD_NEW, 1),
    ("specs/slide_07.json", '"name": "K1 18–29 share of footfall"', '"name": "K1 20–29 share of visitors aged 20+"', 1),
    ("specs/slide_07.json", S7_NOTES_OLD, S7_NOTES_NEW, 1),
    ("specs/slide_07.json", '"on_slide": "ages 18–29 / 18 to 29"', '"on_slide": "ages 20–29 (survey) / 18–29 (member data)"', 1),
    ("specs/slide_07.json",
     "The plan measures Gen Z and young adults as ages 18 to 29 a team definition; surveys reach respondents aged 20 and over (a team definition, not CPN's)",
     "The plan defines Gen Z and young adults as ages 18 to 29 (a team definition, not CPN's); the survey reaches only respondents aged 20 and over (the age of majority), so it measures ages 20 to 29, and The 1 member data cover active members aged 18 to 29", 1),
    ("specs/slide_07.json",
     "Share of footfall for the 18–29 band; baseline to be established by 31 March 2027; target +4 points by the Q4 wave [Proposed]",
     "Share of visitors aged 20 and over who are aged 20–29 (survey); baseline to be established by 31 March 2027; target +4 points by the Q4 wave [Proposed; to be re-checked on the 20–29 baseline]", 1),
    ("specs/slide_07.json",
     '"on_slide": "In what we reviewed, CPN gives no age split of visits (notes)"',
     '"on_slide": "We found no CPN age split of visits, so we set a baseline by 31 March 2027 (notes)"', 1),
    ("specs/slide_02.json",
     "the 18-29 band is the plan's measurement band (a team definition)",
     "the 18-29 band is the plan's definition of the segment (a team definition); the survey measures its 20-29 part and The 1 member data (active members) the 18-29 band", 1),
    ("specs/slide_04.json",
     "Plan band for Gen Z and young adults, a team definition, a team definition; surveys reach respondents aged 20 and over;",
     "Plan band for Gen Z and young adults (a team definition); the survey reaches only respondents aged 20 and over, so it measures ages 20 to 29, and The 1 member data (active members) cover 18 to 29;", 1),
    ("specs/slide_B6.json",
     "Ages 18–29 (team definition). Surveys reach only people aged 20+ (age of majority), who consent alone; younger need a guardian (PDPA s.20). DataReportal's 13–24 is a different band.",
     "Ages 18–29 (team definition). The survey reaches only people aged 20+ (age of majority; younger need a guardian, PDPA s.20), so it measures 20–29; member data cover members 18–29. DataReportal's 13–24 is a different band.", 1),
    ("specs/slide_B6.json",
     "our surveys reach only respondents aged 20 and over, the age of majority, who can consent alone under the PDPA; younger respondents would need a guardian.",
     "our survey reaches only respondents aged 20 and over, the age of majority, so it measures 20 to 29, and member data cover members 18 to 29; younger respondents would need a guardian under the PDPA.", 1),
    ("specs/slide_B6.json",
     "Not yet measured. Team assumptions (25% visit share, +10% frequency, +5% lift) carry 79% of FY2028E uplift. The baseline and gates G2 to G4 test them.",
     "Not yet measured. Team assumptions (25% visit share for ages 18–29, +10% frequency, +5% lift) carry 79% of FY2028E uplift. The baseline and gates G2 to G4 test them; the visit share only by proxy (K1 is ages 20–29).", 1),
    ("specs/slide_B6.json",
     "our volume assumptions carry most of the uplift, and the baseline and gates test them.",
     "our volume assumptions carry most of the uplift, and the baseline and gates test them, the visit share only by proxy because our survey measures 20 to 29.", 1),
    ("specs/slide_B6.json",
     "Gen Z and young adults means ages 18 to 29 for measurement, a team definition, not CPN's, a team definition; surveys reach respondents aged 20 and over",
     "Gen Z and young adults means ages 18 to 29 (a team definition, not CPN's); the survey reaches only respondents aged 20 and over, so it measures ages 20 to 29, and The 1 member data (active members) cover 18 to 29", 1),
    ("specs/slide_B6.json",
     "the survey reaches respondents aged 20 and over; the measurement band stays ages 18–29",
     "the survey reaches respondents aged 20 and over, so K1 is the 20–29 share of visitors aged 20 and over and ages 18 and 19 are seen only in The 1 member data (K2, active members); the plan band stays ages 18–29 (decided 29 Oct 2026)", 1),
    ("specs/slide_B6.json",
     '"on_slide": "Q13: surveys reach only respondents aged 20+, who can consent alone (PDPA s.20); ages 18–29 is the team band"',
     '"on_slide": "Q13: the survey reaches only people aged 20+ (age of majority; younger need a guardian, PDPA s.20), so it measures 20–29; member data cover members 18–29"', 1),
    ("src/corrections.md",
     'Age bands: "Gen Z and young adults" means ages 18-29 for measurement (surveys reach respondents aged 20 and over).',
     'Age bands: "Gen Z and young adults" means ages 18-29 (team definition; the planning segment, model row C1 with its 25% visit share, and slides S2 and S4 keep it). Measurement (decided 29 Oct 2026): the intercept survey reaches only respondents aged 20 and over in every wave, so K1 is the share of visitors aged 20 and over who are 20-29; The 1 member data (K2, active members) cover 18-29 and are the only source for ages 18-19. The 25% is not a K1 estimate.', 1),
    ("src/corrections.md",
     "The measurement band stays ages 18-29; surveys reach respondents aged 20 and over. Open for the team's sign-off: how 18-19 year-olds are measured.",
     "Surveys reach respondents aged 20 and over, so the survey band is 20-29 and ages 18-19 are seen only in The 1 member data (decided 29 Oct 2026).", 1),
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
        flag = "OK " if n == 1 else "BAD"
        if n != 1:
            problems.append((key, n))
        print("%s %s: %d hit(s) [%s]" % (flag, key, n, ", ".join(str(p["start"]) for p in hits)))
    # overlapping finds inside one paragraph would break sequential replacement: check
    reqs = [{"replaceAllText": {"containsText": {"text": o, "matchCase": True}, "replaceText": n, "tabsCriteria": {"tabIds": [TAB_B]}}} for _k, o, n in EDITS_B]
    json.dump(reqs, open(os.path.join(RF, "req_band.json"), "w", encoding="utf-8"), ensure_ascii=False)
    # print every changed paragraph after ALL edits are applied in order
    for p in ps:
        t = p["text"]
        t2 = t
        for _k, o, n in EDITS_B:
            t2 = t2.replace(o, n)
        if t2 != t:
            print("\nAFTER [%d-%d]: %s" % (p["start"], p["end"], t2.strip()))
    print("\nrequests:", len(reqs), "| problems:", problems if problems else "none")

elif MODE == "local":
    write = "--write" in sys.argv
    print("== local report mirrors ==")
    for rel in ("ch456/ch4.md", "ch456/ch5.md", "ch456/ch6.md"):
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
    p = os.path.join(SP, "ch456", "publish", "final_tab.md")
    t = rd(p)
    out = t
    for key, old, new in EDITS_B:
        n = out.count(old)
        print("  %s %s x%d (want 1) %s" % ("final_tab.md", key, n, "OK" if n == 1 else "BAD"))
        if n != 1:
            problems.append(("final_tab " + key, n))
        out = out.replace(old, new)
    if write and out != t:
        wr(p, out)
    print("== deck specs and corrections ==")
    by_file = {}
    for rel, old, new, want in DECK_EDITS:
        by_file.setdefault(rel, []).append((old, new, want))
    for rel, items in by_file.items():
        p = os.path.join(DECK, rel.replace("/", os.sep))
        t = rd(p)
        out = t
        for old, new, want in items:
            n = out.count(old)
            ok = n == want
            if not ok:
                problems.append((rel, old[:50], n))
            print("  %s %s x%d (want %d): %s" % ("ok " if ok else "BAD", rel, n, want, old[:60]))
            out = out.replace(old, new)
        if write and out != t:
            wr(p, out)
    print("PROBLEMS:", problems if problems else "none", "| WRITE" if write else "| DRY RUN")
