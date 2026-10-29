import re, sys
sys.stdout.reconfigure(encoding="utf-8")
t = open(sys.argv[1] + "/publish/refs.md", encoding="utf-8-sig").read().split("\n")
print("lines", len(t))
for i, l in enumerate(t[:6]):
    print(i, l[:160])
for i, l in enumerate(t):
    if re.search(r"(Central Pattana|Central Retail|Government Public|Nation Thailand|S&P|Thai Examiner)[^.]*\. \(", l[:120]):
        print("L%d: %s" % (i + 1, l[:210]))
