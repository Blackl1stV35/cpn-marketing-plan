"""Slide layouts for the deck comps (1920 x 1080)."""
import math
from deckdraw import Cv, PAL, tint, NB

W, H = 1920, 1080
X0, X1 = 80, 1840
BY0, BY1 = 268, 982
ACC = ["maroon", "golddark", "teal", "slate", "purple"]
SEC = {1: "maroon", 2: "maroon", 3: "slate", 4: "slate", 5: "golddark", 6: "golddark", 7: "golddark", 8: "teal", 9: "teal",
       10: "purple", 11: "purple", 12: "maroon"}
NAV = [("Situation", (3,)), ("Strategy", (4,)), ("Tactics", (5, 6, 7)), ("Financials", (8, 9)), ("Controls", (10, 11))]


def C(name):
    return PAL.get(name, name)


def acc(i):
    return C(ACC[i % len(ACC)])


# ------------------------------------------------------------------ frame
def frame(cv, s):
    n = s["n"]
    core = s["kind"] == "core"
    col = C(SEC.get(n, "gray")) if core else C("gray")
    cv.R(0, 0, 26, H, fill=C("maroon"))
    w = cv.chip(X0, 30, s["section"], 24, "#FFFFFF", bg=col, h=44)
    cv.chip(X0 + w + 14, 34, s["status"] if core else "BACKUP", 18, col, bg=tint(col, 0.86), h=36)
    cv.T(X1, 38, ("%d / 12" % n) if core else s["id"], cv.font(24, "semibold"), C("muted"), anchor="ra")
    cv.paren_max = 40
    cv.text_fit((X0, 94, X1, 232), s["headline"], 46, 30, "bold", C("maroon"), gap=1.16, max_lines=2)
    cv.paren_max = 18
    cv.R(X0, 240, X0 + 180, 246, fill=C("gold"))
    cv.line(X0, 1000, X1, 1000, C("line"), 2)
    cv.text_fit((X0, 1010, 1260, 1072), "Sources: " + "; ".join(q.replace(" ", NB) if len(q) <= 46 else q for q in [z for x in s["sources"] for z in x.split("; ")]), 20, 14, "regular", C("muted"), gap=1.2, max_lines=2)
    if core and n in SEC:
        x = X1
        for label, nums in reversed(NAV):
            on = n in nums
            f = cv.font(20, "bold" if on else "regular")
            t = cv.tw(label, f)
            cv.T(x, 1030, label, f, col if on else C("mid"), anchor="ra")
            if on:
                cv.R(x - t, 1060, x, 1064, fill=col)
            x -= t + 30


# ------------------------------------------------------------------ title
def lay_title(cv, s):
    b = s["body"]
    cv.R(0, 0, 780, H, fill=C("maroon"))
    cv.R(70, 840, 250, 848, fill="#E8C85A")
    cv.text_fit((70, 200, 710, 620), b["title"], 72, 44, "bold", "#FFFFFF", gap=1.14, valign="middle")
    cv.text_fit((70, 640, 710, 800), b["subtitle"], 38, 26, "regular", "#F0D78C", gap=1.2)
    cv.T(70, 920, "CPN marketing plan", cv.font(26, "semibold"), "#FFFFFF")
    x = 880
    cv.T(x, 120, "Presented by", cv.font(30, "bold"), C("maroon"))
    y = 176
    for name in b["team"]:
        cv.T(x, y, name, cv.font(40), C("ink"))
        y += 64
    y += 30
    cv.T(x, y, "Presented to", cv.font(30, "bold"), C("maroon"))
    cv.T(x, y + 54, b["instructor"], cv.font(38), C("ink"))
    cv.T(x, y + 120, b["course"], cv.font(32, "semibold"), C("ink"))
    cv.text_fit((x, y + 168, 1840, y + 270), b["term"], 28, 20, "regular", C("muted"), gap=1.25)


