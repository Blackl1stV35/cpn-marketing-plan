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

patch(d + "\\make_pdf.py", [
    ('        h += n * 36 + 12\n    h += 40\n    return items, h', '        h += n * 36 + 12\n    h += 84\n    return items, h'),
    ('''            draw_lines(c, vl, M + 292, yy, "SegoeUI", 26, 36, col("ink"))
    c.showPage()''', '''            draw_lines(c, vl, M + 292, yy, "SegoeUI", 26, 36, col("ink"))
    c.setFillColor(col("maroon"))
    c.setFont("SegoeUI-Semibold", 26)
    lab = "Back to outline"
    lw = sw(lab, "SegoeUI-Semibold", 26)
    c.drawRightString(PW - M, 30, lab)
    c.linkRect("", "outline", (PW - M - lw - 8, 16, PW - M + 8, 62), relative=0, thickness=0)
    c.showPage()'''),
])
patch(d + "\\build_deck.py", [
    ('''        "Canvas 1920 x 1080; palette maroon #8C1D28 and gold #C9A227 as in the 7 Sep deck; sources line at the foot of every slide.",
        "Headline is the full sentence in the comp; one idea per slide; no slide carries a caveat that is not in its spec.",
        "Charts on S8 and S9 as native, editable charts (data in the spec); the rest are shapes and tables.",
        "Footer navigation on S3 to S11 (Situation, Strategy, Tactics, Financials, Controls), current section highlighted.",
        "Speaker notes pasted per slide: %s words in total, timed to the 8:30 speech; backups carry no notes except B6." % "{:,}".format(tot_words),
        "Every number carries a fact line (value, meaning, report location) in its spec file, so the deck can be checked against the report.",
        "Corrections are locked: 23 provinces, The 1 = 23M members, 50% cut by 2034 vs 2024, Phaholyothin 1Q27, base case misses F1.",''',
     '''        "Tap a slide row above, or use the bookmarks, to jump to its page. Each page has the comp, the speaker notes and the slide text to copy.",
        "Canvas 1920 x 1080; palette maroon #8C1D28 and gold #C9A227 as in the 7 Sep deck; sources line at the foot of every slide.",
        "Headlines are the full sentences shown. Keep caveats off the main slides; the only one (The Central Phaholyothin date) sits in the B2 footnote.",
        "Build the charts on S8 and S9 as native, editable charts; their data is under 'Text on the slide' on each page.",
        "Footer navigation on S3 to S11 (Situation, Strategy, Tactics, Financials, Controls), current section highlighted.",
        "Paste the speaker notes into each slide's notes: %s words in total, timed to the 8:30 speech. Backup pages carry short notes; B6 lists owners and first answers." % "{:,}".format(tot_words),
        "Numbers and sources were checked against Chapters 4 to 6 of the report on 29 Oct 2026.",
        "Locked corrections: 23 provinces, The 1 = 23M members, 50% cut by 2034 vs 2024, Phaholyothin 1Q27, base case misses F1.",'''),
    ('''    H = 620 + len(core) * ROWH + 30 + 680 + 40''', '''    H = 620 + len(core) * ROWH + 30 + 740 + 40'''),
    ('''    cv.R(M - 16, y - 12, 1180, y + 668, fill="#FFFFFF", outline=C("line"), width=2, r=16)''', '''    cv.R(M - 16, y - 12, 1180, y + 728, fill="#FFFFFF", outline=C("line"), width=2, r=16)'''),
    ('''    cv.R(x2, y - 12, W - M + 16, y + 668, fill="#FFFFFF", outline=C("line"), width=2, r=16)''', '''    cv.R(x2, y - 12, W - M + 16, y + 728, fill="#FFFFFF", outline=C("line"), width=2, r=16)'''),
    ('''[it], 25, 17, color=C("maroon"), fill=C("ink"), gap=1.2, para_gap=0)
        cy = ey + 22''', '''[it], 24, 17, color=C("maroon"), fill=C("ink"), gap=1.2, para_gap=0)
        cy = ey + 20'''),
])
print("ok")
