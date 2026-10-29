import json, glob, re, os, sys
root = sys.argv[1]
tot = 0
for p in sorted(glob.glob(os.path.join(root, "specs", "slide_[0-9]*.json"))):
    s = json.load(open(p, encoding="utf-8-sig"))
    w = len(re.findall(r"\S+", s["notes"]))
    b = s["seconds"] * 130 / 60.0
    tot += w
    print("%s %3ds words %3d budget %5.1f  %+5.1f%%  at130wpm %5.1fs  at120wpm %5.1fs" % (s["id"], s["seconds"], w, b, (w / b - 1) * 100, w / 130 * 60, w / 120 * 60))
print("total words", tot, "speech at 130wpm %.0fs at 120wpm %.0fs" % (tot / 130 * 60, tot / 120 * 60))
