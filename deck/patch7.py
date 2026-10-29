import sys
d = sys.argv[1]
def patch(p, pairs):
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            raise SystemExit("MISMATCH %d in %s: %s" % (n, p, old[:70]))
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8", newline="\n").write(t)

patch(d + "\\deckdraw.py", [
    ('import math\nfrom PIL', 'import math\nimport os\nfrom PIL'),
    ('        self.used = []', '        self.used = []\n        self.runs = []'),
    ('        self.used.append((round(f.size / float(self.K), 1), round(y), str(s)[:40]))\n',
     '''        self.used.append((round(f.size / float(self.K), 1), round(y), str(s)[:40]))
        try:
            asc, desc = f.getmetrics()
            wpx = f.getlength(str(s))
            hz, vt = anchor[0], anchor[1]
            xl = (self.k(x) - (0 if hz == "l" else wpx / 2.0 if hz == "m" else wpx)) / float(self.K)
            base = (self.k(y) + (asc if vt == "a" else (asc - desc) / 2.0 if vt == "m" else 0)) / float(self.K)
            self.runs.append((round(xl, 2), round(base, 2), str(s), round(f.size / float(self.K), 2), os.path.basename(f.path)))
        except Exception:
            pass
'''),
])
patch(d + "\\deck_layouts.py", [
    ('USED = {}\n', 'USED = {}\nRUNS = {}\nHI = {}\n'),
    ('    USED[s.get("id")] = cv.used', '    USED[s.get("id")] = cv.used\n    RUNS[s.get("id")] = cv.runs\n    HI[s.get("id")] = cv'),
])
patch(d + "\\build_deck.py", [
    ('from deck_layouts import render_slide, C, SEC, USED  # noqa: E402', 'from deck_layouts import render_slide, C, SEC, USED, RUNS, HI  # noqa: E402'),
    ('COMPS = os.path.join(ROOT, "comps")\n', 'COMPS = os.path.join(ROOT, "comps")\nCOMPS_HI = os.path.join(ROOT, "comps_hi")\n'),
    ('for d in (COMPS, SHEETS):', 'for d in (COMPS, COMPS_HI, SHEETS):'),
    ('        img.save(os.path.join(COMPS, "%s.png" % s["id"]))\n        out[s["id"]] = img\n',
     '        img.save(os.path.join(COMPS, "%s.png" % s["id"]))\n        out[s["id"]] = img\n        hcv = HI.pop(s["id"], None)\n        if hcv is not None:\n            hcv.img.save(os.path.join(COMPS_HI, "%s.png" % s["id"]))\n            json.dump(RUNS.get(s["id"], []), open(os.path.join(COMPS_HI, "%s.runs.json" % s["id"]), "w", encoding="utf-8"), ensure_ascii=False)\n            hcv.img = None\n'),
    ('    M = 60\n    cv.R(0, 0, W, 150, fill=C("maroon"))', '    M = 60\n    links = []\n    cv.R(0, 0, W, 150, fill=C("maroon"))'),
    ('        if i % 2 == 0:\n            cv.R(M - 16, y - 6, W - M + 16, y + ROWH - 8, fill="#FAF7F0", r=10)',
     '        links.append((s["id"], M - 16, y - 6, W - M + 16, y + ROWH - 8))\n        if i % 2 == 0:\n            cv.R(M - 16, y - 6, W - M + 16, y + ROWH - 8, fill="#FAF7F0", r=10)'),
    ('        if i < len(back):\n            s = back[i]\n', '        if i < len(back):\n            s = back[i]\n            links.append((s["id"], M - 10, by - 6, 1170, by + 90))\n'),
    ('    cv.img.resize((W, H), Image.LANCZOS).save(path)\n    print("outline"', '    cv.img.save(os.path.join(COMPS_HI, "outline.png"))\n    json.dump(cv.runs, open(os.path.join(COMPS_HI, "outline.runs.json"), "w", encoding="utf-8"), ensure_ascii=False)\n    json.dump({"w": W, "h": H, "links": links}, open(os.path.join(COMPS_HI, "outline.links.json"), "w", encoding="utf-8"))\n    cv.img.resize((W, H), Image.LANCZOS).save(path)\n    print("outline"'),
])
print("ok")
