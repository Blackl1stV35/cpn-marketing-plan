import json, sys
sys.stdout.reconfigure(encoding="utf-8")
p = sys.argv[1] + "/specs/slide_B6.json"
d = json.load(open(p, encoding="utf-8-sig"))
for f in d["facts"]:
    v = f.get("meaning", "")
    if "S7 age band and adults-only surveys" in v:
        v = v.replace("Q12 Spkr 4 (S7 age band and adults-only surveys)", "Q13 Spkr 4 (S7 age band and surveys of ages 20+); Q7 Spkr 5 (S10 gates)").replace("Q10 Spkr 3 (S6 openings)", "Q11 Spkr 3 (S6 openings)")
        f["meaning"] = v
        print("patched tag legend fact")
open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
