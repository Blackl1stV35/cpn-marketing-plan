import sys
def patch(p, pairs):
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            raise SystemExit("MISMATCH %d in %s: %s" % (n, p, old[:60]))
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="\n").write(t)

d = sys.argv[1]
patch(d + "\\deckdraw.py", [
    ('bw = min(96.0, gw * 0.7 / nb)', 'bw = min(96.0, gw * 0.8 / nb)'),
    ('if v >= base_v and ybase - ytop > ls * 1.8 and any(abs(fy - (ly - ls * 0.35)) < ls * 0.62 for fy in flat_ys):',
     'if (v >= base_v and ybase - ytop > ls * 1.8 and any(abs(fy - (ly - ls * 0.35)) < ls * 0.62 for fy in flat_ys)\n                            and self.tw(fmt_num(v, unit, False), self.font(ls, "semibold")) <= bw - 8):'),
])
patch(d + "\\deck_layouts.py", [
    ('    mx0, my0, cs = 150, BY0 + 66, 152\n', '    mx0, my0, cs, chh = 150, BY0 + 92, 190, 140\n'),
    ('            x = mx0 + im * cs\n            y = my0 + row * cs\n            cv.R(x, y, x + cs - 3, y + cs - 3, fill=tint(C("maroon"), shades[li + im]), r=6)',
     '            x = mx0 + im * cs\n            y = my0 + row * chh\n            cv.R(x, y, x + cs - 3, y + chh - 3, fill=tint(C("maroon"), shades[li + im]), r=6)'),
    ('        cv.T(mx0 - 22, my0 + i * cs + cs / 2, lab, cv.font(26, "bold"), C("muted"), anchor="mm")',
     '        cv.T(mx0 - 22, my0 + i * chh + chh / 2, lab, cv.font(26, "bold"), C("muted"), anchor="mm")'),
    ('        cv.T(mx0 + i * cs + cs / 2, my0 + 3 * cs + 20, lab, cv.font(26, "bold"), C("muted"), anchor="mm")',
     '        cv.T(mx0 + i * cs + cs / 2, my0 + 3 * chh + 20, lab, cv.font(26, "bold"), C("muted"), anchor="mm")'),
    ('    cv.T(X0, my0 - 34, "Likelihood", cv.font(21, "semibold"), C("muted"))\n    cv.T(mx0 + 3 * cs, my0 + 3 * cs + 20, "Impact", cv.font(21, "semibold"), C("muted"), anchor="lm")',
     '    cv.T(X0, my0 - 30, "Likelihood", cv.font(21, "semibold"), C("muted"))\n    cv.T(mx0 + 3 * cs + 10, my0 + 3 * chh + 20, "Impact", cv.font(21, "semibold"), C("muted"), anchor="lm")'),
    ('        cy0 = my0 + row * cs\n        for j, r in enumerate(rs):\n            px = cx0 + 38 + (j % 3) * 46\n            py = cy0 + 40 + (j // 3) * 52',
     '        cy0 = my0 + row * chh\n        for j, r in enumerate(rs):\n            px = cx0 + 36 + (j % 4) * 46\n            py = cy0 + 36 + (j // 4) * 50'),
    ('    ly = my0 + 3 * cs + 62\n', '    ly = my0 + 3 * chh + 58\n'),
    ('        lx = X0 + col_i * 460\n', '        lx = X0 + col_i * 470\n'),
])
print("ok")
