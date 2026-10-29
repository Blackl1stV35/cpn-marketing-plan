import sys
sys.stdout.reconfigure(encoding="utf-8")
lines = open(sys.argv[1] + "/deck/src/sec23_final.txt", encoding="utf-8").read().split("\n")
for n in (57, 129, 140, 178, 187):
    print("L%d: %s\n" % (n, lines[n - 1][:1400]))
print("total lines", len(lines))
# reference list start
for i, l in enumerate(lines):
    if l.strip().lower().startswith("references") or l.strip().lower() == "reference list":
        print("refs header at", i + 1, l[:60])
