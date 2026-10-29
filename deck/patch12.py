import sys
d = sys.argv[1]
def patch(p, pairs):
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            raise SystemExit("MISMATCH %d in %s: %s" % (n, p, old[:80]))
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="\n").write(t)

BIND = '''NB = "\\u00a0"
_MON = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"


def _paren(m):
    return m.group(1) + NB + m.group(2).replace(" ", NB)


_BIND = [
    (re.compile(r"\\b(\\d{1,2}) (" + _MON + r") (\\d{4})\\b"), lambda m: NB.join(m.groups())),
    (re.compile(r"\\b(" + _MON + r") (\\d{4})\\b"), lambda m: NB.join(m.groups())),
    (re.compile(r"\\b(\\d{1,2}) (" + _MON + r")\\b"), lambda m: NB.join(m.groups())),
    (re.compile(r"\\b(Gen) (Z)\\b"), lambda m: NB.join(m.groups())),
    (re.compile(r"\\b(ages) (\\d+[\\u2013-]\\d+)"), lambda m: NB.join(m.groups())),
    (re.compile(r"\\b(Q[1-4]) (\\d{2,4})\\b"), lambda m: NB.join(m.groups())),
    (re.compile(r"(\\d[\\d,.]*) (million|billion|baht|percent|points?)\\b"), lambda m: NB.join(m.groups())),
    (re.compile(r"\\b(million|billion) (baht)\\b"), lambda m: NB.join(m.groups())),
    (re.compile(r"(\\S+) (\\([^()]{1,14}\\))"), _paren),
]


def bind(s):
    """Keeps dates, ages, quarters, number+unit and short parentheticals on one line (non-breaking spaces)."""
    for rx, fn in _BIND:
        s = rx.sub(fn, s)
    return s


'''

patch(d + "\\deckdraw.py", [
    ("import math\nimport os\nfrom PIL", "import math\nimport os\nimport re\nfrom PIL"),
    ("class Cv:\n    def __init__(self, w, h, K=2, bg=\"#FFFFFF\"):", BIND + "class Cv:\n    def __init__(self, w, h, K=2, bg=\"#FFFFFF\"):"),
    ("        self.used = []\n        self.runs = []", "        self.used = []\n        self.runs = []\n        self.meta = []"),
    ('        for para in str(s).split("\\n"):', '        for para in bind(str(s)).split("\\n"):'),
    ("            for word in para.split():", "            for word in [w_ for w_ in para.split(\" \") if w_]:"),
    ("    def chart(self, box, ch, palette=None):\n        palette = palette or PAL",
     '''    def chart_plan(self, box, ch):
        """Legend rows and height of the category notes, so paired charts can share one plot height."""
        x0, y0, x1, y1 = box
        f = self.font(21)
        lx, rows = x0, 1
        for se in ch["series"]:
            iw = 42 if se.get("kind") == "line" else 30
            item_w = iw + self.tw(se["name"], f) + 28
            if lx + item_w - 28 > x1 and lx > x0:
                lx = x0
                rows += 1
            lx += item_w
        left = x0 + 86
        lines0 = [s for s in ch["series"] if s.get("kind") == "line"]
        right = x1 - 12 - (76 if any(len(set(s["values"])) == 1 for s in lines0) else 0)
        gw = (right - left) / float(len(ch["categories"]))
        fa_ = self.font(19, "semibold")
        notes = {}
        for an in ch.get("annotations", []):
            notes.setdefault(an.get("category", 0), []).append(self.wrap(an["text"], fa_, gw - 20))
        extra = 0
        for lst in notes.values():
            extra = max(extra, sum(len(l_) * 24 + 20 for l_ in lst))
        return rows, extra

    def chart(self, box, ch, palette=None, min_rows=1, min_extra=0):
        palette = palette or PAL'''),
    ("        top = ty + 50\n        left = x0 + 86", "        ty = max(ty, y0 + 40 + 30 * (min_rows - 1))\n        top = ty + 50\n        left = x0 + 86"),
    ("self.wrap(an[\"text\"], fa_, gw - 40))\n        extra = 0\n        for lst in notes.values():\n            extra = max(extra, sum(len(l_) * 24 + 20 for l_ in lst))\n        bottom = y1 - 52 - extra",
     "self.wrap(an[\"text\"], fa_, gw - 20))\n        extra = 0\n        for lst in notes.values():\n            extra = max(extra, sum(len(l_) * 24 + 20 for l_ in lst))\n        extra = max(extra, min_extra)\n        bottom = y1 - 52 - extra"),
    ("        base_v = vmin if vmin > 0 else 0\n", "        base_v = vmin if vmin > 0 else 0\n        self.meta.append({\"title\": ch.get(\"title\", \"\"), \"unit\": unit, \"vmin\": vmin, \"vmax\": vmax, \"step\": step, \"type\": ch[\"type\"]})\n"),
    ("        for s in lines:\n            col = col_of(s)\n", "        for s in lines:\n            col = col_of(s)\n            tcol = PAL[\"golddark\"] if s.get(\"color\") == \"gold\" else col\n"),
    ("fmt_num(s[\"values\"][0], unit, False), self.font(21, \"bold\"), col, anchor=\"lm\")", "fmt_num(s[\"values\"][0], unit, False), self.font(21, \"bold\"), tcol, anchor=\"lm\")"),
    ("self.font(19, \"semibold\"), col, anchor=\"ls\", halo=halo)", "self.font(19, \"semibold\"), tcol, anchor=\"ls\", halo=halo)"),
])

