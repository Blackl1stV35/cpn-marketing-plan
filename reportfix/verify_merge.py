"""Checks the live doc after the reference merge: one list in tab B, none in tab A, edits present.

Usage: python -I verify_merge.py SCRATCHPAD DUMP.json
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
SP, DUMP = sys.argv[1], sys.argv[2]
TAB_A, TAB_B = "t.pu1p2hjsan6g", "t.8nyhv8rr5vec"
d = docparse.load(DUMP)
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
pa = docparse.paragraphs(tabs[TAB_A])
pb = docparse.paragraphs(tabs[TAB_B])
print("revision:", d["revisionId"])


def key(text):
    m = re.match(r"^(.*?)\.?\s*\((?:(\d{4})([a-z]?)|n\.d\.-([a-z]))", text.strip())
    author = re.sub(r"[^a-z0-9]", "", m.group(1).lower())
    if m.group(4):
        return (author, 0, 0, m.group(4))
    return (author, 1, int(m.group(2)), m.group(3) or "")


all_a = "".join(p["text"] for p in pa)
all_b = "".join(p["text"] for p in pb)
print("tab A: 'References' paragraphs:", sum(1 for p in pa if p["text"].strip() == "References"),
      "| pointer present:", "References for Chapters 2 and 3 are in the combined reference list after Chapter 6." in all_a,
      "| 'Accenture.' still in A:", "Accenture. (2021)" in all_a)
hb = [i for i, p in enumerate(pb) if p["text"].strip() == "References"][0]
notes = pb[hb + 1]["text"]
entries = [p["text"].strip() for p in pb[hb + 2:] if p["text"].strip()]
urls = [re.search(r"https?://\S+", e).group(0) for e in entries if re.search(r"https?://\S+", e)]
print("tab B list entries:", len(entries), "| with URL:", len(urls), "| duplicate URLs:", len(urls) - len(set(urls)))
ks = [key(e) for e in entries]
print("tab B sorted:", all(ks[i] >= ks[i - 1] for i in range(1, len(ks))))
print("notes start:", notes.strip()[:60])
print("keys sentence:", "Keys 2025a and 2026b are unchanged from Chapters 2 and 3," in notes)
for s in ["four asset types: shopping centres, offices, hotels and residential projects.",
          "(Central Pattana, 2026h)", "Chapter 5 is different: Table 5.2 anchors",
          "labelled M1 to M5 in the order listed", "financial objective F1: that CPN sustain"]:
    print("present:", s[:50], "->", s in all_a or s in all_b)
print("'n.d.-h' left in A:", "n.d.-h" in all_a, "| 'Wikipedia' in A/B/X:", "Wikipedia" in all_a + all_b)
print("entries by label (first 6):", [e[:28] for e in entries[:6]])
