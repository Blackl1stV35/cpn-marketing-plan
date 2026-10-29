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

p, s = load("02")
s["notes"] = ("One: a proposed gross ceiling of 2,760 million baht. Two: net-new spend, 560 million a year. "
              "Three: our base case adds 328 million, then 696 million; repaying 560 million a year needs 933 million. "
              "Four: growth of 6.6 percent against 7.0 and margin of 34.6 against our 35.5 floor miss our objective, F1. "
              "Only the optimistic case, a target by definition, meets it. Five: money is released after each gate. Our second speaker covers the situation.")
print("S2 spoken", spoken_words(s["notes"]), "band", [round(x, 1) for x in (band(45)[0] * 0.97, band(45)[0] * 1.02)])
save(p, s)
p, s = load("08")
s["body"]["note"] = "Tactics: the ฿240m that earns modelled revenue, repaid in 1.2 years; the other ฿320m earns none. Pass-through assumed 50%."
print("S8 note len", len(s["body"]["note"]))
save(p, s)
p, s = load("11")
s["headline"] = "If 2020 repeated, CPN's own 51.6% core profit fall would cut FY2027E profit by ฿10.5bn, more than marketing can absorb, so credit is the constraint to watch."
print("S11 headline len", len(s["headline"]))
save(p, s)
p, s = load("B6")
for col in s["body"]["columns"]:
    for bl in col:
        for it in bl.get("items", []):
            if it.get("head", "").startswith("Q2 "):
                it["text"] = "No. On assumed uplift, ฿560m a year is not repaid by FY2028E (needs 67% pass-through). ฿240m of tactics repay in 1.2 years; ฿320m earns none."
                print("B6 Q2 len", len(it["text"]))
save(p, s)
