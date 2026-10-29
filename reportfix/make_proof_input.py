import sys, difflib
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d1 = docparse.load(sys.argv[2]); d2 = docparse.load(sys.argv[3])
m1 = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d1["tabs"])}
m2 = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d2["tabs"])}
out = []
for tid, label in (("t.pu1p2hjsan6g", "SECTIONS 2-3 TAB"), ("t.8nyhv8rr5vec", "CHAPTERS 4-6 TAB")):
    a = [p["text"] for p in docparse.paragraphs(m1[tid])]
    pb = docparse.paragraphs(m2[tid])
    b = [p["text"] for p in pb]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out.append("##### %s: changed or new paragraphs (after the edit) #####" % label)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "insert"):
            for k in range(j1, j2):
                out.append("[%s %d] %s" % ("NEW REFERENCE" if (tid == "t.pu1p2hjsan6g" and k >= 180 and b[k][:1].isalpha() and "(" in b[k][:80] and "http" in b[k]) else "EDITED", k, b[k].strip()))
                out.append("")
open(sys.argv[4], "w", encoding="utf-8").write("\n".join(out))
print("written", len(out), "lines")
# also print nation thailand 2026c ref line
for p in docparse.paragraphs(m2["t.pu1p2hjsan6g"]):
    if p["text"].startswith("Nation Thailand. (2026c"):
        print(p["text"].strip())
