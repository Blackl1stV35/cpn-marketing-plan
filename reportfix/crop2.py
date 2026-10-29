import fitz, sys
pdf = fitz.open(sys.argv[1])
pg = pdf[0]
pix = pg.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), clip=fitz.Rect(980, 2000, 1920, pg.rect.height))
pix.save(sys.argv[2])
pg = pdf[19]
pix = pg.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), clip=fitz.Rect(0, 850, 1920, 1080))
pix.save(sys.argv[3])
