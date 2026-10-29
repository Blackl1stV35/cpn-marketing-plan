import math
def phi(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
n = 1500
for p in (0.5, 0.25):
    se = math.sqrt(2 * p * (1 - p) / n)
    thr = 1.96 * se
    pw4 = 1 - phi(1.96 - 0.04 / se) + phi(-1.96 - 0.04 / se)
    mde80 = (1.96 + 0.8416) * se
    need_n = 2 * (1.96 + 0.8416) ** 2 * p * (1 - p) / 0.04 ** 2
    print("p=%.2f se_diff=%.4f threshold=%.2f pts power(+4)=%.2f MDE80=%.2f pts n_per_wave_for_80pct_at_+4=%.0f" % (p, se, thr * 100, pw4, mde80 * 100, need_n))
se = math.sqrt(2 * 0.25 / 400)
print("M5 threshold n=400 p=.5: %.2f" % (1.96 * se * 100))
