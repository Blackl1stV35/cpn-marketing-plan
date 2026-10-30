import re, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
print("revision", d["revisionId"][:20])
TAB = {"A": "t.pu1p2hjsan6g", "B": "t.8nyhv8rr5vec", "X": "t.x1zy13a445a4"}
C = {k: docparse.paragraphs(tabs[v]) for k, v in TAB.items()}
def count(k, s): return sum(p["text"].count(s) for p in C[k])
checks = [
 ("B", "4.2 Price\n", 1), ("B", "4.3 Place (distribution)", 1), ("B", "4.4 Promotion (marketing communications)", 1),
 ("B", "4.6 Marketing Budget", 1), ("B", "Table 4.1. FY2027 marketing budget", 1), ("B", "Gross ceiling, lines 1 to 11 (Table 4.1)", 1),
 ("B", "Table 4.2. Tenant choice", 1), ("B", "Table 4.3. Terms beyond the list price", 1),
 ("B", "A tenant's choice of mall runs in five stages", 1), ("B", "Leasing space is a direct channel", 1),
 ("B", "A CPN product is a bundle", 1), ("B", "Promotion uses four tools", 1), ("B", "Mass communication builds awareness", 1),
 ("B", "Pricing combines two bases", 1), ("B", "This chapter uses two marketing mixes", 1),
 ("B", "and 2.0% above its top in FY2028E on TRIS's basis", 1), ("B", "5.3% above", 0),
 ("B", "components are rounded and may not add exactly", 1), ("B", "unaided question tests associative memory", 1),
 ("A", "Central Pattana. (n.d.-h).", 1), ("A", "Segments are defined on three bases", 1),
 ("A", "The two areas are on different bases", 1), ("A", "branded as Market Place", 1),
 ("A", "Wikipedia", 0), ("A", "Central Pattana, n.d.-h", 1),
 ("X", "Retail malls", 1), ("X", "close to a 35%", 0), ("X", "a 35.5% net margin (team calculation)", 1),
 ("X", "11 properties at FY2025 year-end (team count)", 1), ("X", "Moderate–High", 1),
]
bad = []
for k, s, want in checks:
    n = count(k, s)
    flag = "ok " if n == want else "BAD"
    if n != want: bad.append((k, s[:40], n, want))
    print("%s %s x%d (want %d): %s" % (flag, k, n, want, s[:60]))
# style of the new heading and the new caption
for p in C["B"]:
    if p["text"].strip() == "4.6 Marketing Budget":
        print("4.6 heading start", p["start"], "runs", len(p["runs"]), "style", p["style"])
# new table row counts
for name in ("Table 4.2. Tenant choice", "Table 4.3. Terms beyond"):
    i = [j for j, p in enumerate(C["B"]) if p["text"].startswith(name)][0]
    print(name[:9], "next cell text:", repr(C["B"][i + 1]["text"][:20]), "| cell 2 text:", repr(C["B"][i + 2]["text"][:20]))
print("BAD:", bad if bad else "none")
