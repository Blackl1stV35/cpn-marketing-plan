import sys
d = sys.argv[1]

def patch(p, pairs):
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            raise SystemExit("MISMATCH %d in %s: %s" % (n, p, old[:90]))
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="\n").write(t)

patch(d + "\\build_deck.py", [
    ('    cv = Cv(W, H, K=2, bg="#FFFFFF")\n    M = 60', '    cv = Cv(W, H, K=2, bg="#FFFFFF")\n    cv.paren_max = 40\n    M = 60'),
])

p = d + "\\make_pdf.py"
t = open(p, encoding="utf-8").read()
# other-text block
a = t.index("    have = set()\n")
b = t.index("    if other:\n        add(\"Other text on the comp")
NEWOTHER = '''    alltext = norm(" ".join(v for k, v in E))
    nav_hit = [r for r in runs if norm(r[2]) in NAV]
    other, seen_runs = [], set()
    for r in runs:
        t_ = norm(r[2])
        if len(t_) < 2 or t_ in NAV or re.fullmatch(r"[\\d.,%\\u0e3f\\- /x]+", t_) or t_ in seen_runs:
            continue
        t2 = re.sub(r"^\\d+\\s+", "", t_)
        if t_ in alltext or t2 in alltext:
            continue
        seen_runs.add(t_)
        other.append(t_)
'''
t = t[:a] + NEWOTHER + t[b:]
open(p, "w", encoding="utf-8", newline="\n").write(t)

patch(p, [
    ("def acc_name(i):", "def fax(v, unit):\n    return (\"%g%%\" % v) if \"%\" in unit else num(v)\n\n\ndef fvu(v, unit):\n    return (\"%.1f%%\" % v) if \"%\" in unit else num(v)\n\n\ndef acc_name(i):"),
    ('        add("Tag", "%s  [%s]" % (s["section"], s["status"] if core else "BACKUP"))',
     '        add("Section chip", s["section"])\n        add("Status chip", s["status"] if core else "BACKUP")'),
    ('''                trunc = "; axis does not start at zero, so show the note 'Axis starts at %s'" % num(mt["vmin"]) if mt["vmin"] > 0 else "; starts at zero"
                add("Chart %d value axis" % ci, "%s to %s, gridlines every %s%s" % (num(mt["vmin"]), num(mt["vmax"]), num(mt["step"]), trunc))''',
     '''                trunc = "; the axis does not start at zero, so show the note 'Axis starts at %s'" % fax(mt["vmin"], ch["unit"]) if mt["vmin"] > 0 else "; starts at zero"
                add("Chart %d value axis" % ci, "%s to %s, gridlines every %s%s" % (fax(mt["vmin"], ch["unit"]), fax(mt["vmax"], ch["unit"]), fax(mt["step"], ch["unit"]), trunc))'''),
    ('" | ".join(num(v) for v in se["values"])))', '" | ".join(fvu(v, ch["unit"]) for v in se["values"])))'),
    ('add("Chart %d note under %s" % (ci, ch["categories"][an.get("category", 0)]), "%s (pale-yellow chip with gold outline)" % an["text"])',
     'add("Chart %d chip under %s (pale yellow, gold outline)" % (ci, ch["categories"][an.get("category", 0)]), an["text"])'),
    ('''        for i, t in enumerate(b["top"], 1):
            add("Watch %d" % i, "%s | %s | %s" % (t["risk"], t["trigger"], t["response"]))''',
     '''        for i, t in enumerate(b["top"], 1):
            add("Watch %d" % i, "%s | %s | %s" % (t["risk"], t["trigger"], t["response"]))
        if b.get("ladder"):
            ld = b["ladder"]
            add("Response ladder (three pills: Amber gold-dark, Red maroon, Crisis black)", ld["title"] + "\\n" + "\\n".join("%s | %s" % (st["name"], st["text"]) for st in ld["steps"]))'''),
    ('''                if t == "table":
                    add(label, " | ".join(bl["cols"]) + "\\n" + "\\n".join(" | ".join(r) for r in bl["rows"]))''',
     '''                if t == "table":
                    add(label, " | ".join(bl["cols"]) + "\\n" + "\\n".join(" | ".join(r) for r in bl["rows"]))
                    if bl.get("widths"):
                        add(label + ": column widths", " / ".join("%d%%" % round(w_ * 100) for w_ in bl["widths"]) + " (maroon header, zebra rows, first column bold maroon)")'''),
    ('''                elif t == "kpis":
                    add(label, "\\n".join("%s | %s" % (it["value"], it["label"]) for it in bl["items"]))''',
     '''                elif t == "kpis":
                    add(label if bl.get("title") else "Summary tiles", "\\n".join("%s | %s" % (it["value"], it["label"]) for it in bl["items"]))'''),
    ('if core else s["section"]\n            glyph_check(right', 'if core else "%s  ·  %s" % (s["section"], s["status"])\n            glyph_check(right'),
    ('"Cards, tiles and bars rotate through: maroon, gold-dark, teal, slate, purple. Card fill is the accent colour at 93% tint towards white with a 2 px outline in the accent colour; KPI tiles are white with a 14 px accent bar on top.",',
     '"Cards, tiles and bars on S2, S5, S6, S7 and S12 rotate through: maroon, gold-dark, teal, slate, purple. Card fill is the accent colour at 93% tint towards white with a 2 px outline in the accent colour; KPI tiles are white with a 14 px accent bar on top. S3: SWOT cards teal (Strengths), orange (Weaknesses), slate (Opportunities), maroon (Threats). S4: three columns with maroon, gold-dark and slate header bands.",'),
    ("table text 24 to 30 with a bold header row", "table text 19 to 30 on core slides (14 to 17 on reference pages) with a bold header row"),
    ("the superscript 2, the en dash and the 'at most' sign (<=).", "the superscript 2 and the en dash."),
    ('names = ["maroon", "gold", "golddark", "slate", "teal", "purple", "gray", "warn", "ink", "muted", "line", "faint", "edge", "mid"]\n        yy = H - (colour_label_y + 56)',
     'names = ["maroon", "gold", "golddark", "slate", "teal", "purple", "gray", "warn", "ink", "muted", "line", "faint", "edge", "mid", "#E8C85A", "#F0D78C", "#FFF8E1", "#F6F2EA", "#E6E1D7"]\n        yy = H - (colour_label_y + 56)'),
    ("    c.save()\n    print(\"pdf:\"", "    c.showOutline()\n    c.save()\n    print(\"pdf:\""),
])
print("patched")
