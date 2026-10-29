import difflib, json, os, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
RF, OLD, NEW, REQ = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
def tm(path):
    d = docparse.load(path)
    return d, {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
do, to = tm(OLD); dn, tn = tm(NEW)
print("revision old", do["revisionId"][:16], "new", dn["revisionId"][:16])
bad = []
for tid in to:
    a = [p["text"] for p in docparse.paragraphs(to[tid])]
    b = [p["text"] for p in docparse.paragraphs(tn[tid])]
    if tid != "t.8nyhv8rr5vec":
        if a != b:
            bad.append("tab changed " + tid)
        continue
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag != "replace" or i2 - i1 != j2 - j1:
            bad.append("unexpected " + tag)
            continue
        n += i2 - i1
    print("Ch4-6 replaced paragraphs:", n)
full = "".join(p["text"] for p in docparse.paragraphs(tn["t.8nyhv8rr5vec"]))
for r in json.load(open(REQ, encoding="utf-8")):
    f = r["replaceAllText"]["containsText"]["text"]; t = r["replaceAllText"]["replaceText"]
    ok = full.count(t) == 1 and full.count(f) == 0
    print("%s repl x%d old x%d | %s" % ("OK " if ok else "BAD", full.count(t), full.count(f), f[:55]))
    if not ok:
        bad.append(f[:40])
print("PROBLEMS:", bad if bad else "none")
