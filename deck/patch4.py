import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
def rep(old, new):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("MISMATCH %d: %s" % (n, old[:70]))
    t = t.replace(old, new)

rep('''def mmss(sec):''', '''FRIENDLY = {"title": "Title slide", "kpi5": "5 key numbers", "swot_issues": "SWOT + 3 issues", "three_col": "3 columns",
            "table_side": "Table + figures", "channels_calendar": "Channels + calendar", "research_kpis": "Research + KPIs",
            "chart": "Charts", "gantt_org": "Timeline + roles", "risk_matrix": "Risk map", "takeaways": "3 takeaways", "blocks": "Reference page"}


def mmss(sec):''')
rep('''(mmss(s["seconds"]), s["presenter"], s["layout"]),''', '''(mmss(s["seconds"]), s["presenter"], FRIENDLY.get(s["layout"], s["layout"])),''')
rep('''        cv.R(x0, by0, x1 - 3, by0 + 78, fill=col, r=8)
        cv.T((x0 + x1 - 3) / 2, by0 + 24, "S%d" % n, cv.font(28, "bold"), "#FFFFFF", anchor="mm")
        cv.T((x0 + x1 - 3) / 2, by0 + 56, mmss(bys[n]["seconds"]) if n in bys else "", cv.font(22), "#FFFFFF", anchor="mm")''',
'''        cv.R(x0, by0, x1 - 3, by0 + 78, fill=col, r=8)
        if x1 - 3 - x0 < 60:
            cv.T((x0 + x1 - 3) / 2, by0 + 39, "S%d" % n, cv.font(18, "bold"), "#FFFFFF", anchor="mm")
        else:
            cv.T((x0 + x1 - 3) / 2, by0 + 24, "S%d" % n, cv.font(28, "bold"), "#FFFFFF", anchor="mm")
            cv.T((x0 + x1 - 3) / 2, by0 + 56, mmss(bys[n]["seconds"]) if n in bys else "", cv.font(22), "#FFFFFF", anchor="mm")''')
rep('''cv.text_fit((colx["title"] + 74, y, colx["head"] - 24, y + 42), s["title"]''', '''cv.text_fit((colx["title"] + 96, y, colx["head"] - 24, y + 42), s["title"]''')
rep('''s["layout"].replace("_", " "), 22, 15, "regular", C("muted"), max_lines=1)''', '''FRIENDLY.get(s["layout"], s["layout"]), 22, 15, "regular", C("muted"), max_lines=1)''')
rep('''    H = 560 + len(core) * ROWH + 60 + 640''', '''    H = 620 + len(core) * ROWH + 30 + 680 + 40''')
rep('''    cv.R(M - 16, y - 12, 1180, y + 600, fill="#FFFFFF", outline=C("line"), width=2, r=16)''', '''    cv.R(M - 16, y - 12, 1180, y + 668, fill="#FFFFFF", outline=C("line"), width=2, r=16)''')
rep('''    cv.R(x2, y - 12, W - M + 16, y + 600, fill="#FFFFFF", outline=C("line"), width=2, r=16)''', '''    cv.R(x2, y - 12, W - M + 16, y + 668, fill="#FFFFFF", outline=C("line"), width=2, r=16)''')
rep('''        sz, ey = cv.bullets_fit((x2 + 30, cy, W - M - 20, cy + 78), [it], 24, 17, color=C("maroon"), fill=C("ink"), gap=1.18, para_gap=0)
        cy += 80''', '''        sz, ey = cv.bullets_fit((x2 + 30, cy, W - M - 20, cy + 92), [it], 25, 17, color=C("maroon"), fill=C("ink"), gap=1.2, para_gap=0)
        cy = ey + 22''')
rep('''        by += 90
    x2 = 1240''', '''        by += 98
    x2 = 1240''')
open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
