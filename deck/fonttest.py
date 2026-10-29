from PIL import Image, ImageDraw, ImageFont
import sys
im = Image.new("RGB", (900, 260), "white")
d = ImageDraw.Draw(im)
for i, (name, path) in enumerate([("segoeui", r"C:\Windows\Fonts\segoeui.ttf"), ("tahoma", r"C:\Windows\Fonts\tahoma.ttf"), ("leelawui", r"C:\Windows\Fonts\LeelawUI.ttf")]):
    try:
        f = ImageFont.truetype(path, 44)
        d.text((10, 10 + i * 80), name + ": \u0e3f2,760m 18\u201329 \u2248 \u00d7 \u2192 \u2713", font=f, fill="black")
        print(name, "ok; bbox of baht:", f.getbbox("\u0e3f"), "bbox of A:", f.getbbox("A"))
    except Exception as e:
        print(name, "fail", e)
im.save(sys.argv[1])
