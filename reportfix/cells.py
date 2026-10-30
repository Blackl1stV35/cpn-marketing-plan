import sys
sys.path.insert(0, sys.argv[1])
import docparse
sys.stdout.reconfigure(encoding="utf-8")
d = docparse.load(sys.argv[2])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
B = docparse.paragraphs(tabs["t.8nyhv8rr5vec"])
print("revision", d["revisionId"][:20])
def cells_after(prefix, n):
    k = [i for i, p in enumerate(B) if p["text"].startswith(prefix)]
    assert len(k) == 1, (prefix, len(k))
    i = k[0]
    print(prefix[:20], "caption", B[i]["start"], "| next 3:", [(B[j]["start"], B[j]["text"].strip()[:18]) for j in range(i + 1, i + 4)])
    cells = [B[j] for j in range(i + 1, i + 1 + n)]
    after = B[i + 1 + n]
    print("   cells", n, "first", cells[0]["start"], "last", cells[-1]["start"], "| after:", after["start"], after["text"].strip()[:30])
    return cells
c42 = cells_after("Table 4.2. Tenant choice", 30)
c43 = cells_after("Table 4.3. Terms beyond", 27)
import json
json.dump({"t42": [c["start"] for c in c42], "t43": [c["start"] for c in c43]}, open(sys.argv[3], "w"))
