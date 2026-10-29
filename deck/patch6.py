import sys
d = sys.argv[1]
def patch(p, pairs):
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            raise SystemExit("MISMATCH %d in %s: %s" % (n, p, old[:70]))
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="\n").write(t)

patch(d + "\\deck_layouts.py", [
    ('''    cv.text_fit((x + 34, wy + 60, X1 - 20, wy + 160), wc["text"], 24, 15, "regular", C("ink"), max_lines=4, gap=1.15)
    nums = wc["numbers"]
    nw = (X1 - x - 34 - 20 - (len(nums) - 1) * 14) / float(len(nums))
    for i, n_ in enumerate(nums):
        nx = x + 34 + i * (nw + 14)
        ny = wy + 172
        cv.R(nx, ny, nx + nw, BY1 - 20, fill=tint(C("maroon"), 0.94), r=10)
        cv.text_fit((nx + 10, ny + 6, nx + nw - 10, ny + 64), n_["value"], 46, 24, "bold", C("maroon"), max_lines=1, align="center", valign="middle")
        cv.text_fit((nx + 10, ny + 64, nx + nw - 10, BY1 - 24), n_["label"], 20, 13, "regular", C("ink"), max_lines=2, align="center", gap=1.1)''',
     '''    cv.text_fit((x + 34, wy + 56, X1 - 20, wy + 148), wc["text"], 25, 18, "regular", C("ink"), max_lines=3, gap=1.15)
    nums = wc["numbers"]
    nw = (X1 - x - 34 - 20 - (len(nums) - 1) * 14) / float(len(nums))
    for i, n_ in enumerate(nums):
        nx = x + 34 + i * (nw + 14)
        ny = wy + 156
        cv.R(nx, ny, nx + nw, BY1 - 18, fill=tint(C("maroon"), 0.94), r=10)
        cv.text_fit((nx + 10, ny + 2, nx + nw - 10, ny + 56), n_["value"], 46, 24, "bold", C("maroon"), max_lines=1, align="center", valign="middle")
        cv.text_fit((nx + 10, ny + 56, nx + nw - 10, BY1 - 20), n_["label"], 22, 17, "regular", C("ink"), max_lines=2, align="center", gap=1.1)'''),
])
patch(d + "\\deckdraw.py", [
    ('self.font(17, "italic"), "#5A554C")', 'self.font(18, "italic"), "#5A554C")'),
])
print("ok")
