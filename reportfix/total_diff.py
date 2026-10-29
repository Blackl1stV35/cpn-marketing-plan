import difflib, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
def tm(p):
    d = docparse.load(p)
    return d, {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
d0, t0 = tm(sys.argv[2]); d1, t1 = tm(sys.argv[3])
print("revisions", d0["revisionId"][:12], "->", d1["revisionId"][:12])
for tid in t0:
    a = [p["text"] for p in docparse.paragraphs(t0[tid])]
    b = [p["text"] for p in docparse.paragraphs(t1[tid])]
    if a != b:
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        n = sum(i2 - i1 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")
        print("tab", tid, t0[tid]["tabProperties"].get("title"), "changed paragraphs:", n, "| paragraph count", len(a), "->", len(b))
print("all other tabs unchanged")
