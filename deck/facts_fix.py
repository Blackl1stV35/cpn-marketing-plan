import json, glob, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = sys.argv[1]
for fp in sorted(glob.glob(R + "/specs/slide_*.json")):
    d = json.load(open(fp, encoding="utf-8-sig"))
    ch = 0
    for f in d.get("facts", []):
        for k in ("on_slide", "meaning", "where"):
            v = f.get(k, "")
            for m in re.finditer(r".{0,60}(adults[- ]only|18 and over|18\+).{0,60}", v):
                print(fp.split("\\")[-1].split("/")[-1], k, "::", m.group(0))
            nv = v.replace("adults-only wave 1", "surveys ages 20+ only")
            if nv != v:
                f[k] = nv
                ch += 1
    if ch:
        open(fp, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        print("updated", fp.split("\\")[-1].split("/")[-1], ch)
