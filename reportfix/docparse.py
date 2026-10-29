"""Helpers to read a saved Google Docs read_doc dump: tabs, paragraphs with indices, text search.

Usage:
  python -I docparse.py DUMP.json tabs
  python -I docparse.py DUMP.json find TABID "substring" [more substrings...]
  python -I docparse.py DUMP.json refs TABID            (reference paragraphs with start indices)
"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")


def load(path):
    t = open(path, encoding="utf-8").read()
    return json.loads(t[t.find("{"):])["content"]


def walk_tabs(tabs, out=None):
    out = out if out is not None else []
    for tb in tabs:
        out.append(tb)
        walk_tabs(tb.get("childTabs", []), out)
    return out


def paragraphs(tab):
    """List of dicts: start, end, text, style (namedStyleType), indent info."""
    res = []
    body = tab["documentTab"]["body"]["content"]

    def para(el):
        p = el["paragraph"]
        text = "".join(e.get("textRun", {}).get("content", "") for e in p.get("elements", []))
        st = p.get("paragraphStyle", {})
        res.append({"start": el["startIndex"], "end": el["endIndex"], "text": text, "style": st.get("namedStyleType"),
                    "indentStart": st.get("indentStart", {}).get("magnitude"), "indentFirst": st.get("indentFirstLine", {}).get("magnitude"),
                    "runs": [(e["startIndex"], e["endIndex"], e["textRun"].get("textStyle", {})) for e in p.get("elements", []) if "textRun" in e]})

    def rec(content):
        for el in content:
            if "paragraph" in el:
                para(el)
            elif "table" in el:
                for row in el["table"]["tableRows"]:
                    for cell in row["tableCells"]:
                        rec(cell["content"])

    rec(body)
    return res


if __name__ == "__main__":
    d = load(sys.argv[1])
    tabs = walk_tabs(d["tabs"])
    cmd = sys.argv[2]
    if cmd == "tabs":
        print("title:", d["title"], "revision:", d["revisionId"])
        for tb in tabs:
            pr = tb["tabProperties"]
            ps = paragraphs(tb)
            print(pr["tabId"], "|", pr.get("title"), "| paragraphs", len(ps), "| last end", ps[-1]["end"] if ps else None)
    else:
        tab = [tb for tb in tabs if tb["tabProperties"]["tabId"] == sys.argv[3]][0]
        ps = paragraphs(tab)
        if cmd == "find":
            for sub in sys.argv[4:]:
                hits = [p for p in ps if sub in p["text"]]
                print("== %r: %d paragraph(s)" % (sub, len(hits)))
                for p in hits:
                    i = p["text"].index(sub)
                    print("   [%d-%d] style=%s ...%s..." % (p["start"], p["end"], p["style"], p["text"][max(0, i - 80):i + len(sub) + 80].replace("\n", "\\n")))
        elif cmd == "refs":
            on = False
            for p in ps:
                if p["text"].strip() == "References":
                    on = True
                    print("HEADING at", p["start"], p["style"])
                    continue
                if on and p["text"].strip():
                    print("[%d-%d] indS=%s indF=%s %s" % (p["start"], p["end"], p["indentStart"], p["indentFirst"], p["text"].strip()[:140]))
