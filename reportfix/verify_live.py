"""Verifies the live Google Doc after the report + reference fix by diffing two dumps (before and after).

Usage: python -I verify_live.py REPORTFIX_DIR OLD_DUMP NEW_DUMP
"""
import difflib
import json
import os
import sys

ROOT, OLD, NEW = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, ROOT)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
A = "t.pu1p2hjsan6g"
B = "t.8nyhv8rr5vec"


def tabmap(path):
    d = docparse.load(path)
    return d, {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}


do, to = tabmap(OLD)
dn, tn = tabmap(NEW)
print("revision old:", do["revisionId"][:16], "new:", dn["revisionId"][:16])
problems = []

# 1. other tabs unchanged
for tid in to:
    if tid in (A, B):
        continue
    a = [p["text"] for p in docparse.paragraphs(to[tid])]
    b = [p["text"] for p in docparse.paragraphs(tn[tid])]
    same = a == b
    print("tab %-16s %-18s unchanged: %s" % (tid, to[tid]["tabProperties"].get("title"), same))
    if not same:
        problems.append("tab changed: " + tid)

# 2. paragraph-level diff on the two edited tabs
for tid in (A, B):
    po = docparse.paragraphs(to[tid])
    pn = docparse.paragraphs(tn[tid])
    a = [p["text"] for p in po]
    b = [p["text"] for p in pn]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    print("\n== diff for", tid, "old paras", len(a), "new paras", len(b))
    nrep = nins = ndel = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace":
            nrep += i2 - i1
            print("  replace old[%d:%d] -> new[%d:%d]" % (i1, i2, j1, j2))
            for k in range(j1, j2):
                print("      new:", b[k].strip()[:110])
        elif tag == "insert":
            nins += j2 - j1
            print("  insert  new[%d:%d]" % (j1, j2))
            for k in range(j1, j2):
                p = pn[k]
                print("      new:", b[k].strip()[:100], "| style", p["style"], "indS", p["indentStart"], "indF", p["indentFirst"], "runs", len(p["runs"]))
        else:
            ndel += i2 - i1
            print("  DELETE old[%d:%d]" % (i1, i2))
            problems.append("deleted paragraphs in " + tid)
    print("  totals: replaced %d, inserted %d, deleted %d" % (nrep, nins, ndel))

# 3. every replacement present once, old text gone
for name, tid, path in (("sec23", A, "req_sec23.json"), ("ch456", B, "req_ch456.json")):
    reqs = json.load(open(os.path.join(ROOT, path), encoding="utf-8"))
    full = "".join(p["text"] for p in docparse.paragraphs(tn[tid]))
    for r in reqs:
        if "replaceAllText" not in r:
            continue
        find = r["replaceAllText"]["containsText"]["text"]
        repl = r["replaceAllText"]["replaceText"]
        nrepl = full.count(repl)
        nfind = full.count(find)
        expect_find = 1 if repl.startswith(find) else 0
        ok = nrepl >= 1 and nfind == expect_find
        print("%s %s repl x%d, old x%d | %s" % ("OK " if ok else "BAD", name, nrepl, nfind, find[:60]))
        if not ok:
            problems.append("replacement " + find[:40])

# 4. new reference paragraphs: style equals neighbours' style
pn = docparse.paragraphs(tn[A])
head = [p for p in pn if p["text"].strip() == "References"][-1]["start"]
refs = [p for p in pn if p["start"] > head and p["text"].strip()]
keys = ["S&P Global. (2026)", "Nation Thailand. (2026g", "Nation Thailand. (2026l", "Government Public Relations Department. (2026",
        "Central Retail Corporation. (2026", "Central Pattana. (2026t", "Central Pattana Investor Relations. (n.d.-c)"]
print()
for k in keys:
    idx = [i for i, p in enumerate(refs) if p["text"].startswith(k)]
    if len(idx) != 1:
        print("BAD ref", k, idx)
        problems.append("ref " + k)
        continue
    i = idx[0]
    p = refs[i]
    prev, nxt = refs[i - 1], refs[(i + 1) % len(refs)]
    style = p["runs"][0][2] if p["runs"] else None
    pstyle = prev["runs"][0][2] if prev["runs"] else None
    print("ref ok: %-46s indS %s indF %s runs %d same-run-style-as-prev %s" % (k, p["indentStart"], p["indentFirst"], len(p["runs"]), style == pstyle))
    print("     prev:", prev["text"].strip()[:70])
    print("     next:", nxt["text"].strip()[:70])
    if p["indentStart"] != 48 or p["indentFirst"] != 24 or style != pstyle:
        problems.append("ref style " + k)

# 5. new keys cited in the body (outside the reference list)
body = "".join(p["text"] for p in pn if p["start"] < head)
for cite in ["Government Public Relations Department, 2026", "Nation Thailand, 2026g", "2026l", "Central Retail Corporation, 2026",
             "Central Pattana, 2026t", "Central Pattana Investor Relations, n.d.-c", "S&P Global, 2026"]:
    n = body.count(cite)
    print("cited in body: %-48s x%d" % (cite, n))
    if n == 0:
        problems.append("orphan " + cite)

# 6. stale phrases
stale_a = ["22 million members as of September 2025", "pre-pandemic peak", "roughly 30%", "86.7% of GDP in the fourth quarter of 2025, a fragile",
           "hit 86.7%", "DJSI Best-in-Class sustainability indices"]
stale_b = ["adults only", "adults-only", "aged 18 and over", "1,500 adults", "reach adults"]
fa = "".join(p["text"] for p in docparse.paragraphs(tn[A]))
fb = "".join(p["text"] for p in docparse.paragraphs(tn[B]))
for s in stale_a:
    print("stale A %-55s x%d" % (s, fa.count(s)))
    if fa.count(s):
        problems.append("stale A " + s)
for s in stale_b:
    print("stale B %-55s x%d" % (s, fb.count(s)))
    if fb.count(s):
        problems.append("stale B " + s)

print("\nPROBLEMS:", problems if problems else "none")
