"""Validates one slide spec JSON against deck/src/SPEC.md.

Usage: python -I validate_spec.py FILE.json [FILE2.json ...]
Prints ERROR lines (must fix) and WARN lines (over a length limit or word budget).
"""
import json
import re
import sys

SECONDS = {1: 10, 2: 45, 3: 35, 4: 35, 5: 55, 6: 55, 7: 35, 8: 55, 9: 55, 10: 50, 11: 50, 12: 30}
PRES = {1: "P1", 2: "P1", 3: "P2", 4: "P2", 5: "P3", 6: "P3", 7: "P4", 8: "P4", 9: "P5", 10: "P5", 11: "P6", 12: "P6"}
LAYOUT_OF = {1: "title", 2: "kpi5", 3: "swot_issues", 4: "three_col", 5: "table_side", 6: "channels_calendar", 7: "research_kpis",
             8: "chart", 9: "chart", 10: "gantt_org", 11: "risk_matrix", 12: "takeaways"}


def run(path):
    errs, warns = [], []
    try:
        s = json.load(open(path, encoding="utf-8-sig"))
    except Exception as e:
        return ["cannot parse JSON: %s" % e], []

    def E(m):
        errs.append(m)

    def W(m):
        warns.append(m)

    def need(d, keys, where):
        for k in keys:
            if k not in d:
                E("%s: missing '%s'" % (where, k))

    def lim(v, n, where):
        if not isinstance(v, str):
            E("%s: expected a string, got %r" % (where, type(v).__name__))
        elif len(v) > n:
            W("%s: %d chars > %d: %s" % (where, len(v), n, v[:50]))

    need(s, ["n", "id", "kind", "layout", "title", "section", "status", "seconds", "presenter", "headline", "body", "sources", "facts"], "slide")
    if errs:
        return errs, warns
    n = s["n"]
    core = s["kind"] == "core"
    if core and n in SECONDS:
        if s["seconds"] != SECONDS[n]:
            E("seconds should be %d" % SECONDS[n])
        if s["presenter"] != PRES[n]:
            E("presenter should be %s" % PRES[n])
        if s["layout"] != LAYOUT_OF[n]:
            E("layout for slide %d should be %s" % (n, LAYOUT_OF[n]))
    if s["status"] not in ("NEW", "RECAP"):
        E("status must be NEW or RECAP")
    lim(s["title"], 32, "title")
    lim(s["section"], 34, "section")
    lim(s["headline"], 160, "headline")
    if len(s["sources"]) > 4:
        W("more than 4 sources")
    if not s["facts"]:
        E("facts is empty")
    for i, f in enumerate(s["facts"]):
        for k in ("on_slide", "meaning", "where"):
            if not f.get(k):
                E("facts[%d] missing %s" % (i, k))
    if core:
        words = len(re.findall(r"\S+", s.get("notes", "")))
        budget = s["seconds"] * 130 / 60.0
        if words == 0:
            E("notes missing")
        elif words > budget * 1.1:
            W("notes %d words > budget %.0f +10%%" % (words, budget))
        elif words < budget * 0.6:
            W("notes %d words < 60%% of budget %.0f" % (words, budget))
    b = s["body"]
    L = s["layout"]
    try:
        if L == "title":
            need(b, ["title", "subtitle", "team", "course", "instructor", "term"], "body")
            if len(b["team"]) != 6:
                E("team must list 6 names")
        elif L == "kpi5":
            need(b, ["tiles", "ask"], "body")
            if len(b["tiles"]) != 5:
                E("exactly 5 tiles")
            for i, t in enumerate(b["tiles"]):
                need(t, ["value", "label", "note"], "tile%d" % i)
                lim(t["value"], 9, "tile%d.value" % i)
                lim(t["label"], 30, "tile%d.label" % i)
                lim(t["note"], 46, "tile%d.note" % i)
            lim(b["ask"], 120, "ask")
        elif L == "swot_issues":
            need(b, ["swot", "issues"], "body")
            for q in "SWOT":
                items = b["swot"].get(q, [])
                if len(items) != 2:
                    E("swot %s needs 2 bullets" % q)
                for j, t in enumerate(items):
                    lim(t, 54, "swot.%s[%d]" % (q, j))
            if len(b["issues"]) != 3:
                E("exactly 3 issues")
            for i, t in enumerate(b["issues"]):
                need(t, ["title", "why"], "issue%d" % i)
                lim(t["title"], 34, "issue%d.title" % i)
                lim(t["why"], 72, "issue%d.why" % i)
        elif L == "three_col":
            need(b, ["cols"], "body")
            if len(b["cols"]) != 3:
                E("exactly 3 columns")
            for i, c in enumerate(b["cols"]):
                need(c, ["title", "bullets"], "col%d" % i)
                lim(c["title"], 24, "col%d.title" % i)
                if not 3 <= len(c["bullets"]) <= 4:
                    E("col%d needs 3 or 4 bullets" % i)
                for j, t in enumerate(c["bullets"]):
                    lim(t, 70, "col%d.bullet%d" % (i, j))
        elif L == "table_side":
            need(b, ["table", "side"], "body")
            t = b["table"]
            need(t, ["title", "cols", "rows", "widths"], "table")
            if not 3 <= len(t["rows"]) <= 5:
                E("table needs 3 to 5 rows")
            if len(t["cols"]) != len(t["widths"]) or abs(sum(t["widths"]) - 1) > 0.02:
                E("widths must match cols and sum to 1")
            for i, r in enumerate(t["rows"]):
                if len(r) != len(t["cols"]):
                    E("row %d has %d cells, expected %d" % (i, len(r), len(t["cols"])))
                for j, c in enumerate(r):
                    lim(c, 96, "row%d.cell%d" % (i, j))
            need(b["side"], ["title", "items"], "side")
            if not 2 <= len(b["side"]["items"]) <= 4:
                E("side needs 2 to 4 items")
        elif L == "channels_calendar":
            need(b, ["hub", "nodes", "calendar", "budget"], "body")
            if not 4 <= len(b["nodes"]) <= 5:
                E("4 or 5 nodes")
            need(b["calendar"], ["months", "bars"], "calendar")
            if not 3 <= len(b["calendar"]["bars"]) <= 5:
                E("3 to 5 bars")
            m = len(b["calendar"]["months"])
            for i, x in enumerate(b["calendar"]["bars"]):
                need(x, ["label", "start", "end"], "bar%d" % i)
                if not (0 <= x["start"] < x["end"] <= m):
                    E("bar%d start/end outside 0..%d" % (i, m))
        elif L == "research_kpis":
            need(b, ["methods", "kpis"], "body")
            if not 3 <= len(b["methods"]) <= 4:
                E("3 or 4 methods")
            if len(b["kpis"]) != 4:
                E("exactly 4 kpis")
            for i, k in enumerate(b["kpis"]):
                need(k, ["name", "baseline", "target", "tag"], "kpi%d" % i)
        elif L == "chart":
            need(b, ["charts", "callouts", "note"], "body")
            if not 1 <= len(b["charts"]) <= 2:
                E("1 or 2 charts")
            for ci, c in enumerate(b["charts"]):
                need(c, ["type", "title", "unit", "categories", "series"], "chart%d" % ci)
                if c["type"] not in ("bars", "stacked"):
                    E("chart%d type must be bars or stacked" % ci)
                for si, se in enumerate(c["series"]):
                    need(se, ["name", "values", "color"], "chart%d.series%d" % (ci, si))
                    if len(se["values"]) != len(c["categories"]):
                        E("chart%d.series%d has %d values for %d categories" % (ci, si, len(se["values"]), len(c["categories"])))
            if not 2 <= len(b["callouts"]) <= 3:
                E("2 or 3 callouts")
            lim(b["note"], 130, "note")
        elif L == "gantt_org":
            need(b, ["months", "rows", "gates", "org"], "body")
            if not 4 <= len(b["rows"]) <= 6:
                E("4 to 6 rows")
            if not 3 <= len(b["gates"]) <= 5:
                E("3 to 5 gates")
            need(b["org"], ["top", "units"], "org")
            if not 3 <= len(b["org"]["units"]) <= 5:
                E("3 to 5 org units")
        elif L == "risk_matrix":
            need(b, ["risks", "top", "worst"], "body")
            if not 6 <= len(b["risks"]) <= 10:
                E("6 to 10 risks")
            if len(b["top"]) != 3:
                E("exactly 3 top risks")
            need(b["worst"], ["title", "text", "numbers"], "worst")
        elif L == "takeaways":
            need(b, ["cards", "closing"], "body")
            if len(b["cards"]) != 3:
                E("exactly 3 cards")
        elif L == "blocks":
            need(b, ["columns"], "body")
            if not 1 <= len(b["columns"]) <= 2:
                E("1 or 2 columns")
            for ci, col in enumerate(b["columns"]):
                for bi, bl in enumerate(col):
                    if bl.get("type") not in ("table", "bullets", "cards", "text", "kpis"):
                        E("column %d block %d has unknown type %r" % (ci, bi, bl.get("type")))
        else:
            E("unknown layout %r" % L)
    except (KeyError, TypeError, AttributeError) as e:
        E("structure problem: %r" % e)
    return errs, warns


code = 0
for p in sys.argv[1:]:
    errs, warns = run(p)
    print("%s: %d error(s), %d warning(s)" % (p.split("\\")[-1], len(errs), len(warns)))
    for e in errs:
        print("  ERROR", e)
        code = 1
    for w in warns:
        print("  WARN ", w)
sys.exit(code)
