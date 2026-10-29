import sys
sys.stdout.reconfigure(encoding="utf-8")
lines = open(sys.argv[1] + "/deck/src/sec23_final.txt", encoding="utf-8").read().split("\n")
for i in range(141, len(lines)):
    l = lines[i].strip()
    if l:
        print("L%d: %s" % (i + 1, l[:230]))
