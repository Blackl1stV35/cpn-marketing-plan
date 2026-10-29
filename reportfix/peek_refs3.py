import sys
sys.stdout.reconfigure(encoding="utf-8")
t = open(sys.argv[1] + "/ch456/publish/refs.md", encoding="utf-8-sig").read().split("\n")
for i, l in enumerate(t):
    if l.startswith("@ref Government Public Relations") or l.startswith("@ref Nation Thailand. (2026g") or l.startswith("@ref Nation Thailand. (2026l") or l.startswith("@ref Nation Thailand. (2026i"):
        print(l[5:])
        print()
