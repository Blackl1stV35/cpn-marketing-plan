import sys, re
d = sys.argv[1]
def patch(p, pairs):
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            raise SystemExit("MISMATCH %d in %s: %s" % (n, p, old[:80]))
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="\n").write(t)

p = d + "\\build_deck.py"
t = open(p, encoding="utf-8").read()
a = t.index('    items = [\n        "Tap a slide row')
b = t.index('    ]\n    cy = y + 62')
new_items = '''    items = [
        "Tap a slide row above, or use the bookmarks, to jump to its page. Each page has the comp, the speaker notes and the slide text to copy; page 2 is the build key (colours, type, layout rules).",
        "Canvas 1920 x 1080; palette maroon #8C1D28 and gold #C9A227 as in the 7 Sep deck, with that deck's fonts (the comps use Segoe UI as a stand-in); sources line at the foot of every slide except S1.",
        "Headlines are the full sentences shown. Keep caveats off the main slides; the only one (The Central Phaholyothin date) sits in the B2 footnote.",
        "Build the charts on S8 and S9 as native, editable charts; their data, axes and colours are under 'Text on the slide' on each page.",
        "Footer navigation (Situation, Strategy, Tactics, Financials, Controls) on S2 to S12; the current section is highlighted on S3 to S11 only.",
        "Paste the speaker notes into each slide's notes: %s words written, about %s spoken with numbers read aloud, which is %d s at 130 words a minute against the 510 s budget. Backup pages carry short notes; B6 lists owners and first answers." % ("{:,}".format(tot_words), "{:,}".format(tot_spoken), round(tot_spoken / 130.0 * 60)),
        "Numbers and sources were checked against Chapters 4 to 6 of the report on 29 Oct 2026.",
        "Locked corrections: 23 provinces; Central Retail's loyalty ecosystem has 23M members in Thailand (we read it as The 1); 50% cut by 2034 vs 2024; Phaholyothin 1Q27; base case misses F1.",
'''
t = t[:a] + new_items + t[b:]
open(p, "w", encoding="utf-8", newline="\n").write(t)

patch(p, [
    ("def mmss(sec):", "def spk(p):\n    return \"Spkr \" + p[1:] if p and p[0] == \"P\" and p[1:].isdigit() else p\n\n\ndef mmss(sec):"),
    ("from deckdraw import Cv, tint  # noqa: E402", "from deckdraw import Cv, tint  # noqa: E402\nfrom spoken import spoken_words  # noqa: E402"),
    ('mmss(s["seconds"]), s["presenter"], FRIENDLY', 'mmss(s["seconds"]), spk(s["presenter"]), FRIENDLY'),
    ('"%s  %s" % (pn, mmss(secs))', '"%s  %s" % (spk(pn), mmss(secs))'),
    ('"%s · %d words" % (s["presenter"], words(s))', '"%s · %d words" % (spk(s["presenter"]), words(s))'),
    ('"presenter block P1 to P6 (names assigned by the team)"', '"speaker block Spkr 1 to Spkr 6 (names assigned by the team)"'),
    ('"headline = the full sentence printed on each slide"', '"headline = the sentence at the top of each slide (S1 shows a one-line summary instead)"'),
    ("    tot_words = sum(words(s) for s in core)\n", "    tot_words = sum(words(s) for s in core)\n    tot_spoken = sum(spoken_words(s.get(\"notes\", \"\")) for s in core)\n"),
    ('            json.dump(RUNS.get(s["id"], []), open(os.path.join(COMPS_HI, "%s.runs.json" % s["id"]), "w", encoding="utf-8"), ensure_ascii=False)\n',
     '            json.dump(RUNS.get(s["id"], []), open(os.path.join(COMPS_HI, "%s.runs.json" % s["id"]), "w", encoding="utf-8"), ensure_ascii=False)\n            json.dump(hcv.meta, open(os.path.join(COMPS_HI, "%s.meta.json" % s["id"]), "w", encoding="utf-8"), ensure_ascii=False)\n'),
])

patch(d + "\\audit_pdf.py", [
    ('if doc.page_count != 1 + len(order):\n    P("page count %d, expected %d" % (doc.page_count, 1 + len(order)))', 'if doc.page_count != 2 + len(order):\n    P("page count %d, expected %d" % (doc.page_count, 2 + len(order)))'),
    ('    imgs = pg.get_images(full=True)\n    if len(imgs) != 1:', '    imgs = pg.get_images(full=True)\n    if i == 1:\n        continue\n    if len(imgs) != 1:'),
    ('want = 1 + 1 + len(core) + 1 + len(back)', 'want = 1 + 1 + 1 + len(core) + 1 + len(back)'),
    ('want_dests = list(range(2, doc.page_count + 1))', 'want_dests = list(range(3, doc.page_count + 1))'),
    ('    pn = idx + 2\n', '    pn = idx + 3\n'),
])
print("ok")
