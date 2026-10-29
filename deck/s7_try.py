import json, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, sys.argv[1])
from spoken import spoken_words, band
s = json.load(open(sys.argv[1] + "/specs/slide_07.json", encoding="utf-8-sig"))
print("CURRENT:", s["notes"])
print([ (m["name"], m["what"]) for m in s["body"]["methods"]])
cands = {
 "A": "We propose to measure Gen Z and young adults as ages 18 to 29. Surveys reach only respondents aged 20 and over, who can consent alone. In what we reviewed, CPN gives no age split of visits. Our January to March 2027 baseline uses member analytics, a survey, tourist research and a sustainability tracker. The only published comparator, 14.7 percent of the population aged 13 to 24, is a different band, so indicative only. Four indicators track our proposed targets.",
 "B": "We propose to measure Gen Z and young adults as ages 18 to 29. Surveys reach only respondents aged 20 and over, who can consent alone. In what we reviewed, CPN gives no age split of visits. Our baseline, from January to March 2027, uses member analytics, a survey, tourist research and a sustainability tracker. The only published comparator, 14.7 percent of those aged 13 to 24, is a different band. Four indicators track our proposed targets.",
}
b = band(35)
print("band", round(b[0] * 0.97, 1), round(b[0] * 1.02, 1))
for k, v in cands.items():
    print(k, "spoken", spoken_words(v), "written", len(v.split()))
