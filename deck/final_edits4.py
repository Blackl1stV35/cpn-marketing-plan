import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, sys.argv[1])
from spoken import spoken_words, band
R = sys.argv[1]

def load(n):
    p = R + "/specs/slide_%s.json" % n
    return p, json.load(open(p, encoding="utf-8-sig"))

def save(p, d):
    open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

# ---------------- S7: consent age 20
p, s = load("07")
s["notes"] = ("We propose to measure Gen Z and young adults as ages 18 to 29. Surveys reach only respondents aged 20 and over, who can consent alone. "
              "In what we reviewed, CPN gives no age split of visits. Our baseline, from January to March 2027, uses member analytics, a survey, "
              "tourist research and a sustainability tracker. The only published comparator, 14.7 percent of those aged 13 to 24, is a different band. "
              "Four indicators track our proposed targets.")
lo, hi = band(35)[0] * 0.97, band(35)[0] * 1.02
print("S7 spoken", spoken_words(s["notes"]), "band %.1f-%.1f" % (lo, hi))
m = s["body"]["methods"][1]
assert m["what"] == "1,500 adults, 300 per centre, weighted to footfall"
m["what"] = "1,500 respondents aged 20+, 300 per centre, weighted to footfall"
print("S7 method len", len(m["what"]))
save(p, s)

# ---------------- S11 / B5: respondents aged 20+ only
p, s = load("11")
old = "S1 set-up; aggregated extracts only; adults only"
assert s["body"]["top"][2]["response"] == old
s["body"]["top"][2]["response"] = "S1 set-up; aggregated extracts only; surveys ages 20+ only"
save(p, s)
p, s = load("B5")
n = 0
for col in s["body"]["columns"]:
    for bl in col:
        if bl.get("type") == "table":
            for r in bl["rows"]:
                for i, c in enumerate(r):
                    if "adults only" in c:
                        r[i] = c.replace("adults only", "surveys ages 20+ only")
                        n += 1
                        print("B5 cell:", r[i], len(r[i]))
assert n == 1
save(p, s)

# ---------------- B6: new break-even card (Q7), renumber, consent wording
p, s = load("B6")
left = s["body"]["columns"][0][0]["items"]
right = s["body"]["columns"][1][0]["items"]
new = {"head": "Q7 What stops a loss-making FY2028 repeat?", "tag": "Spkr 5",
       "text": "G4 requires ฿400m uplift and pass-through above 29% (tactics break-even); a miss limits FY2028 to tactics that passed. The full ฿560m needs ฿933m and 67%: reviewed, not required."}
print("B6 new card len", len(new["text"]))
assert len(left) == 6 and len(right) == 6
left.append(new)
for it in right:
    m = re.match(r"Q(\d+) (.*)", it["head"])
    it["head"] = "Q%d %s" % (int(m.group(1)) + 1, m.group(2))
q13 = [it for it in right if it["head"].startswith("Q13 ")][0]
q13["head"] = "Q13 How is Gen Z defined, and what consent age?"
q13["text"] = "Ages 18–29 (team definition). Surveys reach only respondents aged 20+, who can consent alone (PDPA s.20). DataReportal's 13–24 is a different band."
print("B6 Q13 len", len(q13["text"]))
s["headline"] = "We answer the 13 likely questions plainly, with a suggested speaker for each: the base case misses F1 and the extra revenue is our assumption."
notes = s["notes"]
for k in range(12, 6, -1):
    notes = notes.replace("Q%d (" % k, "Q%d (" % (k + 1))
q7 = ("Q7 (Spkr 5): G4 requires the tactics break-even, 400 million of uplift and pass-through above 29 percent; below that FY2028 is limited to the tactics that passed. "
      "The full 560 million needs 933 million and 67 percent, which G4 reviews but does not require. ")
notes = notes.replace("Q8 (Spkr 2):", q7 + "Q8 (Spkr 2):", 1)
old13 = "Q13 (Spkr 4): Gen Z and young adults means ages 18–29, and we treat respondents aged 18 and over as able to consent alone."
assert old13 in notes
notes = notes.replace(old13, "Q13 (Spkr 4): Gen Z and young adults means ages 18–29; our surveys reach only respondents aged 20 and over, who can consent alone under the PDPA.")
s["notes"] = notes
for f in s["facts"]:
    if "18+ as able to consent alone" in f.get("on_slide", "") or "aged 18 and over" in f.get("meaning", ""):
        f["on_slide"] = "Q13: surveys reach only respondents aged 20+, who can consent alone (PDPA s.20); ages 18–29 is the team band"
        f["meaning"] = "The team uses the Civil Code majority of 20 as the PDPA consent age (decided 29 Oct 2026, replacing the earlier 18); the survey reaches respondents aged 20 and over; the measurement band stays ages 18–29"
        f["where"] = "corrections.md Facts, Survey consent; ch4.md 4.5 age-band and PDPA paragraphs still say 18 (report fix pending)"
s["facts"].append({"on_slide": "Q7: G4 requires 400m uplift and pass-through above 29%; the full 560m needs 933m and 67%",
                   "meaning": "Table 6.2 G4 pass test is the tactics break-even (uplift run-rate at least 400 million, pass-through above 29%, K12); a failed G4 limits FY2028 to the tactics that passed; K12 also lists 933 million and 67% for all net-new spend, which G4 reviews with all Table 6.3 KPIs but does not require",
                   "where": "ch6.md Table 6.2 row G4; Table 6.3 row K12; ch5.md section 5.1 and Table 5.4",
                   "cite": "team proposal (Chapter 6 Table 6.2); team calculation (Chapter 5)"})
save(p, s)

# ---------------- stale phrase in facts across specs
import glob
for fp in glob.glob(R + "/specs/slide_*.json"):
    d = json.load(open(fp, encoding="utf-8-sig"))
    ch = 0
    for f in d.get("facts", []):
        for k in ("on_slide", "meaning", "where"):
            v = f.get(k, "")
            nv = v.replace("because surveys reach adults only", "a team definition; surveys reach respondents aged 20 and over").replace("surveys reach adults only", "surveys reach respondents aged 20 and over")
            if nv != v:
                f[k] = nv
                ch += 1
    if ch:
        save(fp, d)
        print("facts updated in", fp.split("\\")[-1].split("/")[-1], ch)
