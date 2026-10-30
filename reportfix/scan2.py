import re, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
TAB = {"A": "t.pu1p2hjsan6g", "B": "t.8nyhv8rr5vec", "X": "t.x1zy13a445a4"}
C = {k: docparse.paragraphs(tabs[v]) for k, v in TAB.items()}
def find_start(k, s):
    for p in C[k]:
        if p["start"] == s:
            return p
    raise SystemExit("no paragraph at %s %d" % (k, s))
def cut(t, n):
    t = t.replace("\n", " ")
    return t if len(t) <= n else t[:n] + " ..."
print("== B 2025 citations and entries")
for p in C["B"]:
    if re.search(r"Central Pattana\. \(2025|Central Pattana, 2025[cde]", p["text"]):
        print("  B[%d-%d] %s" % (p["start"], p["end"], cut(p["text"], 150)))
print("== A[16204] and A[17259] full")
print("  A16204:", cut(find_start("A", 16204)["text"], 420))
print("  A17259:", cut(find_start("A", 17259)["text"], 620))
print("== B[55194] TRIS paragraph")
print("  ", cut(find_start("B", 55194)["text"], 700))
print("== Table 5.7 cells after heading")
idx = [i for i, p in enumerate(C["B"]) if p["start"] == 54463][0]
print("  ", " | ".join(cut(p["text"].strip(), 40) for p in C["B"][idx + 1: idx + 41] if p["text"].strip()))
print("== (Section 4.5) occurrences")
for k in "AB":
    for p in C[k]:
        for m in re.finditer(r"\(Section 4\.5\)", p["text"]):
            print("  %s[%d] %s" % (k, p["start"], cut(p["text"][max(0, m.start() - 80):m.end() + 10], 120)))
print("== X tab BCG malls row and 35% wording")
xs = C["X"]
for i, p in enumerate(xs):
    if p["text"].strip() == "Retail malls":
        print("  X idx", i, "start", p["start"], [(q["start"], q["end"], cut(q["text"].strip(), 30)) for q in xs[i:i + 4]])
        break
for p in xs:
    if "close to a 35%" in p["text"]:
        print("  X close-35 start", p["start"], "end", p["end"], "len", len(p["text"]))
print("== headings and paragraph before 4.1")
for p in C["B"]:
    if p["text"].strip() in ("4.1 Product", "4.2 Pricing", "4.3 Distribution (Place)", "4.4 Marketing Communications (Promotion)", "4.5 Marketing Research"):
        print("  head", p["start"], p["end"], p["text"].strip())
prev = [p for p in C["B"] if p["end"] <= 1131][-1]
print("  prev", prev["start"], prev["end"], cut(prev["text"], 140))
print("== budget paragraph and 3.4 next paragraph")
b = find_start("B", 30223)
print("  budget", b["start"], b["end"], cut(b["text"], 110))
a = [p for p in C["A"] if p["text"].strip() == "3.4 Target Markets"][0]
nxt = [p for p in C["A"] if p["start"] >= a["end"]][0]
print("  3.4 next", nxt["start"], nxt["end"], cut(nxt["text"], 120))
m5 = [p for p in C["B"] if "so M5 targets are set above that after wave 0" in p["text"]]
print("  M5 para count", len(m5), [ (p["start"], p["end"]) for p in m5])
