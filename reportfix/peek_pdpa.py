import sys, re
sys.path.insert(0, sys.argv[1])
from docparse import load, walk_tabs, paragraphs
d = load(sys.argv[1] + "/dump_live1.json")
tab = [t for t in walk_tabs(d["tabs"]) if t["tabProperties"]["tabId"] == "t.8nyhv8rr5vec"][0]
ps = paragraphs(tab)
want = [(21709, 22594), (24751, 25736), (25819, 26080), (69334, 69462), (75801, 75919), (84977, 85415)]
for p in ps:
    if (p["start"], p["end"]) in want:
        t = p["text"].replace("\n", "")
        print("[%d-%d]" % (p["start"], p["end"]))
        print(t)
        print()
