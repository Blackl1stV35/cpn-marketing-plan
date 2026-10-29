# Slide spec format (one JSON file per slide)

Files: `deck\specs\slide_01.json` ... `slide_12.json` for the core deck, `slide_B1.json` ... `slide_B6.json` for the backup slides.
Slides are drawn by a renderer at 1920 x 1080, so every text field has a length limit. Validate with
`python -I deck\validate_spec.py FILE.json` before you finish.

## Common fields (every slide)

```json
{
  "n": 5,                       // 1-12 for core slides; for backup use 13-18 (B1=13 ... B6=18)
  "id": "S5",                   // S1..S12 or B1..B6
  "kind": "core",               // "core" or "backup"
  "layout": "table_side",       // one of the layouts below
  "title": "Product + pricing", // short label for the outline, at most 32 characters
  "section": "4.1-4.2 · Marketing tactics",   // tag, at most 34 characters
  "status": "NEW",              // "NEW" or "RECAP" (RECAP = reworked from the 7 Sep deck)
  "seconds": 55,                // speaking time; see the time table
  "presenter": "P3",            // P1..P6
  "headline": "One full sentence carrying the key number and the so-what.",   // at most 160 characters
  "body": { },                  // layout-specific, see below
  "notes": "Speaker notes in plain spoken English.",   // core slides only; word budget = seconds x 2.17, +/-10%
  "sources": ["Central Pattana, 2026g, p. 7"],  // short citations exactly as keyed in the report, at most 4; "team calculation" allowed
  "facts": [ { "on_slide": "฿2,760 million", "meaning": "...", "where": "ch4.md budget table, total row", "cite": "Central Pattana, 2026a; team calculation" } ]
}
```

`facts` lists EVERY number, date and named claim that appears on the slide (headline, body, notes) with where it is in the final
chapters (file plus section, table or row ID). A number that is not in the report may not be on a slide.

Time table (core): S1 10 s, S2 45, S3 35, S4 35, S5 55, S6 55, S7 35, S8 55, S9 55, S10 50, S11 50, S12 30 (total 510 s).
Presenter blocks: S1-S2 P1, S3-S4 P2, S5-S6 P3, S7-S8 P4, S9-S10 P5, S11-S12 P6.

## Layouts and their `body`

All strings are plain text; keep within the limits (the renderer shrinks text, but overflow is a defect).

### title (S1)
`{"title": "Marketing Plan of Central Pattana Public Company Limited", "subtitle": "Final presentation: Sections 1 to 6", "team": ["name", ... 6 names], "course": "Marketing Business Economics (01101423)", "instructor": "Assoc. Prof. Mana Luksamee-arunothai, Ph.D.", "term": "Faculty of Economics, Kasetsart University · Semester 1, Academic Year 2026"}`

### kpi5 (S2)
`{"tiles": [{"value": "≤ 9 chars", "label": "≤ 30 chars", "note": "≤ 46 chars"}, ... exactly 5], "ask": "bottom banner, at most 120 chars"}`

### swot_issues (S3)
`{"swot": {"S": ["≤ 54 chars", "..."], "W": [...], "O": [...], "T": [...]}, "issues": [{"title": "≤ 34 chars", "why": "≤ 72 chars"}, ... exactly 3]}`  (2 bullets per SWOT cell)

### three_col (S4)
`{"cols": [{"title": "≤ 24 chars", "bullets": ["≤ 70 chars", ... 3 or 4], "big": {"value": "≤ 8 chars", "label": "≤ 28 chars"}}, ... exactly 3]}`  (`big` optional)

### table_side (S5)
`{"table": {"title": "≤ 40 chars", "cols": ["ID", "Tactic", "Objective", "Timing"], "rows": [["P1", "≤ 96 chars", "M1", "Q1"], ... 3 to 5 rows], "widths": [0.08, 0.56, 0.16, 0.20]}, "side": {"title": "≤ 28 chars", "items": [{"value": "≤ 9 chars", "label": "≤ 40 chars"}, ... 2 to 4]}}`

