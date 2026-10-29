"""Turns hyphens in numeric, quarter, month and code ranges into en dashes across the slide specs (not the facts lists).

Usage: python -I apply_dashes.py DECKDIR [--write]     (without --write it only reports what would change)
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = sys.argv[1]
WRITE = "--write" in sys.argv
MON = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
EN = "–"
RULES = [
    (re.compile(r"(?<![\w.\-])(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)(?![\w.\-]*\w)"), r"\1" + EN + r"\2"),
    (re.compile(r"\b(Q[1-4])-(Q[1-4])\b"), r"\1" + EN + r"\2"),
    (re.compile(r"\b(" + MON + r")-(" + MON + r")\b"), r"\1" + EN + r"\2"),
    (re.compile(r"(\b\d{1,2} (?:" + MON + r"))-(\d{1,2} )"), r"\1" + EN + r"\2"),
    (re.compile(r"(\b(?:" + MON + r"))-(\d{1,2} (?:" + MON + r"))"), r"\1" + EN + r"\2"),
    (re.compile(r"\b([MFDKCRPS]\d{1,2})-([MFDKCRPS]\d{1,2})\b"), r"\1" + EN + r"\2"),
]
SKIP = {"facts", "id", "kind", "layout", "status", "color", "tone", "type", "likelihood", "impact"}
changes = []


def fix(s):
    out = s
    for rx, rep in RULES:
        out = rx.sub(rep, out)
    return out


def walk(o, path):
    if isinstance(o, str):
        n = fix(o)
        if n != o:
            changes.append((path, o, n))
        return n
    if isinstance(o, dict):
        return {k: (v if k in SKIP else walk(v, path + "." + k)) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v, "%s[%d]" % (path, i)) for i, v in enumerate(o)]
    return o


for p in sorted(glob.glob(os.path.join(ROOT, "specs", "slide_*.json"))):
    d = json.load(open(p, encoding="utf-8-sig"))
    nd = walk(d, os.path.basename(p)[6:-5])
    if WRITE and nd != d:
        open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(nd, ensure_ascii=False, indent=2) + "\n")
print("strings changed:", len(changes))
for path, a, b in changes[:60]:
    import difflib
    sm = difflib.SequenceMatcher(None, a, b)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            print("  %s: ...%s -> %s..." % (path[:34], a[max(0, i1 - 14):i2 + 10], b[max(0, j1 - 14):j2 + 10]))
            break
