"""Counts the merged reference list (live tab B) by author type, n.d. keys and Retrieved entries.

Usage: python -I count_refs.py DUMP.json
"""
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docparse  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
TAB_B = "t.8nyhv8rr5vec"
d = docparse.load(sys.argv[1])
tabs = {t["tabProperties"]["tabId"]: t for t in docparse.walk_tabs(d["tabs"])}
pb = docparse.paragraphs(tabs[TAB_B])
hb = [i for i, p in enumerate(pb) if p["text"].strip() == "References"][-1]
entries = [p["text"].strip() for p in pb[hb + 2:] if p["text"].strip()]

CATS = [
    ("CPN group", lambda a: a.startswith("Central Pattana") or a == "CPNREIT"),
    ("Central Group and The 1", lambda a: a.startswith(("Central Group", "Central Retail", "The1"))),
    ("Official and legal", lambda a: a.startswith(("Bank of Thailand", "Government Public Relations", "Personal Data Protection",
                                                    "Revenue Department", "National Statistical Office", "Tourism Authority"))),
    ("Advisers, raters, research", lambda a: a.startswith(("Accenture", "CBRE", "Cushman", "DataReportal", "JLL", "KPMG",
                                                           "PS Global", "S&P Global", "Standard Insights", "TRIS Rating", "Tilleke"))),
]
cat_count, news, unmatched = Counter(), Counter(), []
for e in entries:
    author = re.match(r"^(.*?)\.?\s*\(", e).group(1).strip()
    for name, test in CATS:
        if test(author):
            cat_count[name] += 1
            break
    else:
        cat_count["News and media"] += 1
        news[author] += 1
        if author not in ("Bangkok Post", "Bloomberg", "GlobeNewswire", "Inside Retail Asia", "Nation Thailand", "Nikkei Asia",
                          "Thai Examiner", "Thai Publica", "ThaiPR.net", "The Nation", "The Story Thailand", "The Thaiger"):
            unmatched.append(author)
print("entries:", len(entries))
for name, _ in CATS + [("News and media", None)]:
    print("  %-28s %d" % (name, cat_count[name]))
print("news by author:", dict(news))
print("unmatched news authors:", unmatched or "none")
print("n.d. keys:", sum(1 for e in entries if re.search(r"\(n\.d\.-", e)))
print("entries with Retrieved:", sum(1 for e in entries if "Retrieved" in e))
print("Nation Thailand:", sum(1 for e in entries if e.startswith("Nation Thailand.")))
