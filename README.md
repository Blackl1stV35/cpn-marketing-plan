# CPN final talk: sketch PDF and report fix (Marketing Business Economics 01101423)

Marketing plan for Central Pattana (CPN), 10-minute final talk plus Q&A. State as of 29 Oct 2026.

## Deliverable
- `deck/package/CPN_final_deck_sketch.pdf`: 20 pages (outline, build key, 12 core slides S1-S12, 6 backups B1-B6). Each slide page has the comp, speaker notes, copyable slide text and a link back to the outline. The team builds the slides by hand in Canva from this sketch; no Canva deck was built here.

## Rebuild the PDF (run from `deck/`, Python 3 with Pillow, reportlab, PyMuPDF, pypdf)
    python -I validate_spec.py specs/slide_*.json
    python -I build_deck.py all        # comps, sheets, outline
    python -I make_pdf.py              # writes package/CPN_final_deck_sketch.pdf
    python -I audit_pdf.py package/CPN_final_deck_sketch.pdf
    python -I spoken.py specs/slide_[0-9]*.json   # spoken-word budget (510 s core)

## Layout
- `deck/specs/`: one JSON per slide (headline, body, notes, sources, facts). `deck/src/corrections.md` holds the locked facts.
- `ch456/`: local source of truth for Chapters 4-6 (`publish/final_tab.md` mirrors the live tab); `deck/src/sec23_final.txt` mirrors Sections 2-3.
- `reportfix/`: tools used to edit the live Google Doc (`docparse.py`, `band_edits*.py`, `verify_*.py`) plus the plan and context files of the last change.

## Live report
Google Doc `11rMZgKaX13GeYYs-N-pqrFF_Tj5lcHLc6ShE-w79dsc`: tab `ch2ch3_report` (Sections 2-3) and tab `ch4ch5ch6_report` (Chapters 4-6). Edits go in with `update_doc` and a required revision id; other tabs are untouched.

## Decisions in force
- PDPA consent age 20: the intercept survey reaches respondents aged 20+ in every wave.
- Gen Z and young adults = ages 18-29 (planning segment, model row C1 with its 25% visit share, slides S2, S4, B4). K1 = share of visitors aged 20+ who are aged 20-29; The 1 member data (K2, active members) cover 18-29.
- Line 5 launch money stays gated on CPN confirming each opening date.

## Open
- Optional: tighten gate G4 to require 933m of uplift and 67% pass-through (changes Table 6.2 and K12).
