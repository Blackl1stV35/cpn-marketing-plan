import json, glob, re, os, sys
sys.stdout.reconfigure(encoding="utf-8")
for p in sorted(glob.glob(os.path.join(sys.argv[1], "specs", "slide_[0-9]*.json"))):
    s = json.load(open(p, encoding="utf-8-sig"))
    print("%s [%d words] %s" % (s["id"], len(s["notes"].split()), s["notes"]))
    print()
