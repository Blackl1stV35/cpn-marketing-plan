#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chapter 5 (Financials) model: Central Pattana (CPN) marketing plan, Marketing Business
Economics 01101423, Kasetsart University.  Data cut-off 28 October 2026.

Stdlib only.  Run:   python -I model.py
It recomputes every number in Chapter 5 (break-even, sales forecast, expense forecast,
P&L-lite, tests of objective F1) from the inputs and assumptions below, runs self-checks, and prints
(1) the inputs, (2) every scenario, (3) the Markdown tables used in the chapter and
(4) the text values quoted in the prose.

All money is THB million unless stated.  Reported inputs come from CPN documents named in
the comments; everything under ASSUMPTIONS is a TEAM ASSUMPTION or TEAM PROPOSAL, not
company guidance.  Forecast years: FY2026E (base year = 6M26 actual + 2H26E), FY2027E
(plan year) and FY2028E.
"""
import sys
from collections import OrderedDict

# =====================================================================================
# 1. REPORTED INPUTS  (THB million)
# =====================================================================================
# FY2025, MD&A 4Q25 and 2025 (Central Pattana, 2026p): P&L table p.5, reconciliation p.3.
FY25 = dict(rs=43721, hotel=1962, resi=4351, other=2975, rev=53009,
            c_rs=17469, c_hotel=653, c_resi=2912, c_total=21035,
            sga=8692, op=23281, jv=2414, inv=1570, fin=3705, tax=4385, mi=335, np=18841,
            netcomb=4105,            # "Net Finance Cost/Income Tax/Others" line, MD&A p.5
            one_off_other=1234,      # Rama 2 lease-extension gain in other income (pre-tax), 3Q25
            inv_rama=1415,           # Rama 2 lease interest inside investment income (pre-tax)
            rama_after_tax=2119,     # 987 + 1,132 after tax; removed from CPN's core profit
            rev_core=51775, op_core=22047, np_core=16722)
# 6M25 and 6M26, MD&A 2Q26 (Central Pattana, 2026g): P&L table p.4.
H1_25 = dict(rs=21516, hotel=970, resi=1095, other=726, rev=24308,
             c_rs=8681, c_hotel=330, c_resi=749, c_total=9760, sga=4042, op=10506,
             netcomb=1806, mi=168, np=8532, np_core=7749)
H1_26 = dict(rs=22957, hotel=1020, resi=1247, other=1233, rev=26457,
             c_rs=8899, c_hotel=334, c_resi=859, c_total=10092, sga=4329, op=12035,
             netcomb=2123, mi=191, np=9721, np_core=9524)
# 2Q26 detail, MD&A 2Q26 p.3-4 (the latest quarter with a below-the-line split).
Q2_26 = dict(jv=741, inv=285, inv_rama=123, fin=1017, tax=980, mi=92, other=471, other_2q25=486,
             rs=11530, rs_2q25=10724, op=5813)
# Administrative expenses by quarter, MD&A 4Q25 and 2025 (Central Pattana, 2026p)
SGA_3Q25, SGA_4Q25 = 1962, 2689
# FY2025 utility expenses (One Report 2025 note 24; Central Pattana Investor Relations, 2026)
UTIL_25 = 6272
# Visits, FY2025 (Central Pattana, 2026a): over 510 million, of which over 70 million international.
VISITS_M = 510.0
INTL_VISITS_M = 70.0
# The 1 BIZ stores (Central Pattana, 2026m) and partner stores (Central Pattana, 2026a).
BIZ_STORES, PARTNER_STORES = 3000.0, 18000.0
# New net leasable area opening 4Q26-2Q27 (sqm; MD&A 2Q26 p.7) and total NLA (2.4 million sqm)
# Listed in the 2Q26 MD&A (Central Pattana, 2026g, p. 7): Central Phuket new luxury zone 4Q26 (about 10,000), the project named
# "The Central" at 1Q27 (about 100,000; the team reads it as The Central Phaholyothin, whose Q4 2026 target is in Central Pattana, 2026b),
# CenTRal cENtrAL retail 2Q27 (about 30,000).  The CenTRal cENtrAL offices (4Q27) are not a launch.
NLA_PHUKET, NLA_THE_CENTRAL, NLA_CENTRAL_RETAIL = 10000, 100000, 30000
NEW_NLA_SQM = NLA_PHUKET + NLA_THE_CENTRAL + NLA_CENTRAL_RETAIL
TOTAL_NLA_SQM = 2400000
# TRIS base case, 2026-2028 (TRIS Rating, 2026): total operating revenue THB 55-60 billion a year.
TRIS_LOW, TRIS_HIGH = 55000, 60000
# ---- Reference facts cited in the chapter (quoted, not calculated); source in each comment ----
TRIS_CAPEX_BN = 62                 # TRIS Rating (2026): capex of THB 62 billion over 2026-2028
TRIS_RENT_G = (2, 3)               # TRIS Rating (2026): rental-rate growth 2% to 3% a year
TRIS_EBITDA_M = (60, 62)           # TRIS Rating (2026): EBITDA margin about 60% to 62%
BOT_GDP = (2.4, 2.1)               # Bank of Thailand (2026) = MPC decision 5/2026, 28 October 2026 (Press release No. 41/2026): GDP growth 2026, 2027 (%)
BOT_INFL = (2.1, 1.3)              # Bank of Thailand (2026), same release: headline inflation 2026, 2027 (%)
SGA_BAND = (0.16, 0.18)            # CPN SG&A / total revenue, 3Q25 16%, 4Q25 18%, 1Q26 16.3%, 2Q26 16.4% (MD&A 4Q25, MD&A 2Q26)
SGA_REPORTED_FY25 = 17             # MD&A 4Q25 and 2025: SG&A to total revenue 17% in 2025 and 2024 (%)
SGA_REPORTED_4Q25 = 18             # MD&A 4Q25 and 2025: 18% in 4Q25 (%)
GUIDE_COD_BPS = (10, 20)           # Central Pattana (2026q) slide 15: cost of debt down 10 to 20 bps
GUIDE_NDE = 0.5                    # slide 15: net D/E about 0.5x
GUIDE_NEW_NLA = 6                  # slide 15: new NLA 4Q25 to mid-26 about +6% (%)
GUIDE_NEW_HOTELS = (5, 375)        # slide 15: five new hotels, 375 keys
CALL_3Q26 = "16 November 2026"     # Central Pattana Investor Relations (n.d.-d) calendar; the 3Q26 MD&A filing date is not announced
FLAGSHIP_LATEST = (600, 600, 800)  # latest editions: GCNY 2026 (Thai Publica, 2026), Summer Fest 2026 (Central Pattana, 2026s), Magical Stars (Nation Thailand, 2025c)
BIZ_PARTNER_MKT = 200              # The 1 BIZ: THB 200 million a year of platform marketing investment, funder not stated (Central Pattana, 2024e); the team assumes CPN funds an equal amount
NP_CORE_FY24 = 15593               # FY2024 core net profit (MD&A 4Q25 and 2025, p. 5; Central Pattana, 2026p); FY2025 core is FY25['np_core']
CORE_GROWTH_REPORTED = 7           # CPN prints core net profit +7% YoY for 2025 (MD&A 4Q25 and 2025, p. 5)

# Chapter 4 FY2027 marketing budget: line -> (label, gross ceiling, latest disclosed edition
# already in the FY2026E cost base [team assumption], spend window quarters)
BUDGET = OrderedDict([
    (1,  ("Great Chinese New Year with Central Retail", 500, 600, (1,))),
    (2,  ("Summer Fest 2027 including Songkran",        600, 600, (1, 2))),
    (3,  ("Year-end season including Countdown",        800, 800, (4,))),
    (4,  ("Gen Z content, fandom, creator and Pride",   150,   0, (2, 3, 4))),
    (5,  ("Opening launches",                           250,   0, (1, 2))),
    (6,  ("Tourist programme, India, Gulf, Europe",     100,   0, (2, 3, 4))),
    (7,  ("CENTRAL X and The 1 O2O incentives",          60,   0, (1, 2, 3, 4))),
    (8,  ("The 1 BIZ tenant programme",                 200, 200, (1, 2, 3, 4))),
    (9,  ("LEAD Year 9 and Thai-brand pop-ups",          30,   0, (1, 2, 3))),
    (10, ("Sustainability storytelling",                 50,   0, (2, 3, 4))),
    (11, ("Marketing research",                          20,   0, (1, 2, 3, 4))),
])
GATED_LINES = (4, 6, 7)          # released in two equal tranches (Chapter 4)
UPLIFT_LINES = (1, 4, 6, 7, 9)   # tactics tied to M1-M4 in Chapter 4 that carry net-new spend (line 1: the 100 cut funds line 6)
SUPPORT_LINES = (5, 10, 11)      # opening launches, sustainability storytelling, research: no revenue credited

# =====================================================================================
# 2. ASSUMPTIONS  (team assumptions unless a source is named)
# =====================================================================================
TAX = 0.20                  # tax rate on profit before tax excluding JV profit (FY2025 implied 20.7%, 2Q26 19.3%)
OTHER_G_2H = -0.03          # 2H26E core other income vs 2H25: 2Q26 y/y was -3% (471 v 486)
OTHER_G_YR = 0.02           # recurring other income growth after 2026
MI_G = 0.05                 # minority interest growth a year
THRESH_LOW, THRESH_HIGH = 0.07, 0.09   # team definition of "high-single-digit"
MARGIN_FLOOR = 0.355        # FY2025 net margin to protect: 18,841 / 53,009 = 35.54%, rounded to 35.5% (the shortfalls use the rounded floor)

FLOOR_EXACT = 18841 / 53009   # 35.54%: the unrounded quotient behind MARGIN_FLOOR
assert round(FLOOR_EXACT, 3) == MARGIN_FLOOR
GZ_ALT_SHARE, GZ_ALT_SHARE_TXT = 0.147, "14.7%"   # DataReportal (2025): ages 13-24 are 14.7% of the population (team sum of 13-17 and 18-24); a different band from 18-29

# Programme uplift chain (full run-rate, share of ORGANIC rental-and-services revenue)
GZ_SHARE, GZ_FREQ, GZ_YIELD = 0.25, 0.10, 0.50          # M1: share of visits by ages 18-29 (team assumption), frequency uplift (team assumption; Chapter 6 K2 adopts +10% as a [Proposed] target), yield
INTL_UPLIFT, INTL_YIELD = 0.04, 1.00                    # M2: extra international visits, yield
BIZ_LIFT = 0.05                                         # M4: partner-store sales lift (team assumption; Chapter 6 K5 adopts +5% as a [Proposed] target)
PASS_THROUGH = 0.50         # share of a gain in visits or tenant sales that reaches CPN revenue
RAMP = (0.5, 1.0)           # FY2027E, FY2028E share of the run-rate effect
PLAN_REPEATS_FY28 = True    # net-new spend repeated in FY2028E

SCEN = OrderedDict()
SCEN["Conservative"] = dict(
    g_rs_2h=0.05, g_hotel_2h=0.00, g_resi_2h=-0.15, imp_2h=0.000, g_sga_2h=0.08,
    g_rs=(0.040, 0.040), g_hotel=(0.03, 0.03), g_resi=(0.00, 0.00),
    drag=(0.010, 0.005), g_sga=(0.06, 0.06),
    g_jv=(0.00, 0.00), g_fin=(0.04, 0.04), delivery=0.5)
SCEN["Base"] = dict(
    g_rs_2h=0.075, g_hotel_2h=0.05, g_resi_2h=-0.05, imp_2h=0.010, g_sga_2h=0.06,
    g_rs=(0.065, 0.060), g_hotel=(0.08, 0.08), g_resi=(0.10, 0.10),
    drag=(0.005, 0.000), g_sga=(0.05, 0.05),
    g_jv=(0.05, 0.05), g_fin=(0.02, 0.02), delivery=1.0)
SCEN["Optimistic"] = dict(
    g_rs_2h=0.090, g_hotel_2h=0.08, g_resi_2h=0.05, imp_2h=0.015, g_sga_2h=0.05,
    g_rs=(0.080, 0.075), g_hotel=(0.10, 0.10), g_resi=(0.15, 0.15),
    drag=(-0.003, -0.002), g_sga=(0.04, 0.04),
    g_jv=(0.08, 0.08), g_fin=(0.00, 0.00), delivery=1.5)

TIER_A = "Programme tactics (lines 1, 4, 6, 7, 9; net)"
TIER_B = "All net-new spend charged to SG&A"
TIER_C = "Whole FY2027 ceiling (lines 1 to 11)"

# =====================================================================================
# 3. FORMATTING HELPERS
# =====================================================================================
def n0(x):  return f"{x:,.0f}"
def n1(x):  return f"{x:,.1f}"
def n2(x):  return f"{x:,.2f}"
def pc(x, d=1):  return f"{x * 100:.{d}f}%"
def sg(x, d=1):  return f"{x * 100:+.{d}f}%"
def pts(x, d=1): return f"{x * 100:+.{d}f}"
def yrs(y):
    """Payback in years; above 2.0 the FY2028E run-rate is extrapolated beyond the forecast horizon."""
    if y is None:
        return "not reached"
    return n1(y) if y <= 2.0 else f"{n1(y)} (beyond FY2028E)"

def md(header, rows, align=None):
    """GitHub pipe table."""
    align = align or ["l"] + ["r"] * (len(header) - 1)
    sep = ["---:" if a == "r" else ":---" for a in align]
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(sep) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)

# =====================================================================================
# 4. DERIVED BASELINE AND INPUT CHECKS
# =====================================================================================
KEYS_H2 = ("rs", "hotel", "resi", "other", "rev", "c_rs", "c_hotel", "c_resi", "c_total",
           "sga", "op", "netcomb", "mi", "np")
H2_25 = {k: FY25[k] - H1_25[k] for k in KEYS_H2}

def selfcheck_inputs():
    tol = 2          # CPN's MD&A tables carry rounding of up to 1-2 million
    assert abs(FY25["rs"] + FY25["hotel"] + FY25["resi"] + FY25["other"] - FY25["rev"]) <= tol
    assert abs(FY25["c_rs"] + FY25["c_hotel"] + FY25["c_resi"] - FY25["c_total"]) <= tol
    assert abs(FY25["rev"] - FY25["c_total"] - FY25["sga"] - FY25["op"]) <= tol
    assert abs(FY25["op"] - FY25["netcomb"] - FY25["mi"] - FY25["np"]) <= tol
    assert abs(FY25["op"] + FY25["jv"] + FY25["inv"] - FY25["fin"] - FY25["tax"] - FY25["mi"] - FY25["np"]) <= tol
    assert FY25["rev"] - FY25["one_off_other"] == FY25["rev_core"]
    assert abs(FY25["np"] - FY25["rama_after_tax"] - FY25["np_core"]) <= tol
    for h in (H1_25, H1_26):
        assert abs(h["rs"] + h["hotel"] + h["resi"] + h["other"] - h["rev"]) <= tol
        assert abs(h["c_rs"] + h["c_hotel"] + h["c_resi"] - h["c_total"]) <= tol
        assert abs(h["rev"] - h["c_total"] - h["sga"] - h["op"]) <= tol
        assert abs(h["op"] - h["netcomb"] - h["mi"] - h["np"]) <= tol
    assert abs(H2_25["np"] - (5424 + 4885)) <= tol       # 3Q25 + 4Q25 net profit (MD&A 4Q25)
    assert abs(H2_25["rev"] - (13558 + 15144)) <= tol    # 3Q25 + 4Q25 total revenue
    assert abs(H2_25["sga"] - (SGA_3Q25 + SGA_4Q25)) <= tol
    assert sum(v[1] for v in BUDGET.values()) == 2760    # Chapter 4 total
    assert set(UPLIFT_LINES) | set(SUPPORT_LINES) | {2, 3, 8} == set(BUDGET)
    assert tuple(BUDGET[k][2] for k in (1, 2, 3)) == FLAGSHIP_LATEST and BUDGET[8][2] == BIZ_PARTNER_MKT

# =====================================================================================
# 5. MARKETING BUDGET: bridge to P&L and quarterly phasing
# =====================================================================================
def budget_calc():
    gross = sum(v[1] for v in BUDGET.values())
    embedded = sum(v[2] for v in BUDGET.values())
    net_new = gross - embedded
    net = {k: v[1] - v[2] for k, v in BUDGET.items()}
    uplift_cost = sum(net[k] for k in UPLIFT_LINES)
    support_cost = sum(net[k] for k in SUPPORT_LINES)
    lines_4_11 = sum(v[1] for k, v in BUDGET.items() if k >= 4)
    flagships = sum(v[1] for k, v in BUDGET.items() if k <= 3)
    flagships_prior = sum(v[2] for k, v in BUDGET.items() if k <= 3)
    q_gross, q_emb = [0.0] * 4, [0.0] * 4
    for k, (lab, g, e, win) in BUDGET.items():
        for q in win:
            q_gross[q - 1] += g / len(win)
            q_emb[q - 1] += e / len(win)
    q_net = [a - b for a, b in zip(q_gross, q_emb)]
    gated = sum(BUDGET[k][1] for k in GATED_LINES)
    assert abs(sum(q_gross) - gross) < 1e-9 and abs(sum(q_net) - net_new) < 1e-9
    assert uplift_cost + support_cost == net_new
    return dict(gross=gross, embedded=embedded, net_new=net_new, net=net, uplift_cost=uplift_cost,
                support_cost=support_cost, lines_4_11=lines_4_11, flagships=flagships,
                flagships_prior=flagships_prior, q_gross=q_gross, q_emb=q_emb, q_net=q_net,
                gated=gated, second_tranche=gated / 2)

# =====================================================================================
# 6. PROGRAMME UPLIFT PARAMETERS (full run-rate, share of organic R&S revenue, before pass-through and delivery)
# =====================================================================================
def uplift_params(gz_share=None):
    u1 = (GZ_SHARE if gz_share is None else gz_share) * GZ_FREQ * GZ_YIELD
    u2 = (INTL_VISITS_M / VISITS_M) * INTL_UPLIFT * INTL_YIELD
    u3 = 0.0                                              # M3: counted inside M1, M2 and M4
    u4 = (BIZ_STORES / PARTNER_STORES) * BIZ_LIFT
    raw = u1 + u2 + u3 + u4
    return dict(u1=u1, u2=u2, u3=u3, u4=u4, raw=raw, full=raw * PASS_THROUGH,
                intl_share=INTL_VISITS_M / VISITS_M, biz_share=BIZ_STORES / PARTNER_STORES)

# Contribution-margin cases (from CPN's disclosed FY2025 cost structure)
CM_LOW = FY25["op_core"] / FY25["rev_core"]               # 42.6%: every cost varies (core operating margin)
CM_BASE = 1 - FY25["c_rs"] / FY25["rs"]                   # 60.0%: cost of services varies, SG&A fixed
CM_HIGH = 1 - UTIL_25 / (FY25["rs"] + FY25["hotel"])      # 86.3%: only utilities vary with traffic

# =====================================================================================
# 7. SCENARIO ENGINE
# =====================================================================================
def run_scenario(S, plan=True, bud=None, up=None):
    bud = bud or budget_calc()
    up = up or uplift_params()
    out = OrderedDict()
    h2 = H2_25
    # ---- 2H26E: built from 2H25 --------------------------------------------------------
    rs2 = h2["rs"] * (1 + S["g_rs_2h"])
    ht2 = h2["hotel"] * (1 + S["g_hotel_2h"])
    rd2 = h2["resi"] * (1 + S["g_resi_2h"])
    ot2 = (h2["other"] - FY25["one_off_other"]) * (1 + OTHER_G_2H)
    rev2 = rs2 + ht2 + rd2 + ot2
    r_rs25h2 = h2["c_rs"] / h2["rs"]
    r_hotel = H1_26["c_hotel"] / H1_26["hotel"]
    r_resi = H1_26["c_resi"] / H1_26["resi"]
    c_rs2 = rs2 * (r_rs25h2 - S["imp_2h"])
    c_ht2 = ht2 * r_hotel
    c_rd2 = rd2 * r_resi
    c2 = c_rs2 + c_ht2 + c_rd2
    sga2 = h2["sga"] * (1 + S["g_sga_2h"])
    op2 = rev2 - c2 - sga2
    jv2, inv2, fin2 = 2 * Q2_26["jv"], 2 * Q2_26["inv"], 2 * Q2_26["fin"]
    pbt2 = op2 + jv2 + inv2 - fin2
    tax2 = TAX * (pbt2 - jv2)
    mi2 = H1_26["mi"]
    np2 = pbt2 - tax2 - mi2
    out["2H26"] = dict(rs=rs2, hotel=ht2, resi=rd2, other=ot2, rev=rev2, c_rs=c_rs2,
                       c_hotel=c_ht2, c_resi=c_rd2, c_total=c2, sga=sga2, mkt=0.0, op=op2,
                       jv=jv2, inv=inv2, fin=fin2, tax=tax2, mi=mi2, np=np2,
                       netcomb=fin2 + tax2 - jv2 - inv2, uplift=0.0, rs_org=rs2)
    # ---- FY2026E = 6M26 actual + 2H26E ---------------------------------------------------
    f = {}
    for k in ("rs", "hotel", "resi", "other", "rev", "c_rs", "c_hotel", "c_resi", "c_total",
              "sga", "op", "netcomb", "mi", "np"):
        f[k] = H1_26[k] + out["2H26"][k]
    f.update(mkt=0.0, uplift=0.0, rs_org=f["rs"], jv=None, inv=None, fin=None, tax=None)
    out["FY26"] = f
    ratio_rs = f["c_rs"] / f["rs"]
    sga_org = f["sga"]
    jv_run, inv_run, fin_run = 2 * jv2, 2 * inv2, 2 * fin2     # 2H26E annualised
    mi_prev = f["mi"]
    rs_org_prev, hotel_prev, resi_prev = f["rs"], f["hotel"], f["resi"]
    jv_prev, fin_cur = jv_run, fin_run
    for i, yr in enumerate(("FY27", "FY28")):
        rs_org = rs_org_prev * (1 + S["g_rs"][i])
        hotel = hotel_prev * (1 + S["g_hotel"][i])
        resi = resi_prev * (1 + S["g_resi"][i])
        other = 4 * Q2_26["other"] * (1 + OTHER_G_YR) ** (i + 1)   # recurring: 4 x 2Q26, +2% a year
        m = {}
        for key in ("u1", "u2", "u3", "u4"):
            m[key] = rs_org * up[key] * PASS_THROUGH * S["delivery"] * RAMP[i] if plan else 0.0
        uplift = sum(m.values())
        rs = rs_org + uplift
        rev = rs + hotel + resi + other
        ratio_rs = ratio_rs + S["drag"][i]
        c_rs = rs_org * ratio_rs + uplift * (1 - CM_BASE)
        c_hotel = hotel * r_hotel
        c_resi = resi * r_resi
        c_total = c_rs + c_hotel + c_resi
        sga_org = sga_org * (1 + S["g_sga"][i])
        mkt = bud["net_new"] if (plan and (i == 0 or PLAN_REPEATS_FY28)) else 0.0
        op = rev - c_total - sga_org - mkt
        jv = jv_run * (1 + S["g_jv"][0]) if i == 0 else jv_prev * (1 + S["g_jv"][1])
        inv = inv_run
        fin_cur = fin_run * (1 + S["g_fin"][0]) if i == 0 else fin_cur * (1 + S["g_fin"][1])
        pbt = op + jv + inv - fin_cur
        tax = TAX * (pbt - jv)
        mi = mi_prev * (1 + MI_G)
        np_ = pbt - tax - mi
        out[yr] = dict(rs=rs, rs_org=rs_org, hotel=hotel, resi=resi, other=other, rev=rev,
                       c_rs=c_rs, c_hotel=c_hotel, c_resi=c_resi, c_total=c_total,
                       sga=sga_org, mkt=mkt, op=op, jv=jv, inv=inv, fin=fin_cur, tax=tax, mi=mi,
                       np=np_, netcomb=fin_cur + tax - jv - inv, uplift=uplift,
                       **{"up_" + k: v for k, v in m.items()})
        rs_org_prev, hotel_prev, resi_prev, jv_prev, mi_prev = rs_org, hotel, resi, jv, mi
    return out

def check_identities(sc):
    for yr in ("2H26", "FY27", "FY28"):
        d = sc[yr]
        assert abs(d["op"] - (d["rev"] - d["c_total"] - d["sga"] - d["mkt"])) < 1e-6
        assert abs(d["np"] - (d["op"] - d["netcomb"] - d["mi"])) < 1e-6
        assert abs(d["rev"] - (d["rs"] + d["hotel"] + d["resi"] + d["other"])) < 1e-6
    for yr in ("FY27", "FY28"):
        d = sc[yr]
        assert abs(d["rs"] - d["rs_org"] - sum(d["up_" + k] for k in ("u1", "u2", "u3", "u4"))) < 1e-6
    f, h = sc["FY26"], sc["2H26"]
    assert abs(f["np"] - (H1_26["np"] + h["np"])) < 1e-6 and abs(f["rev"] - (H1_26["rev"] + h["rev"])) < 1e-6

# =====================================================================================
# 8. ANALYSES
# =====================================================================================
def payback_years(cost, cont27, cont28):
    """Years from 1 January 2027 until cumulative contribution repays the repeated annual cost.
    Contribution and cost accrue evenly; beyond FY2028E the FY2028E net profit is extrapolated."""
    net27, net28 = cont27 - cost, cont28 - cost
    if net27 >= 0:
        return cost / cont27, net27, net28
    if net28 <= 0:
        return None, net27, net28
    return 1 + (-net27) / net28, net27, net28

def compute():
    selfcheck_inputs()
    bud = budget_calc()
    up = uplift_params()
    R = OrderedDict(bud=bud, up=up)
    R["S"] = OrderedDict((n, run_scenario(S, True, bud)) for n, S in SCEN.items())
    R["S0"] = OrderedDict((n, run_scenario(S, False, bud)) for n, S in SCEN.items())   # without the plan
    for n in SCEN:
        check_identities(R["S"][n]); check_identities(R["S0"][n])
        assert abs(R["S"][n]["FY26"]["np"] - R["S0"][n]["FY26"]["np"]) < 1e-9     # plan starts in FY2027
    base = R["S"]["Base"]
    rs26, rev26 = base["FY26"]["rs"], base["FY26"]["rev"]
    cms = OrderedDict([("Low", CM_LOW), ("Base", CM_BASE), ("High", CM_HIGH)])
    R["cms"] = cms
    tiers = OrderedDict([(TIER_A, bud["uplift_cost"]), (TIER_B, bud["net_new"]), (TIER_C, bud["gross"])])
    R["tiers"] = tiers
    # ---- 5.1 (a) required revenue by tier and contribution margin ---------------------------
    be = OrderedDict()
    for tn in (TIER_A, TIER_B):
        for cn, cm in cms.items():
            req = tiers[tn] / cm
            be[(tn, cn)] = dict(cm=cm, cost=tiers[tn], req=req, pct_rs=req / rs26, pct_rev=req / rev26,
                                visits=req / rs26 * VISITS_M, per_visit=req / VISITS_M,
                                visits_half=req / rs26 * VISITS_M / GZ_YIELD, romi=1 / cm)
    R["be"] = be
    R["rs_rev_per_visit"] = rs26 / VISITS_M
    # ---- 5.1 (b) ladder and payback using base-case uplift --------------------------------
    pb = OrderedDict()
    u27, u28 = base["FY27"]["uplift"], base["FY28"]["uplift"]
    for tn, c in tiers.items():
        cont27, cont28 = u27 * CM_BASE, u28 * CM_BASE
        y, n27, n28 = payback_years(c, cont27, cont28)
        pb[tn] = dict(cost=c, req=c / CM_BASE, pct_rs=c / CM_BASE / rs26, cont27=cont27, cont28=cont28,
                      net27=n27, net28=n28, cum=n27 + n28, years=y, cover27=cont27 / c, cover28=cont28 / c)
    R["pb"] = pb
    pbs = OrderedDict()
    for sn, sc in R["S"].items():
        row = OrderedDict()
        for tn in (TIER_A, TIER_B):
            for cn, cm in cms.items():
                y, n27, n28 = payback_years(tiers[tn], sc["FY27"]["uplift"] * cm, sc["FY28"]["uplift"] * cm)
                row[(tn, cn)] = dict(years=y, net27=n27, net28=n28, cum=n27 + n28)
        row["romi_b"] = sc["FY28"]["uplift"] / tiers[TIER_B]
        row["romi_a"] = sc["FY28"]["uplift"] / tiers[TIER_A]
        pbs[sn] = row
    R["pbs"] = pbs
    req28_b = tiers[TIER_B] / CM_BASE
    R["p_be"] = req28_b / base["FY28"]["rs_org"] / up["raw"]                 # break-even pass-through, all net-new
    R["p_be_a"] = tiers[TIER_A] / CM_BASE / base["FY28"]["rs_org"] / up["raw"]
    R["req28_pct"] = req28_b / base["FY28"]["rs_org"]
    # ---- 5.2 sales forecast / F1 ---------------------------------------------------------
    f1 = OrderedDict()
    for sn, sc in R["S"].items():
        g = {}
        prev_rs, prev_rev = FY25["rs"], FY25["rev"]
        for yr in ("FY26", "FY27", "FY28"):
            g[yr] = dict(rs=sc[yr]["rs"] / prev_rs - 1, rev=sc[yr]["rev"] / prev_rev - 1)
            prev_rs, prev_rev = sc[yr]["rs"], sc[yr]["rev"]
        g["FY26core"] = sc["FY26"]["rev"] / FY25["rev_core"] - 1
        g["cagr"] = (sc["FY28"]["rev"] / sc["FY26"]["rev"]) ** 0.5 - 1
        g["gap27"] = g["FY27"]["rev"] - THRESH_LOW
        g["gap28"] = g["FY28"]["rev"] - THRESH_LOW
        g["meets"] = (g["FY27"]["rev"] >= THRESH_LOW) and (g["FY28"]["rev"] >= THRESH_LOW)
        f1[sn] = g
    R["f1"] = f1
    s0 = R["S0"]["Base"]
    R["org_growth"] = OrderedDict((yr, s0[yr]["rev"] / s0[prv]["rev"] - 1)
                                  for yr, prv in (("FY27", "FY26"), ("FY28", "FY27")))
    R["org_rs_growth"] = OrderedDict((yr, s0[yr]["rs"] / s0[prv]["rs"] - 1)
                                     for yr, prv in (("FY27", "FY26"), ("FY28", "FY27")))
    R["tris"] = OrderedDict((sn, OrderedDict((yr, TRIS_LOW <= sc[yr]["rev"] <= TRIS_HIGH)
                                             for yr in ("FY26", "FY27", "FY28"))) for sn, sc in R["S"].items())
    # ---- 5.3 margin test -----------------------------------------------------------------
    R["rama_year_after_tax"] = 4 * Q2_26["inv_rama"] * (1 - TAX)
    R["rama_26_after_tax"] = (H1_26["np"] - H1_26["np_core"]) + 2 * Q2_26["inv_rama"] * (1 - TAX)
    mt = OrderedDict()
    for sn, sc in R["S"].items():
        s0 = R["S0"][sn]
        row = {}
        for yr in ("FY26", "FY27", "FY28"):
            rev, npf = sc[yr]["rev"], sc[yr]["np"]
            head = npf - MARGIN_FLOOR * rev
            rama = R["rama_26_after_tax"] if yr == "FY26" else R["rama_year_after_tax"]
            row[yr] = dict(np=npf, rev=rev, margin=npf / rev, head=head, absorb=head / (1 - TAX),
                           margin0=s0[yr]["np"] / s0[yr]["rev"], np0=s0[yr]["np"], rev0=s0[yr]["rev"],
                           eff_pts=npf / rev - s0[yr]["np"] / s0[yr]["rev"],
                           head0=s0[yr]["np"] - MARGIN_FLOOR * s0[yr]["rev"],
                           core_margin=(npf - rama) / rev,
                           sga_ratio=(sc[yr]["sga"] + sc[yr]["mkt"]) / rev,
                           op_margin=sc[yr]["op"] / rev, passes=npf / rev >= MARGIN_FLOOR,
                           passes0=s0[yr]["np"] / s0[yr]["rev"] >= MARGIN_FLOOR)
        mt[sn] = row
    R["mt"] = mt
    R["per100"] = 100 * (1 - TAX) / base["FY27"]["rev"]
    R["second_tranche_pts"] = bud["second_tranche"] * (1 - TAX) / R["S"]["Conservative"]["FY27"]["rev"]
    R["support_pts"] = bud["support_cost"] * (1 - TAX) / base["FY27"]["rev"]
    R["m25"] = FY25["np"] / FY25["rev"]
    R["m25_core"] = FY25["np_core"] / FY25["rev_core"]
    R["h1_26_core_margin"] = H1_26["np_core"] / H1_26["rev"]
    core2h25 = FY25["np_core"] - H1_25["np_core"]
    R["core_2h25"] = core2h25
    R["core_2h26_base"] = base["2H26"]["np"] - 2 * Q2_26["inv_rama"] * (1 - TAX)
    R["core_2h_growth"] = R["core_2h26_base"] / core2h25 - 1
    R["core_fy26_base"] = base["FY26"]["np"] - R["rama_26_after_tax"]
    R["core_fy26_growth"] = R["core_fy26_base"] / FY25["np_core"] - 1
    return R

# =====================================================================================
# 9. ASSUMPTIONS TABLE (generated from the constants above)
# =====================================================================================
def assumption_rows():
    C, B, O = (SCEN[k] for k in ("Conservative", "Base", "Optimistic"))
    up = uplift_params()
    three = lambda key, f=pc: [f(C[key]), f(B[key]), f(O[key])]
    pair = lambda key, f=pc: [f"{f(S[key][0])} / {f(S[key][1])}" for S in (C, B, O)]
    same = lambda txt: [txt, "as base", "as base"]   # value stated once, in the first column
    ptp = lambda x: f"{x * 100:+.1f}"
    b_ = run_scenario(SCEN["Base"])
    a_ = run_scenario(SCEN["Base"], True, None, uplift_params(GZ_ALT_SHARE))
    alt = dict(u27=a_["FY27"]["uplift"], u28=a_["FY28"]["uplift"],
               d_growth=f"{((b_['FY27']['rev'] / b_['FY26']['rev']) - (a_['FY27']['rev'] / a_['FY26']['rev'])) * 100:.1f}")
    mix = lambda k2h, kyr: [f"{pc(S[k2h])}; {pc(S[kyr][0])} / {pc(S[kyr][1])}" for S in (C, B, O)]
    rows = []
    A = rows.append
    # --- frame
    A(["A1", "Horizon", *same("FY2026E is the base year (6M26 actual + 2H26E); FY2027E is the plan year; FY2028E follows"),
       "Team design; 6M26 from the MD&A 2Q26 (Central Pattana, 2026g)"])
    A(["A2", "Scenario meaning",
       "Stress: slower growth, cost pressure and half of the assumed programme gain",
       "2Q26 run-rate, 2026 guidance and full delivery of the assumed programme gain (Table 5.2 rows C1 to C6)",
       "CPN's high-single-digit target met by definition (a target, not a forecast) and 1.5 times the assumed programme gain",
       "Team design"])
    A(["A3", "Revenue basis", *same("MD&A total revenue: rental and services, hotel, residential and other income; investment income excluded"),
       "Central Pattana, 2026p"])
    A(["A4", "One-offs", *same(f"None assumed. FY2025's ฿{n0(FY25['one_off_other'])} million other-income gain and ฿{n0(FY25['inv_rama'])} million lease interest (฿{n0(FY25['rama_after_tax'])} million after tax) are excluded; Rama 2 lease interest continues at ฿{n0(Q2_26['inv_rama'])} million a quarter"),
       "Central Pattana, 2026g, 2026p. Bloomberg (2025) headlines one-off boosts to 3Q25 profit (paywalled, article text not read)"])
    # --- organic revenue
    A(["B1", "Rental and services (R&S) growth, 2H26E y/y", *three("g_rs_2h"),
       f"Team assumption anchored to 6M26 {sg(H1_26['rs'] / H1_25['rs'] - 1)} and 2Q26 {sg(Q2_26['rs'] / Q2_26['rs_2q25'] - 1)} (Central Pattana, 2026g) and 2026 guidance of high single digit, new net leasable area about +{GUIDE_NEW_NLA}%, same-store rental revenue low-to-mid single digit (Central Pattana, 2026q, slide 15)"])
    A(["B2", "R&S organic growth, FY2027E / FY2028E", *pair("g_rs"),
       f"Team assumption anchored to about {n0(NEW_NLA_SQM)} square metres opening from 4Q26 to 2Q27, {pc(NEW_NLA_SQM / TOTAL_NLA_SQM)} of 2.4 million: {n0(NLA_PHUKET)} at Central Phuket (4Q26), {n0(NLA_THE_CENTRAL)} for the project the MD&A lists as \"The Central\" at 1Q27, which the team reads as The Central Phaholyothin (CPN's October 2025 release targeted Q4 2026), and {n0(NLA_CENTRAL_RETAIL)} for CenTRal cENtrAL retail (2Q27) (Central Pattana, 2026b, 2026g, p. 7); rental-rate growth {TRIS_RENT_G[0]}% to {TRIS_RENT_G[1]}% (TRIS Rating, 2026); Bank of Thailand growth projection of {BOT_GDP[0]}% in 2026 and {BOT_GDP[1]}% in 2027 (Bank of Thailand, 2026); CPN targets high-single-digit revenue growth for 2026 to 2030 (Central Pattana, 2026q, slide 16)"])
    A(["B3", "Hotel growth: 2H26E; FY2027E / FY2028E", *mix("g_hotel_2h", "g_hotel"),
       f"Team assumption anchored to 6M26 {sg(H1_26['hotel'] / H1_25['hotel'] - 1)} (Central Pattana, 2026g) and guidance 'maintained' with {GUIDE_NEW_HOTELS[0]} more hotels, {GUIDE_NEW_HOTELS[1]} keys (Central Pattana, 2026q, slide 15)"])
    A(["B4", "Residential growth: 2H26E y/y; FY2027E / FY2028E", *mix("g_resi_2h", "g_resi"),
       "Team assumption anchored to guidance 'maintained' (flat in the base case) and residential revenue growth of about 10% a year over five years (Central Pattana, 2026q, slides 15 and 16)"])
    A(["B5", "Other income", *same(f"2H26E: 2H25 core other income (฿{n0(H2_25['other'] - FY25['one_off_other'])} million) at {sg(OTHER_G_2H, 0)}; then 4 x ฿{n0(Q2_26['other'])} million (2Q26) growing {pc(OTHER_G_YR, 0)} a year; no new FX or lease-extension gains"),
       "Team assumption anchored to 2Q26 other income, 3% below 2Q25 (Central Pattana, 2026g, 2026p)"])
    # --- uplift
    A(["C1", "M1 Gen Z and young-adult visits (ages 18 to 29)", *same(f"{pc(GZ_SHARE, 0)} of visits x {sg(GZ_FREQ, 0)} frequency x {pc(GZ_YIELD, 0)} yield = {pc(up['u1'], 2)} of organic R&S"),
       f"Share, frequency and yield are team assumptions: the {pc(GZ_SHARE, 0)} is the team's assumed share of visits made by the 18 to 29 band that Section 4.5 defines as Gen Z and young adults. CPN publishes no Gen Z share and Section 4.5 sets no visit-frequency KPI (Gen Z targets wait for the Q1 2027 baseline). The only published comparator is DataReportal's ages 13 to 24 ({GZ_ALT_SHARE_TXT} of the population; DataReportal, 2025; team sum), a different band, so the comparison is indicative only; at {GZ_ALT_SHARE_TXT} the base-case uplift would be ฿{n0(alt['u27'])} million in FY2027E and ฿{n0(alt['u28'])} million in FY2028E, and FY2027E revenue growth {alt['d_growth']} point lower (team calculation). Chapter 6 adopts the {sg(GZ_FREQ, 0)} frequency as a [Proposed] target (K2); it is set equal to the assumption and is not evidence for it"])
    A(["C2", "M2 international visits", *same(f"{pc(up['intl_share'])} of visits ({n0(INTL_VISITS_M)} of {n0(VISITS_M)} million, both reported as 'over') x {sg(INTL_UPLIFT, 0)} x {pc(INTL_YIELD, 0)} yield = {pc(up['u2'], 2)}"),
       "Visit counts: Central Pattana, 2026a; uplift and yield: team assumptions"])
    A(["C3", "M3 O2O conversion", *same("No separate revenue; CENTRAL X is the channel that delivers M1, M2 and M4, so counting it again would double count"),
       "Team design"])
    A(["C4", "M4 The 1 BIZ partner stores", *same(f"{pc(up['biz_share'])} of revenue (store-count proxy: over {n0(BIZ_STORES)} of over {n0(PARTNER_STORES)} stores) x {sg(BIZ_LIFT, 0)} sales lift = {pc(up['u4'], 2)}"),
       f"Company-reported store counts, defined differently (Central Pattana, 2026a, 2026m); whether all {n0(BIZ_STORES)} stores are CPN tenants is not disclosed; lift: team assumption (Section 4.5 sets no partner-sales KPI; CPN's own claim is up to 10% within six months, comparison group undefined; Central Pattana, 2024e); CPN publishes no revenue share. Chapter 6 adopts the {sg(BIZ_LIFT, 0)} lift as a [Proposed] target (K5); it is set equal to the assumption and is not evidence for it"])
    A(["C5", "Pass-through to CPN revenue", *same(f"{pc(PASS_THROUGH, 0)} of a gain in visits or tenant sales reaches CPN's revenue (run-rate effect {pc(up['full'], 2)})"),
       "Team assumption; leases carry fixed and variable rent and CPN does not disclose the split (Central Pattana Investor Relations, 2026)"])
    A(["C6", f"Delivery of the assumed programme gain; ramp {pc(RAMP[0], 0)} in FY2027E and {pc(RAMP[1], 0)} in FY2028E",
       f"{C['delivery']:.1f}x", f"{B['delivery']:.1f}x", f"{O['delivery']:.1f}x",
       f"Team assumption; the effect builds from the Q1 baseline to the Q4 target (average {pc(RAMP[0], 0)}) and is full in FY2028E; the plan is repeated in FY2028E"])
    # --- costs
    A(["D1", "R&S cost ratio, 2H26E: improvement on 2H25 (points)", *[f"{S['imp_2h'] * 100:.1f}" for S in (C, B, O)],
       f"Team assumption anchored to the 2H25 ratio of {pc(H2_25['c_rs'] / H2_25['rs'])}; 6M26 improved {(H1_25['c_rs'] / H1_25['rs'] - H1_26['c_rs'] / H1_26['rs']) * 100:.1f} points on 6M25 (Central Pattana, 2026g)"])
    A(["D2", "R&S cost ratio change, FY2027E / FY2028E (points)", *[f"{ptp(S['drag'][0])} / {ptp(S['drag'][1])}" for S in (C, B, O)],
       f"Team assumption for new-space start-up costs; TRIS expects an EBITDA margin of about {TRIS_EBITDA_M[0]}% to {TRIS_EBITDA_M[1]}% (TRIS Rating, 2026)"])
    A(["D3", "Hotel and residential cost ratios", *same(f"{pc(H1_26['c_hotel'] / H1_26['hotel'])} and {pc(H1_26['c_resi'] / H1_26['resi'])} (6M26 actual)"),
       "Team assumption: 6M26 actual ratios held (Central Pattana, 2026g)"])
    A(["D4", "SG&A growth: 2H26E; FY2027E / FY2028E", *mix("g_sga_2h", "g_sga"),
       f"Team assumption anchored to 6M26 {sg(H1_26['sga'] / H1_25['sga'] - 1)} (Central Pattana, 2026g) and Bank of Thailand headline inflation projection of {BOT_INFL[0]}% in 2026 and {BOT_INFL[1]}% in 2027 (Bank of Thailand, 2026)"])
    A(["D5", "Net-new marketing", *same(f"฿{n0(budget_calc()['net_new'])} million in FY2027E and again in FY2028E, all assumed to be borne by CPN (its share of joint or partner-funded campaigns is not stated), spread equally over each line's Section 4.5 spend window and expensed in SG&A as spent"),
       "Section 4.5 budget; bridge in Table 5.9"])
    A(["D6", "Contribution-margin ratio for the break-even test (low / base / high)", f"{pc(CM_LOW)}", f"{pc(CM_BASE)}", f"{pc(CM_HIGH)}",
       f"Low: FY2025 core operating margin; base: R&S gross margin (Central Pattana, 2026p); high: 1 minus utility expenses of ฿{n0(UTIL_25)} million over R&S and hotel revenue of ฿{n0(FY25['rs'] + FY25['hotel'])} million, so only utilities vary with traffic (Central Pattana Investor Relations, 2026, note 24; team calculation)"])
    # --- below the line
    A(["E1", f"Share of JV profit: 2H26E is 2 x ฿{n0(Q2_26['jv'])} million (2Q26); growth a year after",
       *[pc(S["g_jv"][0], 0) for S in (C, B, O)], "Team assumption anchored to the 2Q26 run-rate (Central Pattana, 2026g)"])
    A(["E2", "Investment income", *same(f"2H26E 2 x ฿{n0(Q2_26['inv'])} million; then ฿{n0(4 * Q2_26['inv'])} million a year"),
       "Team assumption: 2Q26 run-rate, which includes ฿123 million of Rama 2 lease interest (Central Pattana, 2026g)"])
    A(["E3", f"Finance cost: 2H26E is 2 x ฿{n0(Q2_26['fin'])} million (2Q26), then ฿{n0(4 * Q2_26['fin'])} million a year growing at",
       *[pc(S["g_fin"][0], 0) for S in (C, B, O)],
       f"Team assumption anchored to the 2Q26 run-rate (Central Pattana, 2026g); guidance: cost of debt down {GUIDE_COD_BPS[0]} to {GUIDE_COD_BPS[1]} basis points, net debt to equity about {GUIDE_NDE}x (Central Pattana, 2026q, slide 15); TRIS assumes capex of ฿{TRIS_CAPEX_BN} billion in 2026 to 2028 (TRIS Rating, 2026)"])
    A(["E4", "Income tax", *same(f"{pc(TAX, 0)} of profit before tax excluding JV profit"),
       f"Team assumption between the FY2025 implied rate of {pc(FY25['tax'] / (FY25['op'] + FY25['inv'] - FY25['fin']))} and the 2Q26 implied rate of {pc(Q2_26['tax'] / (Q2_26['op'] + Q2_26['inv'] - Q2_26['fin']))} (team calculation from Central Pattana, 2026g, 2026p)"])
    A(["E5", "Minority interest", *same(f"2H26E equals 6M26 (฿{n0(H1_26['mi'])} million); {sg(MI_G, 0)} a year after"),
       "Team assumption anchored to 6M26 (Central Pattana, 2026g)"])
    # --- tests
    A(["V1", "Visit base for the break-even visit counts", *same(f"{n0(VISITS_M)} million ('over', FY2025), held flat; revenue per visit is CPN's R&S revenue divided by visits, not shopper spend; the half-yield case reuses Table 5.2 row C1's {pc(GZ_YIELD, 0)}"),
       "Company-reported visits (Central Pattana, 2026a)"])
    A(["V2", "Tests for objective F1", *same(f"High single digit = {pc(THRESH_LOW)} to {pc(THRESH_HIGH)}; margin floor {pc(MARGIN_FLOOR)}, which is the quotient 18,841 / 53,009 = {pc(FLOOR_EXACT, 2)} rounded to {pc(MARGIN_FLOOR)}; the shortfalls in Section 5.3 and Table 5.11 use the rounded floor"),
       "Team definition; the MD&A prints 35.6% for FY2025 (Central Pattana, 2026p)"])
    return rows

# =====================================================================================
# 10. TABLES (Markdown) AND TEXT VALUES
# =====================================================================================
def tables(R):
    T = OrderedDict()
    B = R["S"]["Base"]
    bud, up = R["bud"], R["up"]
    T["assump"] = md(["ID", "Assumption", "Conservative", "Base", "Optimistic", "Source or status"],
                     assumption_rows(), ["l", "l", "l", "l", "l", "l"])
    # --- baseline ---------------------------------------------------------------------
    rows = []
    def rowb(lab, key):
        rows.append([lab] + [n0(v[key]) for v in (FY25, H1_25, H2_25, H1_26)])
    for lab, key in (("Rental and services revenue", "rs"), ("Hotel revenue", "hotel"), ("Residential revenue", "resi"),
                     ("Other income", "other"), ("Total revenue", "rev"), ("Cost of rental and services", "c_rs"),
                     ("Cost of hotel", "c_hotel"), ("Cost of residential", "c_resi"), ("SG&A (administrative expenses)", "sga"),
                     ("Operating profit", "op"), ("Net finance cost, income tax and others", "netcomb"),
                     ("Minority interest", "mi"), ("Net profit to parent", "np")):
        rowb(lab, key)
    rows.append(["Net margin (net profit / total revenue)"] + [pc(h["np"] / h["rev"]) for h in (FY25, H1_25, H2_25, H1_26)])
    T["baseline"] = md(["THB million", "FY2025A", "6M25A", "2H25 (derived)", "6M26A"], rows)
    # --- (a) break-even ----------------------------------------------------------------
    rows = []
    for (tn, cn), v in R["be"].items():
        rows.append([f"{tn.split(' (')[0]}, ฿{n0(v['cost'])}m", f"{cn}: {pc(v['cm'])}", n0(v["req"]), pc(v["pct_rs"]),
                     pc(v["pct_rev"]), n1(v["visits"]), n2(v["per_visit"]), n1(v["visits_half"])])
    T["be"] = md(["Cost base", "Contribution margin", "Extra revenue needed (THB m)", "% of FY2026E R&S revenue",
                  "% of FY2026E total revenue", "Extra visits (million)", "Extra revenue per visit (THB)",
                  "Extra visits if each earns half the average (million)"],
                 rows, ["l", "l", "r", "r", "r", "r", "r", "r"])
    # --- (b) ladder ---------------------------------------------------------------------
    rows = []
    for tn, v in R["pb"].items():
        rows.append([f"{tn}", n0(v["cost"]), n0(v["req"]), pc(v["pct_rs"]), n0(v["cont27"]), n0(v["cont28"]),
                     n0(v["cum"]), yrs(v["years"])])
    T["pb"] = md(["Cost base (a year)", "Cost (THB m)", "Break-even revenue at 60.0% (THB m)", "% of FY2026E R&S revenue",
                  "Base-case contribution FY2027E (THB m)", "Base-case contribution FY2028E (THB m)",
                  "Cumulative profit to FY2028E (THB m)", "Payback (years)"], rows)
    rows = []
    for sn, row in R["pbs"].items():
        rows.append([sn, n0(R["S"][sn]["FY27"]["uplift"]), n0(R["S"][sn]["FY28"]["uplift"]), n2(row["romi_b"]),
                     yrs(row[(TIER_A, "Base")]["years"]), yrs(row[(TIER_B, "Base")]["years"]), yrs(row[(TIER_B, "High")]["years"])])
    T["pbs"] = md(["Scenario", "Uplift FY2027E (THB m)", "Uplift FY2028E (THB m)",
                   "FY2028E revenue per baht of net-new spend", "Payback: programme tactics (years)",
                   "Payback: all net-new, base margin (years)", "Payback: all net-new, high margin (years)"], rows)
    # --- revenue by scenario --------------------------------------------------------------
    rows = []
    for sn, sc in R["S"].items():
        g = R["f1"][sn]
        rows.append([f"{sn}: total revenue (growth)", n0(FY25["rev"]),
                     f"{n0(sc['FY26']['rev'])} ({sg(g['FY26']['rev'])})",
                     f"{n0(sc['FY27']['rev'])} ({sg(g['FY27']['rev'])})",
                     f"{n0(sc['FY28']['rev'])} ({sg(g['FY28']['rev'])})"])
        rows.append([f"{sn}: organic baseline", n0(FY25["rev"]), n0(sc["FY26"]["rev"]),
                     n0(sc["FY27"]["rev"] - sc["FY27"]["uplift"]), n0(sc["FY28"]["rev"] - sc["FY28"]["uplift"])])
        rows.append([f"{sn}: programme uplift (M1 to M4)", "-", "-", n0(sc["FY27"]["uplift"]), n0(sc["FY28"]["uplift"])])
    T["rev"] = md(["THB million", "FY2025A", "FY2026E", "FY2027E", "FY2028E"], rows)
    # --- base-case build ------------------------------------------------------------------
    rows = []
    rows.append(["Rental and services, organic", n0(FY25["rs"])] + [n0(B[y]["rs_org"]) for y in ("FY26", "FY27", "FY28")])
    for key, lab in (("up_u1", "M1 Gen Z visits"), ("up_u2", "M2 international visits"),
                     ("up_u3", "M3 O2O conversion (counted in M1, M2, M4)"), ("up_u4", "M4 The 1 BIZ partner stores")):
        rows.append(["Uplift, " + lab, "-", "-", n0(B["FY27"][key]), n0(B["FY28"][key])])
    for lab, key in (("Rental and services, total", "rs"), ("Hotel", "hotel"), ("Residential", "resi"),
                     ("Other income", "other"), ("Total revenue", "rev")):
        rows.append([lab, n0(FY25[key])] + [n0(B[y][key]) for y in ("FY26", "FY27", "FY28")])
    rows.append(["Total revenue growth", "-"] + [sg(R["f1"]["Base"][y]["rev"]) for y in ("FY26", "FY27", "FY28")])
    rows.append(["Rental and services growth", "-"] + [sg(R["f1"]["Base"][y]["rs"]) for y in ("FY26", "FY27", "FY28")])
    T["build"] = md(["THB million (base case)", "FY2025A", "FY2026E", "FY2027E", "FY2028E"], rows)
    # --- F1 test ---------------------------------------------------------------------------
    rows = []
    for sn in SCEN:
        g = R["f1"][sn]
        rows.append([sn, f"{sg(g['FY27']['rs'])} / {sg(g['FY28']['rs'])}", f"{sg(g['FY27']['rev'])} / {sg(g['FY28']['rev'])}",
                     f"{pts(g['gap27'])} / {pts(g['gap28'])}", pc(g["cagr"]), "Yes" if g["meets"] else "No"])
    T["f1"] = md(["Scenario", "R&S growth FY2027E / FY2028E", "Total revenue growth FY2027E / FY2028E",
                  "Gap to 7.0% (points) FY2027E / FY2028E", "Total revenue CAGR FY2026E to FY2028E",
                  "F1 revenue test met (7.0% or more in both years)"], rows)
    # --- budget bridge and phasing -------------------------------------------------------
    q = lambda arr: [n0(x) for x in arr] + [n0(sum(arr))]
    rows = [["Gross ceiling, lines 1 to 11 (Section 4.5)"] + q(bud["q_gross"]),
            ["Less: already in the FY2026E cost base (flagships at their latest disclosed editions, The 1 BIZ flat)"] + q(bud["q_emb"]),
            ["Net-new spend charged to SG&A"] + q(bud["q_net"])]
    T["bud"] = md(["THB million", "Q1", "Q2", "Q3", "Q4", "FY2027E"], rows)
    # --- P&L-lite, base case -------------------------------------------------------------------
    h26, h2 = B["FY26"], B["2H26"]
    cols = [("FY2025A", FY25), ("6M26A", H1_26), ("2H26E", h2), ("FY2026E", h26), ("FY2027E", B["FY27"]), ("FY2028E", B["FY28"])]
    mk = lambda d: d.get("mkt", 0.0)
    line = lambda lab, f: [lab] + [f(c[1]) for c in cols]
    rows = [line("Total revenue", lambda d: n0(d["rev"])),
            line("Cost of sales and services", lambda d: n0(d["c_total"])),
            line("SG&A before net-new marketing", lambda d: n0(d["sga"])),
            line("Net-new marketing (plan)", lambda d: n0(mk(d)) if mk(d) else "-"),
            line("Operating profit", lambda d: n0(d["op"])),
            line("Net finance cost, income tax and others", lambda d: n0(d["netcomb"])),
            line("Minority interest", lambda d: n0(d["mi"])),
            line("Net profit to parent", lambda d: n0(d["np"])),
            line("Net margin", lambda d: pc(d["np"] / d["rev"])),
            line("SG&A including net-new marketing, % of revenue", lambda d: pc((d["sga"] + mk(d)) / d["rev"]))]
    s0 = R["S0"]["Base"]
    rows.append(["Net margin without the plan", "-", "-", "-", pc(s0["FY26"]["np"] / s0["FY26"]["rev"]),
                 pc(s0["FY27"]["np"] / s0["FY27"]["rev"]), pc(s0["FY28"]["np"] / s0["FY28"]["rev"])])
    rows.append(["Core net margin (excluding Rama 2 lease interest)", pc(FY25["np_core"] / FY25["rev_core"]),
                 pc(H1_26["np_core"] / H1_26["rev"]), "-", pc(R["mt"]["Base"]["FY26"]["core_margin"]),
                 pc(R["mt"]["Base"]["FY27"]["core_margin"]), pc(R["mt"]["Base"]["FY28"]["core_margin"])])
    T["pl"] = md(["THB million"] + [c[0] for c in cols], rows)
    # --- margin test by scenario ------------------------------------------------------------------
    rows = []
    for sn in SCEN:
        m = R["mt"][sn]
        rows.append([sn] + [f"{n0(m[y]['np'])} ({pc(m[y]['margin'])})" for y in ("FY26", "FY27", "FY28")] +
                    [pc(m["FY27"]["margin0"]), pc(m["FY27"]["core_margin"]), n0(m["FY27"]["head"])])
    T["mt"] = md(["Scenario", "Net profit (net margin) FY2026E", "FY2027E", "FY2028E",
                  "FY2027E margin without the plan", "FY2027E core margin",
                  "FY2027E profit above the 35.5% floor (THB m)"], rows)
    return T

def solve_organic_growth():
    """Base-case organic R&S growth that lifts total revenue growth to the 7.0% low end of 'high single digit'
    (bisection): FY2027E with FY2028E at base, then FY2028E with FY2027E at base."""
    import copy
    def rev_growth(g27, g28, yr):
        S = copy.deepcopy(SCEN["Base"]); S["g_rs"] = (g27, g28)
        o = run_scenario(S, True)
        prev = "FY26" if yr == "FY27" else "FY27"
        return o[yr]["rev"] / o[prev]["rev"] - 1
    def bisect(f):
        lo, hi = 0.0, 0.2
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) < THRESH_LOW else (lo, mid)
        return (lo + hi) / 2
    b27, b28 = SCEN["Base"]["g_rs"]
    return bisect(lambda x: rev_growth(x, b28, "FY27")), bisect(lambda y: rev_growth(b27, y, "FY28"))

def values(R):
    """Text values quoted in the prose, formatted once so the chapter and the model agree."""
    V = OrderedDict()
    B, C, O = R["S"]["Base"], R["S"]["Conservative"], R["S"]["Optimistic"]
    bud, up, be, pb, mt, f1 = R["bud"], R["up"], R["be"], R["pb"], R["mt"], R["f1"]
    A_, B_, C_ = TIER_A, TIER_B, TIER_C
    V["gross"] = n0(bud["gross"]); V["net_new"] = n0(bud["net_new"]); V["emb"] = n0(bud["embedded"])
    V["tier_a"] = n0(bud["uplift_cost"]); V["support"] = n0(bud["support_cost"])
    V["lines411"] = n0(bud["lines_4_11"]); V["flag"] = n0(bud["flagships"]); V["flag_prior"] = n0(bud["flagships_prior"])
    V["gross_pct25"] = pc(bud["gross"] / FY25["rev"]); V["gross_pct27"] = pc(bud["gross"] / B["FY27"]["rev"])
    V["nn_pct27"] = pc(bud["net_new"] / B["FY27"]["rev"], 2)
    V["q_net"] = " / ".join(n0(x) for x in bud["q_net"])
    V["tranche2"] = n0(bud["second_tranche"])
    V["cm_low"], V["cm_base"], V["cm_high"] = pc(CM_LOW), pc(CM_BASE), pc(CM_HIGH)
    V["romi_base"] = n2(1 / CM_BASE)
    for cn, key in (("Low", "low"), ("Base", "base"), ("High", "high")):
        for tn, tk in ((A_, "a"), (B_, "b")):
            v = be[(tn, cn)]
            V[f"req_{tk}_{key}"] = n0(v["req"]); V[f"pct_{tk}_{key}"] = pc(v["pct_rs"])
            V[f"vis_{tk}_{key}"] = n1(v["visits"]); V[f"pv_{tk}_{key}"] = n2(v["per_visit"])
    V["pctrev_b_base"] = pc(be[(B_, "Base")]["pct_rev"]); V["pctrev_a_base"] = pc(be[(A_, "Base")]["pct_rev"])
    V["vis_half_b"] = n1(be[(B_, "Base")]["visits_half"]); V["visshare_b"] = pc(be[(B_, "Base")]["visits"] / VISITS_M)
    V["rpv"] = n1(R["rs_rev_per_visit"]); V["rpv_pct_b"] = pc(be[(B_, "Base")]["per_visit"] / R["rs_rev_per_visit"])
    V["rs26_base"] = n0(B["FY26"]["rs"]); V["rev26_base"] = n0(B["FY26"]["rev"])
    V["u1"], V["u2"], V["u4"] = pc(up["u1"], 2), pc(up["u2"], 2), pc(up["u4"], 2)
    V["u_raw"], V["u_full"] = pc(up["raw"], 2), pc(up["full"], 2)
    V["intl_share"], V["biz_share"] = pc(up["intl_share"]), pc(up["biz_share"])
    V["p_be"] = pc(R["p_be"], 0); V["p_be_a"] = pc(R["p_be_a"], 0); V["req28_pct"] = pc(R["req28_pct"], 2)
    for tk, tn in (("a", A_), ("b", B_), ("c", C_)):
        v = pb[tn]
        V[f"pb_cost_{tk}"] = n0(v["cost"]); V[f"pb_req_{tk}"] = n0(v["req"]); V[f"pb_pct_{tk}"] = pc(v["pct_rs"])
        V[f"pb_c27_{tk}"] = n0(v["cont27"]); V[f"pb_c28_{tk}"] = n0(v["cont28"]); V[f"pb_cum_{tk}"] = n0(v["cum"])
        V[f"pb_cov27_{tk}"] = pc(v["cover27"], 0); V[f"pb_cov28_{tk}"] = pc(v["cover28"], 0); V[f"pb_yrs_{tk}"] = yrs(v["years"])
    for sn, key in (("Conservative", "c"), ("Base", "b"), ("Optimistic", "o")):
        S = R["S"][sn]
        for yr, y in (("FY26", "26"), ("FY27", "27"), ("FY28", "28")):
            V[f"rev{key}{y}"] = n0(S[yr]["rev"]); V[f"rs{key}{y}"] = n0(S[yr]["rs"])
            V[f"np{key}{y}"] = n0(S[yr]["np"]); V[f"mg{key}{y}"] = pc(mt[sn][yr]["margin"])
            V[f"gr{key}{y}"] = sg(f1[sn][yr]["rev"]); V[f"grs{key}{y}"] = sg(f1[sn][yr]["rs"])
            V[f"up{key}{y}"] = n0(S[yr]["uplift"]); V[f"cm{key}{y}"] = pc(mt[sn][yr]["core_margin"])
        V[f"cagr{key}"] = pc(f1[sn]["cagr"])
        V[f"gap27{key}"] = pts(f1[sn]["gap27"]); V[f"gap28{key}"] = pts(f1[sn]["gap28"])
        V[f"pba{key}"] = yrs(R["pbs"][sn][(A_, "Base")]["years"]); V[f"pbb{key}"] = yrs(R["pbs"][sn][(B_, "Base")]["years"])
        V[f"pbh{key}"] = yrs(R["pbs"][sn][(B_, "High")]["years"])
        V[f"romi{key}"] = n2(R["pbs"][sn]["romi_b"]); V[f"romia{key}"] = n2(R["pbs"][sn]["romi_a"])
        V[f"m0_27{key}"] = pc(mt[sn]["FY27"]["margin0"]); V[f"m0_28{key}"] = pc(mt[sn]["FY28"]["margin0"])
        V[f"eff27{key}"] = pts(mt[sn]["FY27"]["eff_pts"], 1); V[f"eff28{key}"] = pts(mt[sn]["FY28"]["eff_pts"], 1)
        V[f"head27{key}"] = n0(mt[sn]["FY27"]["head"]); V[f"head28{key}"] = n0(mt[sn]["FY28"]["head"])
        V[f"head0_27{key}"] = n0(mt[sn]["FY27"]["head0"])
        V[f"absorb27{key}"] = n0(mt[sn]["FY27"]["absorb"])
    V["gr26core_b"] = sg(f1["Base"]["FY26core"])
    V["org27"], V["org28"] = sg(R["org_growth"]["FY27"]), sg(R["org_growth"]["FY28"])
    V["orgrs27"], V["orgrs28"] = sg(R["org_rs_growth"]["FY27"]), sg(R["org_rs_growth"]["FY28"])
    V["m25"], V["m25c"] = pc(R["m25"]), pc(R["m25_core"]); V["m_h126c"] = pc(R["h1_26_core_margin"])
    V["sga27_b"] = pc(mt["Base"]["FY27"]["sga_ratio"]); V["sga28_b"] = pc(mt["Base"]["FY28"]["sga_ratio"])
    V["sga26_b"] = pc(mt["Base"]["FY26"]["sga_ratio"]); V["sga25"] = pc(FY25["sga"] / FY25["rev"])
    V["rama_yr"] = n0(R["rama_year_after_tax"]); V["rama_pts"] = pc(R["rama_year_after_tax"] / B["FY27"]["rev"], 1)
    V["per100"] = pc(R["per100"], 2); V["tr2_pts"] = pc(R["second_tranche_pts"], 2); V["support_pts"] = pc(R["support_pts"], 2)
    V["fin_run"] = n0(4 * Q2_26["fin"]); V["fin_up"] = pc(4 * Q2_26["fin"] / FY25["fin"] - 1)
    V["fin27_b"], V["fin28_b"] = n0(B["FY27"]["fin"]), n0(B["FY28"]["fin"])
    V["np_growth26_b"] = sg(B["FY26"]["np"] / FY25["np"] - 1)
    V["np_growth27_b"] = sg(B["FY27"]["np"] / B["FY26"]["np"] - 1)
    V["core26_growth"] = sg(R["core_fy26_growth"]); V["core_2h_growth"] = sg(R["core_2h_growth"])
    V["opm26_b"], V["opm27_b"] = pc(mt["Base"]["FY26"]["op_margin"]), pc(mt["Base"]["FY27"]["op_margin"])
    V["opm25"] = pc(FY25["op"] / FY25["rev"])
    V["rs_cost_ratio26"] = pc(B["FY26"]["c_rs"] / B["FY26"]["rs"])
    V["rs_cost_ratio_2h25"] = pc(H2_25["c_rs"] / H2_25["rs"])
    V["rs_cost_ratio_1h26"] = pc(H1_26["c_rs"] / H1_26["rs"]); V["rs_cost_ratio_1h25"] = pc(H1_25["c_rs"] / H1_25["rs"])
    V["g_rs_1h26"] = sg(H1_26["rs"] / H1_25["rs"] - 1); V["g_rs_2q26"] = sg(Q2_26["rs"] / Q2_26["rs_2q25"] - 1)
    V["g_sga_1h26"] = sg(H1_26["sga"] / H1_25["sga"] - 1)
    V["rs_fy26_c"] = sg(C["FY26"]["rs"] / FY25["rs"] - 1); V["rs_fy26_b"] = sg(B["FY26"]["rs"] / FY25["rs"] - 1)
    V["rs_fy26_o"] = sg(O["FY26"]["rs"] / FY25["rs"] - 1)
    V["resi_fy26_b"] = sg(B["FY26"]["resi"] / FY25["resi"] - 1)
    V["oth26_b"] = n0(B["FY26"]["other"])
    V["onoff_total"] = n0(FY25["one_off_other"] + FY25["inv_rama"])
    V["rama_at"] = n0(FY25["rama_after_tax"]); V["oneoff_other"] = n0(FY25["one_off_other"]); V["oneoff_inv"] = n0(FY25["inv_rama"])
    V["rama_q"] = n0(Q2_26["inv_rama"])
    V["sga_step"] = n0(SGA_4Q25 - SGA_3Q25)
    V["nla27"] = n0(NEW_NLA_SQM); V["nla27_pct"] = pc(NEW_NLA_SQM / TOTAL_NLA_SQM)
    V["tris_b27"] = "inside" if R["tris"]["Base"]["FY27"] else "outside"
    V["tris_b28"] = "inside" if R["tris"]["Base"]["FY28"] else "outside"
    V["tris_c28"] = "inside" if R["tris"]["Conservative"]["FY28"] else "outside"
    V["tris_c27"] = "inside" if R["tris"]["Conservative"]["FY27"] else "outside"
    V["tris_b28_gap"] = pc(B["FY28"]["rev"] / TRIS_HIGH - 1)
    V["visits"], V["intl"] = n0(VISITS_M), n0(INTL_VISITS_M)
    V["rev_core25"] = n0(FY25["rev_core"])
    V["head_to_floor_b27"] = n0(-mt["Base"]["FY27"]["head"])
    V["np27_b_with"], V["np27_b_without"] = n0(B["FY27"]["np"]), n0(R["S0"]["Base"]["FY27"]["np"])
    V["np_effect27_b"] = n0(B["FY27"]["np"] - R["S0"]["Base"]["FY27"]["np"])
    V["util_ratio"] = pc(UTIL_25 / (FY25["rs"] + FY25["hotel"]))
    V["core_gain_b27"] = pts(mt["Base"]["FY27"]["core_margin"] - R["m25_core"], 1)
    V["m26_b_vs25"] = pts(mt["Base"]["FY26"]["margin"] - R["m25"], 1)
    V["m27_b_vs25"] = pts(mt["Base"]["FY27"]["margin"] - R["m25"], 1)
    V["fx_1q26"] = n0(762 - Q2_26["other"])
    V["g_2h_b"] = pc(SCEN["Base"]["g_rs_2h"]); V["g_2h_c"] = pc(SCEN["Conservative"]["g_rs_2h"]); V["g_2h_o"] = pc(SCEN["Optimistic"]["g_rs_2h"])
    V["g_rs27_c"], V["g_rs28_c"] = (pc(SCEN["Conservative"]["g_rs"][i]) for i in (0, 1))
    V["g_rs27_b"], V["g_rs28_b"] = (pc(SCEN["Base"]["g_rs"][i]) for i in (0, 1))
    V["g_rs27_o"], V["g_rs28_o"] = (pc(SCEN["Optimistic"]["g_rs"][i]) for i in (0, 1))
    V["uplift_pts27"] = pts(f1["Base"]["FY27"]["rev"] - R["org_growth"]["FY27"], 1)
    V["uplift_pts28"] = pts(f1["Base"]["FY28"]["rev"] - R["org_growth"]["FY28"], 1)
    V["m_c27"], V["m_c28"] = pc(mt["Conservative"]["FY27"]["margin"]), pc(mt["Conservative"]["FY28"]["margin"])
    V["m_o27"], V["m_o28"] = pc(mt["Optimistic"]["FY27"]["margin"]), pc(mt["Optimistic"]["FY28"]["margin"])
    V["support_pts_b"] = pc(R["support_pts"], 2)
    V["shortfall_pts_b27"] = pts(MARGIN_FLOOR - mt["Base"]["FY27"]["margin"], 1).lstrip("+")
    V["delivery_c"], V["delivery_o"] = f"{SCEN['Conservative']['delivery']:.1f}", f"{SCEN['Optimistic']['delivery']:.1f}"
    V["sga_cap"] = pc(SGA_BAND[1], 0)
    V["pass_through"] = pc(PASS_THROUGH, 0)
    V["q2_net"] = n0(bud["q_net"][1]); V["q1_net"] = n0(bud["q_net"][0])
    V["fin25"] = n0(FY25["fin"])
    V["short27b"] = f"{abs(f1['Base']['gap27']) * 100:.1f}"; V["short28b"] = f"{abs(f1['Base']['gap28']) * 100:.1f}"
    V["line1_cut"] = n0(BUDGET[1][2] - BUDGET[1][1])
    V["cons_head27_abs"] = n0(-mt["Conservative"]["FY27"]["head"])
    # unsigned or absolute forms for prose ("grows 7.1%", "costs 0.7 points")
    pp = lambda x, d=1: f"{abs(x) * 100:.{d}f}"
    V["pb_cum_b_abs"] = n0(abs(pb[B_]["cum"]))
    for sn, key in (("Conservative", "c"), ("Base", "b"), ("Optimistic", "o")):
        for yr, y in (("FY26", "26"), ("FY27", "27"), ("FY28", "28")):
            V[f"gu{key}{y}"] = pc(f1[sn][yr]["rev"]); V[f"gsu{key}{y}"] = pc(f1[sn][yr]["rs"])
    V["rs_fy26_bu"] = pc(B["FY26"]["rs"] / FY25["rs"] - 1)
    V["gr26core_bu"] = pc(f1["Base"]["FY26core"])
    V["org27u"], V["org28u"] = pc(R["org_growth"]["FY27"]), pc(R["org_growth"]["FY28"])
    V["uplift_pts27u"] = pp(f1["Base"]["FY27"]["rev"] - R["org_growth"]["FY27"])
    V["eff27b_u"] = pp(mt["Base"]["FY27"]["eff_pts"])
    V["per100_pp"] = pp(R["per100"], 2); V["support_pp"] = pp(R["support_pts"], 2); V["rama_pp"] = pp(R["rama_year_after_tax"] / B["FY27"]["rev"])
    V["core_gain_b27_u"] = pp(mt["Base"]["FY27"]["core_margin"] - R["m25_core"])
    V["m1_share28"] = pc(B["FY28"]["up_u1"] / B["FY28"]["uplift"], 0)
    V["m1_28"] = n0(B["FY28"]["up_u1"])
    # cited reference facts (quoted, not calculated) and computed checks against them
    V["call_3q26"] = CALL_3Q26
    V["flag1"], V["flag2"], V["flag3"] = (n0(x) for x in FLAGSHIP_LATEST)
    V["biz_mkt"] = n0(BIZ_PARTNER_MKT)
    V["bot_g26"], V["bot_g27"] = (f"{x}%" for x in BOT_GDP)
    V["tris_lo"], V["tris_hi"] = n0(TRIS_LOW), n0(TRIS_HIGH)
    V["tris_capex"] = n0(TRIS_CAPEX_BN)
    V["sga_band_lo"], V["sga_band_hi"] = pc(SGA_BAND[0], 0), pc(SGA_BAND[1], 0)
    V["sga_fy25_rep"], V["sga_4q25_rep"] = f"{SGA_REPORTED_FY25}%", f"{SGA_REPORTED_4Q25}%"
    V["cod_lo"], V["cod_hi"] = (str(x) for x in GUIDE_COD_BPS)
    bl, cl, ol = mt["Base"]["FY27"], mt["Conservative"]["FY27"], mt["Optimistic"]["FY27"]
    V["floor_exact"] = pc(FLOOR_EXACT, 2)
    V["head_exact_b27"] = n0(-(bl["np"] - FLOOR_EXACT * bl["rev"]))
    V["absorb_exact_b27"] = n0(-(bl["np"] - FLOOR_EXACT * bl["rev"]) / (1 - TAX))
    V["head_exact_c27"] = n0(-(cl["np"] - FLOOR_EXACT * cl["rev"]))
    V["head_exact_o27"] = n0(ol["np"] - FLOOR_EXACT * ol["rev"])
    V["absorb_b27"] = n0(-mt["Base"]["FY27"]["absorb"])
    V["sga25_lfl"] = pc(FY25["sga"] / FY25["rev_core"])
    V["sga_rise27"] = f"{(mt['Base']['FY27']['sga_ratio'] - FY25['sga'] / FY25['rev_core']) * 100:.1f}"
    V["sga_rise28"] = f"{(mt['Base']['FY28']['sga_ratio'] - FY25['sga'] / FY25['rev_core']) * 100:.2f}"
    V["nn_pts27"] = f"{bud['net_new'] / B['FY27']['rev'] * 100:.2f}"
    V["core_np25"], V["core_np24"] = n0(FY25["np_core"]), n0(NP_CORE_FY24)
    V["core_g25"] = f"{(FY25['np_core'] / NP_CORE_FY24 - 1) * 100:.0f}%"
    assert f"{(FY25['np_core'] / NP_CORE_FY24 - 1) * 100:.0f}" == str(CORE_GROWTH_REPORTED)
    V["rs_org28"] = n0(B["FY28"]["rs_org"])
    V["gain28"] = n0(B["FY28"]["rs_org"] * up["raw"])
    V["sga_fy25"] = n0(FY25["sga"])
    V["g_fin_b"] = pc(SCEN["Base"]["g_fin"][0], 0)
    V["oneoff_pts"] = f"{(R['m25'] - R['m25_core']) * 100:.1f}"
    V["sga27_c"] = pc(mt["Conservative"]["FY27"]["sga_ratio"]); V["sga28_c"] = pc(mt["Conservative"]["FY28"]["sga_ratio"])
    V["m14_share28"] = pc((B["FY28"]["up_u1"] + B["FY28"]["up_u4"]) / B["FY28"]["uplift"], 0)
    # what must be true for the revenue half of F1 (7.0% in the year) in the base case
    V["rs_fy26_at_1h"] = sg((H1_26["rs"] + H2_25["rs"] * (H1_26["rs"] / H1_25["rs"])) / FY25["rs"] - 1)
    V["need_2h_rs"] = sg(((1 + THRESH_LOW) * FY25["rs"] - H1_26["rs"]) / H2_25["rs"] - 1)
    nd = solve_organic_growth()
    V["need_org27"], V["need_org28"] = pc(nd[0]), pc(nd[1])
    V["floor"] = pc(MARGIN_FLOOR); V["thresh_lo"] = pc(THRESH_LOW); V["thresh_hi"] = pc(THRESH_HIGH)
    inband = all(SGA_BAND[0] <= mt["Base"][y]["sga_ratio"] <= SGA_BAND[1] for y in ("FY27", "FY28"))
    assert inband, "base-case SG&A ratio left CPN's reported band; revise the chapter wording"
    V["sga_inband"] = "inside"
    return V

# =====================================================================================
# 11. REPORT
# =====================================================================================
def report(R):
    T, V = tables(R), values(R)
    print("CHAPTER 5 MODEL OUTPUT  (THB million unless stated)")
    print("Self-checks on reported inputs and model identities: passed\n")
    print("== INPUTS ==")
    for nm, d in (("FY2025 (MD&A FY2025)", FY25), ("6M25 (MD&A 2Q26)", H1_25), ("6M26 (MD&A 2Q26)", H1_26),
                  ("2H25 = FY2025 - 6M25 (derived)", H2_25), ("2Q26 detail (MD&A 2Q26)", Q2_26)):
        print(f"{nm}: " + ", ".join(f"{k}={v:,}" for k, v in d.items()))
    print(f"utilities FY2025 {UTIL_25:,}; visits {VISITS_M:,.0f}m (international {INTL_VISITS_M:,.0f}m); "
          f"The 1 BIZ stores {BIZ_STORES:,.0f} of {PARTNER_STORES:,.0f}; new NLA {NEW_NLA_SQM:,} of {TOTAL_NLA_SQM:,} sqm")
    print("\n== REFERENCE FACTS QUOTED IN THE CHAPTER (not calculated; source in model.py comments) ==")
    print(f"TRIS (2026): operating revenue {TRIS_LOW:,}-{TRIS_HIGH:,} a year 2026-2028; rental-rate growth {TRIS_RENT_G[0]}%-{TRIS_RENT_G[1]}%; "
          f"EBITDA margin {TRIS_EBITDA_M[0]}%-{TRIS_EBITDA_M[1]}%; capex THB {TRIS_CAPEX_BN} billion 2026-2028")
    print(f"Bank of Thailand (2026), MPC decision 5/2026 of 28 October 2026: GDP growth {BOT_GDP[0]}% (2026), {BOT_GDP[1]}% (2027); headline inflation {BOT_INFL[0]}% (2026), {BOT_INFL[1]}% (2027)")
    print(f"CPN SG&A to revenue band {SGA_BAND[0]:.0%}-{SGA_BAND[1]:.0%} (3Q25-2Q26); FY2025 {SGA_REPORTED_FY25}%; 4Q25 {SGA_REPORTED_4Q25}%")
    print(f"CPN 2Q26 deck slide 15: cost of debt down {GUIDE_COD_BPS[0]}-{GUIDE_COD_BPS[1]} bps; net D/E about {GUIDE_NDE}x; new NLA about +{GUIDE_NEW_NLA}%; "
          f"{GUIDE_NEW_HOTELS[0]} hotels ({GUIDE_NEW_HOTELS[1]} keys)")
    print(f"flagship latest editions {FLAGSHIP_LATEST}; The 1 BIZ partner marketing {BIZ_PARTNER_MKT}; 3Q26 earnings call {CALL_3Q26}")
    print(f"F1 test: high single digit {THRESH_LOW:.1%}-{THRESH_HIGH:.1%}; margin floor {MARGIN_FLOOR:.1%} (exact quotient {FLOOR_EXACT:.2%})")
    print(f"CPN core net profit FY2025 {FY25['np_core']:,} against FY2024 {NP_CORE_FY24:,} (CPN prints +{CORE_GROWTH_REPORTED}%)")
    bud = R["bud"]
    print("\n== BUDGET (Chapter 4) ==")
    print(f"gross {bud['gross']}, embedded {bud['embedded']}, net-new {bud['net_new']} = programme tactics {bud['uplift_cost']} "
          f"+ support {bud['support_cost']}; lines 4-11 {bud['lines_4_11']}; flagships {bud['flagships']} (2026 editions {bud['flagships_prior']}); "
          f"gated {bud['gated']}, second tranche {bud['second_tranche']}")
    print("net by line:", dict(bud["net"]))
    print("quarterly gross :", [round(x, 2) for x in bud["q_gross"]])
    print("quarterly embed :", [round(x, 2) for x in bud["q_emb"]])
    print("quarterly net   :", [round(x, 2) for x in bud["q_net"]])
    up = R["up"]
    print("\n== UPLIFT PARAMETERS (share of organic R&S revenue, before pass-through and delivery) ==")
    print({k: round(v, 5) for k, v in up.items()}, " pass-through", PASS_THROUGH, " ramp", RAMP)
    print("\n== CONTRIBUTION MARGIN CASES ==")
    print({k: round(v, 4) for k, v in R["cms"].items()})
    for sn, sc in R["S"].items():
        print(f"\n== SCENARIO {sn.upper()} (with plan) ==")
        for yr in ("2H26", "FY26", "FY27", "FY28"):
            d = sc[yr]
            print(f"{yr}: " + ", ".join(f"{k}={d[k]:,.1f}" for k in ("rs", "hotel", "resi", "other", "rev", "c_total", "sga", "mkt",
                                                                       "op", "netcomb", "mi", "np", "uplift") if d.get(k) is not None))
    for sn, sc in R["S0"].items():
        print(f"\n== SCENARIO {sn.upper()} (without plan) ==")
        for yr in ("FY26", "FY27", "FY28"):
            d = sc[yr]
            print(f"{yr}: rev={d['rev']:,.1f}, op={d['op']:,.1f}, np={d['np']:,.1f}, margin={d['np'] / d['rev'] * 100:.2f}%")
    print("\n== SUMMARY CHECKS ==")
    print("2H26E core net profit growth vs 2H25 core (base):", pc(R["core_2h_growth"]),
          "| FY2026E core net profit growth (base):", pc(R["core_fy26_growth"]))
    print("TRIS range test (55,000-60,000):", {s: dict(v) for s, v in R["tris"].items()})
    print("Break-even pass-through at FY2028E run-rate (base, all net-new):", pc(R["p_be"], 1),
          "| programme tactics:", pc(R["p_be_a"], 1), "| required uplift % of FY2028E organic R&S:", pc(R["req28_pct"], 2))
    print("\n== MARKDOWN TABLES ==")
    for k, t in T.items():
        print(f"\n[{k}]\n{t}")
    print("\n== TEXT VALUES ==")
    for k, v in V.items():
        print(f"{k} = {v}")

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    report(compute())
