"""Writes speaker_notes.txt and cpn_final_deck_storyboard.zip (full-size comps + sheets + notes).

Usage: python -I package.py
"""
import glob
import json
import os
import re
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "package")
os.makedirs(OUT, exist_ok=True)


def mmss(sec):
    return "%d:%02d" % (sec // 60, sec % 60)


core, back = [], []
for p in sorted(glob.glob(os.path.join(ROOT, "specs", "slide_*.json"))):
    s = json.load(open(p, encoding="utf-8-sig"))
    (core if s["kind"] == "core" else back).append(s)
core.sort(key=lambda s: s["n"])
back.sort(key=lambda s: s["n"])

lines = ["CPN final presentation: speaker notes (10-minute slot; speech 8:30, five handovers of 0:10, 0:40 spare)", ""]
total = 0
for s in core:
    w = len(re.findall(r"\S+", s["notes"]))
    total += w
    lines += ["%s | %s | %s | %s | %d words" % (s["id"], s["title"], mmss(s["seconds"]), s["presenter"], w), s["headline"], "", s["notes"], "", "-" * 60, ""]
lines += ["Total: %d words" % total, "", "BACKUP (Q&A)", ""]
for s in back:
    lines += ["%s | %s" % (s["id"], s["title"]), s["headline"], ""]
    if s.get("notes"):
        lines += [s["notes"], ""]
txt = os.path.join(OUT, "speaker_notes.txt")
open(txt, "w", encoding="utf-8", newline="\n").write("\n".join(lines))

zp = os.path.join(OUT, "cpn_final_deck_storyboard.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for s in core + back:
        src = os.path.join(ROOT, "comps", "%s.png" % s["id"])
        z.write(src, "slides/%02d_%s.png" % (s["n"], s["id"]))
    for src in sorted(glob.glob(os.path.join(ROOT, "sheets", "*.png"))):
        z.write(src, "sheets/" + os.path.basename(src))
    z.write(txt, "speaker_notes.txt")
print("notes words:", total)
print("zip:", zp, os.path.getsize(zp))
