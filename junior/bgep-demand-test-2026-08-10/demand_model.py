#!/usr/bin/env python3
"""
BGEP - the demand test.
Built 10 Aug 2026 to stress the one assumption every other number rests on:
"3 boxes per outlet per month", i.e. 10 sachets a day out of one shop.

economics.py answers "what do we make per sachet". It is sound and unchanged.
This answers "how many sachets are there", which is the question that decides
whether the manufacturing tier we asked for this week is the right one.

All money in INR unless stated. GBP at 106 INR = 1 GBP.
Sources for every external anchor are in RESEARCH-NOTES.md.
"""

INR_GBP = 106.0

# ---- carried over from economics.py, unchanged (base case: 18% GST, no caffeine)
EX_FACTORY = 6.6271      # what we receive per sachet
CONTRIBUTION = 4.0771    # per sachet, after COGS 2.10, freight 0.15, trade 0.30
MRP = 10.00
COGS = 2.10
DISTRIBUTOR_PER_SACHET = 0.5763   # Rs 7.2034 - Rs 6.6271
RETAILER_PER_SACHET = 1.2712      # Rs 8.4746 - Rs 7.2034

# ---- external anchors (see RESEARCH-NOTES.md for sources and read dates)
ORS_CATEGORY_CR_LOW = 800     # Cipla Health CEO, 2025
ORS_CATEGORY_CR_HIGH = 1000
ELECTRAL_CR = 562             # FDC brand turnover
ENERZAL_CR = 234
GLUCOND_CR = 1260             # ~32% of Zydus Wellness FY26 net sales of Rs 3,940 cr
KIRANA_TURNOVER_MO_LOW = 170_000    # CARE Ratings: Rs 20-25 lakh a year
KIRANA_TURNOVER_MO_HIGH = 208_000

# ---- the variable under test
SCENARIOS = {
    "Plan (3 boxes/outlet/mo)": 10.0,
    "Strong":                    5.0,
    "Base":                      2.5,
    "Slow":                      1.0,
}

# Glucon-D, the closest channel analogue, has "pronounced seasonality, peak in
# Q2/Q3". A flat 12-month run rate is not how this category sells.
SEASON_INDEX = {   # multiple of the annual average month
    "Peak (Apr-Jun, summer)": 2.0,
    "Shoulder":               1.0,
    "Trough (Nov-Jan)":       0.4,
}

OUTLETS_YEAR1 = 60_000
DAYS = 30


def cr(rupees):
    """Rupees -> crore."""
    return rupees / 1e7


def line(char="-", n=78):
    print(char * n)


def scenario(rate, outlets=OUTLETS_YEAR1):
    per_outlet_mo = rate * DAYS
    sachets_mo = per_outlet_mo * outlets
    return {
        "rate": rate,
        "per_outlet_mo": per_outlet_mo,
        "sachets_mo": sachets_mo,
        "sachets_yr": sachets_mo * 12,
        "rev_yr_cr": cr(sachets_mo * 12 * EX_FACTORY),
        "retail_yr_cr": cr(sachets_mo * 12 * MRP),
        "contrib_yr_gbp": sachets_mo * 12 * CONTRIBUTION / INR_GBP,
        "tonnes_mo": sachets_mo * 12 / 1000 / 1000,   # 12g sachets -> tonnes
        "retail_value_per_outlet_mo": per_outlet_mo * MRP,
    }


