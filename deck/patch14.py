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

# ---------------- deckdraw.py: new binding block
p = d + "\\deckdraw.py"
t = open(p, encoding="utf-8").read()
a = t.index('NB = "\\u00a0"')
b = t.index("class Cv:")
BIND = '''NB = "\\u00a0"
_MON = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December"


def _join(m):
    return NB.join(m.groups())


def _join_in(m):
    return m.group(1) + NB + m.group(2).replace(" ", NB)


_BIND = [
    (re.compile(r"\\b(\\d{1,2}) (" + _MON + r") (\\d{4})\\b"), _join),
    (re.compile(r"\\b(" + _MON + r") (\\d{4})\\b"), _join),
    (re.compile(r"\\b(\\d{1,2}) (" + _MON + r")\\b"), _join),
    (re.compile(r"\\b([A-Z]\\d) (\\d{1,2} (?:" + _MON + r"))\\b"), _join_in),
    (re.compile(r"\\b(Gen) (Z)\\b"), _join),
    (re.compile(r"\\b(ages) (\\d+[\\u2013-]\\d+)"), _join),
    (re.compile(r"\\b(Q[1-4]) (\\d{2,4})\\b"), _join),
    (re.compile(r"(\\d[\\d,.]*) (million|billion|baht|percent|points?)\\b"), _join),
    (re.compile(r"\\b(million|billion) (baht)\\b"), _join),
    (re.compile(r"\\b([A-Z][a-z]+) (\\d{1,2})\\b"), _join),
    (re.compile(r"\\b(year|years) (\\d{1,2})\\b"), _join),
    (re.compile(r"\\b(The Central) (Phaholyothin)\\b"), _join),
]


def bind(s, pmax=18):
    """Keeps dates, ages, quarters, number+unit and short parentheticals on one line (non-breaking spaces)."""
    for rx, fn in _BIND:
        s = rx.sub(fn, s)
    return re.sub(r"(\\S+) (\\([^()]{1,%d}\\))" % pmax, _join_in, s)


'''
t = t[:a] + BIND + t[b:]
open(p, "w", encoding="utf-8", newline="\n").write(t)
patch(p, [
    ("        self.meta = []", "        self.meta = []\n        self.paren_max = 18"),
    ("for para in bind(str(s)).split(\"\\n\"):", "for para in bind(str(s), self.paren_max).split(\"\\n\"):"),
    ("cells = [self.wrap(str(r[i]) if i < len(r) else \"\", f, cw[i] - 2 * pad) for i in range(n)]",
     "cells = [self.wrap(str(r[i]) if i < len(r) else \"\", (fb if (i in tag_cols or (bold_first and i == 0)) else f), cw[i] - 2 * pad) for i in range(n)]"),
    ("            wide = any(self.tw(x, f) > cw[i] - 2 * pad + 0.5 for cells, _ in rls for i in range(n) for x in cells[i])",
     "            wide = (any(self.tw(x, (fb if (i in tag_cols or (bold_first and i == 0)) else f)) > cw[i] - 2 * pad + 0.5 for cells, _ in rls for i in range(n) for x in cells[i])\n                    or any(self.tw(x, fb) > cw[i] - 2 * pad + 0.5 for i in range(n) for x in hl[i]))"),
])

