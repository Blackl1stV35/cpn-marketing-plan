import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
a = t.index("def lay_blocks(cv, s):")
b = t.index("LAYOUTS = {")
new = '''def lay_blocks(cv, s):
    cols = s["body"]["columns"]
    n = len(cols)
    gap = 40
    cw_ = (X1 - X0 - (n - 1) * gap) / float(n)
    avail = BY1 - BY0

    def fit(blocks):
        sc = 1.2
        while True:
            total = sum(block_h(cv, b, cw_, sc, False) + 18 for b in blocks)
            if total <= avail or sc <= 0.5:
                return sc, total
            sc -= 0.03

    fits = [fit(b) for b in cols]
    sc = min(f[0] for f in fits)
    for ci, blocks in enumerate(cols):
        x = X0 + ci * (cw_ + gap)
        total = sum(block_h(cv, b, cw_, sc, False) + 18 for b in blocks)
        if total > avail:
            cv.warn.append("blocks overflow column %d (scale %.2f, need %d of %d px)" % (ci + 1, sc, total, avail))
        y = BY0 + 6
        for b in blocks:
            h = block_h(cv, b, cw_, sc, True, x, y)
            y += h + 18


'''
t = t[:a] + new + t[b:]
open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
