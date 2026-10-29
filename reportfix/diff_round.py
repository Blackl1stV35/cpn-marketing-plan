import difflib, json, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
def tm(p):
    d = docparse.load(p)
    return d, {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
d0, t0 = tm(sys.argv[2]); d1, t1 = tm(sys.argv[3])
print("revisions", d0["revisionId"][:12], "->", d1["revisionId"][:12])
bad = []
for tid in t0:
    a = [p["text"] for p in docparse.paragraphs(t0[tid])]
    b = [p["text"] for p in docparse.paragraphs(t1[tid])]
    if tid != "t.8nyhv8rr5vec":
        if a != b: bad.append("tab changed " + tid)
        continue
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    n = sum(i2 - i1 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")
    print("Ch4-6 changed paragraphs this round:", n, "| count", len(a), "->", len(b))
full = "".join(p["text"] for p in docparse.paragraphs(t1["t.8nyhv8rr5vec"]))
for r in json.load(open(sys.argv[4], encoding="utf-8")):
    t = r["replaceAllText"]["replaceText"]
    ok = full.count(t) == 1
    print("%s new text x%d | %s" % ("OK " if ok else "BAD", full.count(t), t[:60]))
    if not ok: bad.append(t[:40])
print("PROBLEMS:", bad if bad else "none")
