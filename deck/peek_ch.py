import re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = sys.argv[1]
def show(fn, pats, width=260):
    lines = open(R + "/" + fn, encoding="utf-8-sig").read().split("\n")
    for i, l in enumerate(lines):
        for p in pats:
            for m in re.finditer(p, l):
                s = max(0, m.start() - width // 2); e = min(len(l), m.end() + width // 2)
                print("%s L%d [%s]: ...%s..." % (fn, i + 1, p, l[s:e]))
show("ch4.md", [r"The 1 had", r"The 1 members", r"aged 18 and over", r"adults only", r"adults-only"])
show("ch5.md", [r"22 million", r"23 million"])
show("ch6.md", [r"22 million", r"adults-only", r"adults only", r"33\.55", r"16\.05", r"85\.9", r"86\.7"])
