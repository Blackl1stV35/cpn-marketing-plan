import fitz, sys
pdf = fitz.open(sys.argv[1])
pg = pdf[0]
print("page rect", pg.rect)
pix = pg.get_pixmap(matrix=fitz.Matrix(0.6, 0.6))
pix.save(sys.argv[2])
pix = pg.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), clip=fitz.Rect(980, 2050, 1920, pg.rect.height))
pix.save(sys.argv[3])
