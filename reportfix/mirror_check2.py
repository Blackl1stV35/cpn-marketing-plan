import difflib, re, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
def tm(p):
    d = docparse.load(p)
    return {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
t0, t1 = tm(sys.argv[2]), tm(sys.argv[3])
ft = re.sub(r"\s+", " ", open(sys.argv[4], encoding="utf-8-sig").read())
tid = "t.8nyhv8rr5vec"
a = docparse.paragraphs(t0[tid]); b = docparse.paragraphs(t1[tid])
sm = difflib.SequenceMatcher(None, [p["text"] for p in a], [p["text"] for p in b], autojunk=False)
missing = 0; n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    for k in range(j1, j2):
        n += 1
        t = re.sub(r"\s+", " ", b[k]["text"]).strip()
        ok = t in ft
        if not ok:
            missing += 1
            print("NOT IN final_tab.md:", t[:110])
print("changed live paragraphs:", n, "| missing from final_tab.md:", missing)
