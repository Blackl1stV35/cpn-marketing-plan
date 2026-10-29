import fitz, re, sys
sys.stdout.reconfigure(encoding="utf-8")
pdf = fitz.open(sys.argv[1])
txt = {}
for i, pg in enumerate(pdf, 1):
    txt[i] = pg.get_text()
open(sys.argv[2], "w", encoding="utf-8").write("\n\n=====PAGE=====\n".join(txt[i] for i in sorted(txt)))
pats = [r"report fix pending", r"still say 18", r"adults only", r"adults-only", r"aged 18", r"18 and over", r"log only", r"corrections\.md only", r"not in the (report'?s )?reference list",
        r"older 86\.7", r"roughly 30%", r"pending", r"22 million", r"1,500 adults", r"as corrected, except"]
for p in pats:
    hits = [(i, m.start()) for i in txt for m in re.finditer(p, re.sub(r"\s+", " ", txt[i]))]
    print("%-45s %s" % (p, hits[:6] if hits else "none"))
