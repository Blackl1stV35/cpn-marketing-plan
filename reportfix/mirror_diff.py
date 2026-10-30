"""Compares live doc tabs with local mirror files, paragraph by paragraph (markup and table pipes ignored).

Usage: python -I mirror_diff.py SCRATCHPAD DUMP.json
Prints live paragraphs missing from the mirror ('LIVE ONLY') and mirror lines missing from the live doc ('MIRROR ONLY').
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
SP, DUMP = sys.argv[1], sys.argv[2]
PAIRS = [
    ("t.8nyhv8rr5vec", ["ch456/publish/final_tab.md"], "tab B"),
    ("t.8nyhv8rr5vec", ["ch456/ch4.md", "ch456/ch5.md", "ch456/ch6.md"], "tab B vs ch4/5/6"),
    ("t.pu1p2hjsan6g", ["deck/src/sec23_final.txt"], "tab A"),
    ("t.x1zy13a445a4", ["deck/src/appendix_week6.txt"], "tab X"),
]
MODE = os.environ.get("DIFF_ONLY", "")


def norm(s):
    s = s.replace("**", "").replace("__", "")
    s = re.sub(r"^\s*#+\s*", "", s)
    s = re.sub(r"^\s*@ref\s+", "", s)
    s = re.sub(r"^\s*[-•]\s+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def mirror_units(path):
    units = []
    with open(path, encoding="utf-8-sig") as f:
        for raw in f.read().split("\n"):
            line = raw.strip()
            if not line:
                continue
            if line.startswith("|") and line.count("|") >= 2:
                if re.match(r"^\|[\s:|-]+\|$", line):
                    continue
                for cell in line.strip("|").split("|"):
                    if cell.strip():
                        units.append(norm(cell))
            else:
                units.append(norm(line))
    return [u for u in units if u]


d = docparse.load(DUMP)
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
for tab_id, files, label in PAIRS:
    live = [norm(p["text"]) for p in docparse.paragraphs(tabs[tab_id]) if p["text"].strip()]
    mir = []
    for rel in files:
        mir += mirror_units(os.path.join(SP, rel.replace("/", os.sep)))
    ms, ls = set(mir), set(live)
    live_only = [t for t in live if t not in ms]
    mirror_only = [t for t in mir if t not in ls]
    print("== %s (%s): live %d, mirror %d | LIVE ONLY %d | MIRROR ONLY %d" % (label, " + ".join(files), len(live), len(mir), len(live_only), len(mirror_only)))
    if MODE != "quiet":
        for t in live_only:
            print("  LIVE   :", t[:150])
        for t in mirror_only:
            print("  MIRROR :", t[:150])
