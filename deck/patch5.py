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
    ('        self._fc = {}\n        self.warn = []', '        self._fc = {}\n        self.warn = []\n        self.used = []'),
    ('    def T(self, x, y, s, f, fill="#1E1E1E", anchor="la", halo=None):\n', '    def T(self, x, y, s, f, fill="#1E1E1E", anchor="la", halo=None):\n        self.used.append((round(f.size / float(self.K), 1), round(y), str(s)[:40]))\n'),
])
patch(d + "\\deck_layouts.py", [
    ('def render_slide(s):\n    cv = Cv(W, H, K=2)', 'USED = {}\n\n\ndef render_slide(s):\n    cv = Cv(W, H, K=2)\n    USED[s.get("id")] = cv.used'),
])
patch(d + "\\build_deck.py", [
    ('from deck_layouts import render_slide, C, SEC  # noqa: E402', 'from deck_layouts import render_slide, C, SEC, USED  # noqa: E402'),
    ('        print("%s rendered, %d warning(s)" % (s["id"], len(warn)))',
     '        small = sorted(set((z, t) for z, yy, t in USED.get(s["id"], []) if z < 18 and yy < 1000 and s["kind"] == "core"))\n        print("%s rendered, %d warning(s), min body text %s px" % (s["id"], len(warn), min([z for z, yy, t in USED.get(s["id"], []) if yy < 1000] or [0])))\n        for z, t in small[:6]:\n            print("    small %s px: %s" % (z, t))'),
])
print("ok")
