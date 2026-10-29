"""Deterministic audit of the sketch PDF against the slide specs and the saved text runs.

Usage: python -I audit_pdf.py PDF [--json]
Prints PROBLEM lines (must fix) and INFO lines. Exit code 1 if any PROBLEM.
"""
import glob
import json
import os
import re
import sys

import fitz
from pypdf import PdfReader

ROOT = os.path.dirname(os.path.abspath(__file__))
pdf = sys.argv[1]
problems, info = [], []


def P(m):
    problems.append(m)


def norm(t):
    t = t.replace(" ", " ")
    t = re.sub(r"\s+", " ", t)
    return t.strip()


specs = []
for p in sorted(glob.glob(os.path.join(ROOT, "specs", "slide_*.json"))):
    specs.append(json.load(open(p, encoding="utf-8-sig")))
core = sorted([s for s in specs if s["kind"] == "core"], key=lambda s: s["n"])
back = sorted([s for s in specs if s["kind"] != "core"], key=lambda s: s["n"])
order = core + back

doc = fitz.open(pdf)
reader = PdfReader(pdf, strict=True)
if doc.page_count != 2 + len(order):
    P("page count %d, expected %d" % (doc.page_count, 2 + len(order)))
info.append("pages %d; file %.1f MB" % (doc.page_count, os.path.getsize(pdf) / 1048576.0))

# ---- structure: sizes, images, fonts, links, bookmarks
for i in range(doc.page_count):
    pg = doc[i]
    if round(pg.rect.width) != 1920:
        P("page %d width %s, expected 1920" % (i + 1, pg.rect.width))
    imgs = pg.get_images(full=True)
    if i == 1:
        continue
    if len(imgs) != 1:
        P("page %d has %d images, expected 1" % (i + 1, len(imgs)))
    else:
        w, h = imgs[0][2], imgs[0][3]
        need = 4800 if i == 0 else 3840
        if w < need:
            P("page %d image only %dx%d (hi-res expected %d wide)" % (i + 1, w, h, need))
    fonts = pg.get_fonts(full=True)
    for f in fonts:
        if not f[1] or f[1] in ("n/a",):
            P("page %d font %s not embedded" % (i + 1, f[3]))
toc = doc.get_toc()
want = 1 + 1 + 1 + len(core) + 1 + len(back)
if len(toc) != want:
    P("bookmark count %d, expected %d" % (len(toc), want))
for lvl, title, pno in toc:
    if pno < 1 or pno > doc.page_count:
        P("bookmark %r points to page %s" % (title, pno))
def link_page(l):
    """1-based target page of an internal link (named or explicit), or None."""
    if l.get("kind") == fitz.LINK_GOTO:
        return int(l["page"]) + 1
    if l.get("kind") == fitz.LINK_NAMED and str(l.get("page", "")).isdigit():
        return int(l["page"])
    return None


links = doc[0].get_links()
dests = sorted(x for x in (link_page(l) for l in links) if x)
want_dests = list(range(3, doc.page_count + 1))
if dests != want_dests:
    P("outline links go to pages %s, expected %s" % (dests, want_dests))
info.append("bookmarks %d; outline links %d" % (len(toc), len(links)))
for i in range(1, doc.page_count):
    back_links = [l for l in doc[i].get_links() if link_page(l) == 1]
    if len(back_links) != 1:
        P("page %d has %d back-to-outline links, expected 1" % (i + 1, len(back_links)))
try:
    n_pages = len(reader.pages)
    info.append("pypdf strict read ok; %d pages; %d outline items" % (n_pages, len(reader.outline)))
except Exception as e:  # noqa: BLE001
    P("pypdf strict read failed: %r" % (e,))

# ---- text layer vs saved runs, notes and spec strings
SKIP_KEYS = {"color", "kind", "type", "tone", "likelihood", "impact", "layout", "start", "end", "at", "n", "id", "category", "series", "values", "widths", "ymin", "ymax"}


def strings(o, key=None):
    out = []
    if isinstance(o, str):
        if key not in SKIP_KEYS and len(o.strip()) >= 3:
            out.append(o)
    elif isinstance(o, dict):
        for k, v in o.items():
            out += strings(v, k)
    elif isinstance(o, list):
        for v in o:
            out += strings(v, key)
    return out


for idx, s in enumerate(order):
    pn = idx + 3
    page_text = norm(doc[pn - 1].get_text())
    runs = json.load(open(os.path.join(ROOT, "comps_hi", "%s.runs.json" % s["id"]), encoding="utf-8"))
    joined = norm(" ".join(r[2] for r in runs))
    # every drawn run is present in the PDF text layer
    miss_runs = [r[2] for r in runs if len(norm(r[2])) >= 3 and norm(r[2]) not in page_text]
    if miss_runs:
        P("%s (p%d): %d drawn text runs missing from the PDF text layer, e.g. %r" % (s["id"], pn, len(miss_runs), miss_runs[:3]))
    # every spec string is drawn on the comp
    wanted = ([] if s["layout"] == "title" else [s["headline"]]) + strings(s["body"]) + list(s["sources"])
    miss_spec = []
    for w in wanted:
        nw = norm(w)
        if nw and nw not in joined:
            miss_spec.append(nw[:70])
    if miss_spec:
        P("%s (p%d): %d spec strings not drawn on the comp, e.g. %r" % (s["id"], pn, len(miss_spec), miss_spec[:4]))
    # notes present on the page
    notes = norm(s.get("notes", ""))
    if s["kind"] == "core" and notes and notes not in page_text:
        P("%s (p%d): speaker notes not found as one block in the PDF text" % (s["id"], pn))
    if s["kind"] == "core" and not notes:
        P("%s: no speaker notes" % s["id"])
    # header facts
    if s["id"] not in page_text:
        P("%s (p%d): slide id not on page" % (s["id"], pn))
    bad = re.findall(r"[□�]|\?\?", page_text)
    if bad:
        P("%s (p%d): suspicious glyphs in text: %r" % (s["id"], pn, bad[:3]))

# ---- run of show arithmetic
tot = sum(s["seconds"] for s in core)
if tot != 510:
    P("core seconds sum to %d, expected 510" % tot)
words = sum(len(re.findall(r"\S+", s.get("notes", ""))) for s in core)
info.append("core seconds %d (8:30 expected 510); notes words %d" % (tot, words))
for s in core:
    w = len(re.findall(r"\S+", s["notes"]))
    budget = s["seconds"] * 130 / 60.0
    if w > budget * 1.1 or w < budget * 0.6:
        P("%s notes %d words vs budget %.0f" % (s["id"], w, budget))

# ---- outline page text
t0 = norm(doc[0].get_text())
for s in order:
    if norm(s["headline"]) not in t0:
        P("outline page missing headline of %s" % s["id"])
    if norm(s["title"]) not in t0:
        P("outline page missing title of %s" % s["id"])

print("\n".join("INFO " + x for x in info))
print("\n".join("PROBLEM " + x for x in problems) if problems else "NO PROBLEMS")
if "--json" in sys.argv:
    print(json.dumps({"problems": problems, "info": info}))
sys.exit(1 if problems else 0)
