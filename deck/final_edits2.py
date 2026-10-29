import json, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, sys.argv[1])
from spoken import spoken_words, band
R = sys.argv[1]

def load(n):
    p = R + "/specs/slide_%s.json" % n
    return p, json.load(open(p, encoding="utf-8-sig"))

def save(p, d):
    open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

def chk(name, text, sec=None):
    sp = spoken_words(text)
    b = band(sec)[0] if sec else None
    print("%s: written %d spoken %d%s" % (name, len(text.split()), sp, (" (budget %.1f; 97-102%% = %.1f-%.1f)" % (b, b * 0.97, b * 1.02)) if sec else ""))

# ---- S2
p, s = load("02")
s["headline"] = "We propose a ฿2,760 million gross ceiling for FY2027; the base case misses our financial objective (F1), and net-new money is released after each gate."
s["body"]["ask"] = "Most new effort goes to Gen Z and young adults (18–29). The base case misses F1; only the optimistic target meets it."
s["notes"] = ("One: a proposed gross ceiling of 2,760 million baht. Two: net-new spend of 560 million a year. "
              "Three: our base case adds 328 million of revenue, then 696 million; repaying 560 million a year needs 933 million. "
              "Four: growth of 6.6 percent against 7.0, and margin of 34.6 against our 35.5 floor, miss our financial objective, F1. "
              "Only the optimistic case, a target by definition, meets it. Five: money is released after each gate. Our second speaker covers the situation.")
print("S2 headline len", len(s["headline"]), "ask len", len(s["body"]["ask"]))
chk("S2", s["notes"], 45)
save(p, s)

# ---- S8
p, s = load("08")
s["body"]["note"] = "Tactics are the ฿240m a year that earns modelled revenue; they repay in 1.2 years. The other ฿320m earns none. Pass-through: 50% assumed."
s["notes"] = ("We add 560 million baht a year of net-new marketing. Only 60 percent of extra revenue is kept, so we need 933 million more a year. "
              "The tactics are the 240 million that earns modelled revenue; they need 400 million and repay in 1.2 years. The full 560 million a year does not. "
              "In 2028 it needs 67 percent of any gain to reach CPN's revenue; we assumed 50. The tactics need only 29 percent. "
              "Base-case growth is 6.6 percent in 2027 and 6.9 in 2028, short of 7. Only the optimistic case passes, by definition. Our fifth speaker covers expenses and profit.")
print("S8 note len", len(s["body"]["note"]))
chk("S8", s["notes"], 55)
for f in s["facts"]:
    if "60.0% kept" in f.get("on_slide", ""):
        f["where"] = f.get("where", "") + " (notes: only 60 percent of extra revenue is kept)"
save(p, s)

# ---- S11
p, s = load("11")
s["headline"] = "If 2020 repeated, CPN's own 51.6% core profit fall would cut FY2027E profit by ฿10.5bn, more than marketing cuts can absorb, so credit is the constraint to watch."
print("S11 headline len", len(s["headline"]))
w = s["body"]["worst"]
w["numbers"][0]["label"] = "2020 replay, year 1: FY2027E profit"
w["numbers"][1]["label"] = "Team estimate, severe recession"
w["numbers"][2]["label"] = "EBITDA headroom to 4x, team calculation"
s["body"]["top"][2]["response"] = "S1 set-up; aggregated extracts only; adults only"
s["body"]["ladder"] = {"title": "Response ladder [Proposed]", "steps": [
    {"name": "Amber", "text": "freezes some spending"},
    {"name": "Red", "text": "suspends lines, trims flagship seasons 20%"},
    {"name": "Crisis", "text": "suspends most lines, tenant relief"}]}
s["notes"] = ("The ratings are our judgement. Only household debt is rated high on both likelihood and impact. "
              "In our assessment, Gen Z disengagement is our biggest exposure. Our thesis rests on Gen Z, so gate three tests it. "
              "Our response is a three-step ladder. Amber freezes some spending. Red suspends lines and trims the flagship seasons by 20 percent. "
              "Crisis suspends most lines and runs tenant relief. A closure like 2020 would trigger Crisis. "
              "CPN's own core profit fell 51.6 percent then; the same fall on our base is 10.5 billion baht. Marketing cuts cannot absorb that, so credit is the constraint we watch.")
chk("S11", s["notes"], 50)
save(p, s)

# ---- S12
p, s = load("12")
old = "Thank you. We welcome your questions."
assert old in s["notes"]
s["notes"] = s["notes"].replace(old, "Thank you; we welcome questions.")
chk("S12", s["notes"], 30)
save(p, s)

# ---- S5, B5, B6
p, s = load("05")
it = s["body"]["side"]["items"][3]
assert it["label"] == "Voucher rate, 400 per 4,500 baht (team)"
it["label"] = "Voucher rate, 400 per 4,500 baht (team calculation)"
save(p, s)
p, s = load("B5")
n = 0
for col in s["body"]["columns"]:
    for bl in col:
        if bl.get("type") == "table":
            for r in bl["rows"]:
                for i, c in enumerate(r):
                    if "adults-only wave 1" in c:
                        r[i] = c.replace("adults-only wave 1", "adults only")
                        n += 1
print("B5 adults-only replaced:", n)
save(p, s)
p, s = load("B6")
done = 0
for col in s["body"]["columns"]:
    for bl in col:
        for it in bl.get("items", []):
            if it.get("head", "").startswith("Q2 "):
                it["text"] = "No. On assumed uplift, ฿560m a year is not repaid by FY2028E: it needs 67% pass-through (50% assumed). ฿240m of tactics repay in 1.2 years; ฿320m earns none."
                print("B6 Q2 text len", len(it["text"]))
                done += 1
assert done == 1
save(p, s)
