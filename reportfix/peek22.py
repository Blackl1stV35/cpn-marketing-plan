import fitz, re, sys
sys.stdout.reconfigure(encoding="utf-8")
pdf = fitz.open(sys.argv[1])
t = re.sub(r"\s+", " ", pdf[18].get_text())
for m in re.finditer(r"22 million", t):
    print("p19:", t[max(0, m.start() - 90): m.end() + 60])
