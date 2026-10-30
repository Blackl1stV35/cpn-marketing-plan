"""Writes one text file per tab of a saved read_doc dump: index, start, end, style, indent, text.

Usage: python -I dump_tabs.py SCRATCHPAD DUMP.json
Output: SCRATCHPAD/dumps/tab_<tabId>.txt (tab-separated; text last).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
SP = sys.argv[1]
d = docparse.load(sys.argv[2])
print("title:", d["title"], "| revision:", d["revisionId"])
for tb in docparse.walk_tabs(d["tabs"]):
    pr = tb["tabProperties"]
    ps = docparse.paragraphs(tb)
    name = os.path.join(SP, "dumps", "tab_%s.txt" % pr["tabId"])
    with open(name, "w", encoding="utf-8", newline="") as f:
        for i, p in enumerate(ps):
            ind = "" if p["indentStart"] is None else p["indentStart"]
            f.write("%d\t%d\t%d\t%s\t%s\t%s\n" % (i, p["start"], p["end"], p["style"] or "", ind, p["text"].rstrip("\n")))
    print(pr["tabId"], "|", pr.get("title"), "|", len(ps), "paragraphs | last end", ps[-1]["end"] if ps else None)
