import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
def rep(old, new):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("MISMATCH %d for: %s" % (n, old[:60]))
    t = t.replace(old, new)

rep('''        left = x0 + 86
        right = x1 - 12
        n = len(cats)
        gw = (right - left) / float(n)
        fa_ = self.font(19, "semibold")''', '''        left = x0 + 86
        lines0 = [s for s in series if s.get("kind") == "line"]
        right = x1 - 12 - (76 if any(len(set(s["values"])) == 1 for s in lines0) else 0)
        n = len(cats)
        gw = (right - left) / float(n)
        fa_ = self.font(19, "semibold")''')
rep('''        step = nice_step((vmax - vmin) or 1, 4)
        vmax = math.ceil(vmax / step) * step if vmax > 0 else 0
        vmin = math.floor(vmin / step) * step if vmin < 0 else 0
        if vmax == vmin:
            vmax = vmin + step
        vmax_draw = vmax + step * 0.25

        def Y(v):''', '''        trunc = ch.get("ymin")
        if trunc is None and not stacked and bars and "%" in unit:
            pos = [v for v in vals_all if v > 0]
            if pos and len(pos) == len(vals_all) and (max(pos) - min(pos)) / max(pos) < 0.2:
                st0 = nice_step((max(pos) - min(pos)) * 2.4, 4)
                trunc = max(0, math.floor((min(pos) - (max(pos) - min(pos)) * 1.1) / st0) * st0)
        if trunc is not None:
            vmin = trunc
        step = nice_step((vmax - vmin) or 1, 4)
        vmax = math.ceil(vmax / step) * step if vmax > 0 else 0
        vmin = math.floor(vmin / step) * step if (vmin < 0 or trunc) else 0
        if vmax == vmin:
            vmax = vmin + step
        vmax_draw = vmax + step * 0.25
        base_v = vmin if vmin > 0 else 0

        def Y(v):''')
rep('''            zero = abs(tick) < 1e-9''', '''            zero = abs(tick - base_v) < 1e-9''')
rep('''            tick += step
        nb = 1 if stacked else max(1, len(bars))''', '''            tick += step
        if base_v > 0:
            self.T(x0, bottom + 14, "Axis starts at %s" % fmt_num(base_v, unit), self.font(17, "italic"), "#5A554C")
        flat_ys = [Y(s["values"][0]) for s in lines if len(set(s["values"])) == 1]
        nb = 1 if stacked else max(1, len(bars))''')
rep('''                    ytop, ybase = Y(max(v, 0)), Y(min(v, 0))
                    self.R(bx + 3, ytop, bx + bw - 3, ybase, fill=col_of(s))
                    ly = ytop - 8 if v >= 0 else ybase + 26
                    self.T(bx + bw / 2, ly, fmt_num(v, unit, False), self.font(20, "semibold"), "#1E1E1E", anchor="ms", halo=halo)''', '''                    ytop, ybase = Y(max(v, base_v)), Y(min(v, base_v))
                    self.R(bx + 3, ytop, bx + bw - 3, ybase, fill=col_of(s))
                    ls = max(15, min(20, bw * 0.34))
                    ly = ytop - 8 if v >= base_v else ybase + 26
                    if v >= base_v and ybase - ytop > ls * 1.8 and any(abs(fy - (ly - ls * 0.35)) < ls * 0.62 for fy in flat_ys):
                        self.T(bx + bw / 2, ytop + ls * 1.25, fmt_num(v, unit, False), self.font(ls, "semibold"), "#FFFFFF", anchor="ms")
                    else:
                        self.T(bx + bw / 2, ly, fmt_num(v, unit, False), self.font(ls, "semibold"), "#1E1E1E", anchor="ms", halo=halo)''')
rep('''                self.T(right - 2, pts[0][1] - 6, fmt_num(s["values"][0], unit, False), self.font(21, "bold"), col, anchor="rs", halo=halo)''',
    '''                self.T(right + 10, pts[0][1], fmt_num(s["values"][0], unit, False), self.font(21, "bold"), col, anchor="lm")''')
open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched")
