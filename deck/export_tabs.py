"""Exports the plain text of selected tabs from a read_doc dump.

Usage: python -I export_tabs.py DUMP.json OUTDIR TAB_ID=filename [TAB_ID=filename ...]
Paragraphs become lines; table rows become " | " joined lines.
"""
import json
import os
import sys

dump, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
d = json.load(open(dump, encoding="utf-8"))
root = d.get("content", d)


def walk(ts):
    for t in ts:
        yield t
        yield from walk(t.get("childTabs", []))


def ptext(par):
    return "".join(r.get("textRun", {}).get("content", "") for r in par.get("elements", []))


tabs = {t["tabProperties"]["tabId"]: t for t in walk(root["tabs"])}
for spec in sys.argv[3:]:
    tab_id, fname = spec.split("=", 1)
    t = tabs[tab_id]
    lines = []
    for el in t["documentTab"]["body"]["content"]:
        if "paragraph" in el:
            s = ptext(el["paragraph"]).rstrip("\n")
            if s.strip():
                lines.append(s)
        elif "table" in el:
            for row in el["table"]["tableRows"]:
                cells = []
                for cell in row["tableCells"]:
                    cells.append(" ".join(" ".join(ptext(x["paragraph"]).split()) for x in cell["content"] if "paragraph" in x))
                lines.append(" | ".join(cells))
    with open(os.path.join(outdir, fname), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print(t["tabProperties"].get("title"), "->", fname, len(lines), "lines")
