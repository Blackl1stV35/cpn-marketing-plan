"""Merges the Chapters 2-3 reference list (tab A) into the Chapters 4-6 list (tab B) and builds update_doc requests.

Usage: python -I merge_refs.py SCRATCHPAD DUMP.json
Writes SCRATCHPAD/reportfix/req_merge_refs.json (requests + writeControl) and prints a summary.
Duplicates are matched by URL; A-only entries are placed before the first B entry that sorts after them.
"""
import bisect
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
SP, DUMP = sys.argv[1], sys.argv[2]
TAB_A, TAB_B = "t.pu1p2hjsan6g", "t.8nyhv8rr5vec"
RF = os.path.join(SP, "reportfix")

d = docparse.load(DUMP)
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
pa = docparse.paragraphs(tabs[TAB_A])
pb = docparse.paragraphs(tabs[TAB_B])


def heading(ps):
    hits = [i for i, p in enumerate(ps) if p["text"].strip() == "References"]
    print("'References' paragraphs at", hits, "| using the last one")
    return hits[-1]


ha, hb = heading(pa), heading(pb)
A = [p for p in pa[ha + 1:] if p["text"].strip()]
B = [p for p in pb[hb + 2:] if p["text"].strip()]
sent_a, sent_b = pa[-1], pb[-1]
assert not sent_a["text"].strip() and not sent_b["text"].strip()
print("A entries:", len(A), "| B entries:", len(B), "| B notes:", pb[hb + 1]["text"].strip()[:30])


def key(text):
    m = re.match(r"^(.*?)\.?\s*\((?:(\d{4})([a-z]?)|n\.d\.-([a-z]))", text.strip())
    if not m:
        raise SystemExit("no key in: " + text[:80])
    author = re.sub(r"[^a-z0-9]", "", m.group(1).lower())
    if m.group(4):
        return (author, 0, 0, m.group(4))
    return (author, 1, int(m.group(2)), m.group(3) or "")


def label(text):
    m = re.match(r"^(.*?)\.?\s*\((\d{4}[a-z]?|n\.d\.-[a-z])", text.strip())
    return m.group(2)


def url(text):
    m = re.search(r"https?://\S+", text)
    return m.group(0).rstrip(".") if m else None


B_urls = {url(p["text"]): p for p in B}
dups, a_only = [], []
for p in A:
    if url(p["text"]) in B_urls:
        dups.append((p, B_urls[url(p["text"])]))
    else:
        a_only.append(p)
print("duplicates (same URL):", len(dups), "| A-only:", len(a_only))
for p, q in dups:
    if label(p["text"]) != label(q["text"]):
        print("  label differs: A %s -> B %s | %s" % (label(p["text"]), label(q["text"]), q["text"].strip()[:60]))

kB = [key(p["text"]) for p in B]
viol = [i for i in range(1, len(kB)) if kB[i] < kB[i - 1]]
print("B order violations:", viol)
assert not viol

groups = {}
for p in sorted(a_only, key=lambda p: key(p["text"])):
    pos = bisect.bisect_right(kB, key(p["text"]))
    groups.setdefault(pos, []).append(p)
ins = []
for pos, items in groups.items():
    index = B[pos]["start"] if pos < len(B) else sent_b["start"]
    text = "".join(p["text"].strip() + "\n" for p in items)
    succ = B[pos]["text"].strip()[:35] if pos < len(B) else "(end of list)"
    ins.append((index, text, succ, [label(p["text"]) + " " + p["text"].strip()[:25] for p in items]))
    print("insert before [%s] -> %s" % (succ, "; ".join(x[:40] for x in ins[-1][3])))
ins.sort(key=lambda x: x[0], reverse=True)

POINTER = "References for Chapters 2 and 3 are in the combined reference list after Chapter 6."
reqs = [{"insertText": {"location": {"index": i, "tabId": TAB_B}, "text": t}} for i, t, _s, _l in ins]
reqs.append({"deleteContentRange": {"range": {"startIndex": pa[ha]["start"], "endIndex": sent_a["start"], "tabId": TAB_A}}})
reqs.append({"insertText": {"location": {"index": pa[ha]["start"], "tabId": TAB_A}, "text": POINTER + "\n"}})

REPL = [
    (TAB_A, "CPN's physical portfolio is built around four asset classes.",
     "CPN's physical portfolio is built around four asset types: shopping centres, offices, hotels and residential projects."),
    (TAB_A, "(Central Pattana, n.d.-h)", "(Central Pattana, 2026h)"),
    (TAB_A, "framed as such in the text rather than cited as company fact.",
     "framed as such in the text rather than cited as company fact. Chapter 5 is different: Table 5.2 anchors several of its assumptions to CPN's published 2026 guidance, each cited to its source."),
    (TAB_A, "The following marketing objectives are proposed by the team, built to extend CPN's stated strategic direction rather than reproducing official company guidance:",
     "The five marketing objectives below, labelled M1 to M5 in the order listed, are proposed by the team, built to extend CPN's stated strategic direction rather than reproducing official company guidance:"),
    (TAB_A, "On this basis, the team proposes that CPN sustain",
     "On this basis, the team proposes financial objective F1: that CPN sustain"),
    (TAB_B, "Notes on this list. Letter suffixes", "Notes on this list, which covers Chapters 2 to 6. Letter suffixes"),
    (TAB_B, "Keys 2025a and 2026b come from the Section 2–3 list unchanged,", "Keys 2025a and 2026b are unchanged from Chapters 2 and 3,"),
]
texts = {TAB_A: "".join(p["text"] for p in pa), TAB_B: "".join(p["text"] for p in pb)}
problems = []
for tab, old, new in REPL:
    n = texts[tab].count(old)
    print("%s x%d  %s" % ("ok " if n == 1 else "BAD", n, old[:60]))
    if n != 1:
        problems.append(old[:40])
    reqs.append({"replaceAllText": {"containsText": {"text": old, "matchCase": True}, "replaceText": new,
                                    "tabsCriteria": {"tabIds": [tab]}}})

print("requests:", len(reqs), "| problems:", problems or "none")
print("expected list length after merge:", len(B) + len(a_only) - 0, "(B %d + A-only %d)" % (len(B), len(a_only)))
with open(os.path.join(RF, "req_merge_refs.json"), "w", encoding="utf-8") as f:
    json.dump({"requiredRevisionId": d["revisionId"], "requests": reqs}, f, ensure_ascii=False)
print("written:", os.path.join(RF, "req_merge_refs.json"))
