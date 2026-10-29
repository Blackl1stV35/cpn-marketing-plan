import re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
pat = re.compile(r"https?://[^\s\"'\\)\]]*centralpattana\.co\.th[^\s\"'\\)\]]*")
seen = {}
n = 0
with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
    for line in f:
        n += 1
        if "Best-in-Class" not in line and "Dow Jones" not in line:
            continue
        for m in pat.findall(line):
            m = m.rstrip(".,;")
            if m not in seen:
                seen[m] = n
print("lines:", n)
for u, ln in seen.items():
    print(ln, u[:260])
