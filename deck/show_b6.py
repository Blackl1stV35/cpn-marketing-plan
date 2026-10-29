import json, sys
sys.stdout.reconfigure(encoding="utf-8")
s = json.load(open(sys.argv[1] + "/specs/slide_B6.json", encoding="utf-8-sig"))
print("headline:", s["headline"])
for ci, col in enumerate(s["body"]["columns"]):
    for bi, bl in enumerate(col):
        print("col", ci, "block", bi, bl.get("type"), bl.get("title"))
        for it in bl.get("items", []):
            print("   ", it["head"], "|", it["tag"], "|", len(it["text"]), "|", it["text"])
print("NOTES:", s["notes"])
print("sources:", s["sources"])
print("n facts:", len(s["facts"]))
