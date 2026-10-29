"""Mirrors the live-doc report fix into the local source files and updates the deck specs, outline text and corrections log.

Usage: python -I mirror_and_patch.py SCRATCHPAD [--write]
Without --write it only reports counts.
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
SP = sys.argv[1]
WRITE = "--write" in sys.argv
RF = os.path.join(SP, "reportfix")
sys.path.insert(0, RF)
import docparse  # noqa: E402

problems = []


def rd(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return f.read()


def wr(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def apply(path, pairs, expect=None, label=None):
    """pairs: list of (old, new). expect: dict old-> expected count (default 1)."""
    txt = rd(path)
    out = txt
    for old, new in pairs:
        n = out.count(old)
        want = (expect or {}).get(old, 1)
        flag = "ok " if n == want else "BAD"
        if n != want:
            problems.append((os.path.basename(path), old[:50], n, want))
        print("  %s %s x%d (want %d): %s" % (flag, label or os.path.basename(path), n, want, old[:70].replace("\n", " ")))
        out = out.replace(old, new)
    if WRITE and out != txt:
        wr(path, out)
    return out != txt


reqA = json.load(open(os.path.join(RF, "req_sec23.json"), encoding="utf-8"))
reqB = json.load(open(os.path.join(RF, "req_ch456.json"), encoding="utf-8"))
editsA = [(r["replaceAllText"]["containsText"]["text"], r["replaceAllText"]["replaceText"]) for r in reqA if "replaceAllText" in r]
editsB = [(r["replaceAllText"]["containsText"]["text"], r["replaceAllText"]["replaceText"]) for r in reqB if "replaceAllText" in r]

# ---------------------------------------------------------------- 1. chapters 4-6 local sources
print("== Chapters 4-6 local sources (age 20) ==")
tot = {}
for rel in ("ch456/ch4.md", "ch456/ch5.md", "ch456/ch6.md"):
    p = os.path.join(SP, rel.replace("/", os.sep))
    txt = rd(p)
    for old, new in editsB:
        tot[old] = tot.get(old, 0) + txt.count(old)
for old, n in tot.items():
    want = 3 if old == "1,500 adults" else 1
    print("  %s total across ch4/5/6 md: %d (want %d): %s" % ("ok " if n == want else "BAD", n, want, old[:60]))
    if n != want:
        problems.append(("ch456 total", old[:50], n, want))
for rel in ("ch456/ch4.md", "ch456/ch5.md", "ch456/ch6.md"):
    p = os.path.join(SP, rel.replace("/", os.sep))
    txt = rd(p)
    pairs = [(o, nw) for o, nw in editsB if o in txt]
    expect = {o: txt.count(o) for o, _ in pairs}
    print(" ", rel)
    apply(p, pairs, expect)
# final_tab.md holds the whole Ch.4-6 text
p = os.path.join(SP, "ch456", "publish", "final_tab.md")
print("  ch456/publish/final_tab.md")
apply(p, editsB, {"1,500 adults": 3})

# ---------------------------------------------------------------- 2. Sections 2-3 local export
print("== Sections 2-3 local export (sec23_final.txt) ==")
p = os.path.join(SP, "deck", "src", "sec23_final.txt")
txt = rd(p)
apply(p, editsA)
txt = rd(p) if not WRITE else rd(p)
d = docparse.load(os.path.join(RF, "dump_live1.json"))
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
paras = docparse.paragraphs(tabs["t.pu1p2hjsan6g"])
byStart = {q["start"]: q["text"].rstrip("\n") for q in paras}
lines = txt.split("\n")
newlines = list(lines)
for r in reqA:
    if "insertText" not in r:
        continue
    idx = r["insertText"]["location"]["index"]
    anchor = byStart[idx]
    add = r["insertText"]["text"].rstrip("\n").split("\n")
    pos = [i for i, ln in enumerate(newlines) if ln.rstrip("\r") == anchor]
    ok = len(pos) == 1
    print("  %s insert %d line(s) before: %s" % ("ok " if ok else "BAD", len(add), anchor[:60]))
    if not ok:
        problems.append(("sec23 anchor", anchor[:50], len(pos), 1))
        continue
    newlines[pos[0]:pos[0]] = add
if WRITE:
    wr(p, "\n".join(newlines))

# ---------------------------------------------------------------- 3. deck specs, outline, corrections log
print("== deck specs ==")
D = os.path.join(SP, "deck")
S = os.path.join(D, "specs")
apply(os.path.join(S, "slide_03.json"), [
    ("(Section 2 gives the older 86.7% at Q4 2025)",
     "(Section 2 of the report gives the same 85.9%, with 86.7% at Q4 2025 in brackets)"),
    ("sec23_final.txt 2.2.4 Threats item 3 (86.7% at Q4 2025)",
     "sec23_final.txt 2.2.4 Threats item 3 and 2.6 (85.9% at Q1 2026; 86.7% at Q4 2025)"),
    ("(Section 2 says only that arrivals remain well under it). The earlier wording 'roughly 30% from their peak' (Section 2.2.4 item 4, citing Nikkei Asia, 2026a) is not used",
     "(Section 2 of the report now gives the same two figures; its earlier 'roughly 30% from their peak' wording was replaced on 29 Oct 2026)"),
])
apply(os.path.join(S, "slide_B2.json"), [
    ("Section 2 gives the older 86.7% at Q4 2025. Economic slowdown threat",
     "Section 2 of the report gives the same 85.9%, with 86.7% at Q4 2025 in brackets. Economic slowdown threat"),
    ("sec23_final.txt 2.2.4 item 3 (86.7% at Q4 2025)",
     "sec23_final.txt 2.2.4 items 3 and 4 (85.9% at Q1 2026; 86.7% at Q4 2025)"),
    ("Neither is a fall from the pre-pandemic peak, and the report gives no peak figure. The earlier 'about 30% below peak' (Section 2.2.4 item 4, citing Nikkei Asia, 2026a) is not used",
     "Neither is a fall from the pre-pandemic peak, and the report gives no peak figure. Section 2 of the report now gives the same two figures (its earlier 'about 30% below peak' wording was replaced on 29 Oct 2026)"),
    ("SWOT and rivals are from the Section 2 text as corrected, except two Threats figures that follow Table 6.6 in Chapter 6: China arrivals",
     "SWOT and rivals are from the Section 2 text as corrected on 29 Oct 2026; the Threats figures match Table 6.6 in Chapter 6: China arrivals"),
])
apply(os.path.join(S, "slide_B6.json"), [
    ("Central Retail Corporation, press release of 14 Aug 2026 (corrections.md only; not in the reference list)",
     "Central Retail Corporation, 2026 (Sections 2-3 reference list)"),
    ("corrections.md Facts, The 1 loyalty programme",
     "sec23_final.txt 2.4; corrections.md Facts, The 1 loyalty programme"),
    ("S&P Sustainability Yearbook 2026 (corrections.md only; not in the reference list)",
     "S&P Global, 2026 (Sections 2-3 reference list)"),
    ("ch4.md 4.5 age-band and PDPA paragraphs still say 18 (report fix pending)",
     "ch4.md 4.5 age-band and PDPA paragraphs now say 20 (report fixed 29 Oct 2026)"),
    ("The MD&A prints 35.6%; 33.1% and 36% are in corrections.md only (the report prints 35.6% for the MD&A)",
     "The MD&A prints 35.6%; the report (Section 2.5) now prints all three: 33.1% (Central Pattana Investor Relations, n.d.-c), 35.6% and 36% (One Report)"),
    ('"cite": "Central Pattana, 2026p; Central Pattana Investor Relations, 2026"',
     '"cite": "Central Pattana, 2026p; Central Pattana Investor Relations, n.d.-c, 2026"'),
    ('"where": "corrections.md Facts, ESG",\n      "cite": "per CPN, 9 Apr 2026"',
     '"where": "sec23_final.txt 3.5; corrections.md Facts, ESG",\n      "cite": "Central Pattana, 2026t (per CPN, 9 Apr 2026)"'),
    ('"where": "corrections.md Facts, ESG",\n      "cite": "S&P Global, 2026 (Sections 2-3 reference list)"',
     '"where": "sec23_final.txt 3.5; corrections.md Facts, ESG",\n      "cite": "S&P Global, 2026 (Sections 2-3 reference list)"'),
    # B6 Q13 card and note: state the basis of the 20
    ("Ages 18–29 (team definition). Surveys reach only respondents aged 20+, who can consent alone (PDPA s.20). DataReportal's 13–24 is a different band.",
     "Ages 18–29 (team definition). Surveys reach only people aged 20+ (age of majority), who consent alone; younger need a guardian (PDPA s.20). DataReportal's 13–24 is a different band."),
    ("our surveys reach only respondents aged 20 and over, who can consent alone under the PDPA.",
     "our surveys reach only respondents aged 20 and over, the age of majority, who can consent alone under the PDPA; younger respondents would need a guardian."),
])
apply(os.path.join(S, "slide_B1.json"), [
    ("Sections 2–3 keep their own reference list, so sources cited only there (for example Inside Retail Asia, 2026) are not counted here.",
     "Sections 2–3 keep their own reference list, so sources cited only there (for example Inside Retail Asia, 2026, and the Central Retail, S&P Yearbook and April 2026 CPN releases that B6 cites) are not counted here."),
])
print("== outline text and corrections log ==")
apply(os.path.join(D, "build_deck.py"), [
    ("Numbers and sources were checked against Chapters 4 to 6 of the report and the corrections log on 29 Oct 2026. Five items cited on B6 are in the log only, not in the report's reference list: the Central Retail release, the CPN 9 Apr 2026 release, the S&P Yearbook 2026, CPN IR 33.1% and the One Report 36%.",
     "Numbers and sources were checked against the report and the corrections log on 29 Oct 2026, and the report was aligned with this deck the same day. Sources B6 cites outside Chapters 4 to 6 (the Central Retail release, the CPN 9 Apr 2026 release, the S&P Yearbook 2026, the CPN IR page) are in the Sections 2–3 reference list."),
])
apply(os.path.join(D, "src", "corrections.md"), [
    ("Chapter 4 of the report and its live tab still say 18 (report fix pending).",
     "Chapter 4 of the report and its live tab were changed from 18 to 20 on 29 Oct 2026."),
])
if WRITE:
    cm = os.path.join(D, "src", "corrections.md")
    t = rd(cm)
    add = ("\n- Report aligned with the deck (29 Oct 2026, live Google Doc): Sections 2-3 now give China arrivals -33.55% in 2025 and +16.05% in January-August 2026 (Government Public Relations Department, 2026; Nation Thailand, 2026g), household debt 85.9% at Q1 2026 with 86.7% at Q4 2025 (Nation Thailand, 2026c, 2026l), Central Retail's 23 million members (Central Retail Corporation, 2026), the Dow Jones Best-in-Class Indices 8 and 12 consecutive years (Central Pattana, 2026t) with S&P's Yearbook 2026 (S&P Global, 2026), and CPN's published margins 33.1%, about 35.6% and 36% (Section 2.5). Chapters 4-6 say respondents aged 20 and over.\n")
    if "Report aligned with the deck" not in t:
        wr(cm, t.rstrip("\n") + "\n" + add)

print("\nPROBLEMS:", problems if problems else "none")
print("WRITE" if WRITE else "DRY RUN")