# ------------------------------------------------------------------ kpi5
def lay_kpi5(cv, s):
    b = s["body"]
    tw_ = (X1 - X0 - 4 * 22) / 5.0
    vsize = 88
    for t in b["tiles"]:
        while cv.tw(t["value"], cv.font(vsize, "bold")) > tw_ - 28 and vsize > 36:
            vsize -= 1
    for i, t in enumerate(b["tiles"]):
        x = X0 + i * (tw_ + 22)
        y = 288
        c = acc(i)
        cv.R(x, y, x + tw_, y + 410, fill="#FFFFFF", outline=C("line"), width=2, r=18)
        cv.R(x + 2, y, x + tw_ - 2, y + 14, fill=c)
        cv.text_fit((x + 14, y + 44, x + tw_ - 14, y + 190), t["value"], vsize, vsize, "bold", c, align="center", valign="middle", max_lines=1)
        cv.text_fit((x + 20, y + 205, x + tw_ - 20, y + 305), t["label"], 32, 21, "bold", C("ink"), align="center", max_lines=3, gap=1.2)
        cv.text_fit((x + 20, y + 312, x + tw_ - 20, y + 398), t["note"], 25, 17, "regular", C("muted"), align="center", max_lines=3, gap=1.2)
    cv.R(X0, 730, X1, 920, fill=C("maroon"), r=24)
    cv.R(X0 + 26, 760, X0 + 40, 890, fill="#E8C85A", r=7)
    cv.text_fit((X0 + 70, 748, X1 - 40, 902), b["ask"], 38, 24, "bold", "#FFFFFF", valign="middle", gap=1.22)


