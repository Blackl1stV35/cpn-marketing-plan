import re, sys, json
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
pat = re.compile(r"18\s*(?:–|-|to)\s*29|ages? 18|aged 18|18 and over|\bK1\b")
print("== other tabs mentioning the band or K1 ==")
for t in docparse.walk_tabs(d["tabs"]):
    tid = t["tabProperties"]["tabId"]
    if tid in ("t.pu1p2hjsan6g", "t.8nyhv8rr5vec"):
        continue
    hits = [p for p in docparse.paragraphs(t) if pat.search(p["text"])]
    print(tid, t["tabProperties"].get("title"), len(hits))
    for p in hits[:4]:
        m = pat.search(p["text"])
        print("    [%d] ...%s..." % (p["start"], p["text"][max(0, m.start() - 60): m.end() + 80].replace("\n", " ")))
print()
print("== B6 JSON strings containing the band ==")
b6 = json.load(open(sys.argv[3] + r"\deck\specs\slide_B6.json", encoding="utf-8-sig"))
def walk(o, path=""):
    if isinstance(o, str):
        if re.search(r"18.29|18 to 29|20\+|aged 20|20 and over", o):
            print(path, "::", o[:600])
    elif isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, "%s[%d]" % (path, i))
walk(b6)
