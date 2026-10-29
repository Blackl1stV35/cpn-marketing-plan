import sys
p = sys.argv[1] + r"\build_deck.py"
t = open(p, encoding="utf-8", newline="").read()
for old, new in (("y + 768, fill=", "y + 816, fill="), ("+ 30 + 780 + 40", "+ 30 + 828 + 40")):
    n = t.count(old)
    print(old, "x", n)
    assert n in (1, 2)
    t = t.replace(old, new)
open(p, "w", encoding="utf-8", newline="").write(t)
