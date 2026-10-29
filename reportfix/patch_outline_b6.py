import sys, json
sys.stdout.reconfigure(encoding="utf-8")
D = sys.argv[1]
def rd(p):
    return open(p, encoding="utf-8-sig", newline="").read()
def wr(p, t):
    open(p, "w", encoding="utf-8", newline="").write(t)
def rep(p, old, new):
    t = rd(p)
    assert t.count(old) == 1, (p, t.count(old), old[:60])
    wr(p, t.replace(old, new))
    print("patched", p.split("\\")[-1], len(old), "->", len(new))

old = "Numbers and sources were checked against the report and the corrections log on 29 Oct 2026, and the report was aligned with this deck the same day. Sources B6 cites outside Chapters 4 to 6 (the Central Retail release, the CPN 9 Apr 2026 release, the S&P Yearbook 2026, the CPN IR page) are in the Sections 2–3 reference list."
new = "Numbers and sources were checked against the report and the corrections log on 29 Oct 2026, and the report was aligned with the deck. B6 sources outside Chapters 4 to 6 (Central Retail, CPN 9 Apr 2026, S&P Yearbook, CPN IR page) are in the Sections 2–3 list."
rep(D + r"\build_deck.py", old, new)

p = D + r"\specs\slide_B6.json"
j = json.loads(rd(p))
print("B6 sources before:", j["sources"])
t = rd(p)
a = '"Central Pattana, 2026a, 2026g (p. 7), 2026p, n.d.-g (pp. 1, 5)",'
b = '"Central Pattana, 2026a, 2026g (p. 7), 2026p, 2026t, n.d.-g (pp. 1, 5); Central Pattana Investor Relations, n.d.-c, 2026",'
assert t.count(a) == 1
t = t.replace(a, b)
a2 = '"Central Retail Corporation, press release of 14 Aug 2026",'
b2 = '"Central Retail Corporation, 2026; S&P Global, 2026",'
assert t.count(a2) == 1
t = t.replace(a2, b2)
wr(p, t)
print("B6 sources after:", json.loads(t)["sources"])
