import json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = sys.argv[1]
def L(n): return json.load(open(R + "/specs/slide_%s.json" % n, encoding="utf-8-sig"))
s2, s8, s11, s12, s5, b5, b6 = L("02"), L("08"), L("11"), L("12"), L("05"), L("B5"), L("B6")
print("S2 headline:", s2["headline"]); print("S2 ask:", s2["body"]["ask"]); print("S2 notes:", s2["notes"])
print("S8 note:", s8["body"]["note"]); print("S8 notes:", s8["notes"])
print("S11 headline:", s11["headline"]); print("S11 worst:", json.dumps(s11["body"]["worst"], ensure_ascii=False)); print("S11 top:", json.dumps(s11["body"]["top"], ensure_ascii=False)); print("S11 notes:", s11["notes"])
print("S12 notes:", s12["notes"])
print("S5 side:", [i["label"] for i in s5["body"]["side"]["items"]])
for col in b6["body"]["columns"]:
    for bl in col:
        for it in bl.get("items", []):
            if it["head"].startswith("Q2"):
                print("B6 Q2:", json.dumps(it, ensure_ascii=False))
print("B5 adults-only:", [c for r in b5["body"]["columns"][0][0]["rows"] for c in r if "adults-only" in c])
print("S11 top responses:", [t["response"] for t in s11["body"]["top"]])
