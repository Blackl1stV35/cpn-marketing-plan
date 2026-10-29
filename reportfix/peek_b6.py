import json, sys
sys.stdout.reconfigure(encoding="utf-8")
b6 = json.load(open(sys.argv[1] + r"\deck\specs\slide_B6.json", encoding="utf-8-sig"))
for col in b6["body"]["columns"]:
    for blk in col:
        for it in blk.get("items", []):
            if it.get("head", "").startswith("Q4") or it.get("head", "").startswith("Q13"):
                print(it["head"], "||", it["text"], "||", len(it["text"]))
print()
n = b6["notes"]
i = n.find("Q4 (Spkr")
print(n[i:i+190])
heads = [
 "We propose to measure Gen Z and young adults by survey (ages 20–29) and member data (18–29), with baselines by 31 March 2027 so each target is set against our own data.",
 "We propose to measure Gen Z and young adults by survey (ages 20–29) and member data (18–29), with baselines set by 31 March 2027 so targets are set against our own data.",
 "We propose to measure Gen Z and young adults by survey (ages 20–29) and member data (18–29), and to set baselines by 31 March 2027 against our own data.",
]
for h in heads:
    print(len(h), h)
q13 = [
 "Ages 18–29 (team definition). The survey reaches only people aged 20+ (age of majority; younger need a guardian, PDPA s.20), so it measures 20–29; member data cover members 18–29. DataReportal's 13–24 differs.",
 "Ages 18–29 (team definition). The survey reaches only people aged 20+ (age of majority; younger need a guardian, PDPA s.20), so it measures 20–29; member data cover 18–29 members. DataReportal's 13–24 is a different band.",
]
for q in q13:
    print(len(q), q)
q4 = "Not yet measured. Team assumptions (25% visit share for ages 18–29, +10% frequency, +5% lift) carry 79% of FY2028E uplift. The baseline and gates G2 to G4 test them; the visit share only by proxy (K1 is ages 20–29)."
print(len(q4), q4)
