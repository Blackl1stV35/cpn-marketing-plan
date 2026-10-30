"""Regenerates the report mirrors from a live read_doc dump and diffs them against the current mirror files.

Usage: python -I sync_mirrors.py SCRATCHPAD DUMP.json [DIFFLINES]
Writes SCRATCHPAD/reportfix/sync_out/<name> (new versions) and prints a unified diff against each mirror.
Tab B -> ch456/publish/final_tab.md (+ ch456/ch4.md, ch5.md, ch6.md split, ch456/publish/refs.md)
Tab A -> deck/src/sec23_final.txt ; tab X -> deck/src/appendix_week6.txt (plain text, one line per paragraph)
"""
import difflib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
SP, DUMP = sys.argv[1], sys.argv[2]
DIFFLINES = int(sys.argv[3]) if len(sys.argv) > 3 else 60
OUT = os.path.join(SP, "reportfix", "sync_out")
os.makedirs(OUT, exist_ok=True)
TAB_A, TAB_B, TAB_X = "t.pu1p2hjsan6g", "t.8nyhv8rr5vec", "t.x1zy13a445a4"

d = docparse.load(DUMP)
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}


def para_text(p):
    return "".join(e.get("textRun", {}).get("content", "") for e in p.get("elements", [])).replace("\n", "").replace("\x0b", " ")


def para_bold(p):
    runs = [e for e in p.get("elements", []) if "textRun" in e and e["textRun"].get("content", "").strip()]
    return bool(runs) and all(e["textRun"].get("textStyle", {}).get("bold") for e in runs)


def cell_text(cell):
    parts = []
    for el in cell.get("content", []):
        if "paragraph" in el:
            t = para_text(el["paragraph"]).strip()
            if t:
                parts.append(t)
    return " ".join(parts)


def blocks(tab):
    out = []
    for el in tab["documentTab"]["body"]["content"]:
        if "paragraph" in el:
            p = el["paragraph"]
            out.append(("p", para_text(p).strip(), para_bold(p)))
        elif "table" in el:
            rows = [[cell_text(c) for c in row["tableCells"]] for row in el["table"]["tableRows"]]
            out.append(("table", rows, False))
    return out


_old_lines = []
for _rel in ("ch456/publish/final_tab.md", "ch456/ch4.md", "ch456/ch5.md", "ch456/ch6.md"):
    with open(os.path.join(SP, _rel.replace("/", os.sep)), encoding="utf-8-sig") as f:
        _old_lines += f.read().replace("\r\n", "\n").split("\n")
SEP = {}
for _i in range(len(_old_lines) - 1):
    if _old_lines[_i].startswith("| ") and re.match(r"^\|[:\-|]+\|$", _old_lines[_i + 1]):
        SEP[_old_lines[_i]] = _old_lines[_i + 1]
H4SET = {l[5:].strip() for l in _old_lines if l.startswith("#### ")}


def infer_sep(rows):
    out = []
    for j in range(len(rows[0])):
        vals = [r[j].strip() for r in rows[1:] if j < len(r) and r[j].strip()]
        numeric = bool(vals) and all(re.fullmatch(r"[-+−]?[\d,.]+%?|-", v) for v in vals)
        out.append("---:" if numeric else ":---")
    return "|" + "|".join(out) + "|"


def render_b(tab):
    lines, in_refs = [], False
    for kind, payload, bold in blocks(tab):
        if kind == "table":
            header = "| " + " | ".join(payload[0]) + " |"
            sep = SEP.get(header) or infer_sep(payload)
            for i, r in enumerate(payload):
                lines.append("| " + " | ".join(r) + " |")
                if i == 0:
                    lines.append(sep)
            lines.append("")
            continue
        t = payload
        if not t:
            continue
        if t == "References":
            in_refs = True
            lines += ["## References", ""]
            continue
        if in_refs and not t.startswith("Notes on this list"):
            lines.append("@ref " + t)
            continue
        if t in H4SET:
            lines += ["#### " + t, ""]
        elif re.match(r"^\d+\. [A-Z]", t) and len(t) < 100:
            lines += ["## " + t, ""]
        elif re.match(r"^\d+\.\d+ [A-Z]", t) and len(t) < 100:
            lines += ["### " + t, ""]
        elif bold:
            lines += ["**" + t + "**", ""]
        else:
            lines += [t, ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def render_plain(tab, table_rows=False):
    lines = []
    for kind, payload, _bold in blocks(tab):
        if kind == "table":
            for r in payload:
                lines.append(" | ".join(r) if table_rows else " | ".join(r))
            continue
        if payload:
            lines.append(payload)
    return "\n".join(lines) + "\n"


def write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return os.path.join(OUT, name)


def compare(name, new_text, mirror_rel):
    mirror = os.path.join(SP, mirror_rel.replace("/", os.sep))
    with open(mirror, encoding="utf-8-sig", newline="") as f:
        old = f.read().replace("\r\n", "\n")
    diff = list(difflib.unified_diff(old.split("\n"), new_text.split("\n"), "mirror:" + mirror_rel, "live:" + name, lineterm="", n=0))
    changed = sum(1 for x in diff if x[:1] in "+-" and not x.startswith(("+++", "---")))
    print("== %s: changed lines %d (mirror %d lines, new %d lines)" % (name, changed, old.count("\n"), new_text.count("\n")))
    for x in diff[:DIFFLINES]:
        print("   " + x[:160])


b_text = render_b(tabs[TAB_B])
write("final_tab.md", b_text)
compare("final_tab.md", b_text, "ch456/publish/final_tab.md")

# chapter files: split the new final_tab at the chapter headings
parts = {}
current = None
for line in b_text.split("\n"):
    m = re.match(r"^## (\d)\. ", line)
    if m:
        current = m.group(1)
        parts[current] = []
    elif line.startswith("## References"):
        current = None
    if current:
        parts[current].append(line)
for n in ("4", "5", "6"):
    txt = "\n".join(parts[n]).rstrip("\n") + "\n"
    write("ch%s.md" % n, txt)
    compare("ch%s.md" % n, txt, "ch456/ch%s.md" % n)

refs_lines = [l for l in b_text.split("\n") if l.startswith("@ref ")]
refs_text = "\n".join(refs_lines) + "\n"
write("refs_entries.md", refs_text)
print("== refs entries in new final_tab:", len(refs_lines))

a_text = render_plain(tabs[TAB_A])
write("sec23_final.txt", a_text)
compare("sec23_final.txt", a_text, "deck/src/sec23_final.txt")

x_text = render_plain(tabs[TAB_X], table_rows=True)
write("appendix_week6.txt", x_text)
compare("appendix_week6.txt", x_text, "deck/src/appendix_week6.txt")
