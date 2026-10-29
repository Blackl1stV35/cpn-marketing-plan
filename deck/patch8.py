import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
def rep(old, new):
    global t
    n = t.count(old)
    if n != 1:
        raise SystemExit("MISMATCH %d: %s" % (n, old[:70]))
    t = t.replace(old, new)
rep('''def invisible_layer(c, runs, sc, H, y_off=0.0):
    t = c.beginText()''', '''def invisible_layer(c, runs, sc, H, y_off=0.0):
    c.saveState()
    t = c.beginText()''')
rep('''    c.drawText(t)


def draw_lines''', '''    c.drawText(t)
    c.restoreState()


def draw_lines''')
rep('''def draw_slide_page(c, s, key):''', '''def draw_slide_page(c, s, key, extra_keys=()):''')
rep('''    c.bookmarkPage(key, fit="FitH", top=H)
    c.setFillColor(HexColor("#F4F0E8"))''', '''    c.bookmarkPage(key, fit="FitH", top=H)
    for ek in extra_keys:
        c.bookmarkPage(ek, fit="FitH", top=H)
    c.setFillColor(HexColor("#F4F0E8"))''')
rep('''    c.addOutlineEntry("Core slides S1 to S12", keys[core[0]["id"]], 0)
    for s in core:
        c.addOutlineEntry("%s  %s" % (s["id"], s["title"]), keys[s["id"]], 1)
        draw_slide_page(c, s, keys[s["id"]])
    c.addOutlineEntry("Backup slides B1 to B6", keys[back[0]["id"]], 0)
    for s in back:
        c.addOutlineEntry("%s  %s" % (s["id"], s["title"]), keys[s["id"]], 1)
        draw_slide_page(c, s, keys[s["id"]])''', '''    c.addOutlineEntry("Core slides S1 to S12", "group_core", 0)
    for i, s in enumerate(core):
        c.addOutlineEntry("%s  %s" % (s["id"], s["title"]), keys[s["id"]], 1)
        draw_slide_page(c, s, keys[s["id"]], ("group_core",) if i == 0 else ())
    c.addOutlineEntry("Backup slides B1 to B6", "group_backup", 0)
    for i, s in enumerate(back):
        c.addOutlineEntry("%s  %s" % (s["id"], s["title"]), keys[s["id"]], 1)
        draw_slide_page(c, s, keys[s["id"]], ("group_backup",) if i == 0 else ())''')
open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
