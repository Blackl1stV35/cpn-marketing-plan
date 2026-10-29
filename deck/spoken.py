"""Counts the words a presenter actually SAYS (numerals read aloud) and checks them against the slide's time.

Usage: python -I spoken.py SPEC.json [SPEC2.json ...]     (prints written words, spoken words, seconds at 130 wpm, target band)
       python -I spoken.py --text "some notes text" SECONDS
Rule: spoken words should land within 97% to 102% of seconds x 130 / 60.
"""
import json
import re
import sys

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def int_words(n):
    """Number of spoken words for a non-negative integer (hyphenated tens count as one word)."""
    if n < 20:
        return 1
    if n < 100:
        return 1
    if n < 1000:
        h, r = divmod(n, 100)
        return 2 + (int_words(r) if r else 0)
    for size, _ in ((10 ** 9, "billion"), (10 ** 6, "million"), (10 ** 3, "thousand")):
        if n >= size:
            q, r = divmod(n, size)
            return int_words(q) + 1 + (int_words(r) if r else 0)
    return 1


def num_token_words(tok):
    tok = tok.replace(",", "")
    if "." in tok:
        a, b = tok.split(".", 1)
        return int_words(int(a or 0)) + 1 + len(b)
    n = int(tok)
    if 1900 <= n <= 2099 and "," not in tok:
        return 2
    return int_words(n)


def spoken_words(text):
    total = 0
    for raw in re.split(r"\s+", text.strip()):
        if not raw:
            continue
        tok = raw.strip(".,;:!?()[]\"'")
        if not tok:
            continue
        parts = re.split(r"[–\-](?=\d)", tok)  # numeric ranges 18-29
        if len(parts) > 1 and all(re.fullmatch(r"[\d,.]+", p) for p in parts):
            total += sum(num_token_words(p) for p in parts) + (len(parts) - 1)
            continue
        if re.fullmatch(r"[\d,]*\d(\.\d+)?", tok):
            total += num_token_words(tok)
            continue
        m = re.fullmatch(r"([A-Za-z]{1,4})(\d+)([A-Za-z]?)", tok)
        if m and (m.group(1).isupper() or m.group(3)):
            letters = len(m.group(1)) + len(m.group(3))
            total += letters + num_token_words(m.group(2))
            continue
        total += 1
    return total


def band(seconds):
    b = seconds * 130 / 60.0
    return b, int(b * 0.97), int(b * 1.02 + 0.999)


def report(path):
    d = json.load(open(path, encoding="utf-8-sig"))
    notes = d.get("notes", "")
    w = len(notes.split())
    sp = spoken_words(notes)
    b, lo, hi = band(d["seconds"])
    flag = "OK" if lo <= sp <= hi else ("TOO LONG" if sp > hi else "short")
    print("%s: written %d, spoken %d, %.1f s at 130 wpm for %d s (target spoken %d-%d) %s" % (d["id"], w, sp, sp / 130.0 * 60, d["seconds"], lo, hi, flag))
    return sp


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 1 and sys.argv[1] == "--text":
        t, sec = sys.argv[2], float(sys.argv[3])
        b, lo, hi = band(sec)
        print("written %d, spoken %d, target spoken %d-%d" % (len(t.split()), spoken_words(t), lo, hi))
    else:
        tot = 0
        for p in sys.argv[1:]:
            tot += report(p)
        if len(sys.argv) > 2:
            print("total spoken", tot, "= %.0f s at 130 wpm (core speech budget 510 s)" % (tot / 130.0 * 60))
