export const meta = {
  name: 'cpn-pdf-qa-round2',
  description: 'Second independent read-only QA of the sketch PDF after the round-1 fixes: verify fixes, hunt regressions, check text, numbers and timing',
  phases: [{ title: 'Review', detail: 'seven independent reviewers run in parallel' }],
}

const ROOT = 'D:/Temp/claude/C--Users-user-AppData-Roaming-Claude-scratch-workspaces-c7acaf2f-ed5f-4f26-814b-0755985b8641-704b7f5d-017e-4c68-a76d-e0c46600fd5a-scratch-2026-10-28-a5a567/f70456b0-3e52-4829-9ee1-0dafc1d96524/scratchpad'
const DECK = ROOT + '/deck'
const PDF = DECK + '/package/CPN_final_deck_sketch.pdf'
const SPECS = DECK + '/specs'

const COMMON = `Context: a six-person student team (Kasetsart University) will present a 10-minute marketing plan for Central Pattana (CPN) and will build the slide deck BY HAND from a sketch PDF. The PDF is at ${PDF} (20 pages, all 1920 pt wide): page 1 = outline and run of show; page 2 = build key (colours, type, chart rules); pages 3-14 = core slides S1-S12; pages 15-20 = backup slides B1-B6. Each slide page = the slide comp (the top 1080 pt, an image with an invisible searchable text layer), then a panel with the slide header (id, title, time, speaker, layout, status), the speaker notes ('Say', with written and spoken word counts), the slide text in reading order ('Text on the slide'), and a 'Back to outline' link. Speakers are named Spkr 1 to Spkr 6 (S1-S2 Spkr 1, S3-S4 Spkr 2, S5-S6 Spkr 3, S7-S8 Spkr 4, S9-S10 Spkr 5, S11-S12 Spkr 6).
Slide content lives in JSON specs: ${SPECS}/slide_01.json ... slide_12.json and slide_B1.json ... slide_B6.json (fields: headline, body, notes, sources, facts). Report text for fact checks: ${ROOT}/ch456/ch4.md, ch5.md, ch6.md, ${DECK}/src/sec23_final.txt, ${ROOT}/ch456/model_out.txt. Locked wording rules: ${DECK}/src/corrections.md.
A FIRST independent QA round found 129 issues (list: ${DECK}/qa_issues.json, a JSON list; indices below refer to it). Fixes were then applied to specs, renderer, outline and PDF code (the notes were also cut to a spoken-word budget: numbers are counted as spoken words, target 97% to 102% of seconds x 130 / 60; tool: python -I ${DECK}/spoken.py FILE.json). YOUR JOB is round 2: confirm the round-1 fixes that fall in your scope really are fixed, and find defects that REMAIN or were INTRODUCED by the fixes. Report only real, specific, verified defects (do not repeat a round-1 finding that is now fixed).
You are READ-ONLY: do not edit any file except your own scratch images under ${DECK}/qa2_<yourkey>/.
To look at pages: python -I ${DECK}/render_pages.py ${PDF} ${DECK}/qa2_<yourkey> <comma-separated pages> <zoom> (saves p03.png ...; zoom 0.5 gives a 960-px-wide overview), then open the PNGs with the Read tool. For detail write a short Python (import fitz): pg = fitz.open(PDF)[page-1]; pix = pg.get_pixmap(matrix=fitz.Matrix(1.5,1.5), clip=fitz.Rect(x0,y0,x1,y1)); pix.save(path). The comp is the rect (0,0,1920,1080) in PDF points (top-left origin); inspect it in 960x540 quadrants. Always run python with -I and sys.stdout.reconfigure(encoding='utf-8').
Severity: critical = wrong or misleading content, or unreadable/clipped text; major = visible layout defect or a content inconsistency; minor = polish.
For each issue give: page, slide id, what is wrong, evidence, the fix, and where it belongs: 'renderer' (deck_layouts.py / deckdraw.py), 'spec' (a slide JSON field), 'outline' (build_deck.py outline code), 'pdf' (make_pdf.py).`

const SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string' },
    issues: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          page: { type: 'string' }, slide: { type: 'string' },
          severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
          problem: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' }, where: { type: 'string' },
        },
        required: ['page', 'slide', 'severity', 'problem', 'evidence', 'fix', 'where'],
      },
    },
  },
  required: ['summary', 'issues'],
}

const visual = (key, pages, label, fixes) => `${COMMON}

Your key: ${key}. Your scope: VISUAL QA of ${label} (PDF pages ${pages}). Round-1 findings to re-check in your scope: ${fixes}. For every page check: (1) comp area: text clipped, overflowing or overlapping; labels colliding with bars, lines or shapes; legends cut; text too small to read on a laptop screen (below about 14 px on the 1920 canvas, footers excepted); awkward line breaks (a date, age range or parenthetical split across lines); numbers or labels that differ from the slide's spec JSON; (2) panel: header (id, title, time, speaker, status) agrees with the outline and spec; notes complete; the 'Say' word counts are right; 'Text on the slide' is complete versus the comp (nothing visible on the comp is missing from it, no mangled characters); (3) page: 'Back to outline' link visible, nothing off the page; (4) phone check at zoom 0.3: headline and key numbers legible.`

const consistency = `${COMMON}

Your key: consistency. Your scope: CROSS-SLIDE CONSISTENCY, TIMING AND CONTENT, text only (specs and PDF text via fitz get_text; no images needed). Re-check round-1 entries 9, 10, 11, 12, 13, 14, 16, 17, 19, 20, 34-36, 86-96, 98-104. Then verify afresh: (a) times and speakers on the outline page versus the specs: S1 10 s, S2 45, S3 35, S4 35, S5 55, S6 55, S7 35, S8 55, S9 55, S10 50, S11 50, S12 30 (510 s); speaker blocks; five 10-second handovers; 40 s spare; handover sentence ordinal matches the next speaker on S2, S4, S6, S8, S10 and a thank-you on S12; (b) SPOKEN-word budget: run spoken.py on every core spec; report any slide outside 97%-102% of its budget and the total against 510 s; (c) every repeated number, date and name agrees across slides, notes, outline and B6 (2,760 / 560 a year / 2,200 / 328 / 696 / 933 / 400 / 240 / 6.6 / 6.9 / 7.0 / 34.6 / 35.5 / 35.2 / 558 / 51.6 / 44 versus 45 centres / 16 / 23 provinces / five gates and dates / 1Q27 / 23 million / 18 to 29 / the China arrivals figures / household debt figure); terms used the same way (gross ceiling, net-new, tactics, F1 defined before it is relied on, our 35.5% floor); (d) notes versus slide: each notes sentence is supported by the slide or its facts; (e) corrections.md rules (read it fully); (f) the outline page's build-checklist claims are true of this PDF (including the spoken-word totals it quotes); (g) plain English, typos, units, number formats, dash use (en dashes in ranges).`

const adversarial = `${COMMON}

Your key: adversarial. Your scope: ADVERSARIAL CONTENT REVIEW as the course instructor (sceptical associate professor of economics; 5 to 10 minutes of questions after the talk). Read every slide spec and the PDF text and check claims against ch4.md, ch5.md, ch6.md, sec23_final.txt, model_out.txt and corrections.md. Re-check round-1 entries 0, 13-24, 82, 94, 105-114. Then verify afresh the NEW or CHANGED claims: the Chinese-arrivals figures (-33.55% in 2025, +16.05% Jan-Aug 2026) and household debt 85.9% (Q1 2026) on S3 and B2; the yearly 560 million wording and the 'tactics = 240 million' definition on S8, S2, S12, B4 and B6; every number on the new B6 cards (2,119 million one-offs, 3.2 points, core 32.3% and 33.9%, 25% / +10% / +5% / 79%, 0.14 points per 100 million, 45% / 250 / 310 / 55% by gate, 6.0% and 35.2% no-plan figures, 67% pass-through, the 1.2 years); the S10 statement that gates 0 and 1 test readiness; S5 side figures (82.5%, 8.9%, 3,769 per sq m a month). Recompute what can be recomputed. List anything unsupported, overstated, mislabelled (team versus company figure) or inconsistent, and any question the B6 cards still do not answer well.`

