import sys
sys.path.insert(0, sys.argv[1])
from docparse import load, walk_tabs, paragraphs
d = load(sys.argv[1] + "/dump_live1.json")
tab = [t for t in walk_tabs(d["tabs"]) if t["tabProperties"]["tabId"] == "t.pu1p2hjsan6g"][0]
ps = paragraphs(tab)
for p in ps:
    if p["start"] >= 34000 and p["text"].strip():
        runs = p["runs"]
        link = any(r[2].get("link") for r in runs)
        print("[%d-%d] indS=%s indF=%s link=%s runs=%d %s" % (p["start"], p["end"], p["indentStart"], p["indentFirst"], link, len(runs), p["text"].strip()[:110]))
