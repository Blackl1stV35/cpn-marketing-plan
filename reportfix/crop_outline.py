import fitz, sys
sys.stdout.reconfigure(encoding="utf-8")
pdf = fitz.open(sys.argv[1])
pg = pdf[0]
print("page rect", pg.rect)
clip = fitz.Rect(980, 2000, 1920, pg.rect.height)
pix = pg.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), clip=clip)
pix.save(sys.argv[2])
print("saved", pix.width, pix.height)
