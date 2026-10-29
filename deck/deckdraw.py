"""Drawing library for the deck comps (Pillow, supersampled)."""
import math
import os
import re
from PIL import Image, ImageDraw, ImageFont

FONTDIR = "C:\\Windows\\Fonts\\"
FILES = {"regular": "segoeui.ttf", "bold": "segoeuib.ttf", "semibold": "seguisb.ttf", "light": "segoeuil.ttf", "italic": "segoeuii.ttf"}

PAL = dict(
    bg="#FFFFFF", ink="#1E1E1E", muted="#5A554C", line="#D8D2C6", faint="#F1EDE5", edge="#BDB7AA", mid="#9A9385",
    maroon="#8C1D28", gold="#C9A227", golddark="#855C00", slate="#2F4B7C", teal="#1B6B5A", purple="#5B3F8C", gray="#8A857B",
    good="#1B6B5A", warn="#B4531A", neutral="#5A554C", white="#FFFFFF",
)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def tint(h, t):
    r, g, b = hex2rgb(h)
    return "#%02x%02x%02x" % tuple(int(round(v * (1 - t) + 255 * t)) for v in (r, g, b))


def nice_step(span, ticks=4):
    raw = span / float(ticks)
    mag = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            return m * mag
    return 10 * mag


def fmt_num(v, unit="", trim=True):
    if v is None:
        return ""
    if "%" in unit:
        s = "%.1f" % v
        return (s.rstrip("0").rstrip(".") if trim else s) + "%"
    if abs(v) >= 1000 or float(v).is_integer():
        return "{:,.0f}".format(v)
    return ("%.1f" % v)


NB = "\u00a0"
_MON = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December"


def _join(m):
    return NB.join(m.groups())


def _join_in(m):
    return m.group(1) + NB + m.group(2).replace(" ", NB)


_BIND = [
    (re.compile(r"\b(\d{1,2}) (" + _MON + r") (\d{4})\b"), _join),
    (re.compile(r"\b(" + _MON + r") (\d{4})\b"), _join),
    (re.compile(r"\b(\d{1,2}) (" + _MON + r")\b"), _join),
    (re.compile(r"\b([A-Z]\d) (\d{1,2} (?:" + _MON + r"))\b"), _join_in),
    (re.compile(r"\b(Gen) (Z)\b"), _join),
    (re.compile(r"\b(ages) (\d+[\u2013-]\d+)"), _join),
    (re.compile(r"\b(Q[1-4]) (\d{2,4})\b"), _join),
    (re.compile(r"(\d[\d,.]*) (million|billion|baht|percent|points?)\b"), _join),
    (re.compile(r"\b(million|billion) (baht)\b"), _join),
    (re.compile(r"\b([A-Z][a-z]+) (\d{1,2})\b"), _join),
    (re.compile(r"\b(year|years) (\d{1,2})\b"), _join),
    (re.compile(r"\b(The Central) (Phaholyothin)\b"), _join),
]


def bind(s, pmax=18):
    """Keeps dates, ages, quarters, number+unit and short parentheticals on one line (non-breaking spaces)."""
    for rx, fn in _BIND:
        s = rx.sub(fn, s)
    return re.sub(r"(\S+) (\([^()]{1,%d}\))" % pmax, _join_in, s)


