"""Builds the sketch PDF: outline page, build key, 12 core slide pages, 6 backup pages.

Each slide page = hi-res comp (with an invisible, searchable text layer) + speaker notes + the slide text in reading order.
Usage: python -I make_pdf.py [OUT.pdf]
"""
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from reportlab.pdfgen import canvas  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.lib.colors import HexColor  # noqa: E402
from deckdraw import PAL  # noqa: E402
from deck_layouts import ACC  # noqa: E402
from spoken import spoken_words  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "package", "CPN_final_deck_sketch.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
HI = os.path.join(ROOT, "comps_hi")
FONTDIR = "C:\\Windows\\Fonts\\"
FONTS = {"segoeui.ttf": "SegoeUI", "segoeuib.ttf": "SegoeUI-Bold", "seguisb.ttf": "SegoeUI-Semibold",
         "segoeuil.ttf": "SegoeUI-Light", "segoeuii.ttf": "SegoeUI-Italic"}
for fn, nm in FONTS.items():
    pdfmetrics.registerFont(TTFont(nm, FONTDIR + fn))

PW, M = 1920, 64
SEC = {1: "maroon", 2: "maroon", 3: "slate", 4: "slate", 5: "golddark", 6: "golddark", 7: "golddark", 8: "teal", 9: "teal",
       10: "purple", 11: "purple", 12: "maroon"}
FRIENDLY = {"title": "Title slide", "kpi5": "5 key numbers", "swot_issues": "SWOT + 3 issues", "three_col": "3 columns",
            "table_side": "Table + figures", "channels_calendar": "Channels + calendar", "research_kpis": "Research + KPIs",
            "chart": "Charts", "gantt_org": "Timeline + roles", "risk_matrix": "Risk map", "takeaways": "3 takeaways",
            "blocks": "Reference page"}
NAV = ["Situation", "Strategy", "Tactics", "Financials", "Controls"]
MISSING = {}


def spk(p):
    return "Spkr " + p[1:] if p and p[0] == "P" and p[1:].isdigit() else p


def col(name):
    return HexColor(PAL.get(name, name))


def hexof(name):
    return PAL.get(name, name)


