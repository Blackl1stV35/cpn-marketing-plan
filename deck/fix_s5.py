import json, sys
sys.stdout.reconfigure(encoding="utf-8")
p = sys.argv[1] + "/specs/slide_05.json"
s = json.load(open(p, encoding="utf-8-sig"))
it = s["body"]["side"]["items"][2]
print("before:", it)
it["label"] = "Bangkok prime asking rent/mo, Q3 2026; not CPN's"
for f in s["facts"]:
    if "3,769" in f.get("on_slide", ""):
        f["on_slide"] = "฿3,769/m²; Bangkok prime asking rent/mo, Q3 2026; not CPN's"
open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(s, ensure_ascii=False, indent=2) + "\n")
print("after:", it)