class Cv:
    def __init__(self, w, h, K=2, bg="#FFFFFF"):
        self.w, self.h, self.K = w, h, K
        self.img = Image.new("RGB", (w * K, h * K), bg)
        self.d = ImageDraw.Draw(self.img)
        self._fc = {}
        self.warn = []
        self.used = []
        self.runs = []
        self.meta = []
        self.paren_max = 18

    # -------------------------------------------------- primitives
    def k(self, v):
        return int(round(v * self.K))

    def font(self, size, weight="regular"):
        key = (round(size * 2) / 2.0, weight)
        if key not in self._fc:
            self._fc[key] = ImageFont.truetype(FONTDIR + FILES[weight], max(2, int(round(key[0] * self.K))))
        return self._fc[key]

    def R(self, x0, y0, x1, y1, fill=None, outline=None, width=1, r=0):
        box = [self.k(x0), self.k(y0), self.k(x1), self.k(y1)]
        w = self.k(width) if outline else 0
        if r > 0:
            self.d.rounded_rectangle(box, radius=self.k(r), fill=fill, outline=outline, width=w)
        else:
            self.d.rectangle(box, fill=fill, outline=outline, width=w)

    def circle(self, cx, cy, r, fill=None, outline=None, width=1):
        self.d.ellipse([self.k(cx - r), self.k(cy - r), self.k(cx + r), self.k(cy + r)], fill=fill,
                       outline=outline, width=self.k(width) if outline else 0)

    def line(self, x0, y0, x1, y1, fill="#1E1E1E", width=2):
        self.d.line([self.k(x0), self.k(y0), self.k(x1), self.k(y1)], fill=fill, width=self.k(width))

    def dline(self, x0, y0, x1, y1, fill="#1E1E1E", width=2, dash=12, gap=8):
        length = math.hypot(x1 - x0, y1 - y0)
        if length == 0:
            return
        ux, uy = (x1 - x0) / length, (y1 - y0) / length
        p = 0.0
        while p < length:
            q = min(p + dash, length)
            self.line(x0 + ux * p, y0 + uy * p, x0 + ux * q, y0 + uy * q, fill, width)
            p += dash + gap

    def poly(self, pts, fill=None, outline=None, width=1):
        self.d.polygon([(self.k(x), self.k(y)) for x, y in pts], fill=fill, outline=outline)

    def T(self, x, y, s, f, fill="#1E1E1E", anchor="la", halo=None):
        self.used.append((round(f.size / float(self.K), 1), round(y), str(s)[:40]))
        try:
            asc, desc = f.getmetrics()
            wpx = f.getlength(str(s))
            hz, vt = anchor[0], anchor[1]
            xl = (self.k(x) - (0 if hz == "l" else wpx / 2.0 if hz == "m" else wpx)) / float(self.K)
            base = (self.k(y) + (asc if vt == "a" else (asc - desc) / 2.0 if vt == "m" else 0)) / float(self.K)
            self.runs.append((round(xl, 2), round(base, 2), str(s), round(f.size / float(self.K), 2), os.path.basename(f.path)))
        except Exception:
            pass
        if halo:
            self.d.text((self.k(x), self.k(y)), s, font=f, fill=fill, anchor=anchor, stroke_width=self.k(3), stroke_fill=halo)
        else:
            self.d.text((self.k(x), self.k(y)), s, font=f, fill=fill, anchor=anchor)

    def tw(self, s, f):
        return f.getlength(s) / self.K

    def wrap(self, s, f, maxw):
        lines = []
        for para in bind(str(s), self.paren_max).split("\n"):
            cur = ""
            for word in [w_ for w_ in para.split(" ") if w_]:
                t = (cur + " " + word).strip()
                if self.tw(t, f) <= maxw or not cur:
                    cur = t
                else:
                    lines.append(cur)
                    cur = word
            lines.append(cur)
        return lines

    def chip(self, x, y, s, size, fg, bg=None, outline=None, weight="bold", padx=None, h=None, align="l"):
        f = self.font(size, weight)
        padx = size * 0.6 if padx is None else padx
        h = size * 1.7 if h is None else h
        w = self.tw(s, f) + 2 * padx
        x0 = x if align == "l" else x - w
        self.R(x0, y, x0 + w, y + h, fill=bg, outline=outline, width=2, r=h / 2)
        self.T(x0 + w / 2, y + h / 2 + 1, s, f, fg, anchor="mm")
        return w

    # -------------------------------------------------- text blocks
    def text_fit(self, box, text, max_size, min_size=14, weight="regular", fill="#1E1E1E", gap=1.22, align="left",
                 valign="top", max_lines=None, step=1):
        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0
        size = max_size
        while True:
            f = self.font(size, weight)
            lines = self.wrap(text, f, w)
            lh = size * gap
            ok = (len(lines) * lh <= h + 0.5 and (max_lines is None or len(lines) <= max_lines)
                  and max(self.tw(x, f) for x in lines) <= w + 0.5)
            if ok or size <= min_size:
                break
            size -= step
        if not ok:
            self.warn.append("text overflow: %s" % str(text)[:50])
        total = len(lines) * lh
        y = y0 + (h - total) / 2 if valign == "middle" else y0
        for ln in lines:
            if align == "center":
                self.T((x0 + x1) / 2, y, ln, f, fill, anchor="ma")
            elif align == "right":
                self.T(x1, y, ln, f, fill, anchor="ra")
            else:
                self.T(x0, y, ln, f, fill)
            y += lh
        return size, y

    def bullets_fit(self, box, items, max_size, min_size=16, color="#8C1D28", fill="#1E1E1E", gap=1.2, para_gap=0.45, weight="regular"):
        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0
        size = max_size
        while True:
            f = self.font(size, weight)
            ind = size * 0.95
            blocks = [self.wrap(it, f, w - ind) for it in items]
            lh = size * gap
            total = sum(len(b) * lh for b in blocks) + para_gap * size * (len(items) - 1)
            wide = max([self.tw(x, f) for b in blocks for x in b] + [0]) > w - ind + 0.5
            if (total <= h + 0.5 and not wide) or size <= min_size:
                break
            size -= 1
        if total > h + 0.5:
            self.warn.append("bullets overflow: %s" % (items[0][:40] if items else ""))
        y = y0
        for b in blocks:
            self.circle(x0 + size * 0.28, y + lh * 0.52, size * 0.15, fill=color)
            for ln in b:
                self.T(x0 + ind, y, ln, f, fill)
                y += lh
            y += para_gap * size
        return size, y

    # -------------------------------------------------- table
    def table(self, box, cols, rows, widths, head_fill="#8C1D28", size_max=26, size_min=15, pad=10, zebra=True,
              col_align=None, bold_first=False, tag_cols=(), fixed_size=None, draw=True, stretch=False, max_extra=70):
        x0, y0, x1, y1 = box
        W, H = x1 - x0, y1 - y0
        cw = [W * wd for wd in widths]
        n = len(cols)
        size = fixed_size or size_max
        while True:
            f = self.font(size)
            fb = self.font(size, "bold")
            hl = [self.wrap(c, fb, cw[i] - 2 * pad) for i, c in enumerate(cols)]
            hh = max(len(x) for x in hl) * size * 1.2 + 2 * pad * 0.8
            rls = []
            for r in rows:
                cells = [self.wrap(str(r[i]) if i < len(r) else "", (fb if (i in tag_cols or (bold_first and i == 0)) else f), cw[i] - 2 * pad) for i in range(n)]
                rls.append((cells, max(len(c) for c in cells) * size * 1.2 + 2 * pad * 0.9))
            total = hh + sum(rh for _, rh in rls)
            wide = (any(self.tw(x, (fb if (i in tag_cols or (bold_first and i == 0)) else f)) > cw[i] - 2 * pad + 0.5 for cells, _ in rls for i in range(n) for x in cells[i])
                    or any(self.tw(x, fb) > cw[i] - 2 * pad + 0.5 for i in range(n) for x in hl[i]))
            if fixed_size or (total <= H + 0.5 and not wide) or size <= size_min:
                break
            size -= 1
        if not draw:
            return size, y0 + total
        if total > H + 0.5:
            self.warn.append("table overflow (%d rows, size %d): %s" % (len(rows), size, cols[:2]))
        extra = 0.0
        if stretch and total < H and rows:
            extra = min((H - total) / len(rows), max_extra)
            rls = [(c, rh + extra) for c, rh in rls]
        y = y0
        x = x0
        self.R(x0, y, x1, y + hh, fill=head_fill)
        for i in range(n):
            ty = y + pad * 0.8
            for ln in hl[i]:
                self.T(x + pad, ty, ln, fb, "#FFFFFF")
                ty += size * 1.2
            x += cw[i]
        y += hh
        for ri, (cells, rh) in enumerate(rls):
            if zebra and ri % 2 == 1:
                self.R(x0, y, x1, y + rh, fill="#F6F2EA")
            self.line(x0, y + rh, x1, y + rh, "#D8D2C6", 1.5)
            x = x0
            for i in range(n):
                ty = y + pad * 0.9 + extra / 2.0
                weight = "bold" if (bold_first and i == 0) or i in tag_cols else "regular"
                ff = self.font(size, weight)
                for ln in cells[i]:
                    if col_align and col_align[i] == "right":
                        self.T(x + cw[i] - pad, ty, ln, ff, "#1E1E1E", anchor="ra")
                    else:
                        self.T(x + pad, ty, ln, ff, "#8C1D28" if i in tag_cols else "#1E1E1E")
                    ty += size * 1.2
                x += cw[i]
            y += rh
        self.R(x0, y0, x1, y, outline="#BDB7AA", width=1.5)
        return size, y

    # -------------------------------------------------- chart
    def chart_plan(self, box, ch):
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
        palette = palette or PAL
        x0, y0, x1, y1 = box
        cats, series = ch["categories"], ch["series"]
        stacked = ch["type"] == "stacked"
        unit = ch.get("unit", "")
        halo = "#FFFFFF"

        def col_of(s):
            return palette.get(s.get("color", "gray"), s.get("color", "#8A857B"))

        self.T(x0, y0, ch.get("title", ""), self.font(28, "bold"), "#1E1E1E")
        if unit:
            self.T(x1, y0 + 6, unit, self.font(19), "#5A554C", anchor="ra")
        f = self.font(21)
        lx, ty = x0, y0 + 40
        for se in series:
            col = col_of(se)
            iw = 42 if se.get("kind") == "line" else 30
            item_w = iw + self.tw(se["name"], f) + 28
            if lx + item_w - 28 > x1 and lx > x0:
                lx = x0
                ty += 30
            if se.get("kind") == "line":
                self.line(lx, ty + 13, lx + 34, ty + 13, col, 4)
                self.circle(lx + 17, ty + 13, 5, fill=col)
            else:
                self.R(lx, ty + 3, lx + 22, ty + 25, fill=col)
            self.T(lx + iw, ty, se["name"], f, "#5A554C")
            lx += item_w
        ty = max(ty, y0 + 40 + 30 * (min_rows - 1))
        top = ty + 50
        left = x0 + 86
        lines0 = [s for s in series if s.get("kind") == "line"]
        right = x1 - 12 - (76 if any(len(set(s["values"])) == 1 for s in lines0) else 0)
        n = len(cats)
        gw = (right - left) / float(n)
        fa_ = self.font(19, "semibold")
        notes = {}
        for an in ch.get("annotations", []):
            notes.setdefault(an.get("category", 0), []).append(self.wrap(an["text"], fa_, gw - 20))
        extra = 0
        for lst in notes.values():
            extra = max(extra, sum(len(l_) * 24 + 20 for l_ in lst))
        extra = max(extra, min_extra)
        bottom = y1 - 52 - extra
        bars = [s for s in series if s.get("kind", "bar") != "line"]
        lines = [s for s in series if s.get("kind") == "line"]
        vals_all = []
        if stacked:
            for ci in range(n):
                vals_all += [sum(max(0, s["values"][ci]) for s in bars), sum(min(0, s["values"][ci]) for s in bars)]
        else:
            for s in bars:
                vals_all += list(s["values"])
        for s in lines:
            vals_all += list(s["values"])
        vmax = max(vals_all + [0])
        vmin = min(vals_all + [0])
        if ch.get("ymax") is not None:
            vmax = max(vmax, ch["ymax"])
        trunc = ch.get("ymin")
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
        self.meta.append({"title": ch.get("title", ""), "unit": unit, "vmin": vmin, "vmax": vmax, "step": step, "type": ch["type"]})

        def Y(v):
            return bottom - (v - vmin) / float(vmax_draw - vmin) * (bottom - top)

        fa = self.font(19)
        tick = vmin
        while tick <= vmax + 1e-9:
            yy = Y(tick)
            zero = abs(tick - base_v) < 1e-9
            self.line(left, yy, right, yy, "#5A554C" if zero else "#E6E1D7", 2.5 if zero else 1.5)
            self.T(left - 10, yy, fmt_num(tick, unit), fa, "#5A554C", anchor="rm")
            tick += step
        if base_v > 0:
            self.T(x0, bottom + 14, "Axis starts at %s" % fmt_num(base_v, unit), self.font(18, "italic"), "#5A554C")
        flat_ys = [Y(s["values"][0]) for s in lines if len(set(s["values"])) == 1]
        nb = 1 if stacked else max(1, len(bars))
        bw = min(96.0, gw * 0.8 / nb)
        for ci, cat in enumerate(cats):
            cx = left + gw * (ci + 0.5)
            self.T(cx, bottom + 12, str(cat), self.font(22, "semibold"), "#1E1E1E", anchor="ma")
            if stacked:
                pos_y = Y(0)
                neg_y = Y(0)
                for s in bars:
                    v = s["values"][ci]
                    col = col_of(s)
                    if v >= 0:
                        y_top = pos_y - (Y(0) - Y(v))
                        self.R(cx - bw * 0.7, y_top, cx + bw * 0.7, pos_y, fill=col, outline="#FFFFFF", width=1.5)
                        if pos_y - y_top > 30:
                            self.T(cx, (y_top + pos_y) / 2, fmt_num(v, unit, False), self.font(19, "semibold"), "#FFFFFF", anchor="mm")
                        pos_y = y_top
                    else:
                        y_bot = neg_y + (Y(v) - Y(0))
                        self.R(cx - bw * 0.7, neg_y, cx + bw * 0.7, y_bot, fill=col, outline="#FFFFFF", width=1.5)
                        neg_y = y_bot
                self.T(cx, pos_y - 8, fmt_num(sum(s["values"][ci] for s in bars), unit, False), self.font(21, "bold"), "#1E1E1E", anchor="ms", halo=halo)
            else:
                for bi, s in enumerate(bars):
                    v = s["values"][ci]
                    bx = cx - (nb * bw) / 2 + bi * bw
                    ytop, ybase = Y(max(v, base_v)), Y(min(v, base_v))
                    self.R(bx + 3, ytop, bx + bw - 3, ybase, fill=col_of(s))
                    ls = max(15, min(20, bw * 0.34))
                    ly = ytop - 8 if v >= base_v else ybase + 26
                    if (v >= base_v and ybase - ytop > ls * 1.8 and any(abs(fy - (ly - ls * 0.35)) < ls * 0.62 for fy in flat_ys)
                            and self.tw(fmt_num(v, unit, False), self.font(ls, "semibold")) <= bw - 8):
                        self.T(bx + bw / 2, ytop + ls * 1.25, fmt_num(v, unit, False), self.font(ls, "semibold"), "#FFFFFF", anchor="ms")
                    else:
                        self.T(bx + bw / 2, ly, fmt_num(v, unit, False), self.font(ls, "semibold"), "#1E1E1E", anchor="ms", halo=halo)
            ay = bottom + 12 + 36
            for lines_ in notes.get(ci, []):
                hh = len(lines_) * 24 + 14
                ww = max(self.tw(l_, fa_) for l_ in lines_) + 24
                self.R(cx - ww / 2, ay, cx + ww / 2, ay + hh, fill="#FFF8E1", outline="#C9A227", width=2, r=8)
                for i, l_ in enumerate(lines_):
                    self.T(cx, ay + 7 + i * 24, l_, fa_, "#1E1E1E", anchor="ma")
                ay += hh + 6
        for s in lines:
            col = col_of(s)
            tcol = PAL["golddark"] if s.get("color") == "gold" else col
            pts = [(left + gw * (ci + 0.5), Y(v)) for ci, v in enumerate(s["values"])]
            if len(set(s["values"])) == 1:
                self.dline(left, pts[0][1], right, pts[0][1], col, 3.5, 14, 9)
                self.T(right + 10, pts[0][1], fmt_num(s["values"][0], unit, False), self.font(21, "bold"), tcol, anchor="lm")
            else:
                for a, b in zip(pts, pts[1:]):
                    self.line(a[0], a[1], b[0], b[1], col, 4)
                for ci, (px, py) in enumerate(pts):
                    self.circle(px, py, 7, fill=col, outline="#FFFFFF", width=2)
                    self.T(px + 12, py - 12, fmt_num(s["values"][ci], unit, False), self.font(19, "semibold"), tcol, anchor="ls", halo=halo)
    def finish(self):
        return self.img.resize((self.w, self.h), Image.LANCZOS)