### channels_calendar (S6)
`{"hub": "CPN", "nodes": [{"name": "≤ 22 chars", "note": "≤ 44 chars"}, ... 4 or 5], "calendar": {"months": ["Q1","Q2","Q3","Q4"] or 12 month letters, "bars": [{"label": "≤ 30 chars", "start": 0, "end": 3, "note": "≤ 20 chars"}, ... 3 to 5]}, "budget": {"value": "≤ 9 chars", "label": "≤ 44 chars"}}`  (`start` and `end` are positions on the month list, end exclusive)

### research_kpis (S7)
`{"methods": [{"name": "≤ 26 chars", "what": "≤ 64 chars", "when": "≤ 22 chars"}, ... 3 or 4], "kpis": [{"name": "≤ 28 chars", "baseline": "≤ 22 chars", "target": "≤ 22 chars", "tag": "M1"}, ... exactly 4]}`

### chart (S8, S9)
```json
{"charts": [ {"type": "bars", "title": "≤ 46 chars", "unit": "THB million", "categories": ["FY2026E", "FY2027E"],
              "series": [ {"name": "Base", "values": [0, 328], "color": "maroon", "kind": "bar"},
                          {"name": "Break-even", "values": [400, 400], "color": "gray", "kind": "line"} ],
              "annotations": [ {"text": "≤ 40 chars", "category": 1, "series": 0} ] }, ... 1 or 2 charts ],
 "callouts": [ {"value": "≤ 9 chars", "label": "≤ 44 chars", "tone": "good"|"warn"|"neutral"}, ... 2 or 3 ],
 "note": "one-line reading of the charts, at most 130 chars"}
```
`type` is "bars" (grouped bars, with optional line series) or "stacked". Colors: maroon, gold, slate, teal, gray. Up to 4 series and 8 categories per chart. Values are numbers.

### gantt_org (S10)
`{"months": ["Q4 26","Q1 27","Q2 27","Q3 27","Q4 27"], "rows": [{"label": "≤ 30 chars", "start": 0.0, "end": 1.0, "tone": "maroon"|"gold"|"slate"|"teal"}, ... 4 to 6], "gates": [{"label": "G0 15 Dec 2026", "at": 0.4, "release": "≤ 22 chars"}, ... 3 to 5], "org": {"top": "≤ 30 chars", "units": [{"name": "≤ 26 chars", "role": "≤ 40 chars"}, ... 3 to 5]}}`  (`start`, `end`, `at` are positions along the months axis, 0 to the number of months)

### risk_matrix (S11)
`{"risks": [{"id": 1, "name": "≤ 34 chars", "likelihood": "H"|"M"|"L", "impact": "H"|"M"|"L"}, ... 6 to 10], "top": [{"risk": "≤ 34 chars", "trigger": "≤ 60 chars", "response": "≤ 60 chars"}, ... exactly 3], "worst": {"title": "≤ 34 chars", "text": "≤ 150 chars", "numbers": [{"value": "≤ 9 chars", "label": "≤ 34 chars"}, ... 2 or 3]}}`

### takeaways (S12)
`{"cards": [{"n": 1, "title": "≤ 30 chars", "text": "≤ 110 chars"}, ... exactly 3], "closing": "≤ 40 chars"}`

### blocks (backup slides B1-B6, free layout of 1 or 2 columns)
`{"columns": [[BLOCK, ...], [BLOCK, ...]]}` where BLOCK is one of:
- `{"type": "table", "title": "≤ 44 chars", "cols": ["..."], "rows": [["..."], ...], "widths": [0.2, 0.8]}`  (at most 11 rows, 5 columns, cells ≤ 80 chars)
- `{"type": "bullets", "title": "≤ 44 chars", "items": ["≤ 110 chars", ... at most 7]}`
- `{"type": "cards", "title": "≤ 44 chars", "items": [{"head": "≤ 70 chars", "text": "≤ 150 chars", "tag": "≤ 6 chars"}, ... at most 8]}`
- `{"type": "text", "title": "≤ 44 chars", "text": "≤ 420 chars"}`
- `{"type": "kpis", "items": [{"value": "≤ 9 chars", "label": "≤ 36 chars"}, ... 2 to 4]}`
Backup slides carry a `headline` (a topic label sentence), `sources` and `facts`; `notes` is optional (for B6 give the owner and the first sentence of each answer).
