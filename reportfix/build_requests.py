"""Builds the Google Docs batchUpdate requests for the report + reference fix and checks every find string against the live dump.

Usage: python -I build_requests.py REPORTFIX_DIR DUMP.json
Writes req_sec23.json and req_ch456.json (lists of requests) and prints before/after for every edited paragraph.
"""
import json
import os
import sys

ROOT = sys.argv[1]
DUMP = sys.argv[2]
sys.path.insert(0, ROOT)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

d = docparse.load(DUMP)
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
print("revision:", d["revisionId"])
A = "t.pu1p2hjsan6g"  # Sections 2-3
B = "t.8nyhv8rr5vec"  # Chapters 4-6

# ---------------------------------------------------------------- Section 2-3 text edits
EDITS_A = [
    ("E1",
     "the official 2026 arrivals target is 36.7 million, while Chinese arrivals specifically remain well under their pre-pandemic peak (Thai Examiner, 2026a).",
     "the official 2026 arrivals target is 36.7 million (Thai Examiner, 2026a), while Chinese arrivals fell 33.55% in 2025 and rose 16.05% in January–August 2026 (Government Public Relations Department, 2026; Nation Thailand, 2026g)."),
    ("E2",
     "household debt reached 86.7% of GDP in the fourth quarter of 2025, a fragile base for discretionary mall spending (Nation Thailand, 2026c).",
     "household debt stood at 85.9% of GDP in the first quarter of 2026 (86.7% in the fourth quarter of 2025), a fragile base for discretionary mall spending (Nation Thailand, 2026c, 2026l)."),
    ("E3",
     "fell roughly 30% from their peak; an August 2026 update shows a partial year-on-year gain in absolute numbers",
     "fell 33.55% in 2025 (Government Public Relations Department, 2026); an August 2026 update shows a partial year-on-year gain in absolute numbers, up 16.05% in January–August 2026 (Nation Thailand, 2026g),"),
    ("E4",
     "The 1 loyalty ecosystem is Central Group's loyalty programme, reported at approximately 22 million members as of September 2025 (Central Retail Corporation, 2025), up from roughly 18 million in 2021 as the platform has scaled (Nation Thailand, 2021).",
     "The 1 loyalty ecosystem is Central Group's loyalty programme. Central Retail's August 2026 results release reports 23 million members of its loyalty ecosystem in Thailand, which the team reads as The 1 (Central Retail Corporation, 2026), up from roughly 18 million in 2021 as the platform has scaled (Nation Thailand, 2021)."),
    ("E5",
     "Thai household debt hit 86.7% of GDP in the fourth quarter of 2025, increasingly consumption- rather than investment-driven (Nation Thailand, 2026c).",
     "Thai household debt stood at 85.9% of GDP in the first quarter of 2026 (86.7% in the fourth quarter of 2025), increasingly consumption- rather than investment-driven (Nation Thailand, 2026c, 2026l)."),
    ("E6",
     "given that Chinese arrivals to Thailand have fallen well below their pre-pandemic peak (Nikkei Asia, 2026a).",
     "given that Chinese arrivals to Thailand fell 33.55% in 2025 and have only partly recovered in 2026 (Government Public Relations Department, 2026; Nation Thailand, 2026g; Nikkei Asia, 2026a)."),
    ("E7",
     "reports sustained placement on DJSI Best-in-Class sustainability indices and related ESG recognitions (ThaiPR.net, 2025b).",
     "reports sustained placement on the Dow Jones Best-in-Class Indices (formerly the DJSI) and related ESG recognitions (ThaiPR.net, 2025b), including 8 consecutive years in the World index and 12 in the Emerging Markets index (Central Pattana, 2026t). S&P Global's Sustainability Yearbook 2026 independently lists CPN in the top 10% of Corporate Sustainability Assessment scores (S&P Global, 2026)."),
    ("E8",
     "attributable to the parent company, a net profit margin of approximately 35.5% by the team's own calculation from those two figures (Central Pattana, 2026a).",
     "attributable to the parent company, a net profit margin of approximately 35.5% by the team's own calculation from those two figures (Central Pattana, 2026a). CPN itself publishes FY2025 margins of 33.1% on its investor-relations results page (Central Pattana Investor Relations, n.d.-c), about 35.6% in its management discussion and analysis (Central Pattana, 2026p) and 36% in its 2025 One Report (Central Pattana Investor Relations, 2026); the team does not present its 35.5% as a CPN figure."),
]