const builder = `${COMMON}

Your key: builder. Your scope: MANUAL-BUILDER TEST on slides S2, S5, S6, S8, S9, S10, S11 and B3 (pages 4, 7, 8, 10, 11, 12, 13, 17) plus the build key (page 2). Re-check round-1 entries 26-32, 62, 65, 68, 97, 115-122, 125, 128. Pretend you must rebuild these slides in a design tool (Canva) from this PDF alone. For each: is every visible text element in 'Text on the slide' (nothing missing, nothing extra; the 'Other text on the comp' list should hold only headings and labels)? Are chart data, axes, series colours (with hex), bar positions and colours, calendar and timeline positions (with period names), map cells and element order complete and unambiguous? Does the build key give enough (frame geometry, colours with hex, type sizes, radii, chart rules)? Also test copy and paste with fitz: extract page text and confirm the baht sign, en dashes, <=, superscript 2 and apostrophes extract correctly. Report each gap with a concrete fix (usually a line in make_pdf.py slide_entries or key_blocks).`

const jobs = [
  () => agent(visual('v1', '1-6', 'the outline page, the build key and slides S1-S4', 'entries 1, 11, 34-36, 37-44, 86, 87, 114 (outline text, S1 text block, S2 tile size and wording, S3/S4 wording and breaks)'), { label: 'visual:p1-6', phase: 'Review', schema: SCHEMA }),
  () => agent(visual('v2', '7-10', 'slides S5-S8', 'entries 3, 4, 45-53, 2, 9, 28, 29, 103, 107, 108, 115-118 (S5 labels and table gutter, S6 hub spacing and note, S7 headings and [Proposed], S8 legend, notes and callouts)'), { label: 'visual:p7-10', phase: 'Review', schema: SCHEMA }),
  () => agent(visual('v3', '11-14', 'slides S9-S12', 'entries 5, 6, 7, 25, 54-69, 119-121 (S9 charts and labels, S10 chips, connectors, org chart, S11 risk map dots and headings, S12 balance)'), { label: 'visual:p11-14', phase: 'Review', schema: SCHEMA }),
  () => agent(visual('v4', '15-20', 'backup slides B1-B6', 'entries 8, 70-85, 98, 99, 125, 126 (B4 legibility, B2/B3 floors and breaks, B6 card balance and numbering)'), { label: 'visual:p15-20', phase: 'Review', schema: SCHEMA }),
  () => agent(consistency, { label: 'consistency', phase: 'Review', schema: SCHEMA }),
  () => agent(adversarial, { label: 'adversarial', phase: 'Review', schema: SCHEMA }),
  () => agent(builder, { label: 'builder', phase: 'Review', schema: SCHEMA }),
]
const names = ['v1', 'v2', 'v3', 'v4', 'consistency', 'adversarial', 'builder']
const res = await parallel(jobs)
const out = res.map((r, i) => (r ? { reviewer: names[i], summary: r.summary, issues: r.issues } : { reviewer: names[i], summary: 'agent returned null', issues: [] }))
const all = out.flatMap((o) => o.issues.map((x) => ({ reviewer: o.reviewer, ...x })))
const rank = { critical: 0, major: 1, minor: 2 }
all.sort((a, b) => rank[a.severity] - rank[b.severity])
log('issues: ' + all.length + ' (critical ' + all.filter((x) => x.severity === 'critical').length + ', major ' + all.filter((x) => x.severity === 'major').length + ', minor ' + all.filter((x) => x.severity === 'minor').length + ')')
return { summaries: out.map((o) => ({ reviewer: o.reviewer, summary: o.summary, n: o.issues.length })), issues: all }