# ---------------- deck_layouts.py
p = d + "\\deck_layouts.py"
patch(p, [
    ('    cv.text_fit((X0, 94, X1, 232), s["headline"], 46, 30, "bold", C("maroon"), gap=1.16, max_lines=2)',
     '    cv.paren_max = 40\n    cv.text_fit((X0, 94, X1, 232), s["headline"], 46, 30, "bold", C("maroon"), gap=1.16, max_lines=2)\n    cv.paren_max = 18'),
    ('"Sources: " + "; ".join(x.replace(" ", NB) if len(x) <= 46 else x for x in s["sources"])',
     '"Sources: " + "; ".join(q.replace(" ", NB) if len(q) <= 46 else q for q in [z for x in s["sources"] for z in x.split("; ")])'),
    ("    hx, hy = 520, 624", "    hx, hy = 506, 624"),
    ("pos.append((hx + 288 * math.cos(a), hy + 238 * math.sin(a)))", "pos.append((hx + 276 * math.cos(a), hy + 238 * math.sin(a)))"),
])
p = d + "\\deck_layouts.py"
t = open(p, encoding="utf-8").read()
a = t.index("    # top risks\n    x = 1010\n")
b = t.index("# ------------------------------------------------------------------ takeaways")
NEW = '''    # top risks
    x = 1010
    has_l = "ladder" in b
    cv.T(x, BY0 + 2, "Three risks to watch", cv.font(30, "bold"), C("maroon"))
    rows = [[t["risk"], t["trigger"], t["response"]] for t in b["top"]]
    cv.table((x, BY0 + 56, X1, BY0 + (296 if has_l else 400)), ["Risk", "Trigger [Proposed]", "Response [Proposed]"], rows, [0.30, 0.35, 0.35], head_fill=C("maroon"),
             size_max=23, size_min=15, tag_cols=(0,), stretch=True, max_extra=40)
    if has_l:
        ld = b["ladder"]
        ly0 = BY0 + 308
        cv.T(x, ly0, ld["title"], cv.font(24, "bold"), C("maroon"))
        pill = {"Amber": C("golddark"), "Red": C("maroon"), "Crisis": C("ink")}
        for i, st in enumerate(ld["steps"]):
            yy = ly0 + 38 + i * 31
            cv.chip(x, yy, st["name"], 18, "#FFFFFF", bg=pill.get(st["name"], C("slate")), h=26, padx=14)
            cv.text_fit((x + 112, yy - 2, X1, yy + 28), st["text"], 21, 16, "regular", C("ink"), max_lines=1, valign="middle")
    wy = BY0 + (446 if has_l else 424)
    cv.R(x, wy, X1, BY1 - 4, fill="#FFFFFF", outline=C("maroon"), width=3, r=16)
    cv.R(x, wy, x + 14, BY1 - 4, fill=C("maroon"), r=7)
    wc = b["worst"]
    cv.text_fit((x + 34, wy + 12, X1 - 20, wy + 52), wc["title"], 30, 20, "bold", C("maroon"), max_lines=1)
    cv.text_fit((x + 34, wy + 54, X1 - 20, wy + (134 if has_l else 148)), wc["text"], 25, 18, "regular", C("ink"), max_lines=3, gap=1.15)
    nums = wc["numbers"]
    nw = (X1 - x - 34 - 20 - (len(nums) - 1) * 14) / float(len(nums))
    for i, n_ in enumerate(nums):
        nx = x + 34 + i * (nw + 14)
        ny = wy + (142 if has_l else 156)
        cv.R(nx, ny, nx + nw, BY1 - 18, fill=tint(C("maroon"), 0.94), r=10)
        cv.text_fit((nx + 10, ny + 2, nx + nw - 10, ny + 56), n_["value"], 46, 24, "bold", C("maroon"), max_lines=1, align="center", valign="middle")
        cv.text_fit((nx + 10, ny + 56, nx + nw - 10, BY1 - 20), n_["label"], 22, 17, "regular", C("ink"), max_lines=2, align="center", gap=1.1)


'''
t = t[:a] + NEW + t[b:]
open(p, "w", encoding="utf-8", newline="\n").write(t)

# ---------------- build_deck.py (outline text and headline binding)
p = d + "\\build_deck.py"
patch(p, [
    ('"headline = the sentence at the top of each slide (S1 shows a one-line summary instead)"', '"headline = the sentence at the top of each slide (S1 has none; its row shows a one-line summary)"'),
    ("page 2 is the build key (colours, type, layout rules).", "page 2 is the build key (frame, colours, type and chart rules)."),
    ('"Numbers and sources were checked against Chapters 4 to 6 of the report on 29 Oct 2026.",',
     '"Numbers and sources were checked against Chapters 4 to 6 of the report and the corrections log on 29 Oct 2026. Five items cited on B6 are in the log only, not in the report\'s reference list: the Central Retail release, the CPN 9 Apr 2026 release, the S&P Yearbook 2026, CPN IR 33.1% and the One Report 36%.",'),
])
print("patched")
