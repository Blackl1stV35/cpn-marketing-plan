import re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
pat = re.compile(r"(?:9 April 2026|April 9, 2026|9 Apr 2026|2026-04-09|09/04/2026|9 เมษายน 2569)")
url = re.compile(r"https?://[^\s\"'\\)\]]+")
with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
    for n, line in enumerate(f, 1):
        if not pat.search(line):
            continue
        if "Dow Jones" not in line and "Best-in-Class" not in line and "DJSI" not in line:
            continue
        for m in pat.finditer(line):
            s = max(0, m.start() - 350); e = min(len(line), m.end() + 350)
            print("line", n, "...", line[s:e].replace("\\n", " ").replace("\\\\n", " "))
            print("   urls:", sorted(set(u[:200] for u in url.findall(line)))[:6])
            break
