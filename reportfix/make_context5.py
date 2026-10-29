"""Builds the reviewers' context files for the resolution round (gate G4, consent for 18-19 members, significance wording).

Usage: python -I make_context5.py REPORTFIX_DIR LIVE_DUMP.json DECK.pdf
Writes res_context_report.txt and res_context_deck.txt
"""
import sys

sys.path.insert(0, sys.argv[1])
import docparse  # noqa: E402
import fitz  # noqa: E402

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


out = ["REPORT TEXT NOW (Google Doc tab ch4ch5ch6_report, 29 Oct 2026). Table cells are one per line in reading order.", ""]


def emit(title, lo, hi):
    out.append("===== %s =====" % title)
    for p in ps[lo:hi]:
        t = p["text"].strip()
        if t:
            out.append(t)
    out.append("")


a = idx("[Proposed] Age bands, defined once for the plan")
b = idx("[Proposed] M5 tracker")
emit("SECTION 4.5 (age bands, baseline and precision, M5, PDPA, research table S1-S6)", a - 1, b + 12)
c = idx("M1 Gen Z and young-adult visits (ages 18 to 29)")
emit("TABLE 5.2 ROW C1 (model assumption behind objective M1)", c - 2, c + 6)
e = idx("At the base ratio the")
emit("CHAPTER 5 BREAK-EVEN TEXT (after Table 5.3)", e, e + 2)
g0 = idx("Table 6.2. Stage gates and budget release")
g1 = idx("Table 6.3 lists the KPIs")
emit("TABLE 6.2 STAGE GATES (G0-G4)", g0, g1 + 1)
k1 = idx("K1 Share of visitors aged 20 and over")
emit("TABLE 6.3 ROWS K1 AND K2", k1 - 1, k1 + 24)
k12 = idx("K12 Programme uplift and pass-through")
emit("TABLE 6.3 ROW K12", k12, k12 + 9)
k15 = idx("K15 PDPA readiness")
emit("TABLE 6.3 ROW K15", k15, k15 + 5)
r = [i for i, p in enumerate(ps) if "significance threshold at the Q4 wave" in p["text"]]
for i in r:
    emit("RISK REGISTER CELL (risk 10 trigger)", i, i + 1)
open(RF + r"\res_context_report.txt", "w", encoding="utf-8").write("\n".join(out))
print("report context chars:", len("\n".join(out)))

pdf = fitz.open(sys.argv[3])
pages = {1: "OUTLINE PAGE", 4: "S2", 10: "S8", 12: "S10", 19: "B5", 20: "B6"}
o2 = ["DECK TEXT NOW (sketch PDF pages; each slide page = comp text, then speaker notes and the 'Text on the slide' list)", ""]
for pno, label in pages.items():
    o2.append("===== PDF PAGE %d: %s =====" % (pno, label))
    o2.append(pdf[pno - 1].get_text())
open(RF + r"\res_context_deck.txt", "w", encoding="utf-8").write("\n".join(o2))
print("deck context chars:", len("\n".join(o2)))
