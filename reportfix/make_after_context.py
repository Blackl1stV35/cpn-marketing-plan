import re, sys
sys.path.insert(0, sys.argv[1])
import docparse
import fitz
sys.stdout.reconfigure(encoding="utf-8")
RF = sys.argv[1]
d = docparse.load(sys.argv[2])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
ps = docparse.paragraphs(tabs["t.8nyhv8rr5vec"])
def idx(prefix, start=0):
    for i in range(start, len(ps)):
        if ps[i]["text"].strip().startswith(prefix):
            return i
    raise SystemExit("anchor not found: " + prefix)
out = []
def emit(title, lo, hi):
    out.append("===== %s =====" % title)
    for p in ps[lo:hi]:
        t = p["text"].strip()
        if t:
            out.append(t)
    out.append("")
out.append("REPORT TEXT AFTER THE CHANGE (Google Doc tab ch4ch5ch6_report, 29 Oct 2026). Table cells are one per line in reading order.")
out.append("")
a = idx("[Proposed] Age bands, defined once for the plan")
b = idx("[Proposed] M5 tracker")  # end of the S1-S6 table region is a few cells later
emit("SECTION 4.5 (age bands, baseline paragraph, PDPA paragraph, research table S1-S6)", a - 1, b + 12)
c = idx("M1 Gen Z and young-adult visits (ages 18 to 29)")
emit("TABLE 5.2 ROW C1 (model assumption behind objective M1)", c - 2, c + 6)
k1 = idx("K1 Share of visitors aged 20 and over")
emit("TABLE 6.3 ROWS K1 AND K2", k1 - 1, k1 + 24)
r = [i for i, p in enumerate(ps) if "surveys limited to respondents aged 20 and over" in p["text"]]
for i in r:
    emit("RISK TABLE CELL (Chapter 6) around paragraph %d" % i, i, i + 1)
open(RF + r"\band_after_context.txt", "w", encoding="utf-8").write("\n".join(out))
print("report context chars:", len("\n".join(out)))

pdf = fitz.open(sys.argv[3])
pages = {1: "OUTLINE PAGE", 4: "S2", 6: "S4", 9: "S7", 18: "B4", 20: "B6"}
o2 = ["DECK TEXT AFTER THE CHANGE (sketch PDF pages; each slide page = comp text, then speaker notes and the 'Text on the slide' list)", ""]
for pno, label in pages.items():
    o2.append("===== PDF PAGE %d: %s =====" % (pno, label))
    o2.append(pdf[pno - 1].get_text())
open(RF + r"\band_after_deck.txt", "w", encoding="utf-8").write("\n".join(o2))
print("deck context chars:", len("\n".join(o2)))
