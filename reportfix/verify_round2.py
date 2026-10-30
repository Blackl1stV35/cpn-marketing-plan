import fitz, re, sys
sys.stdout.reconfigure(encoding="utf-8")
pdf = fitz.open(sys.argv[1])
text = re.sub(r"\s+", "", "".join(pg.get_text() for pg in pdf))
needles = ["Plan-team time is not in these 11 lines", "assumes a foreign visit earns the same as a Thai visit", "Re-checked 30 Oct 2026 (32 points)"]
missing = [n for n in needles if re.sub(r"\s+", "", n) not in text]
print("pages", len(pdf), "| missing:", missing if missing else "none")
