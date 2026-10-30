import re, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
TAB = {"A": "t.pu1p2hjsan6g", "B": "t.8nyhv8rr5vec", "X": "t.x1zy13a445a4"}
cache = {k: docparse.paragraphs(tabs[v]) for k, v in TAB.items()}

def show(label, rx, keys="ABX", limit=8, w=90):
    r = re.compile(rx)
    print("==", label)
    n = 0
    for k in keys:
        for p in cache[k]:
            m = r.search(p["text"])
            if m:
                n += 1
                if n <= limit:
                    a = max(0, m.start() - w); b = min(len(p["text"]), m.end() + w)
                    print("  %s[%d] %s" % (k, p["start"], p["text"][a:b].replace("\n", " ")))
    print("  matches:", n)

show("2025c/d/e refs and text", r"2025[cde]\b", limit=14, w=55)
show("Wikipedia", r"Wikipedia", limit=6, w=80)
show("areas", r"457,409|152,000|100,000 sq", limit=8, w=80)
show("5.3%", r"5\.3%", limit=6, w=110)
show("guidance", r"guidance", limit=6, w=70)
show("n.d.-d", r"n\.d\.-d", limit=6, w=60)
show("budget table refs", r"budget table|lines 1 to 11|lines 1–11", keys="B", limit=6, w=70)
show("Table 5.7 / payback / 226", r"Table 5\.7|7\.9|\b226\b|\b224\b", keys="B", limit=10, w=60)
print("== hotels with 11")
for k in "ABX":
    for p in cache[k]:
        if re.search(r"(?i)hotel", p["text"]) and re.search(r"\b11\b", p["text"]):
            i = re.search(r"\b11\b", p["text"]).start()
            print("  %s[%d] %s" % (k, p["start"], p["text"][max(0, i - 90):i + 90].replace("\n", " ")))
print("== headings (short paragraphs starting 3.x to 6.x)")
for k in "AB":
    for p in cache[k]:
        t = p["text"].strip()
        if re.match(r"^[3-6]\.\d", t) and len(t) < 90:
            print("  %s[%d] %s" % (k, p["start"], t))