if __name__ == "__main__":
    line("=")
    print("  BGEP - THE DEMAND TEST".center(78))
    print("  Does a shop sell ten a day? - 10 Aug 2026".center(78))
    line("=")

    print("\nThe plan's year one is 60,000 outlets x 3 boxes of 100 a month.")
    print("60,000 outlets is 0.5% of India's ~13m kirana. That part is modest.")
    print("The aggressive number is the OTHER one: 10 sachets a day, every day,")
    print("as an AVERAGE across all 60,000.\n")

    line()
    print(f"{'Rate of sale':<26}{'/outlet/mo':>11}{'sachets/mo':>13}"
          f"{'tonnes/mo':>11}{'contrib/yr':>13}")
    line()
    for label, rate in SCENARIOS.items():
        s = scenario(rate)
        print(f"{label:<26}{s['per_outlet_mo']:>11,.0f}{s['sachets_mo']/1e6:>12.1f}m"
              f"{s['tonnes_mo']:>11,.0f}{'GBP '+format(s['contrib_yr_gbp']/1e6,'.1f')+'m':>13}")
    line()

    # ---------------------------------------------------------- TEST A
    print("\n\nTEST A - against the brands that already won this category")
    line()
    print("Year one revenue at each rate of sale, next to the incumbents.")
    print(f"  Electral (India's No.1 ORS, 50%+ share, selling since the 1970s)"
          f"   Rs {ELECTRAL_CR:,} cr")
    print(f"  Enerzal  (same owner, FDC)                                     "
          f"   Rs {ENERZAL_CR:,} cr")
    print(f"  Glucon-D (59% of glucose powder, ~90-year-old brand)           "
          f"   Rs {GLUCOND_CR:,} cr")
    print()
    for label, rate in SCENARIOS.items():
        s = scenario(rate)
        pct = s["rev_yr_cr"] / ELECTRAL_CR * 100
        print(f"  {label:<26} Rs {s['rev_yr_cr']:>6,.0f} cr   "
              f"= {pct:>5.0f}% of Electral, in year one")
    line()
    print("  Reading: the plan asks a brand with no distribution, no trade")
    print("  relationships and no factory to reach a quarter of Electral in")
    print("  twelve months. Nothing in Indian FMCG has done that.")

    # ---------------------------------------------------------- TEST B
    print("\n\nTEST B - against the size of the category itself")
    line()
    print(f"India's entire ORS category: Rs {ORS_CATEGORY_CR_LOW}-{ORS_CATEGORY_CR_HIGH} cr")
    print("(Cipla Health CEO, 2025. MAT grew Rs 334 cr in 2020 to Rs 716 cr in 2024.)\n")
    for label, rate in SCENARIOS.items():
        s = scenario(rate)
        lo = s["retail_yr_cr"] / ORS_CATEGORY_CR_HIGH * 100
        hi = s["retail_yr_cr"] / ORS_CATEGORY_CR_LOW * 100
        print(f"  {label:<26} Rs {s['retail_yr_cr']:>6,.0f} cr retail "
              f"= {lo:>4.0f}-{hi:<4.0f}% of the whole category")
    line()
    print("  Note: BGEP is positioned as a WANT, not a medical need, so the")
    print("  honest denominator is wider than ORS alone - ORS plus glucose")
    print(f"  powder is roughly Rs {ORS_CATEGORY_CR_HIGH + 2100:,} cr. Against THAT:")
    for label, rate in SCENARIOS.items():
        s = scenario(rate)
        print(f"    {label:<26} {s['retail_yr_cr']/(ORS_CATEGORY_CR_HIGH+2100)*100:>5.1f}%")

    # ---------------------------------------------------------- TEST C
    print("\n\nTEST C - against the shopkeeper's own P&L")
    line()
    print(f"A kirana turns over Rs {KIRANA_TURNOVER_MO_LOW:,}-{KIRANA_TURNOVER_MO_HIGH:,} "
          f"a month (CARE Ratings: Rs 20-25 lakh a year)")
    print("across 1,000-2,000 SKUs. What share of his month is our one sachet?\n")
    for label, rate in SCENARIOS.items():
        s = scenario(rate)
        v = s["retail_value_per_outlet_mo"]
        lo = v / KIRANA_TURNOVER_MO_HIGH * 100
        hi = v / KIRANA_TURNOVER_MO_LOW * 100
        print(f"  {label:<26} Rs {v:>6,.0f}/mo = {lo:>4.1f}-{hi:<4.1f}% of his turnover")
    line()
    print("  Reading: this is the test the plan PASSES. 1.4-1.8% of turnover on")
    print("  one SKU is high but not impossible for a hot-weather impulse line.")
    print("  A single good outlet in May can sell ten a day. The plan's problem")
    print("  is not physics at one shop, it is claiming that as the AVERAGE of")
    print("  60,000 shops for twelve straight months.")

    # ---------------------------------------------------------- SEASONALITY
    print("\n\nSEASONALITY - the flat run rate is wrong, and it is a factory question")
    line()
    print("Glucon-D's own reported seasonality is a Q2/Q3 peak. We are selling")
    print("heat relief. Applying a normal FMCG summer curve to the Base case:\n")
    base = scenario(SCENARIOS["Base"])
    for label, idx in SEASON_INDEX.items():
        m = base["sachets_mo"] * idx
        print(f"  {label:<26}{m/1e6:>7.1f}m sachets/mo   {m*12/1000/1000:>7,.0f} tonnes/mo")
    line()
    peak_plan = scenario(SCENARIOS["Plan (3 boxes/outlet/mo)"])["sachets_mo"] * 2.0
    print(f"  At the PLAN rate, a 2x summer peak is {peak_plan/1e6:.0f}m sachets in a month.")
    print("  We asked Halewood and Hindustan Foods to quote against 18m a month.")
    print("  Nobody has been asked for PEAK capacity, and peak is what a")
    print("  contract manufacturer has to reserve a line for.")

    # ---------------------------------------------------------- DISTRIBUTOR
    print("\n\nTHE DISTRIBUTOR HAS TO EAT - and at 8% he does not")
    line()
    print(f"Distributor earns Rs {DISTRIBUTOR_PER_SACHET:.2f} per sachet (8% of Rs 7.20).")
    print("A district distributor runs a van, a driver, a godown and 2-3 salesmen.")
    print("Call the cost of that Rs 1.5-2 lakh a month before he makes anything.\n")
    for label, rate in SCENARIOS.items():
        for outlets in (300, 1000):
            s = scenario(rate, outlets)
            gross = s["sachets_mo"] * DISTRIBUTOR_PER_SACHET
            if outlets == 300:
                print(f"  {label:<26}", end="")
            else:
                print(f"  {'':<26}", end="")
            print(f"{outlets:>5} outlets -> Rs {gross:>9,.0f}/mo gross "
                  f"({'viable' if gross > 200_000 else 'NOT viable alone'})")
    line()
    print("  Reading: below the plan rate, no distributor can live on BGEP alone.")
    print("  That is not fatal - it means we ride an EXISTING distributor's book")
    print("  as one line among many. But it breaks the premise of the scan app,")
    print("  which assumed a dedicated distributor we control end to end.")

    print()
    line("=")
    print("  WHAT THIS CHANGES THIS WEEK".center(78))
    line("=")
    print("""
  1. The RFQ to Halewood and Hindustan Foods asks for a single price at
     18m sachets a month. Ask instead for a PRICE LADDER at 2m / 5m / 10m
     / 18m, and separately for PEAK monthly capacity. Both quotes are still
     open, so this is a follow-up email, not a retraction.

  2. Rs 2.10 COGS is an estimate priced at 18m/month. At 3m/month it is
     higher, and every 50 paise is 12% of contribution. The ladder prices
     that risk instead of assuming it away.

  3. Year one should be built as outlets x rate of sale x season, not as a
     flat 3 boxes. The pilot's job is to measure rate of sale by outlet type
     and by month. That, not brand awareness, is what the GBP 50k buys.
""")
