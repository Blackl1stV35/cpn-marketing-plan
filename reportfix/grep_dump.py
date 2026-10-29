import re, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
pat = re.compile(sys.argv[3])
for tid, label in (("t.pu1p2hjsan6g", "SEC 2-3"), ("t.8nyhv8rr5vec", "CH 4-6")):
    hits = [(p["start"], p["end"], p["text"]) for p in docparse.paragraphs(tabs[tid]) if pat.search(p["text"])]
    print("#####", label, len(hits))
    for s, e, t in hits:
        ms = [m for m in pat.finditer(t)]
        m = ms[0]
        a = max(0, m.start() - 60); b = min(len(t), m.end() + 110)
        print("[%d-%d] x%d ...%s..." % (s, e, len(ms), t[a:b].replace("\n", " ")))
