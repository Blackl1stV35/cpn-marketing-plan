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
    ('c = canvas.Canvas(OUT, pagesize=(PW, 1080), pageCompression=1)', 'c = canvas.Canvas(OUT, pagesize=(PW, 1080), pageCompression=1, initialFontName="SegoeUI", initialFontSize=12)'),
])
patch(d + "\\audit_pdf.py", [
    ('''links = doc[0].get_links()
dests = sorted(l.get("page", -1) + 1 for l in links if l.get("kind") == fitz.LINK_GOTO)''', '''def link_page(l):
    """1-based target page of an internal link (named or explicit), or None."""
    if l.get("kind") == fitz.LINK_GOTO:
        return int(l["page"]) + 1
    if l.get("kind") == fitz.LINK_NAMED and str(l.get("page", "")).isdigit():
        return int(l["page"])
    return None


links = doc[0].get_links()
dests = sorted(x for x in (link_page(l) for l in links) if x)'''),
    ('''    back_links = [l for l in doc[i].get_links() if l.get("kind") == fitz.LINK_GOTO and l.get("page") == 0]''', '''    back_links = [l for l in doc[i].get_links() if link_page(l) == 1]'''),
])
print("ok")
