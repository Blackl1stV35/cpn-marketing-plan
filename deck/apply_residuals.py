import json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = sys.argv[1]

def load(n):
    p = R + "/specs/slide_%s.json" % n
    return p, json.load(open(p, encoding="utf-8-sig"))

def save(p, d):
    open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

# S5: unit and period on the market rent figure
p, s = load("05")
it = s["body"]["side"]["items"][2]
assert it["value"] == "฿3,769", it
it["value"] = "฿3,769/m²"
it["label"] = "Bangkok prime asking rent/month, Q3 2026"
for f in s["facts"]:
    if "3,769" in f.get("on_slide", ""):
        f["on_slide"] = "฿3,769/m²; Bangkok prime asking rent/month, Q3 2026"
save(p, s)

# S7: proposals are labelled as proposals; K3 base named
p, s = load("07")
old = "We measure Gen Z and young adults as ages 18–29 and build the baseline by 31 March 2027, so every proposed Gen Z target is set against our own data."
assert s["headline"] == old
s["headline"] = "We propose to measure Gen Z and young adults as ages 18–29 and to set the baseline by 31 March 2027, so each Gen Z target is set against our own data."
assert s["body"]["kpis"][1]["name"] == "K3 India/ME/EU tourist share"
s["body"]["kpis"][1]["name"] = "K3 India/ME/EU registrants"
save(p, s)

# S8: legend names carry the plotted revenue, not the cost
p, s = load("08")
ser = s["body"]["charts"][0]["series"]
assert ser[1]["name"] == "Needed: tactics, ฿240m" and ser[2]["name"] == "Needed: all net-new, ฿560m"
ser[1]["name"] = "Needed: tactics, ฿400m"
ser[2]["name"] = "Needed: all net-new, ฿933m"
save(p, s)

# S10: G4 falls in January 2028, so the axis gets a sixth column
p, s = load("10")
assert s["body"]["months"] == ["Q4 26", "Q1 27", "Q2 27", "Q3 27", "Q4 27"]
s["body"]["months"].append("Q1 28")
g4 = [g for g in s["body"]["gates"] if g["label"].startswith("G4")][0]
assert g4["at"] == 5.0
g4["at"] = 5.33
save(p, s)

# B2: footnote wording
p, s = load("B2")
done = 0
for col in s["body"]["columns"]:
    for blk in col:
        if blk.get("type") == "text" and "The team uses 1Q27; CPN has not confirmed it." in blk["text"]:
            blk["text"] = blk["text"].replace("The team uses 1Q27; CPN has not confirmed it.", "The team uses 1Q27, its reading of the MD&A line.")
            done += 1
assert done == 1
save(p, s)
print("residual field fixes applied")
