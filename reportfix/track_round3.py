import os, sys
sys.stdout.reconfigure(encoding="utf-8")
p = os.path.join(sys.argv[1], "reportfix", "review_loop.md")
STATUS = {
 1: "partial: keys agree now (2025c = Q3 results, 2025d = No.1, 2025e = LEAD); the two lists are not merged",
 2: "no change: 2025e is in both lists",
 4: "no change: report already says over 240; the 200 figure is in the frozen presented deck",
 5: "done: appendix malls growth set to High (matches the ~9% CAGR bullet)",
 6: "done: TRIS comparison on operating revenue: 2.0% above the top in FY2028E",
 8: "done: Section 2 reconciles 457,409 sq m (project size) with about 100,000 sq m NLA",
 10: "done: 4.6 Marketing Budget heading and Table 4.1 caption; budget reference now Table 4.1",
 12: "partial: Wikipedia removed (CPN release n.d.-h and One Report used); 2021 ownership date to check",
 13: "done: 11 properties dated FY2025 year-end, marked as team count (not cross-checked)",
 17: "no change: n.d.-d is CPN's emerging risk assessment; the 'The 1 loyalty' title is not in the report",
 18: "done (report appendix): 'close to a 35%' now 35.5% (team calculation)",
 19: "partial: Table 5.7 caption notes rounding; payback 7.9 and optimistic 226 need model inputs",
 21: "done: pricing strategies paragraph (4.2)",
 22: "done: Place as direct channel, selective coverage (4.3)",
 23: "done: four promotion tools (4.4)",
 24: "done: multi-attribute Table 4.2 (proposed weights; unknown ratings marked Not disclosed)",
 25: "done: product as a bundle (4.1)",
 26: "done: Table 4.3, terms beyond the list price (4.2)",
 27: "done: two marketing mixes declared at the start of Chapter 4",
 28: "done: headings 4.2 Price, 4.3 Place (distribution), 4.4 Promotion (marketing communications)",
 29: "done: five-stage tenant decision process (4.3), linked to 4.5",
 30: "done: M5 associative-memory sentence (4.5)",
 31: "done: segmentation bases (3.4)",
 32: "done: mass vs differentiated communication (4.4)",
}
lines = open(p, encoding="utf-8").read().split("\n")
out, n_upd = [], 0
for ln in lines:
    if ln.startswith("| ") and ln.count("|") >= 5:
        cells = ln.split("|")
        try:
            n = int(cells[1].strip())
        except ValueError:
            out.append(ln); continue
        if n in STATUS:
            cells[4] = " " + STATUS[n] + " "
            ln = "|".join(cells); n_upd += 1
    out.append(ln)
t = "\n".join(out)
old = "Scope now: deck outline and deck content only. Report and Google Doc changes wait for the weekly reset (Tue 3 Nov 2026, 1:00 PM)."
new = "Round 3 (30 Oct): report side applied to the live Google Doc (3 tabs); local mirrors not yet synced."
print("header replaced:", t.count(old) == 1)
t = t.replace(old, new)
t = t.rstrip("\n") + "\n\nRound 3 (30 Oct): 17 report points done, 3 no change needed, 3 partial (1, 12, 19). Mirrors and commit wait for your go.\n"
open(p, "w", encoding="utf-8", newline="").write(t)
print("rows updated:", n_upd)