def mmss(sec):
    return "%d:%02d" % (sec // 60, sec % 60)


def sw(text, font, size):
    return pdfmetrics.stringWidth(text, font, size)


def glyph_check(text, font):
    face = pdfmetrics.getFont(font).face
    for ch in text:
        if ch in "\n\t " or ord(ch) in face.charToGlyph:
            continue
        MISSING.setdefault(ch, set()).add(text[:50])


def wrap(text, font, size, width):
    lines = []
    for para in str(text).split("\n"):
        cur = ""
        for word in [w_ for w_ in para.split(" ") if w_]:
            t = (cur + " " + word) if cur else word
            if sw(t, font, size) <= width or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def words(s):
    return len(re.findall(r"\S+", s.get("notes", "")))


def norm(t):
    return re.sub(r"\s+", " ", t.replace("\u00a0", " ")).strip()


def num(v):
    if isinstance(v, float) and not v.is_integer():
        return ("%.2f" % v).rstrip("0").rstrip(".")
    v = int(v) if float(v).is_integer() else v
    return "{:,}".format(v) if isinstance(v, int) and abs(v) >= 1000 else str(v)


def pos_name(months, p, end=False):
    n = len(months)
    i = int(math.floor(p + 1e-9))
    frac = p - i
    if abs(frac) < 1e-6:
        if end and i > 0:
            return "end of " + str(months[i - 1])
        return "start of " + str(months[min(i, n - 1)])
    return "%d%% into %s" % (round(frac * 100), months[min(i, n - 1)])


def fax(v, unit):
    return ("%g%%" % v) if "%" in unit else num(v)


def fvu(v, unit):
    return ("%.1f%%" % v) if "%" in unit else num(v)


def acc_name(i):
    return ACC[i % len(ACC)]


# ------------------------------------------------------------------ slide text in reading order
def slide_entries(s, runs, metas):
    E = []
    b = s["body"]
    L = s["layout"]
    core = s["kind"] == "core"

    def add(k, v):
        if v not in (None, ""):
            E.append((k, str(v)))

    if L != "title":
        add("Section chip", s["section"])
        add("Status chip", s["status"] if core else "BACKUP")
        add("Headline", s["headline"])
    if L == "title":
        add("Title", b["title"])
        add("Subtitle", b["subtitle"])
        add("Presented by", "\n".join(b["team"]))
        add("Presented to", b["instructor"])
        add("Course", b["course"])
        add("Term", b["term"])
    elif L == "kpi5":
        for i, t in enumerate(b["tiles"], 1):
            add("Tile %d (%s #%s)" % (i, acc_name(i - 1), hexof(acc_name(i - 1))[1:]), "%s | %s | %s" % (t["value"], t["label"], t["note"]))
        add("Banner (maroon, white text)", b["ask"])
    elif L == "swot_issues":
        for q, nm in zip("SWOT", ["Strengths", "Weaknesses", "Opportunities", "Threats"]):
            add(nm, "\n".join("- " + x for x in b["swot"][q]))
        for i, it in enumerate(b["issues"], 1):
            add("Issue %d" % i, "%s | %s" % (it["title"], it["why"]))
    elif L == "three_col":
        for i, c in enumerate(b["cols"], 1):
            parts = []
            if c.get("big"):
                parts.append("%s | %s" % (c["big"]["value"], c["big"]["label"]))
            parts += ["- " + x for x in c["bullets"]]
            add("Column %d: %s" % (i, c["title"]), "\n".join(parts))
    elif L == "table_side":
        t = b["table"]
        add("Table title", t["title"])
        add("Table header", " | ".join(t["cols"]))
        for i, r in enumerate(t["rows"], 1):
            add("Row %d" % i, " | ".join(r))
        add("Table column widths", " / ".join("%d%%" % round(w_ * 100) for w_ in t["widths"]) + " (zebra rows, maroon header)")
        add("Side title", b["side"]["title"])
        for i, it in enumerate(b["side"]["items"], 1):
            add("Figure %d (%s)" % (i, acc_name(i - 1)), "%s | %s" % (it["value"], it["label"]))
    elif L == "channels_calendar":
        add("Hub", b["hub"])
        for i, n in enumerate(b["nodes"], 1):
            add("Channel %d (%s; clockwise from 12 o'clock)" % (i, acc_name(i - 1)), "%s | %s" % (n["name"], n.get("note", "")))
        cal = b["calendar"]
        m = len(cal["months"])
        add("Calendar columns", " ".join(str(x) for x in cal["months"]))
        for i, br in enumerate(cal["bars"], 1):
            add("Window %d (%s)" % (i, acc_name(i - 1)), "%s | columns %s to %s of %d | %s" % (br["label"], br["start"] + 1, br["end"], m, br.get("note", "")))
        add("Budget box (maroon)", "%s | %s" % (b["budget"]["value"], b["budget"]["label"]))
    elif L == "research_kpis":
        for i, mth in enumerate(b["methods"], 1):
            add("Method %d (%s)" % (i, acc_name(i - 1)), "%s | %s | %s" % (mth["name"], mth["what"], mth.get("when", "")))
        for i, k in enumerate(b["kpis"], 1):
            add("Indicator %d (%s)" % (i, acc_name(i - 1)), "%s | %s | Baseline: %s | Target [Proposed]: %s" % (k["tag"], k["name"], k["baseline"], k["target"]))
    elif L == "chart":
        for ci, ch in enumerate(b["charts"], 1):
            mt = metas[ci - 1] if ci - 1 < len(metas) else None
            add("Chart %d title" % ci, ch["title"])
            add("Chart %d unit label (top right)" % ci, ch["unit"])
            add("Chart %d type" % ci, "stacked columns" if ch["type"] == "stacked" else "clustered columns, plus dashed full-width reference lines for line series")
            if mt:
                trunc = "; the axis does not start at zero, so show the note 'Axis starts at %s'" % fax(mt["vmin"], ch["unit"]) if mt["vmin"] > 0 else "; starts at zero"
                add("Chart %d value axis" % ci, "%s to %s, gridlines every %s%s" % (fax(mt["vmin"], ch["unit"]), fax(mt["vmax"], ch["unit"]), fax(mt["step"], ch["unit"]), trunc))
            add("Chart %d categories" % ci, " | ".join(str(x) for x in ch["categories"]))
            for se in ch["series"]:
                kind = "dashed reference line, value at the right end" if se.get("kind") == "line" else "columns"
                add("Chart %d series" % ci, "%s | %s | %s #%s | %s" % (se["name"], kind, se["color"], hexof(se["color"])[1:], " | ".join(fvu(v, ch["unit"]) for v in se["values"])))
            for an in ch.get("annotations", []):
                add("Chart %d chip under %s (pale yellow, gold outline)" % (ci, ch["categories"][an.get("category", 0)]), an["text"])
        tone_hex = {"good": PAL["good"], "warn": PAL["warn"], "neutral": PAL["neutral"]}
        for i, c in enumerate(b["callouts"], 1):
            tn = c.get("tone", "neutral")
            add("Callout %d (%s #%s)" % (i, tn, tone_hex.get(tn, PAL["neutral"])[1:]), "%s | %s" % (c["value"], c["label"]))
        add("Reading line", b["note"])
    elif L == "gantt_org":
        months = b["months"]
        add("Timeline scale", "%d equal columns (%s); position 0 is the left edge of the first column and %d the right edge of the last; column k spans k-1 to k" % (len(months), ", ".join(months), len(months)))
        for i, r in enumerate(b["rows"], 1):
            tone = r.get("tone", acc_name(i - 1))
            add("Bar %d (%s #%s)" % (i, tone, hexof(tone)[1:]), "%s | %s to %s | positions %s to %s" % (r["label"], pos_name(months, r["start"]), pos_name(months, r["end"], True), r["start"], r["end"]))
        for g in b["gates"]:
            add("Gate %s (maroon)" % g["label"].split()[0], "%s | dashed vertical line at position %s (%s) | release chip: %s" % (g["label"], g["at"], pos_name(months, g["at"]), g.get("release", "")))
        add("Roles top box (maroon)", b["org"]["top"])
        for i, u in enumerate(b["org"]["units"], 1):
            ex = u.get("role", "").lower().startswith("existing")
            add("Role %d (%s)" % (i, "grey outline, not linked to the sponsor" if ex else acc_name(i)), "%s | %s" % (u["name"], u.get("role", "")))
    elif L == "risk_matrix":
        add("Map layout", "3 x 3 heat map, maroon shading darker towards High likelihood and High impact; rows = Likelihood (H at the top, then M, L); columns = Impact (L, M, H from the left); a numbered white circle per risk sits in its cell")
        cells = {}
        for r in b["risks"]:
            cells.setdefault((r["likelihood"], r["impact"]), []).append(str(r["id"]))
        for (lk, im), ids in sorted(cells.items()):
            add("Cell likelihood %s, impact %s" % (lk, im), "risks " + ", ".join(ids))
        for r in b["risks"]:
            add("Risk %s" % r["id"], "%s | likelihood %s | impact %s" % (r["name"], r["likelihood"], r["impact"]))
        add("Table header", "Risk | Trigger [Proposed] | Response [Proposed]")
        for i, t in enumerate(b["top"], 1):
            add("Watch %d" % i, "%s | %s | %s" % (t["risk"], t["trigger"], t["response"]))
        if b.get("ladder"):
            ld = b["ladder"]
            add("Response ladder (three pills: Amber gold-dark, Red maroon, Crisis black)", ld["title"] + "\n" + "\n".join("%s | %s" % (st["name"], st["text"]) for st in ld["steps"]))
        w = b["worst"]
        add("Worst cases", "%s | %s" % (w["title"], w["text"]))
        for i, n in enumerate(w["numbers"], 1):
            add("Worst figure %d" % i, "%s | %s" % (n["value"], n["label"]))
    elif L == "takeaways":
        for i, c in enumerate(b["cards"], 1):
            add("Card %s (%s)" % (c.get("n", i), acc_name(i - 1)), "%s | %s" % (c["title"], c["text"]))
        add("Closing banner (maroon)", b["closing"] + " | Q&A (gold pill)")
    elif L == "blocks":
        seen = {}
        for cols in b["columns"]:
            for bl in cols:
                k_ = bl.get("title") or bl["type"]
                seen[k_] = seen.get(k_, 0) + 1
        for ci, cols in enumerate(b["columns"], 1):
            for bl in cols:
                t = bl["type"]
                ttl = bl.get("title") or t
                label = ttl if seen[ttl] == 1 else "%s (col %d)" % (ttl, ci)
                if t == "table":
                    add(label, " | ".join(bl["cols"]) + "\n" + "\n".join(" | ".join(r) for r in bl["rows"]))
                    if bl.get("widths"):
                        add(label + ": column widths", " / ".join("%d%%" % round(w_ * 100) for w_ in bl["widths"]) + " (maroon header, zebra rows, first column bold maroon)")
                elif t == "bullets":
                    add(label, "\n".join("- " + x for x in bl["items"]))
                elif t == "cards":
                    add(label, "\n".join("%s | %s%s" % (it["head"], it["text"], (" | " + it["tag"]) if it.get("tag") else "") for it in bl["items"]))
                elif t == "text":
                    add(label, bl["text"])
                elif t == "kpis":
                    add(label if bl.get("title") else "Summary tiles", "\n".join("%s | %s" % (it["value"], it["label"]) for it in bl["items"]))
    if s["sources"] and L != "title":
        add("Sources line", "Sources: " + "; ".join(s["sources"]))
    # anything else drawn on the comp (headings, axis titles, labels) that the entries above do not already carry
    alltext = norm(" ".join(v for k, v in E))
    nav_hit = [r for r in runs if norm(r[2]) in NAV]
    other, seen_runs = [], set()
    for r in runs:
        t_ = norm(r[2])
        if len(t_) < 2 or t_ in NAV or re.fullmatch(r"[\d.,%\u0e3f\- /x]+", t_) or t_ in seen_runs:
            continue
        t2 = re.sub(r"^\d+\s+", "", t_)
        if t_ in alltext or t2 in alltext:
            continue
        seen_runs.add(t_)
        other.append(t_)
    if other:
        add("Other text on the comp (headings, axis titles, labels)", "\n".join(other))
    pc = [norm(r[2]) for r in runs if re.fullmatch(r"\d+ / 12", norm(r[2]))]
    if pc:
        add("Page counter (top right)", pc[0])
    if len(nav_hit) >= 5:
        hl = L != "title" and 3 <= s["n"] <= 11
        add("Footer navigation", " | ".join(NAV) + (" (current section bold, underlined)" if hl else " (no section highlighted)"))
    return E


# ------------------------------------------------------------------ pages
def invisible_layer(c, runs, sc, H, y_off=0.0):
    c.saveState()
    t = c.beginText()
    t.setTextRenderMode(3)
    for xl, base, text, size, fontfile in runs:
        name = FONTS.get(fontfile, "SegoeUI")
        t.setFont(name, max(1.0, size * sc))
        t.setTextOrigin(xl * sc, H - (y_off + base * sc))
        t.textOut(text)
    c.drawText(t)
    c.restoreState()


def draw_lines(c, lines, x, y_top, font, size, leading, color):
    c.setFont(font, size)
    c.setFillColor(color)
    y = y_top
    for ln in lines:
        glyph_check(ln, font)
        c.drawString(x, y - size * 0.85, ln)
        y -= leading
    return y


def back_link(c):
    c.setFillColor(col("maroon"))
    c.setFont("SegoeUI-Semibold", 26)
    lab = "Back to outline"
    lw = sw(lab, "SegoeUI-Semibold", 26)
    c.drawRightString(PW - M, 30, lab)
    c.linkRect("", "outline", (PW - M - lw - 8, 16, PW - M + 8, 62), relative=0, thickness=0)


def plan_slide(s, entries):
    """Returns the panel items and their total height (below the 1080 pt comp)."""
    core = s["kind"] == "core"
    items = []
    h = 56
    items.append(("header", h, 84))
    h += 84 + 12
    txt = s.get("notes") or ""
    if core:
        label = "Say  ·  %d words (%d spoken)  ·  %s  ·  %s" % (words(s), spoken_words(txt), mmss(s["seconds"]), spk(s["presenter"]))
    else:
        label = "Speaker note (backup slide, not presented)"
        if not txt:
            txt = "Backup slide. Not part of the 10-minute run; held for the Q&A that follows."
    items.append(("label", h, label))
    h += 56
    lines = wrap(txt, "SegoeUI", 31, PW - 2 * M)
    items.append(("para", h, lines))
    h += len(lines) * 45 + 28
    items.append(("rule", h, None))
    h += 34
    items.append(("label", h, "Text on the slide, in reading order (to copy)"))
    h += 56
    kw = 360
    for k, v in entries:
        kl = wrap(k, "SegoeUI-Semibold", 24, kw - 20)
        vl = wrap(v, "SegoeUI", 26, PW - 2 * M - kw)
        n = max(len(kl), len(vl))
        items.append(("entry", h, (kl, vl, kw)))
        h += n * 36 + 12
    h += 84
    return items, h


def draw_slide_page(c, s, key, extra_keys=()):
    core = s["kind"] == "core"
    runs = json.load(open(os.path.join(HI, "%s.runs.json" % s["id"]), encoding="utf-8"))
    mp = os.path.join(HI, "%s.meta.json" % s["id"])
    metas = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else []
    entries = slide_entries(s, runs, metas)
    items, panel_h = plan_slide(s, entries)
    H = 1080 + panel_h
    c.setPageSize((PW, H))
    c.bookmarkPage(key, fit="FitH", top=H)
    for ek in extra_keys:
        c.bookmarkPage(ek, fit="FitH", top=H)
    c.setFillColor(HexColor("#F4F0E8"))
    c.rect(0, 0, PW, panel_h, fill=1, stroke=0)
    c.drawImage(os.path.join(HI, "%s.png" % s["id"]), 0, H - 1080, PW, 1080)
    invisible_layer(c, runs, 1.0, H, 0.0)
    c.setStrokeColor(HexColor(PAL["maroon"]))
    c.setLineWidth(5)
    c.line(0, H - 1080, PW, H - 1080)
    top = H - 1080
    ccol = col(SEC.get(s["n"], "gray")) if core else col("gray")
    for kind, y, data in items:
        yy = top - y
        if kind == "header":
            cw = sw(s["id"], "SegoeUI-Bold", 32) + 44
            c.setFillColor(ccol)
            c.roundRect(M, yy - 56, cw, 56, 28, fill=1, stroke=0)
            c.setFillColor(HexColor("#FFFFFF"))
            c.setFont("SegoeUI-Bold", 32)
            c.drawCentredString(M + cw / 2, yy - 40, s["id"])
            glyph_check(s["title"], "SegoeUI-Bold")
            c.setFillColor(col("ink"))
            c.setFont("SegoeUI-Bold", 46)
            c.drawString(M + cw + 24, yy - 44, s["title"])
            right = ("%s  ·  %s  ·  %s  ·  %s" % (mmss(s["seconds"]), spk(s["presenter"]), FRIENDLY.get(s["layout"], s["layout"]), s["status"])) if core else "%s  ·  %s" % (s["section"], s["status"])
            glyph_check(right, "SegoeUI-Semibold")
            c.setFillColor(col("muted"))
            c.setFont("SegoeUI-Semibold", 30)
            c.drawRightString(PW - M, yy - 42, right)
        elif kind == "label":
            glyph_check(data, "SegoeUI-Bold")
            c.setFillColor(col("maroon"))
            c.setFont("SegoeUI-Bold", 32)
            c.drawString(M, yy - 30, data)
        elif kind == "para":
            draw_lines(c, data, M, yy, "SegoeUI", 31, 45, col("ink"))
        elif kind == "rule":
            c.setStrokeColor(col("line"))
            c.setLineWidth(2)
            c.line(M, yy, PW - M, yy)
        elif kind == "entry":
            kl, vl, kw = data
            draw_lines(c, kl, M, yy, "SegoeUI-Semibold", 24, 36, col("muted"))
            draw_lines(c, vl, M + kw, yy, "SegoeUI", 26, 36, col("ink"))
    back_link(c)
    c.showPage()


def draw_outline_page(c, links_by_id):
    meta = json.load(open(os.path.join(HI, "outline.links.json"), encoding="utf-8"))
    sc = PW / float(meta["w"])
    H = int(round(meta["h"] * sc))
    c.setPageSize((PW, H))
    c.bookmarkPage("outline", fit="FitH", top=H)
    c.drawImage(os.path.join(HI, "outline.png"), 0, 0, PW, H)
    runs = json.load(open(os.path.join(HI, "outline.runs.json"), encoding="utf-8"))
    invisible_layer(c, runs, sc, H, 0.0)
    for sid, x0, y0, x1, y1 in meta["links"]:
        if sid in links_by_id:
            c.linkRect("", links_by_id[sid], (x0 * sc, H - y1 * sc, x1 * sc, H - y0 * sc), relative=0, thickness=0)
    c.showPage()


def key_blocks():
    names = [("maroon", "Frame bar, headlines, primary colour; Open and Close sections"), ("gold", "Gold rule under the headline, highlights, release chip outline"),
             ("golddark", "Tactics section colour; text on pale gold"), ("slate", "Situation and Strategy section colour"),
             ("teal", "Financials section colour; positive callouts"), ("purple", "Controls section colour"),
             ("gray", "Backup slides; neutral chart series"), ("warn", "Warning and negative callouts"), ("ink", "Body text"),
             ("muted", "Secondary text, sources line, unit labels"), ("line", "Rules and card outlines"), ("faint", "Header bands in timelines and calendars"),
             ("edge", "Image and table outlines"), ("mid", "Connector lines")]
    extra = [("#E8C85A", "Gold on maroon backgrounds; handover blocks in the run of show"), ("#F0D78C", "Light gold text on maroon"),
             ("#FFF8E1", "Pale-yellow annotation chips and release chips (gold outline)"), ("#F6F2EA", "Zebra rows in tables"),
             ("#E6E1D7", "Chart gridlines (zero line is #5A554C)")]
    colour_lines = ["%s  #%s  %s" % (n, hexof(n)[1:], use) for n, use in names] + ["tint  %s  %s" % (h_, u_) for h_, u_ in extra]
    return [
        ("Canvas and frame", [
            "Canvas 1920 x 1080 px (16:9). Maroon bar down the left edge, x 0 to 26, full height. Content margins x 80 to 1840.",
            "Top row (y 30 to 74): section chip (pill, 44 px high, white bold 24 px on the section colour) and status chip (NEW or RECAP: 36 px pill, bold 18 px in the section colour on a 14% tint). Page counter 'n / 12' right-aligned at x 1840 (24 px semibold, muted).",
            "Headline: bold 46 px maroon, up to two lines (shrinks to 30 px only if needed), box x 80 to 1840, y 94 to 232. Gold rule 180 x 6 px at y 240.",
            "Body area y 268 to 982. Footer: rule at y 1000 (#D8D2C6, 2 px); sources line 20 px muted at the left (width about 1180); footer navigation right-aligned at y 1030 in 20 px, the current section bold with a 4 px underline in its colour.",
            "The title slide (S1) has no frame: maroon panel x 0 to 780 with the title (white bold), subtitle (light gold) and a gold rule; team, supervisor and course on white from x 880.",
        ]),
        ("Colours (name, hex, use)", colour_lines),
        ("Section colours and accent order", [
            "S1, S2, S12 maroon; S3 and S4 slate; S5, S6, S7 gold-dark; S8 and S9 teal; S10 and S11 purple; backup pages grey.",
            "Cards, tiles and bars on S2, S5, S6, S7 and S12 rotate through: maroon, gold-dark, teal, slate, purple. Card fill is the accent colour at 93% tint towards white with a 2 px outline in the accent colour; KPI tiles are white with a 14 px accent bar on top. S3: SWOT cards teal (Strengths), orange (Weaknesses), slate (Opportunities), maroon (Threats). S4: three columns with maroon, gold-dark and slate header bands.",
        ]),
        ("Type and shapes", [
            "The comps use Segoe UI as a stand-in; use the 7 Sep deck's fonts. Whatever font you pick must render the baht sign (U+0E3F), the superscript 2 and the en dash.",
            "Sizes on the 1920 canvas: headline 46 bold; big KPI values 88 bold (one size across a row of tiles, shrunk to fit the longest); tile labels 32 bold; notes under tiles 25; bullets 26 to 31; table text 19 to 30 on core slides (14 to 17 on reference pages) with a bold header row; card titles 28 to 38 bold; chart labels 19 to 22; sources and navigation 20. Smallest body text on core slides is 18.",
            "Corner radii 14 to 20 px on cards, pills fully rounded; outlines 2 px (3 px on highlighted boxes).",
        ]),
        ("Charts (S8, S9)", [
            "Build as native, editable charts. Value above each column; where a value would sit on a dashed reference line it goes inside the column top in white. Reference lines are dashed, full plot width, with the value at the right end in the line colour (gold text uses gold-dark #855C00).",
            "Category notes are pale-yellow chips under the category label. When an axis does not start at zero (S9) the note 'Axis starts at X%' sits under the axis at the left. Series order and colours are listed in each slide's text block.",
        ]),
        ("Labels used on slides", [
            "[Proposed] marks team proposals; 'team assumption', 'team calculation', 'team assessment' mark our own figures; 'per CPN' marks figures reported by CPN. NEW means built for the final deck; RECAP means reworked from the 7 Sep deck.",
        ]),
    ]


def draw_key_page(c):
    blocks = key_blocks()
    items = [("title", 64, "Build key: frame, colours, type and chart rules")]
    h = 64 + 96
    colour_label_y = None
    for ttl, lines in blocks:
        items.append(("label", h, ttl))
        if ttl.startswith("Colours"):
            colour_label_y = h
        h += 56
        for ln in lines:
            wl = wrap(ln, "SegoeUI", 26, PW - 2 * M - 30 - (90 if ttl.startswith("Colours") else 0))
            items.append(("line", h, wl))
            h += len(wl) * 36 + 12
        h += 24
    H = h + 90
    c.setPageSize((PW, H))
    c.bookmarkPage("buildkey", fit="FitH", top=H)
    c.setFillColor(HexColor("#F4F0E8"))
    c.rect(0, 0, PW, H, fill=1, stroke=0)
    for kind, y, data in items:
        yy = H - y
        if kind == "title":
            c.setFillColor(col("maroon"))
            c.setFont("SegoeUI-Bold", 54)
            c.drawString(M, yy - 48, data)
        elif kind == "label":
            c.setFillColor(col("maroon"))
            c.setFont("SegoeUI-Bold", 34)
            c.drawString(M, yy - 32, data)
        else:
            c.setFillColor(col("ink"))
            c.setFont("SegoeUI", 26)
            yl = yy
            for ln in data:
                glyph_check(ln, "SegoeUI")
                c.drawString(M + 30, yl - 22, ln)
                yl -= 36
    # swatches for the 14 named colours, one per colour line
    if colour_label_y is not None:
        names = ["maroon", "gold", "golddark", "slate", "teal", "purple", "gray", "warn", "ink", "muted", "line", "faint", "edge", "mid", "#E8C85A", "#F0D78C", "#FFF8E1", "#F6F2EA", "#E6E1D7"]
        yy = H - (colour_label_y + 56)
        for n in names:
            c.setFillColor(col(n))
            c.setStrokeColor(col("edge"))
            c.rect(PW - M - 60, yy - 30, 60, 26, fill=1, stroke=1)
            yy -= 48
    back_link(c)
    c.showPage()


def main():
    core, back = [], []
    for p in sorted(glob.glob(os.path.join(ROOT, "specs", "slide_*.json"))):
        s = json.load(open(p, encoding="utf-8-sig"))
        (core if s["kind"] == "core" else back).append(s)
    core.sort(key=lambda s: s["n"])
    back.sort(key=lambda s: s["n"])
    keys = {s["id"]: "slide_" + s["id"] for s in core + back}
    c = canvas.Canvas(OUT, pagesize=(PW, 1080), pageCompression=1, initialFontName="SegoeUI", initialFontSize=12)
    c.setTitle("CPN marketing plan: final deck sketch, speaker notes and slide text")
    c.setSubject("Sketch of the 10-minute final presentation (12 core slides, 6 backup slides)")
    draw_outline_page(c, keys)
    c.addOutlineEntry("Outline and run of show", "outline", 0)
    draw_key_page(c)
    c.addOutlineEntry("Build key (colours, type, chart rules)", "buildkey", 0)
    c.addOutlineEntry("Core slides S1 to S12", "group_core", 0)
    for i, s in enumerate(core):
        c.addOutlineEntry("%s  %s" % (s["id"], s["title"]), keys[s["id"]], 1)
        draw_slide_page(c, s, keys[s["id"]], ("group_core",) if i == 0 else ())
    c.addOutlineEntry("Backup slides B1 to B6", "group_backup", 0)
    for i, s in enumerate(back):
        c.addOutlineEntry("%s  %s" % (s["id"], s["title"]), keys[s["id"]], 1)
        draw_slide_page(c, s, keys[s["id"]], ("group_backup",) if i == 0 else ())
    c.showOutline()
    c.save()
    print("pdf:", OUT, os.path.getsize(OUT), "bytes;", 2 + len(core) + len(back), "pages")
    if MISSING:
        print("MISSING GLYPHS:", {k: sorted(v)[:2] for k, v in MISSING.items()})


main()
