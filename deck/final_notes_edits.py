import json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = sys.argv[1]

def edit(n, pairs):
    p = R + "/specs/slide_%s.json" % n
    d = json.load(open(p, encoding="utf-8-sig"))
    t = d["notes"]
    for old, new in pairs:
        assert t.count(old) == 1, (n, old)
        t = t.replace(old, new)
    d["notes"] = t
    open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    print(n, len(t.split()), "words")

edit("02", [
    ("Five: five gates release money only on passed tests. Our next speaker covers the situation.",
     "Five: money is released in five gates, on passed tests. Our second speaker covers the situation."),
])
edit("05", [
    ("State Your Style capped its vouchers at 9,800, about 3.9 million baht at most by our calculation. Rental and services was 43,721 million baht in 2025.",
     "State Your Style gave a 400 baht voucher per 4,500 baht spent, 8.9 percent, capped at 9,800 vouchers. Rental and services was 43,721 million baht in 2025, 82.5 percent of revenue by our calculation."),
    ("The 3,769 baht figure is a Bangkok market asking rent per square metre a month in the third quarter of 2026, not CPN's.",
     "The 3,769 baht is a Bangkok asking rent per square metre a month, not CPN's."),
])
edit("07", [("is a different band, so indicative only.", "is a different band, so it is only indicative.")])
edit("08", [("Next, our teammate covers expenses and profit.", "Our fifth speaker covers expenses and profit.")])
edit("10", [("Gate zero releases the first 155 million baht for the Gen Z and tourist lines, plus line 7.",
             "Gate zero releases the first 155 million baht of lines 4, 6 and 7.")])