# ------------------------------------------------------------------ swot + issues
def lay_swot(cv, s):
    b = s["body"]
    names = {"S": ("Strengths", C("teal")), "W": ("Weaknesses", C("warn")), "O": ("Opportunities", C("slate")), "T": ("Threats", C("maroon"))}
    cw_, ch_ = 446, 330
    for i, q in enumerate("SWOT"):
        x = X0 + (i % 2) * (cw_ + 20)
        y = BY0 + 12 + (i // 2) * (ch_ + 20)
        label, c = names[q]
        cv.R(x, y, x + cw_, y + ch_, fill=tint(c, 0.93), outline=c, width=2, r=16)
        cv.circle(x + 44, y + 46, 30, fill=c)
        cv.T(x + 44, y + 47, q, cv.font(34, "bold"), "#FFFFFF", anchor="mm")
        cv.T(x + 90, y + 28, label, cv.font(30, "bold"), c)
        cv.bullets_fit((x + 24, y + 92, x + cw_ - 20, y + ch_ - 16), b["swot"][q], 26, 17, color=c, gap=1.18)
    x = 1060
    cv.T(x, BY0 + 6, "Critical issues for the plan", cv.font(32, "bold"), C("maroon"))
    for i, it in enumerate(b["issues"]):
        y = BY0 + 66 + i * 212
        cv.R(x, y, X1, y + 196, fill="#FFFFFF", outline=C("line"), width=2, r=16)
        cv.circle(x + 54, y + 98, 34, fill=C("maroon"))
        cv.T(x + 54, y + 99, str(i + 1), cv.font(36, "bold"), "#FFFFFF", anchor="mm")
        cv.text_fit((x + 110, y + 20, X1 - 24, y + 84), it["title"], 32, 22, "bold", C("ink"), max_lines=2, gap=1.15)
        cv.text_fit((x + 110, y + 92, X1 - 24, y + 184), it["why"], 26, 18, "regular", C("muted"), max_lines=3, gap=1.2)


# ------------------------------------------------------------------ three columns
def lay_three(cv, s):
    b = s["body"]
    cw_ = (X1 - X0 - 2 * 24) / 3.0
    cols = [C("maroon"), C("golddark"), C("slate")]
    for i, col in enumerate(b["cols"]):
        x = X0 + i * (cw_ + 24)
        y = BY0 + 10
        cv.R(x, y, x + cw_, BY1 - 6, fill="#FFFFFF", outline=C("line"), width=2, r=18)
        cv.R(x, y, x + cw_, y + 88, fill=cols[i], r=18)
        cv.R(x, y + 60, x + cw_, y + 88, fill=cols[i])
        cv.text_fit((x + 24, y + 6, x + cw_ - 24, y + 84), col["title"], 36, 24, "bold", "#FFFFFF", valign="middle", max_lines=1)
        by = y + 110
        if col.get("big"):
            cv.text_fit((x + 24, by, x + cw_ - 24, by + 100), col["big"]["value"], 84, 40, "bold", cols[i], max_lines=1, valign="middle")
            cv.text_fit((x + 24, by + 100, x + cw_ - 24, by + 140), col["big"]["label"], 26, 18, "semibold", C("muted"), max_lines=1)
            by += 160
        cv.bullets_fit((x + 28, by, x + cw_ - 24, BY1 - 30), col["bullets"], 31, 19, color=cols[i], gap=1.22, para_gap=0.6)


# ------------------------------------------------------------------ table + side panel
def lay_table_side(cv, s):
    b = s["body"]
    t = b["table"]
    cv.T(X0, BY0 + 4, t["title"], cv.font(30, "bold"), C("maroon"))
    cv.table((X0, BY0 + 56, 1270, BY1 - 6), t["cols"], t["rows"], t["widths"], head_fill=C("maroon"), size_max=30, size_min=16, tag_cols=(0,), pad=16,
             stretch=True, max_extra=120)
    x = 1330
    side = b["side"]
    cv.T(x, BY0 + 4, side["title"], cv.font(30, "bold"), C("maroon"))
    items = side["items"]
    hh = (BY1 - 6 - (BY0 + 56) - (len(items) - 1) * 18) / float(len(items))
    hh = min(hh, 200)
    for i, it in enumerate(items):
        y = BY0 + 56 + i * (hh + 18)
        cv.R(x, y, X1, y + hh, fill=tint(acc(i), 0.93), outline=acc(i), width=2, r=14)
        cv.text_fit((x + 18, y + 10, X1 - 18, y + hh * 0.52), it["value"], 54, 28, "bold", acc(i), max_lines=1, valign="middle")
        cv.text_fit((x + 18, y + hh * 0.5, X1 - 18, y + hh - 8), it["label"], 24, 16, "regular", C("ink"), max_lines=3, gap=1.18)


# ------------------------------------------------------------------ channels + calendar
def lay_channels(cv, s):
    b = s["body"]
    hx, hy = 506, 624
    nodes = b["nodes"]
    nn = len(nodes)
    pos = []
    for i in range(nn):
        a = -math.pi / 2 + i * 2 * math.pi / nn
        pos.append((hx + 276 * math.cos(a), hy + 238 * math.sin(a)))
    for (px, py) in pos:
        cv.line(hx, hy, px, py, C("mid"), 3)
    cv.circle(hx, hy, 92, fill=C("maroon"))
    cv.text_fit((hx - 80, hy - 40, hx + 80, hy + 40), b["hub"], 48, 26, "bold", "#FFFFFF", align="center", valign="middle", max_lines=1)
    for i, (px, py) in enumerate(pos):
        w, h = 292, 118
        x0, y0 = px - w / 2, py - h / 2
        cv.R(x0, y0, x0 + w, y0 + h, fill="#FFFFFF", outline=acc(i), width=3, r=16)
        cv.text_fit((x0 + 14, y0 + 8, x0 + w - 14, y0 + 50), nodes[i]["name"], 27, 18, "bold", acc(i), max_lines=1)
        cv.text_fit((x0 + 14, y0 + 52, x0 + w - 14, y0 + h - 6), nodes[i].get("note", ""), 21, 14, "regular", C("ink"), max_lines=3, gap=1.12)
    # calendar
    cal = b["calendar"]
    x0 = 960
    cv.T(x0, BY0 + 4, "Campaign windows", cv.font(30, "bold"), C("maroon"))
    months = cal["months"]
    m = len(months)
    tl0, tl1 = x0 + 330, X1
    mw = (tl1 - tl0) / float(m)
    hy0 = BY0 + 58
    for i, mo in enumerate(months):
        cv.R(tl0 + i * mw, hy0, tl0 + (i + 1) * mw - 2, hy0 + 40, fill=C("faint"))
        cv.T(tl0 + (i + 0.5) * mw, hy0 + 20, str(mo), cv.font(20 if m > 6 else 22, "semibold"), C("muted"), anchor="mm")
    bars = cal["bars"]
    rh = min(88, (BY0 + 560 - (hy0 + 56)) / float(len(bars)))
    for i, bar in enumerate(bars):
        y = hy0 + 56 + i * rh
        cv.text_fit((x0, y, tl0 - 12, y + rh - 8), bar["label"], 24, 16, "semibold", C("ink"), max_lines=3, valign="middle", gap=1.1)
        for j in range(m):
            cv.line(tl0 + j * mw, y, tl0 + j * mw, y + rh - 8, "#EEE9DF", 1)
        bx0, bx1 = tl0 + bar["start"] * mw + 2, tl0 + bar["end"] * mw - 2
        cv.R(bx0, y + 8, bx1, y + rh - 16, fill=acc(i), r=10)
        note = bar.get("note", "")
        if note:
            f = cv.font(21, "bold")
            nw_ = cv.tw(note, f)
            if nw_ < bx1 - bx0 - 14:
                cv.T((bx0 + bx1) / 2, y + (rh - 8) / 2, note, f, "#FFFFFF", anchor="mm")
            elif bx1 + 10 + nw_ <= X1:
                cv.T(bx1 + 10, y + (rh - 8) / 2, note, f, acc(i), anchor="lm")
            else:
                cv.T(bx0 - 10, y + (rh - 8) / 2, note, f, acc(i), anchor="rm")
    by = BY0 + 600
    bud = b["budget"]
    cv.R(x0, by, X1, BY1 - 6, fill=C("maroon"), r=20)
    cv.text_fit((x0 + 24, by + 10, x0 + 330, BY1 - 16), bud["value"], 66, 34, "bold", "#F0D78C", max_lines=1, valign="middle")
    cv.text_fit((x0 + 350, by + 10, X1 - 24, BY1 - 16), bud["label"], 28, 18, "regular", "#FFFFFF", valign="middle", gap=1.2)


# ------------------------------------------------------------------ research + indicators
def lay_research(cv, s):
    b = s["body"]
    cv.T(X0, BY0 + 4, "How we learn", cv.font(30, "bold"), C("maroon"))
    ms = b["methods"]
    mh = (BY1 - 6 - (BY0 + 56) - (len(ms) - 1) * 16) / float(len(ms))
    for i, m in enumerate(ms):
        y = BY0 + 56 + i * (mh + 16)
        cv.R(X0, y, 900, y + mh, fill="#FFFFFF", outline=C("line"), width=2, r=14)
        cv.R(X0, y, X0 + 12, y + mh, fill=acc(i), r=6)
        cv.text_fit((X0 + 30, y + 10, 700, y + 50), m["name"], 28, 18, "bold", acc(i), max_lines=1)
        cv.text_fit((X0 + 30, y + 52, 880, y + mh - 10), m["what"], 24, 15, "regular", C("ink"), max_lines=3, gap=1.15)
        if m.get("when"):
            cv.chip(900 - 16, y + 10, m["when"], 19, acc(i), bg=tint(acc(i), 0.88), align="r", h=34)
    x0 = 960
    cv.T(x0, BY0 + 4, "What we track", cv.font(30, "bold"), C("maroon"))
    kw, kh = 428, 316
    for i, k in enumerate(b["kpis"]):
        x = x0 + (i % 2) * (kw + 24)
        y = BY0 + 56 + (i // 2) * (kh + 20)
        cv.R(x, y, x + kw, y + kh, fill=tint(acc(i), 0.94), outline=acc(i), width=2, r=16)
        cv.chip(x + 18, y + 16, k["tag"], 20, "#FFFFFF", bg=acc(i), h=36)
        cv.text_fit((x + 18, y + 62, x + kw - 18, y + 138), k["name"], 28, 18, "bold", C("ink"), max_lines=2, gap=1.12)
        cv.T(x + 18, y + 148, "Baseline", cv.font(19, "semibold"), C("muted"))
        cv.text_fit((x + 18, y + 172, x + kw - 18, y + 214), k["baseline"], 26, 16, "regular", C("ink"), max_lines=1)
        cv.T(x + 18, y + 224, "Target [Proposed]", cv.font(19, "semibold"), C("muted"))
        cv.text_fit((x + 18, y + 246, x + kw - 18, y + kh - 10), k["target"], 32, 18, "bold", acc(i), max_lines=1)


# ------------------------------------------------------------------ charts
def lay_chart(cv, s):
    b = s["body"]
    charts = b["charts"]
    top, bot = BY0 + 4, BY0 + 520
    boxes = [(X0, top, X1, bot)] if len(charts) == 1 else [(X0, top, 940, bot), (980, top, X1, bot)]
    plans = [cv.chart_plan(bx, ch) for bx, ch in zip(boxes, charts)]
    mrows, mextra = max(p[0] for p in plans), max(p[1] for p in plans)
    for bx, ch in zip(boxes, charts):
        cv.chart(bx, ch, min_rows=mrows, min_extra=mextra)
    co = b["callouts"]
    n = len(co)
    cw_ = (X1 - X0 - (n - 1) * 20) / float(n)
    for i, c in enumerate(co):
        x = X0 + i * (cw_ + 20)
        y = BY0 + 548
        tone = {"good": C("good"), "warn": C("warn"), "neutral": C("neutral")}.get(c.get("tone", "neutral"), C("neutral"))
        cv.R(x, y, x + cw_, y + 118, fill=tint(tone, 0.93), outline=tone, width=2, r=14)
        cv.R(x, y, x + 12, y + 118, fill=tone, r=6)
        cv.text_fit((x + 28, y + 8, x + 260, y + 110), c["value"], 56, 28, "bold", tone, max_lines=1, valign="middle")
        cv.text_fit((x + 270 if cw_ > 520 else x + 28, y + 10 if cw_ > 520 else y + 66, x + cw_ - 18, y + 112), c["label"], 25, 16, "regular", C("ink"), max_lines=3, gap=1.15, valign="middle" if cw_ > 520 else "top")
    cv.text_fit((X0, BY1 - 40, X1, BY1 + 6), b["note"], 28, 18, "semibold", C("ink"), max_lines=1, valign="middle")


# ------------------------------------------------------------------ gantt + org
def lay_gantt(cv, s):
    b = s["body"]
    cv.T(X0, BY0 + 2, "Timeline and gates", cv.font(30, "bold"), C("maroon"))
    lab0, lab1 = X0, 390
    tl0, tl1 = 410, 1290
    months = b["months"]
    m = len(months)
    mw = (tl1 - tl0) / float(m)
    hy = BY0 + 78
    for i, mo in enumerate(months):
        cv.R(tl0 + i * mw, hy, tl0 + (i + 1) * mw - 2, hy + 42, fill=C("faint"))
        cv.T(tl0 + (i + 0.5) * mw, hy + 21, str(mo), cv.font(22, "bold"), C("muted"), anchor="mm")
    rows = b["rows"]
    ry0 = hy + 56
    rh = min(84, (BY1 - 130 - ry0) / float(len(rows)))
    for i, r in enumerate(rows):
        y = ry0 + i * rh
        cv.text_fit((lab0, y, lab1, y + rh - 6), r["label"], 25, 15, "semibold", C("ink"), max_lines=3, valign="middle", gap=1.1)
        for j in range(m + 1):
            cv.line(tl0 + j * mw, y, tl0 + j * mw, y + rh - 6, "#EEE9DF", 1)
        c = C(r.get("tone", ACC[i % len(ACC)]))
        cv.R(tl0 + r["start"] * mw + 2, y + 10, tl0 + r["end"] * mw - 2, y + rh - 16, fill=c, r=10)
    bottom = ry0 + len(rows) * rh
    chip_rows = []
    for gi, g in enumerate(sorted(b["gates"], key=lambda q: q["at"])):
        gx = tl0 + g["at"] * mw
        cv.dline(gx, hy + 46, gx, bottom + 10, C("maroon"), 3, 10, 7)
        f = cv.font(20, "bold")
        lw = cv.tw(g["label"], f) + 20
        lx = min(max(gx - lw / 2, tl0), tl1 - lw)
        row = next((r_ for r_, e_ in enumerate(chip_rows) if lx > e_ + 8), len(chip_rows))
        if row == len(chip_rows):
            chip_rows.append(0)
        chip_rows[row] = lx + lw
        cy_ = hy - 36 - row * 38
        if row > 0:
            cv.line(gx, cy_ + 32, gx, hy, C("maroon"), 3)
        cv.R(lx, cy_, lx + lw, cy_ + 32, fill=C("maroon"), r=8)
        cv.T(lx + lw / 2, cy_ + 16, g["label"], f, "#FFFFFF", anchor="mm")
        if g.get("release"):
            rf = cv.font(21, "bold")
            rw = cv.tw(g["release"], rf) + 18
            rx = min(max(gx - rw / 2, tl0), tl1 - rw)
            ry = bottom + 18 + (gi % 2) * 44
            if gi % 2 == 1:
                cv.line(gx, bottom + 10, gx, ry, C("maroon"), 3)
            cv.R(rx, ry, rx + rw, ry + 36, fill="#FFF8E1", outline=C("gold"), width=2, r=8)
            cv.T(rx + rw / 2, ry + 18, g["release"], rf, C("ink"), anchor="mm")
    x = 1340
    cv.T(x, BY0 + 2, "Who does what", cv.font(30, "bold"), C("maroon"))
    org = b["org"]
    cv.R(x, BY0 + 56, X1, BY0 + 150, fill=C("maroon"), r=14)
    cv.text_fit((x + 14, BY0 + 60, X1 - 14, BY0 + 146), org["top"], 30, 18, "bold", "#FFFFFF", align="center", valign="middle", max_lines=2)
    units = org["units"]
    uy0 = BY0 + 190
    uh = min(124, (BY1 - 8 - uy0 - (len(units) - 1) * 14) / float(len(units)))
    spine_x = x + 22
    last = max([k for k, u_ in enumerate(units) if not u_.get("role", "").lower().startswith("existing")] or [0])
    cv.line(spine_x, BY0 + 150, spine_x, uy0 + last * (uh + 14) + uh / 2, C("mid"), 3)
    for i, u in enumerate(units):
        y = uy0 + i * (uh + 14)
        ex = u.get("role", "").lower().startswith("existing")
        ucol = C("mid") if ex else acc(i + 1)
        if not ex:
            cv.line(spine_x, y + uh / 2, x + 50, y + uh / 2, C("mid"), 3)
        cv.R(x + 50, y, X1, y + uh, fill="#FFFFFF", outline=ucol, width=3, r=12)
        cv.text_fit((x + 64, y + 8, X1 - 12, y + 46), u["name"], 25, 16, "bold", ucol, max_lines=1)
        cv.text_fit((x + 64, y + 48, X1 - 12, y + uh - 6), u.get("role", ""), 21, 14, "regular", C("ink"), max_lines=3, gap=1.12)


# ------------------------------------------------------------------ risk matrix
def lay_risk(cv, s):
    b = s["body"]
    mx0, my0, cs, chh = 150, BY0 + 92, 190, 140
    cv.T(X0, BY0 + 2, "Risk map (team judgement)", cv.font(30, "bold"), C("maroon"))
    idx = {"L": 0, "M": 1, "H": 2}
    shades = [0.9, 0.78, 0.62, 0.45, 0.28]
    for li in range(3):
        for im in range(3):
            row = 2 - li
            x = mx0 + im * cs
            y = my0 + row * chh
            cv.R(x, y, x + cs - 3, y + chh - 3, fill=tint(C("maroon"), shades[li + im]), r=6)
    for i, lab in enumerate("HML"):
        cv.T(mx0 - 22, my0 + i * chh + chh / 2, lab, cv.font(26, "bold"), C("muted"), anchor="mm")
    for i, lab in enumerate("LMH"):
        cv.T(mx0 + i * cs + cs / 2, my0 + 3 * chh + 20, lab, cv.font(26, "bold"), C("muted"), anchor="mm")
    cv.T(X0, my0 - 30, "Likelihood", cv.font(21, "semibold"), C("muted"))
    cv.T(mx0 + 3 * cs + 10, my0 + 3 * chh + 20, "Impact", cv.font(21, "semibold"), C("muted"), anchor="lm")
    cells = {}
    for r in b["risks"]:
        cells.setdefault((idx.get(r["likelihood"], 1), idx.get(r["impact"], 1)), []).append(r)
    for (li, im), rs in cells.items():
        row = 2 - li
        cx0 = mx0 + im * cs
        cy0 = my0 + row * chh
        for j, r in enumerate(rs):
            px = cx0 + 36 + (j % 3) * 46
            py = cy0 + 36 + (j // 3) * 50
            cv.circle(px, py, 21, fill="#FFFFFF", outline=C("maroon"), width=3)
            cv.T(px, py + 1, str(r["id"]), cv.font(21, "bold"), C("maroon"), anchor="mm")
    # legend
    ly = my0 + 3 * chh + 58
    half = (len(b["risks"]) + 1) // 2
    for i, r in enumerate(b["risks"]):
        col_i, row_i = divmod(i, half)
        lx = X0 + col_i * 470
        yy = ly + row_i * 27
        cv.T(lx, yy, "%s  %s" % (r["id"], r["name"]), cv.font(19), C("ink"))
    # top risks
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


# ------------------------------------------------------------------ takeaways
def lay_takeaways(cv, s):
    b = s["body"]
    cw_ = (X1 - X0 - 2 * 28) / 3.0
    for i, c in enumerate(b["cards"]):
        x = X0 + i * (cw_ + 28)
        y = BY0 + 14
        col = acc(i)
        cv.R(x, y, x + cw_, y + 470, fill="#FFFFFF", outline=C("line"), width=2, r=20)
        cv.R(x + 2, y, x + cw_ - 2, y + 14, fill=col)
        cv.circle(x + 60, y + 84, 40, fill=col)
        cv.T(x + 60, y + 85, str(c.get("n", i + 1)), cv.font(44, "bold"), "#FFFFFF", anchor="mm")
        cv.text_fit((x + 24, y + 144, x + cw_ - 24, y + 228), c["title"], 38, 24, "bold", col, max_lines=2, gap=1.12)
        cv.text_fit((x + 24, y + 236, x + cw_ - 24, y + 456), c["text"], 31, 18, "regular", C("ink"), gap=1.25)
    by = BY0 + 512
    cv.R(X0, by, X1, BY1 - 6, fill=C("maroon"), r=24)
    cv.text_fit((X0 + 50, by + 10, X1 - 380, BY1 - 16), b["closing"], 48, 26, "bold", "#FFFFFF", valign="middle", max_lines=2)
    cv.chip(X1 - 330, by + (BY1 - 6 - by) / 2 - 38, "Q&A", 44, C("maroon"), bg="#F0D78C", h=76, padx=44)


# ------------------------------------------------------------------ backup blocks
def block_h(cv, bl, w, sc, draw, x=0, y=0):
    """Measure (draw=False) or draw one block; returns its height."""
    t = bl["type"]
    title_h = 0
    if bl.get("title"):
        title_h = 40 * sc
        if draw:
            cv.T(x, y, bl["title"], cv.font(26 * sc, "bold"), C("maroon"))
    yy = y + title_h
    if t == "table":
        size = max(15, 21 * sc)
        _, y_end = cv.table((x, yy, x + w, yy + 4000), bl["cols"], bl["rows"], bl.get("widths") or [1.0 / len(bl["cols"])] * len(bl["cols"]),
                            head_fill=C("maroon"), fixed_size=size, pad=7, draw=draw, tag_cols=(0,))
        return title_h + (y_end - yy) + 14 * sc
    if t == "bullets":
        size = max(15, 22 * sc)
        f = cv.font(size)
        ind = size * 0.95
        h = 0
        for it in bl["items"]:
            lines = cv.wrap(it, f, w - ind)
            if draw:
                cv.circle(x + size * 0.28, yy + h + size * 0.62, size * 0.15, fill=C("maroon"))
                for k, ln in enumerate(lines):
                    cv.T(x + ind, yy + h + k * size * 1.2, ln, f, C("ink"))
            h += len(lines) * size * 1.2 + size * 0.4
        return title_h + h + 8 * sc
    if t == "text":
        size = max(15, 22 * sc)
        f = cv.font(size)
        lines = cv.wrap(bl["text"], f, w)
        if draw:
            for k, ln in enumerate(lines):
                cv.T(x, yy + k * size * 1.25, ln, f, C("ink"))
        return title_h + len(lines) * size * 1.25 + 10 * sc
    if t == "kpis":
        items = bl["items"]
        n = len(items)
        tw_ = (w - (n - 1) * 14) / float(n)
        hh = 128 * sc
        if draw:
            for i, it in enumerate(items):
                xx = x + i * (tw_ + 14)
                cv.R(xx, yy, xx + tw_, yy + hh, fill=tint(acc(i), 0.93), outline=acc(i), width=2, r=12)
                cv.text_fit((xx + 8, yy + 6, xx + tw_ - 8, yy + hh * 0.55), it["value"], 40 * sc, 16, "bold", acc(i), align="center", max_lines=1, valign="middle")
                cv.text_fit((xx + 8, yy + hh * 0.55, xx + tw_ - 8, yy + hh - 4), it["label"], 20 * sc, 14, "regular", C("ink"), align="center", max_lines=2, gap=1.1)
        return title_h + hh + 14 * sc
    if t == "cards":
        items = bl["items"]
        ncol = 2 if w > 700 else 1
        cw_ = (w - (ncol - 1) * 16) / float(ncol)
        hs, size_h, size_t = [], max(15, 22 * sc), max(14.5, 19 * sc)
        fh, ft = cv.font(size_h, "bold"), cv.font(size_t)
        for it in items:
            hl = cv.wrap(it["head"], fh, cw_ - 100)
            tl = cv.wrap(it["text"], ft, cw_ - 28)
            hs.append(len(hl) * size_h * 1.2 + len(tl) * size_t * 1.2 + 26)
        total = 0
        rows = [items[i:i + ncol] for i in range(0, len(items), ncol)]
        k = 0
        for r in rows:
            rh = max(hs[k:k + len(r)])
            if draw:
                for j, it in enumerate(r):
                    xx = x + j * (cw_ + 16)
                    yy2 = yy + total
                    cv.R(xx, yy2, xx + cw_, yy2 + rh, fill="#FFFFFF", outline=C("line"), width=2, r=10)
                    hl = cv.wrap(it["head"], fh, cw_ - 100)
                    for q, ln in enumerate(hl):
                        cv.T(xx + 14, yy2 + 10 + q * size_h * 1.2, ln, fh, C("maroon"))
                    if it.get("tag"):
                        cv.chip(xx + cw_ - 12, yy2 + 8, it["tag"], max(14, 16 * sc), "#FFFFFF", bg=C("slate"), align="r", h=26)
                    tl = cv.wrap(it["text"], ft, cw_ - 28)
                    for q, ln in enumerate(tl):
                        cv.T(xx + 14, yy2 + 12 + len(hl) * size_h * 1.2 + q * size_t * 1.2, ln, ft, C("ink"))
            total += rh + 12
            k += len(r)
        return title_h + total + 6 * sc
    return title_h


def lay_blocks(cv, s):
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


LAYOUTS = {
    "title": lay_title, "kpi5": lay_kpi5, "swot_issues": lay_swot, "three_col": lay_three, "table_side": lay_table_side,
    "channels_calendar": lay_channels, "research_kpis": lay_research, "chart": lay_chart, "gantt_org": lay_gantt,
    "risk_matrix": lay_risk, "takeaways": lay_takeaways, "blocks": lay_blocks,
}


USED = {}
RUNS = {}
HI = {}


def render_slide(s):
    cv = Cv(W, H, K=2)
    USED[s.get("id")] = cv.used
    RUNS[s.get("id")] = cv.runs
    HI[s.get("id")] = cv
    if s["layout"] != "title":
        frame(cv, s)
    try:
        LAYOUTS[s["layout"]](cv, s)
    except Exception as e:  # keep going so one bad slide does not stop the set
        cv.warn.append("RENDER ERROR %s: %r" % (s.get("id"), e))
        cv.T(100, 400, "RENDER ERROR: %r" % (e,), cv.font(30), "#B00020")
    return cv.finish(), cv.warn