patch(d + "\\deck_layouts.py", [
    ("from deckdraw import Cv, PAL, tint", "from deckdraw import Cv, PAL, tint, NB"),
    ('"Sources: " + "; ".join(s["sources"])', '"Sources: " + "; ".join(x.replace(" ", NB) if len(x) <= 46 else x for x in s["sources"])'),
    ('"Critical issues the plan must fix"', '"Critical issues for the plan"'),
    ('    tw_ = (X1 - X0 - 4 * 22) / 5.0\n    for i, t in enumerate(b["tiles"]):',
     '    tw_ = (X1 - X0 - 4 * 22) / 5.0\n    vsize = 88\n    for t in b["tiles"]:\n        while cv.tw(t["value"], cv.font(vsize, "bold")) > tw_ - 28 and vsize > 36:\n            vsize -= 1\n    for i, t in enumerate(b["tiles"]):'),
    ('t["value"], 88, 36, "bold", c, align="center"', 't["value"], vsize, vsize, "bold", c, align="center"'),
    ('size_max=30, size_min=16, tag_cols=(0,),\n             stretch=True, max_extra=120)', 'size_max=30, size_min=16, tag_cols=(0,), pad=16,\n             stretch=True, max_extra=120)'),
    ("    hx, hy = 506, 624", "    hx, hy = 520, 624"),
    ("pos.append((hx + 262 * math.cos(a), hy + 232 * math.sin(a)))", "pos.append((hx + 288 * math.cos(a), hy + 238 * math.sin(a)))"),
    ("    kw, kh = 428, 306", "    kw, kh = 428, 316"),
    ('cv.T(x + 18, y + 224, "Target", cv.font(19, "semibold"), C("muted"))', 'cv.T(x + 18, y + 224, "Target [Proposed]", cv.font(19, "semibold"), C("muted"))'),
    ('''    if len(charts) == 1:
        cv.chart((X0, top, X1, bot), charts[0])
    else:
        cv.chart((X0, top, 940, bot), charts[0])
        cv.chart((980, top, X1, bot), charts[1])''', '''    boxes = [(X0, top, X1, bot)] if len(charts) == 1 else [(X0, top, 940, bot), (980, top, X1, bot)]
    plans = [cv.chart_plan(bx, ch) for bx, ch in zip(boxes, charts)]
    mrows, mextra = max(p[0] for p in plans), max(p[1] for p in plans)
    for bx, ch in zip(boxes, charts):
        cv.chart(bx, ch, min_rows=mrows, min_extra=mextra)'''),
    ('''            ry = bottom + 18 + (gi % 2) * 44
''', '''            ry = bottom + 18 + (gi % 2) * 44
            if gi % 2 == 1:
                cv.line(gx, bottom + 10, gx, ry, C("maroon"), 3)
'''),
    ('    cv.line(spine_x, BY0 + 150, spine_x, uy0 + (len(units) - 1) * (uh + 14) + uh / 2, C("mid"), 3)',
     '    last = max([k for k, u_ in enumerate(units) if not u_.get("role", "").lower().startswith("existing")] or [0])\n    cv.line(spine_x, BY0 + 150, spine_x, uy0 + last * (uh + 14) + uh / 2, C("mid"), 3)'),
    ('''        cv.line(spine_x, y + uh / 2, x + 50, y + uh / 2, C("mid"), 3)
        cv.R(x + 50, y, X1, y + uh, fill="#FFFFFF", outline=acc(i + 1), width=3, r=12)
        cv.text_fit((x + 64, y + 8, X1 - 12, y + 46), u["name"], 25, 16, "bold", acc(i + 1), max_lines=1)''',
     '''        ex = u.get("role", "").lower().startswith("existing")
        ucol = C("mid") if ex else acc(i + 1)
        if not ex:
            cv.line(spine_x, y + uh / 2, x + 50, y + uh / 2, C("mid"), 3)
        cv.R(x + 50, y, X1, y + uh, fill="#FFFFFF", outline=ucol, width=3, r=12)
        cv.text_fit((x + 64, y + 8, X1 - 12, y + 46), u["name"], 25, 16, "bold", ucol, max_lines=1)'''),
    ('px = cx0 + 36 + (j % 4) * 46', 'px = cx0 + 36 + (j % 3) * 46'),
    ('py = cy0 + 36 + (j // 4) * 50', 'py = cy0 + 36 + (j // 3) * 50'),
    ('["Risk", "Trigger", "Response"], rows', '["Risk", "Trigger [Proposed]", "Response [Proposed]"], rows'),
    ('        size = max(13, 21 * sc)\n', '        size = max(15, 21 * sc)\n'),
    ('        hs, size_h, size_t = [], max(13, 22 * sc), max(12, 19 * sc)', '        hs, size_h, size_t = [], max(15, 22 * sc), max(14.5, 19 * sc)'),
    ('it["tag"], 16 * sc if sc > 0.7 else 13, "#FFFFFF"', 'it["tag"], max(14, 16 * sc), "#FFFFFF"'),
    ('it["label"], 20 * sc, 12,', 'it["label"], 20 * sc, 14,'),
])
# bullets and text blocks share the same size line (two occurrences): patch both
p = d + "\\deck_layouts.py"
t = open(p, encoding="utf-8").read()
assert t.count("        size = max(13, 22 * sc)\n") == 2
t = t.replace("        size = max(13, 22 * sc)\n", "        size = max(15, 22 * sc)\n")
open(p, "w", encoding="utf-8", newline="\n").write(t)
print("renderer patched")
