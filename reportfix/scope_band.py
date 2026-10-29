import re, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
pat = re.compile(r"18\s*(?:–|-|to)\s*29|ages? 18|aged 18|18\s*(?:–|-)\s*19|18 and over|20 and over|aged 20|ages 20|20\+")
for tid, label in (("t.pu1p2hjsan6g", "SEC 2-3"), ("t.8nyhv8rr5vec", "CH 4-6")):
    print("#####", label)
    for p in docparse.paragraphs(tabs[tid]):
        t = p["text"]
        ms = list(pat.finditer(t))
        if not ms:
            continue
        print("[%d-%d] (%d hits) %s" % (p["start"], p["end"], len(ms), t.strip()[:100].replace("\n", " ")))
        for m in ms:
            s = max(0, m.start() - 70); e = min(len(t), m.end() + 90)
            print("      ...%s" % t[s:e].replace("\n", " "))
