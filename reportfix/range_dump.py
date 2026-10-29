import re, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
ps = docparse.paragraphs(tabs["t.8nyhv8rr5vec"])
lo, hi = int(sys.argv[3]), int(sys.argv[4])
for p in ps:
    if lo <= p["start"] < hi:
        print("[%d-%d] %s" % (p["start"], p["end"], p["text"].strip().replace("\n", " ")))
