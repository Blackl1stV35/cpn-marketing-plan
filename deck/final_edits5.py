import json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = sys.argv[1]
p = R + "/specs/slide_07.json"
s = json.load(open(p, encoding="utf-8-sig"))
s["notes"] = ("We propose to measure Gen Z and young adults as ages 18 to 29. Surveys reach only respondents aged 20 and over, who can consent alone. "
              "In what we reviewed, CPN gives no age split of visits. Our baseline, January to March 2027, uses member analytics, a survey, "
              "tourist research and sustainability tracking. The only published comparator, 14.7 percent for ages 13 to 24, is a different band. "
              "Four indicators track proposed targets.")
open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(s, ensure_ascii=False, indent=2) + "\n")

cp = R + "/src/corrections.md"
t = open(cp, encoding="utf-8").read()
old1 = "(surveys reach adults only)"
assert t.count(old1) == 1
t = t.replace(old1, "(surveys reach respondents aged 20 and over)")
a = t.index("- Survey consent (decided 29 Oct 2026)")
b = t.index("\n", a)
new = ("- Survey consent (decided 29 Oct 2026, revised later the same day): the team uses 20 as the PDPA consent age (Civil Code majority): respondents aged 20 and over "
       "can consent alone; younger respondents need a guardian (s.20). The measurement band stays ages 18-29; surveys reach respondents aged 20 and over. "
       "Open for the team's sign-off: how 18-19 year-olds are measured. Chapter 4 of the report and its live tab still say 18 (report fix pending).")
t = t[:a] + new + t[b:]
open(cp, "w", encoding="utf-8", newline="\n").write(t)
print("corrections.md updated")