# Reference entries: (anchor prefix of the paragraph that must FOLLOW the new entries, entry text lines)
REFS_A = [
    ("Thai Examiner. (2026a)", [
        "S&P Global. (2026). 2026 rankings: The Sustainability Yearbook [Web page]. https://www.spglobal.com/sustainable1/en/csa/yearbook/2026/ranking",
    ]),
    ("National Statistical Office. (2025)", [
        "Nation Thailand. (2026g, September 7). Foreign arrivals to Thailand decline 3% in first eight months. https://www.nationthailand.com/business/economy/40070737",
        "Nation Thailand. (2026l, July 15). Thai household debt-to-GDP ratio falls amid restricted credit access. https://www.nationthailand.com/business/economy/40068669",
    ]),
    ("Inside Retail Asia. (2025)", [
        "Government Public Relations Department. (2026, January 16). Thailand tourism earns US$86.6 billion, arttracts [sic] higher-quality travelers in 2025. https://thailand.prd.go.th/en/content/category/detail/id/2078/iid/466167",
    ]),
    ("CPNREIT. (2024)", [
        "Central Retail Corporation. (2026, August 14). Central Retail sets another record in Q2/2026, profit up 124% to THB 2,114 million, accelerating long-term growth with “New Heights, Next Growth”. https://www.centralretail.com/en/newsroom/news-and-activities/1439/central-retail-sets-another-record-in-q2-2026-profit-up-124-to-thb-2114-million-accelerating-long-term-growth-with-new-heights-next-growth",
    ]),
    ("Central Pattana Investor Relations. (2026)", [
        "Central Pattana. (2026t, April 9). Central Pattana reinforces its position as a world-class sustainable organization, consistently ranked in the Dow Jones Best-in-Class Indices and recognized with multiple Asia-level ESG awards, while advancing collaboration across all sectors to build a sustainable ecosystem [Press release]. ThaiPR.net. https://www.thaipr.net/en/business_en/3711713",
        "Central Pattana Investor Relations. (n.d.-c). Performance highlights [Web page]. Retrieved October 29, 2026, from https://investor.centralpattana.co.th/en/results-and-reporting/performance-highlights",
    ]),
]

# ---------------------------------------------------------------- Chapters 4-6 text edits (PDPA age 20)
EDITS_B = [
    ("F1",
     "ages 18 to 29, because the surveys reach adults only (a team definition, not CPN's; the team treats respondents aged 18 and over as able to consent alone under the PDPA)",
     "ages 18 to 29 (a team definition, not CPN's); the surveys reach only respondents aged 20 and over, whom the team treats as able to consent alone under the PDPA, and younger respondents would need a guardian (s.20)"),
    ("F2",
     "and adults only are surveyed in wave 1 (the team treats respondents aged 18 and over as able to consent alone under s.20)",
     "and only respondents aged 20 and over are surveyed in wave 1 (the team treats them as able to consent alone under s.20)"),
    ("F3",
     "adults only in wave 1 of the S4 intercept survey",
     "respondents aged 20 and over only in wave 1 of the S4 intercept survey"),
    ("F4",
     "because surveys reach adults only (Section 4.5)",
     "as a team definition (Section 4.5); surveys reach respondents aged 20 and over"),
    ("F5",
     "72-hour breach drill, adults-only wave 1 (S1)",
     "72-hour breach drill, wave 1 limited to respondents aged 20 and over (S1)"),
    ("F6",
     "aggregated extracts only; adults-only wave 1; count-only counters",
     "aggregated extracts only; wave 1 limited to respondents aged 20 and over; count-only counters"),
    ("F7",
     "1,500 adults",
     "1,500 respondents aged 20 and over"),
]
EXPECT_B = {"F7": 3}


def count_hits(tab, find):
    return sum(p["text"].count(find) for p in docparse.paragraphs(tab))


def check_edits(tid, edits, expect):
    ok = True
    ps = docparse.paragraphs(tabs[tid])
    for key, find, repl in edits:
        n = count_hits(tabs[tid], find)
        want = expect.get(key, 1)
        flag = "OK " if n == want else "BAD"
        if n != want:
            ok = False
        print("%s %s: %d hit(s) (want %d)" % (flag, key, n, want))
        for p in ps:
            if find in p["text"]:
                new = p["text"].replace(find, repl)
                print("   [%d-%d] AFTER: %s" % (p["start"], p["end"], new.strip()))
    return ok


def ref_inserts(tid, refs):
    ps = docparse.paragraphs(tabs[tid])
    head = [p for p in ps if p["text"].strip() == "References"][-1]["start"]
    out = []
    for anchor, lines in refs:
        hits = [p for p in ps if p["start"] > head and p["text"].startswith(anchor)]
        assert len(hits) == 1, (anchor, len(hits))
        h = hits[0]
        assert h["indentStart"] == 48 and h["indentFirst"] == 24, (anchor, h["indentStart"], h["indentFirst"])
        out.append((h["start"], "".join(x + "\n" for x in lines), anchor))
        print("insert %d line(s) before [%d] %s" % (len(lines), h["start"], h["text"][:60]))
    return out


print("\n== Section 2-3 edits ==")
okA = check_edits(A, EDITS_A, {})
insA = ref_inserts(A, REFS_A)
print("\n== Chapters 4-6 edits ==")
okB = check_edits(B, EDITS_B, EXPECT_B)
print("\nALL FINDS OK:", okA and okB)

reqA = []
for start, text, _a in sorted(insA, reverse=True):
    reqA.append({"insertText": {"location": {"index": start, "tabId": A}, "text": text}})
for key, find, repl in EDITS_A:
    reqA.append({"replaceAllText": {"containsText": {"text": find, "matchCase": True}, "replaceText": repl, "tabsCriteria": {"tabIds": [A]}}})
reqB = []
for key, find, repl in EDITS_B:
    reqB.append({"replaceAllText": {"containsText": {"text": find, "matchCase": True}, "replaceText": repl, "tabsCriteria": {"tabIds": [B]}}})

json.dump(reqA, open(os.path.join(ROOT, "req_sec23.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(reqB, open(os.path.join(ROOT, "req_ch456.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("requests:", len(reqA), len(reqB))
