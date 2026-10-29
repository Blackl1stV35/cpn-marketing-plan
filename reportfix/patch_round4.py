import os, sys
sys.stdout.reconfigure(encoding="utf-8")
SP = sys.argv[1]
def rd(p): return open(p, encoding="utf-8-sig", newline="").read()
def wr(p, t): open(p, "w", encoding="utf-8", newline="").write(t)
OLD = "Gen Z footfall share gain below the 3.1-point detection limit at the Q4 wave"
NEW = "K1 gain (the 20–29 share of visitors aged 20 and over) below the 3.1-point detection limit at the Q4 wave"
for rel, want in (("ch456/ch6.md", 1), ("ch456/publish/final_tab.md", 1), ("deck/specs/slide_B5.json", 1)):
    p = os.path.join(SP, rel.replace("/", os.sep))
    t = rd(p)
    n = t.count(OLD)
    print(rel, "x%d" % n, "OK" if n == want else "BAD")
    if n == want:
        wr(p, t.replace(OLD, NEW))
p = os.path.join(SP, "deck", "specs", "slide_B6.json")
t = rd(p)
o2 = "Gen Z and young adults means ages 18 to 29"
n = t.count(o2)
print("slide_B6.json means x%d" % n)
wr(p, t.replace(o2, "Gen Z and young adults are ages 18 to 29"))
