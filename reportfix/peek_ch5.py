import re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = sys.argv[1]
lines = open(R + "/ch456/ch5.md", encoding="utf-8-sig").read().split("\n")
for n in (57, 175):
    l = lines[n - 1]
    for m in re.finditer(r"35\.6%", l):
        print("ch5 L%d: ...%s..." % (n, l[max(0, m.start() - 330):m.end() + 260]))
        print()
        break
