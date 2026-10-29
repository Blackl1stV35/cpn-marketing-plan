import fitz, sys, os
pdf = sys.argv[1]; out = sys.argv[2]; pages = [int(x) for x in sys.argv[3].split(",")]; zoom = float(sys.argv[4])
os.makedirs(out, exist_ok=True)
doc = fitz.open(pdf)
print("pages", doc.page_count)
for i in range(doc.page_count):
    r = doc[i].rect
    print(i + 1, round(r.width), round(r.height), len(doc[i].get_text()), "chars of text", len(doc[i].get_links()), "links")
for p in pages:
    pix = doc[p - 1].get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    pix.save(os.path.join(out, "p%02d.png" % p))
print("toc", doc.get_toc()[:4])
