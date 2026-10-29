import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")
b6 = json.load(open(sys.argv[1] + r"\deck\specs\slide_B6.json", encoding="utf-8-sig"))
print("B6 notes:", b6["notes"])
print()
b2 = open(sys.argv[1] + r"\deck\specs\slide_B2.json", encoding="utf-8-sig").read().splitlines()
for i in (153, 154, 155):
    print("B2 line", i + 1, b2[i][:700])
