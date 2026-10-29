"""Renders the slide comps, the sheets (comp + speaker notes) and the outline PNG.

Usage: python -I build_deck.py [comps|sheets|outline|all] [S5,S6 ...]
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from PIL import Image  # noqa: E402
from deckdraw import Cv, tint  # noqa: E402
from spoken import spoken_words  # noqa: E402
from deck_layouts import render_slide, C, SEC, USED, RUNS, HI  # noqa: E402

SPECS = os.path.join(ROOT, "specs")
COMPS = os.path.join(ROOT, "comps")
COMPS_HI = os.path.join(ROOT, "comps_hi")
SHEETS = os.path.join(ROOT, "sheets")
for d in (COMPS, COMPS_HI, SHEETS):
    os.makedirs(d, exist_ok=True)


FRIENDLY = {"title": "Title slide", "kpi5": "5 key numbers", "swot_issues": "SWOT + 3 issues", "three_col": "3 columns",
            "table_side": "Table + figures", "channels_calendar": "Channels + calendar", "research_kpis": "Research + KPIs",
            "chart": "Charts", "gantt_org": "Timeline + roles", "risk_matrix": "Risk map", "takeaways": "3 takeaways", "blocks": "Reference page"}


def spk(p):
    return "Spkr " + p[1:] if p and p[0] == "P" and p[1:].isdigit() else p


def mmss(sec):
    return "%d:%02d" % (sec // 60, sec % 60)


def load():
    core, back = [], []
    for p in sorted(glob.glob(os.path.join(SPECS, "slide_*.json"))):
        s = json.load(open(p, encoding="utf-8-sig"))
        (core if s["kind"] == "core" else back).append(s)
    core.sort(key=lambda s: s["n"])
    back.sort(key=lambda s: s["n"])
    return core, back


def words(s):
    return len(re.findall(r"\S+", s.get("notes", "")))


def render_all(slides, only=None):
    out = {}
    for s in slides:
        if only and s["id"] not in only:
            p = os.path.join(COMPS, "%s.png" % s["id"])
            if os.path.exists(p):
                out[s["id"]] = Image.open(p).convert("RGB")
            continue
        img, warn = render_slide(s)
        img.save(os.path.join(COMPS, "%s.png" % s["id"]))
        out[s["id"]] = img
        hcv = HI.pop(s["id"], None)
        if hcv is not None:
            hcv.img.save(os.path.join(COMPS_HI, "%s.png" % s["id"]))
            json.dump(RUNS.get(s["id"], []), open(os.path.join(COMPS_HI, "%s.runs.json" % s["id"]), "w", encoding="utf-8"), ensure_ascii=False)
            json.dump(hcv.meta, open(os.path.join(COMPS_HI, "%s.meta.json" % s["id"]), "w", encoding="utf-8"), ensure_ascii=False)
            hcv.img = None
        small = sorted(set((z, t) for z, yy, t in USED.get(s["id"], []) if z < 18 and yy < 1000 and s["kind"] == "core"))
        print("%s rendered, %d warning(s), min body text %s px" % (s["id"], len(warn), min([z for z, yy, t in USED.get(s["id"], []) if yy < 1000] or [0])))
        for z, t in small[:6]:
            print("    small %s px: %s" % (z, t))
        for w in warn:
            print("    ! %s" % w)
    return out


def paste(cv, img, x, y, w, h):
    im = img.resize((cv.k(w), cv.k(h)), Image.LANCZOS)
    cv.img.paste(im, (cv.k(x), cv.k(y)))


# ------------------------------------------------------------------ sheets
def make_sheet(slides, comps, path, heading, cols=2, scale=0.75):
    CW, CH = int(1920 * scale), int(1080 * scale)
    pad, inner = 40, 20
    card_w = CW + 2 * inner
    probe = Cv(10, 10, K=1)
    fnote = probe.font(24)
    cards = []
    for s in slides:
        core = s["kind"] == "core"
        txt = s.get("notes", "") if s.get("notes") else ""
        if not txt and not core:
            txt = "Backup slide. Not part of the 10-minute run; held for the Q&A that follows."
        lines = probe.wrap(txt, fnote, card_w - 2 * inner)
        cards.append((s, txt, 56 + len(lines) * 24 * 1.32 + 24))
    rows = [cards[i:i + cols] for i in range(0, len(cards), cols)]
    head_h = 70
    heights = [head_h + CH + 22 + max(c[2] for c in r) + 16 for r in rows]
    top = 120
    W = pad + cols * (card_w + pad)
    H = top + sum(h + pad for h in heights) + 10
    cv = Cv(int(W), int(H), K=1, bg="#F4F0E8")
    cv.R(0, 0, W, 96, fill=C("maroon"))
    cv.T(pad, 48, heading, cv.font(44, "bold"), "#FFFFFF", anchor="lm")
    cv.T(W - pad, 48, "CPN final deck comps · 1920 x 1080 · maroon and gold", cv.font(26), "#F0D78C", anchor="rm")
    y = top
    for ri, r in enumerate(rows):
        for ci, (s, txt, nh) in enumerate(r):
            x = pad + ci * (card_w + pad)
            h = heights[ri]
            cv.R(x, y, x + card_w, y + h, fill="#FFFFFF", outline=C("line"), width=2, r=14)
            core = s["kind"] == "core"
            col = C(SEC.get(s["n"], "gray")) if core else C("gray")
            cx = x + inner
            w1 = cv.chip(cx, y + 14, s["id"], 30, "#FFFFFF", bg=col, h=44, padx=18)
            cv.T(cx + w1 + 16, y + 36, s["title"], cv.font(34, "bold"), C("ink"), anchor="lm")
            right = x + card_w - inner
            if core:
                st = s["status"]
                w2 = cv.chip(right, y + 18, st, 20, col, bg=tint(col, 0.86), align="r", h=36)
                cv.T(right - w2 - 18, y + 36, "%s  ·  %s  ·  %s" % (mmss(s["seconds"]), spk(s["presenter"]), FRIENDLY.get(s["layout"], s["layout"])),
                     cv.font(24, "semibold"), C("muted"), anchor="rm")
            else:
                cv.T(right, y + 36, s["section"], cv.font(24, "semibold"), C("muted"), anchor="rm")
            paste(cv, comps[s["id"]], cx, y + head_h, CW, CH)
            cv.R(cx, y + head_h, cx + CW, y + head_h + CH, outline=C("edge"), width=2)
            ny = y + head_h + CH + 22
            label = ("Say  (%d words, %s)" % (words(s), mmss(s["seconds"]))) if core else "Backup"
            cv.T(cx, ny, label, cv.font(24, "bold"), C("maroon"))
            fn = cv.font(24)
            ly = ny + 36
            for ln in cv.wrap(txt, fn, card_w - 2 * inner):
                cv.T(cx, ly, ln, fn, C("ink"))
                ly += 24 * 1.32
        y += heights[ri] + pad
    cv.img.save(path)
    print("sheet", os.path.basename(path), cv.img.size)


# ------------------------------------------------------------------ outline
def make_outline(core, back, comps, path):
    W = 2400
    cv = Cv(W, 100, K=1)  # probe only
    ROWH = 124
    n_back = max(len(back), 6)
    H = 620 + len(core) * ROWH + 30 + 828 + 40
    cv = Cv(W, H, K=2, bg="#FFFFFF")
    cv.paren_max = 40
    M = 60
    links = []
    cv.R(0, 0, W, 150, fill=C("maroon"))
    cv.T(M, 20, "CPN marketing plan: final deck outline", cv.font(64, "bold"), "#FFFFFF")
    cv.T(M, 98, "10-minute slot: 12 core slides + 6 backup  ·  speech 8:30 + 5 handovers x 0:10 + 0:40 spare  ·  Q&A follows (5 to 10 min)",
         cv.font(30), "#F0D78C")
    cv.chip(W - M, 40, "Updated 29 Oct 2026", 26, C("maroon"), bg="#F0D78C", align="r", h=48)
    # ---- run of show ribbon
    cv.T(M, 176, "Run of show", cv.font(34, "bold"), C("maroon"))
    cv.T(M + 230, 184, "600 s = 510 s speech + 50 s handovers + 40 s spare", cv.font(24), C("muted"))
    bys = {s["n"]: s for s in core}
    order = list(range(1, 13))
    pblocks = [("P1", [1, 2]), ("P2", [3, 4]), ("P3", [5, 6]), ("P4", [7, 8]), ("P5", [9, 10]), ("P6", [11, 12])]
    left, right = M, W - M
    ppx = (right - left) / 600.0
    pos = {}
    t = 0.0
    handover = []
    for bi, (pn, nums) in enumerate(pblocks):
        for n in nums:
            sec = bys[n]["seconds"] if n in bys else 0
            pos[n] = (left + t * ppx, left + (t + sec) * ppx, t, t + sec)
            t += sec
        if bi < len(pblocks) - 1:
            handover.append((left + t * ppx, left + (t + 10) * ppx))
            t += 10
    spare = (left + t * ppx, right)
    groups = [("Open", [1, 2]), ("Recap", [3, 4]), ("Tactics", [5, 6, 7]), ("Financials", [8, 9]), ("Controls", [10, 11]), ("Close", [12])]
    gy = 236
    for name, nums in groups:
        gx0, gx1 = pos[nums[0]][0], pos[nums[-1]][1]
        secs = sum(bys[n]["seconds"] for n in nums if n in bys)
        col = C(SEC.get(nums[0], "gray"))
        cv.R(gx0, gy, gx1 - 3, gy + 46, fill=tint(col, 0.86), outline=col, width=2, r=10)
        cv.text_fit((gx0 + 8, gy + 2, gx1 - 11, gy + 44), "%s  %s" % (name, mmss(secs)), 26, 17, "bold", col, align="center", valign="middle", max_lines=1)
    by0 = 296
    for n in order:
        x0, x1, ta, tb = pos[n]
        col = C(SEC.get(n, "gray"))
        cv.R(x0, by0, x1 - 3, by0 + 78, fill=col, r=8)
        if x1 - 3 - x0 < 60:
            cv.T((x0 + x1 - 3) / 2, by0 + 39, "S%d" % n, cv.font(18, "bold"), "#FFFFFF", anchor="mm")
        else:
            cv.T((x0 + x1 - 3) / 2, by0 + 24, "S%d" % n, cv.font(28, "bold"), "#FFFFFF", anchor="mm")
            cv.T((x0 + x1 - 3) / 2, by0 + 56, mmss(bys[n]["seconds"]) if n in bys else "", cv.font(22), "#FFFFFF", anchor="mm")
    for hx0, hx1 in handover:
        cv.R(hx0, by0 + 8, hx1 - 3, by0 + 70, fill="#E8C85A", r=6)
    cv.R(spare[0], by0 + 8, spare[1], by0 + 70, fill="#EEE9DF", outline=C("edge"), width=2, r=8)
    cv.T((spare[0] + spare[1]) / 2, by0 + 39, "spare 0:40", cv.font(22, "semibold"), C("muted"), anchor="mm")
    py = by0 + 92
    for pn, nums in pblocks:
        x0, x1 = pos[nums[0]][0], pos[nums[-1]][1]
        secs = sum(bys[n]["seconds"] for n in nums if n in bys)
        cv.R(x0, py, x1 - 3, py + 50, fill="#FFFFFF", outline=C("maroon"), width=2, r=10)
        cv.T((x0 + x1 - 3) / 2, py + 25, "%s  %s" % (spk(pn), mmss(secs)), cv.font(26, "bold"), C("maroon"), anchor="mm")
    ay = py + 66
    cv.line(left, ay, right, ay, C("mid"), 2)
    for m in range(0, 11):
        xx = left + m * 60 * ppx
        cv.line(xx, ay - 8, xx, ay + 8, C("mid"), 2)
        cv.T(xx, ay + 12, "%d:00" % m, cv.font(20), C("muted"), anchor="ma")
    lgx = M
    lgy = ay + 52
    cv.R(lgx, lgy + 4, lgx + 34, lgy + 28, fill="#E8C85A", r=4)
    cv.T(lgx + 44, lgy, "handover 0:10 (x5)", cv.font(22), C("muted"))
    cv.R(lgx + 330, lgy + 4, lgx + 364, lgy + 28, fill="#FFFFFF", outline=C("maroon"), width=2, r=4)
    cv.T(lgx + 374, lgy, "speaker block Spkr 1 to Spkr 6 (names assigned by the team)", cv.font(22), C("muted"))
    # ---- 12 slides
    ty = lgy + 56
    cv.T(M, ty, "The 12 core slides", cv.font(36, "bold"), C("maroon"))
    cv.T(M + 380, ty + 8, "headline = the sentence at the top of each slide (S1 has none; its row shows a one-line summary)", cv.font(24), C("muted"))
    y = ty + 58
    colx = dict(thumb=M, title=M + 224, head=M + 760, time=M + 1740, status=M + 2000)
    for i, s in enumerate(core):
        col = C(SEC.get(s["n"], "gray"))
        links.append((s["id"], M - 16, y - 6, W - M + 16, y + ROWH - 8))
        if i % 2 == 0:
            cv.R(M - 16, y - 6, W - M + 16, y + ROWH - 8, fill="#FAF7F0", r=10)
        im = comps.get(s["id"])
        if im is not None:
            paste(cv, im, colx["thumb"], y, 192, 108)
            cv.R(colx["thumb"], y, colx["thumb"] + 192, y + 108, outline=C("edge"), width=1.5)
        cv.chip(colx["title"], y + 2, s["id"], 24, "#FFFFFF", bg=col, h=36, padx=14)
        cv.text_fit((colx["title"] + 96, y, colx["head"] - 24, y + 42), s["title"], 28, 18, "bold", C("ink"), max_lines=1, valign="middle")
        cv.text_fit((colx["title"], y + 46, colx["head"] - 24, y + 100), s["section"], 22, 15, "regular", C("muted"), max_lines=2)
        cv.text_fit((colx["head"], y, colx["time"] - 24, y + 108), s["headline"], 27, 17, "regular", C("ink"), max_lines=4, valign="middle", gap=1.2)
        cv.T(colx["time"], y + 14, mmss(s["seconds"]), cv.font(34, "bold"), col)
        cv.T(colx["time"], y + 60, "%s · %d words" % (spk(s["presenter"]), words(s)), cv.font(22, "semibold"), C("muted"))
        cv.chip(colx["status"], y + 10, s["status"], 22, col, bg=tint(col, 0.86), h=38)
        cv.text_fit((colx["status"], y + 58, W - M, y + 100), FRIENDLY.get(s["layout"], s["layout"]), 22, 15, "regular", C("muted"), max_lines=1)
        y += ROWH
    # ---- backup + checklist
    y += 30
    cv.R(M - 16, y - 12, 1180, y + 816, fill="#FFFFFF", outline=C("line"), width=2, r=16)
    cv.T(M, y, "Backup slides (not presented; ready for the Q&A)", cv.font(34, "bold"), C("maroon"))
    by = y + 62
    for i in range(6):
        if i < len(back):
            s = back[i]
            links.append((s["id"], M - 10, by - 6, 1170, by + 90))
            cv.chip(M, by, s["id"], 24, "#FFFFFF", bg=C("gray"), h=36, padx=14)
            cv.text_fit((M + 80, by - 2, 1150, by + 40), s["title"], 28, 18, "bold", C("ink"), max_lines=1, valign="middle")
            cv.text_fit((M + 80, by + 40, 1150, by + 86), s["headline"], 22, 15, "regular", C("muted"), max_lines=2, gap=1.15)
        else:
            cv.chip(M, by, "B%d" % (i + 1), 24, "#FFFFFF", bg=C("gray"), h=36, padx=14)
            cv.T(M + 80, by + 18, "in preparation", cv.font(26), C("muted"), anchor="lm")
        by += 98
    x2 = 1240
    cv.R(x2, y - 12, W - M + 16, y + 816, fill="#FFFFFF", outline=C("line"), width=2, r=16)
    cv.T(x2 + 30, y, "Build checklist", cv.font(34, "bold"), C("maroon"))
    tot_words = sum(words(s) for s in core)
    tot_spoken = sum(spoken_words(s.get("notes", "")) for s in core)
    items = [
        "Tap a slide row above, or use the bookmarks, to jump to its page. Each page has the comp, the speaker notes and the slide text to copy; page 2 is the build key (frame, colours, type and chart rules).",
        "Canvas 1920 x 1080; palette maroon #8C1D28 and gold #C9A227 as in the 7 Sep deck, with that deck's fonts (the comps use Segoe UI as a stand-in); sources line at the foot of every slide except S1.",
        "Headlines are the full sentences shown. Keep caveats off the main slides; they sit in the B2 footnote (The Central Phaholyothin date) and on the B6 cards.",
        "Build the charts on S8 and S9 as native, editable charts; their data, axes and colours are under 'Text on the slide' on each page.",
        "Footer navigation (Situation, Strategy, Tactics, Financials, Controls) on S2 to S12; the current section is highlighted on S3 to S11 only.",
        "Paste the speaker notes into each slide's notes: %s words written, about %s spoken with numbers read aloud, which is %d s at 130 words a minute against the 510 s budget. Backup pages carry short notes; B6 lists owners and first answers." % ("{:,}".format(tot_words), "{:,}".format(tot_spoken), round(tot_spoken / 130.0 * 60)),
        "Numbers and sources were checked against the report and the corrections log on 29 Oct 2026, and the report was aligned with the deck. B6 sources outside Chapters 4 to 6 (Central Retail, CPN 9 Apr 2026, S&P Yearbook, CPN IR page) are in the Sections 2–3 list.",
        "Locked corrections: 23 provinces; Central Retail's loyalty ecosystem has 23M members in Thailand (we read it as The 1); 50% cut by 2034 vs 2024; Phaholyothin 1Q27; base case misses F1.",
    ]
    cy = y + 62
    for it in items:
        sz, ey = cv.bullets_fit((x2 + 30, cy, W - M - 20, cy + 92), [it], 24, 17, color=C("maroon"), fill=C("ink"), gap=1.2, para_gap=0)
        cy = ey + 20
    cv.img.save(os.path.join(COMPS_HI, "outline.png"))
    json.dump(cv.runs, open(os.path.join(COMPS_HI, "outline.runs.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"w": W, "h": H, "links": links}, open(os.path.join(COMPS_HI, "outline.links.json"), "w", encoding="utf-8"))
    cv.img.resize((W, H), Image.LANCZOS).save(path)
    print("outline", os.path.basename(path), (W, H), cv.warn)


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    only = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None
    core, back = load()
    comps = render_all(core + back, only)
    if what in ("sheets", "all"):
        for k in range(0, len(core), 4):
            grp = core[k:k + 4]
            make_sheet(grp, comps, os.path.join(SHEETS, "%02d_slides_%d-%d.png" % (k // 4 + 1, grp[0]["n"], grp[-1]["n"])),
                       "Slides %d to %d of 12" % (grp[0]["n"], grp[-1]["n"]))
        if back:
            make_sheet(back, comps, os.path.join(SHEETS, "04_backup_B1-B6.png"), "Backup slides B1 to B6 (not presented)")
    if what in ("outline", "all"):
        make_outline(core, back, comps, os.path.join(SHEETS, "00_final_outline.png"))


main()
