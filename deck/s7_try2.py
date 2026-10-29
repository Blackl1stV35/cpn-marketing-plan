import json, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, sys.argv[1])
from spoken import spoken_words, band
lo, hi = band(35)[0] * 0.97, band(35)[0] * 1.02
c = {
 "C": "We propose to measure Gen Z and young adults as ages 18 to 29. Surveys reach only respondents aged 20 and over, who can consent alone. In what we reviewed, CPN gives no age split of visits. Our baseline, January to March 2027, uses member analytics, a survey, tourist research and a sustainability tracker. The only published comparator, 14.7 percent of those aged 13 to 24, is a different band. Four indicators track proposed targets.",
 "D": "We propose to measure Gen Z and young adults as ages 18 to 29. Surveys reach only respondents aged 20 and over, who can consent alone. In what we reviewed, CPN gives no age split of visits. Our baseline, January to March 2027, uses member analytics, a survey, tourist research and sustainability tracking. The only published comparator, 14.7 percent of those aged 13 to 24, is a different band. Four indicators track proposed targets.",
 "E": "We propose to measure Gen Z and young adults as ages 18 to 29. Surveys reach only respondents aged 20 and over, who can consent alone. In what we reviewed, CPN gives no age split of visits. Our baseline, January to March 2027, uses member analytics, a survey, tourist research and sustainability tracking. The only published comparator, 14.7 percent for ages 13 to 24, is a different band. Four indicators track proposed targets.",
}
print("band %.1f-%.1f" % (lo, hi))
for k, v in c.items():
    print(k, spoken_words(v), len(v.split()))
