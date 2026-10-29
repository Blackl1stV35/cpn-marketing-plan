import sys
import fitz
src, dst = sys.argv[1], sys.argv[2]
doc = fitz.open(src)
out = []
for i, page in enumerate(doc, 1):
    out.append("\n=====PAGE %d=====\n" % i + page.get_text())
open(dst, "w", encoding="utf-8").write("".join(out))
print("pages", len(doc), "chars", sum(len(x) for x in out))
