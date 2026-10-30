import re, sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
A = docparse.paragraphs(tabs["t.pu1p2hjsan6g"]); B = docparse.paragraphs(tabs["t.8nyhv8rr5vec"]); X = docparse.paragraphs(tabs["t.x1zy13a445a4"])
def one(lst, pred, label):
    hits = [p for p in lst if pred(p["text"])]
    for p in hits[:3]:
        print(label, p["start"], p["end"], repr(p["text"][:70]))
    if not hits: print(label, "NONE")
one(A, lambda t: t.strip() == "3.4 Target Markets" and True, "A 3.4 heading")
one(A, lambda t: t.startswith("Wikipedia. (2026)"), "A wiki entry")
one(A, lambda t: t.startswith("Central Pattana. (2024a)"), "A 2024a entry")
one(A, lambda t: t.startswith("Restating the Market Summary"), "A 3.4 body")
one(X, lambda t: "close to a 35%" in t, "X close35")
one(X, lambda t: "11 properties, mostly Centara" in t, "X 11 props")
for p in X:
    if "close to a 35%" in p["text"]:
        i = p["text"].index("close to a 35%")
        print("X ctx:", repr(p["text"][max(0, i - 40): i + 40]))
    if "11 properties, mostly" in p["text"]:
        i = p["text"].index("11 properties, mostly")
        print("X ctx2:", repr(p["text"][max(0, i - 30): i + 45]))
