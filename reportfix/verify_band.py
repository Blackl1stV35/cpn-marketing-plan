"""Verifies the live Google Doc after the measurement-band change by diffing two dumps.

Usage: python -I verify_band.py REPORTFIX_DIR OLD_DUMP NEW_DUMP
"""
import collections
import difflib
import json
import os
import re
import sys

ROOT, OLD, NEW = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, ROOT)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
B = "t.8nyhv8rr5vec"
problems = []


def tabmap(path):
    d = docparse.load(path)
    return d, {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}


do, to = tabmap(OLD)
dn, tn = tabmap(NEW)
print("revision old:", do["revisionId"][:16], "new:", dn["revisionId"][:16])

for tid in to:
    if tid == B:
        continue
    same = [p["text"] for p in docparse.paragraphs(to[tid])] == [p["text"] for p in docparse.paragraphs(tn[tid])]
    print("tab %-16s %-18s unchanged: %s" % (tid, to[tid]["tabProperties"].get("title"), same))
    if not same:
        problems.append("tab changed " + tid)

po = docparse.paragraphs(to[B])
pn = docparse.paragraphs(tn[B])
a = [p["text"] for p in po]
b = [p["text"] for p in pn]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
print("\nparagraphs old %d new %d" % (len(a), len(b)))
nrep = 0
numtok = re.compile(r"\d[\d,\.]*%?")
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    if tag != "replace" or (i2 - i1) != (j2 - j1):
        problems.append("unexpected %s old[%d:%d] new[%d:%d]" % (tag, i1, i2, j1, j2))
        print("UNEXPECTED", tag, i1, i2, j1, j2)
        continue
    for k in range(i2 - i1):
        nrep += 1
        o, n = a[i1 + k], b[j1 + k]
        co, cn = collections.Counter(numtok.findall(o)), collections.Counter(numtok.findall(n))
        gained = cn - co
        lost = co - cn
        print("  replaced [%d] numbers gained %s lost %s" % (po[i1 + k]["start"], dict(gained), dict(lost)))
        allowed = {"20", "29", "18", "19", "20.", "29.", "29;", "18."}
        bad = [t for t in gained if t.strip(".,;") not in allowed]
        if bad or lost.keys() - {"18", "29", "18."}:
            # lost numbers other than age tokens would be suspicious
            extra = [t for t in lost if t.strip(".,;") not in {"18", "29"}]
            if bad or extra:
                problems.append("numbers changed in [%d]: gained %s lost %s" % (po[i1 + k]["start"], bad, extra))
print("replaced paragraphs:", nrep, "(expected 6)")
if nrep != 6:
    problems.append("replaced count %d" % nrep)

# replacements present once, old text gone
reqs = json.load(open(os.path.join(ROOT, "req_band.json"), encoding="utf-8"))
full = "".join(b)
for r in reqs:
    f = r["replaceAllText"]["containsText"]["text"]
    t = r["replaceAllText"]["replaceText"]
    ok = full.count(t) == 1 and full.count(f) == 0
    print("%s repl x%d old x%d | %s" % ("OK " if ok else "BAD", full.count(t), full.count(f), f[:55]))
    if not ok:
        problems.append("repl " + f[:40])

# stale phrases
stale = ["(18–29) share of footfall", "the same band as K1", "use this band", "reporting the 18–29 band",
         "measures Gen Z and young adults as ages 18 to 29", "surveys reach respondents aged 20 and over\n"]
for s in stale:
    n = full.count(s)
    print("stale %-55r x%d" % (s, n))
    if n:
        problems.append("stale " + s)

# remaining mentions of the band, for the record
pat = re.compile(r"18\s*(?:–|to)\s*29|20\s*(?:–|to)\s*29")
print("\nremaining band mentions:")
for p in pn:
    for m in pat.finditer(p["text"]):
        print("  [%d] ...%s..." % (p["start"], p["text"][max(0, m.start() - 55): m.end() + 55].replace("\n", " ")))
print("\nPROBLEMS:", problems if problems else "none")
