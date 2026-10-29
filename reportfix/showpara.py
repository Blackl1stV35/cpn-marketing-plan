import sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
tabs = docparse.walk_tabs(d["tabs"])
tab = [t for t in tabs if t["tabProperties"]["tabId"] == sys.argv[3]][0]
ps = docparse.paragraphs(tab)
want = [int(x) for x in sys.argv[4:]]
for p in ps:
    if p["start"] in want:
        print("=== [%d-%d] runs=%d style=%s" % (p["start"], p["end"], len(p["runs"]), p["style"]))
        print(p["text"])
