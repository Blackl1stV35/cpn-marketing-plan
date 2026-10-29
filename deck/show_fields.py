import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")
R = sys.argv[1]
def L(n): return json.load(open(R + "/specs/slide_%s.json" % n, encoding="utf-8-sig"))
s5, s6, s7, s8, s10, b2 = L("05"), L("06"), L("07"), L("08"), L("10"), L("B2")
print("S5 side:", json.dumps(s5["body"]["side"], ensure_ascii=False))
print("S5 notes:", s5["notes"])
print("S6 headline:", s6["headline"]); print("S6 budget:", s6["body"]["budget"]); print("S6 hub/nodes:", [n["name"] + ": " + n.get("note", "") for n in s6["body"]["nodes"]])
print("S6 notes:", s6["notes"])
print("S7 headline:", s7["headline"]); print("S7 kpis:", [k["name"] for k in s7["body"]["kpis"]]); print("S7 notes:", s7["notes"])
print("S8 series:", [[se["name"] for se in c["series"]] for c in s8["body"]["charts"]], "| title:", [c["title"] for c in s8["body"]["charts"]])
print("S10 months:", s10["body"]["months"], "gates:", json.dumps(s10["body"]["gates"], ensure_ascii=False))
for blk in b2["body"]["columns"][1] + b2["body"]["columns"][0]:
    if "text" in blk and "Phaholyothin" in blk.get("title", ""):
        print("B2 footnote:", blk["title"], "|", blk["text"])
