"""Lists every table of a tab in body order: size, text just before it, first and last row, and cell indices.

Usage: python -I table_check.py DUMP.json TABID [--cells]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
DUMP, TAB = sys.argv[1], sys.argv[2]
SHOW_CELLS = "--cells" in sys.argv
d = docparse.load(DUMP)
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}


def ptext(p):
    return "".join(e.get("textRun", {}).get("content", "") for e in p.get("elements", [])).replace("\n", "")


prev = None
k = 0
for el in tabs[TAB]["documentTab"]["body"]["content"]:
    if "table" in el:
        k += 1
        rows = el["table"]["tableRows"]
        grid = []
        for r in rows:
            row = []
            for c in r["tableCells"]:
                paras = [x for x in c.get("content", []) if "paragraph" in x]
                txt = " / ".join(ptext(x["paragraph"]).strip() for x in paras if ptext(x["paragraph"]).strip())
                row.append((txt, paras[0]["startIndex"] if paras else None))
            grid.append(row)
        ncols = len(grid[0]) if grid else 0
        print("T%d start=%d rows=%d cols=%s | before: %r" % (k, el["startIndex"], len(rows), [len(r) for r in grid][:1] and ncols, (prev or "")[:45]))
        print("    row0:", [t[:22] for t, _ in grid[0]])
        print("    last:", [t[:22] for t, _ in grid[-1]])
        if SHOW_CELLS:
            for i, row in enumerate(grid):
                print("    r%d:" % i, [(t[:18], s) for t, s in row])
        prev = None
    elif "paragraph" in el:
        t = ptext(el["paragraph"]).strip()
        prev = t if t else prev
