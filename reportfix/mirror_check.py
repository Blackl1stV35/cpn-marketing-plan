import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
SP = sys.argv[1]
ft = open(os.path.join(SP, "ch456", "publish", "final_tab.md"), encoding="utf-8-sig").read()
s23 = open(os.path.join(SP, "deck", "src", "sec23_final.txt"), encoding="utf-8-sig").read()
bad = 0
for name, text in (("req_ch456.json", ft), ("req_band.json", ft), ("req_band2.json", ft), ("req_band3.json", ft), ("req_sec23.json", s23)):
    reqs = json.load(open(os.path.join(SP, "reportfix", name), encoding="utf-8"))
    for r in reqs:
        if "replaceAllText" in r:
            t = r["replaceAllText"]["replaceText"]
            ok = t in text
        else:
            t = r["insertText"]["text"].rstrip("\n").split("\n")[0]
            ok = t in text
        if not ok:
            bad += 1
            print("MISSING in mirror:", name, t[:70])
# D1 (risk-10 trigger) and a few superseded strings must not remain
d1 = "K1 gain (the 20–29 share of visitors aged 20 and over) below the 3.1-point detection limit at the Q4 wave"
print("D1 in final_tab.md:", d1 in ft)
print("superseded 'surveys limited to respondents aged 20 and over' left:", ft.count("surveys limited to respondents aged 20 and over"))
print("mirror problems:", bad)
