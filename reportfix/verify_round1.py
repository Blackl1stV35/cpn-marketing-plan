import fitz, re, sys
sys.stdout.reconfigure(encoding="utf-8")
pdf = fitz.open(sys.argv[1])
text = " ".join(re.sub(r"\s+", " ", pg.get_text()) for pg in pdf)
for needle in ("assumes a foreign visit earns the same as a Thai visit", "Re-checked 30 Oct 2026 (32 points)", "report points open", "NO PROBLEMS"):
    print("%-62s %s" % (needle, "found" if needle in text else "MISSING"))
print("pages:", len(pdf))
