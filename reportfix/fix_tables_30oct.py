"""Fixes three defects in the live tab B (ch4ch5ch6_report) found on 30 Oct 2026:
  1. Tables 4.2 and 4.3: the header's first cell sits in a stray paragraph above the table, so every cell is one place late.
     Fix: delete the stray paragraph and rewrite each cell so cell k holds the sequence value k (row-major).
  2. Budget table: two captions ('Table 4.1...' above the text and 'Proposed FY2027...' above the table).
     Fix: keep one caption above the table, 'Table 4.1. FY2027 marketing budget, lines 1 to 11 (team proposal)', in bold.

Usage: python -I fix_tables_30oct.py SCRATCHPAD DUMP.json REVISION_ID
Writes SCRATCHPAD/reportfix/req_fix_tables.json and prints a summary.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
SP, DUMP, REV = sys.argv[1], sys.argv[2], sys.argv[3]
TAB_B = "t.8nyhv8rr5vec"
CAPTION = "Table 4.1. FY2027 marketing budget, lines 1 to 11 (team proposal)"
OLD_CAPTION = "Proposed FY2027 marketing budget by tactic (THB million)"
OLD_TABLE_CAPTION = "Table 4.1. FY2027 marketing budget, lines 1 to 11 (team proposal)"

d = docparse.load(DUMP)
tab = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}[TAB_B]
body = tab["documentTab"]["body"]["content"]


def ptext(p):
    return "".join(e.get("textRun", {}).get("content", "") for e in p.get("elements", [])).replace("\n", "")


def cell_text(cell):
    return " ".join(ptext(x["paragraph"]).strip() for x in cell.get("content", []) if "paragraph" in x and ptext(x["paragraph"]).strip())


tables = []
cap_above, cap_table = None, None
for i, el in enumerate(body):
    if "paragraph" in el:
        t = ptext(el["paragraph"]).strip()
        if t == OLD_TABLE_CAPTION:
            cap_above = el
        if t == OLD_CAPTION:
            cap_table = el
    if "table" in el and i > 0 and "paragraph" in body[i - 1]:
        stray = ptext(body[i - 1]["paragraph"]).strip()
        if stray in ("Term", "Attribute"):
            cells = []
            for r in el["table"]["tableRows"]:
                for c in r["tableCells"]:
                    p = [x for x in c.get("content", []) if "paragraph" in x][0]
                    cells.append((p["startIndex"], p["endIndex"], cell_text(c)))
            S = [t for _, _, t in cells]
            assert S[-1] == "", (stray, S[-1])
            D = [stray] + S[:-1]
            tables.append((body[i - 1]["startIndex"], body[i - 1]["endIndex"], cells, D, stray))
            print("table after '%s': %d cells; row0 now %s" % (stray, len(cells), S[:5]))
assert cap_above and cap_table, (cap_above is not None, cap_table is not None)
print("caption above text at", cap_above["startIndex"], cap_above["endIndex"], "| old caption at", cap_table["startIndex"], cap_table["endIndex"])

reqs = []
# 2. budget caption: rewrite the table caption (higher index) and delete the caption above the text
s, e = cap_table["startIndex"], cap_table["endIndex"]
reqs.append({"deleteContentRange": {"range": {"startIndex": s, "endIndex": e - 1, "tabId": TAB_B}}})
reqs.append({"insertText": {"location": {"index": s, "tabId": TAB_B}, "text": CAPTION}})
reqs.append({"updateTextStyle": {"range": {"startIndex": s, "endIndex": s + len(CAPTION), "tabId": TAB_B},
                                 "textStyle": {"bold": True}, "fields": "bold"}})
reqs.append({"deleteContentRange": {"range": {"startIndex": cap_above["startIndex"], "endIndex": cap_above["endIndex"], "tabId": TAB_B}}})

# 1. table shifts: work from the last table to the first, last cell to first
for stray_s, stray_e, cells, D, stray in sorted(tables, key=lambda x: -x[0]):
    for k in reversed(range(len(cells))):
        cs, ce, old = cells[k]
        new = D[k]
        if old == new:
            continue
        if old:
            reqs.append({"deleteContentRange": {"range": {"startIndex": cs, "endIndex": ce - 1, "tabId": TAB_B}}})
        reqs.append({"insertText": {"location": {"index": cs, "tabId": TAB_B}, "text": new}})
    reqs.append({"deleteContentRange": {"range": {"startIndex": stray_s, "endIndex": stray_e, "tabId": TAB_B}}})

with open(os.path.join(SP, "reportfix", "req_fix_tables.json"), "w", encoding="utf-8") as f:
    json.dump({"requiredRevisionId": REV, "requests": reqs}, f, ensure_ascii=False)
print("requests:", len(reqs))
print(json.dumps(reqs, ensure_ascii=False))
