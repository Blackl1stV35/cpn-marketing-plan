import sys
sys.stdout.reconfigure(encoding="utf-8")
c = [
 "We propose to measure Gen Z and young adults by survey (ages 20–29) and member data (18–29), with baselines by 31 March 2027 so targets are set against our data.",
 "We propose to measure Gen Z and young adults by survey (ages 20–29) and member data (18–29), with baselines due 31 March 2027 so targets rest on our data.",
 "We propose to measure Gen Z and young adults by survey (ages 20–29) and member data (18–29), and to set baselines by 31 March 2027 before fixing targets.",
 "We propose to measure Gen Z and young adults by survey (20–29) and member data (18–29), with baselines by 31 March 2027 so each target is set against our own data.",
]
for s in c:
    print(len(s), s)
