#!/usr/bin/env python3
"""
Bear Grylls Everest Power - unit economics model.
Built 6 Aug 2026. All figures in INR unless stated.

REVISED 11 Aug 2026, two corrections:
  1. FX now imported from fx.py, verified at source. This file previously carried
     INR_GBP = 106.0 while setup_costs.py had been corrected to the real rate, so
     every GBP figure below was 21% too high.
  2. The scale table ran on 10 sachets/outlet/day, which the demand test of 10 Aug
     established is about four times too high as a twelve-month average. The base
     case is now 2.5/day and 10/day is shown as the bull case, clearly labelled.

Sources for the anchors used here are listed in PLAN.md. Everything below the
"ASSUMPTION" label is our estimate and needs a real quote before it goes in a deck
that asks anyone for money.
"""

from fx import INR_GBP, INR_USD, fx_note


def money(x):
    return f"Rs {x:,.2f}"


# ---------------------------------------------------------------- INPUTS
MRP = 10.00          # consumer price per sachet, GST-inclusive. The India impulse price point.
SACHET_G = 12.0      # grams of powder, makes 300-500ml

# GST is the single biggest swing in this model. Three possible classifications:
GST_SCENARIOS = {
    "ORS / drug (HSN 3004)": 0.00,
    "Proprietary food (HSN 2106)": 0.18,
    "Caffeinated beverage (post 22 Sep 2025)": 0.40,
}

# Channel margins - India FMCG norms
RETAILER_MARGIN = 0.15    # kirana, packaged FMCG band is 8-15%; we pay top of band to buy shelf
DISTRIBUTOR_MARGIN = 0.08  # district distributor, norm is 4-8%
SUPERSTOCKIST_MARGIN = 0.03  # state-level, only where we use one

# ASSUMPTION - COGS. Anchor: 21.8g ORS sachet trades at Rs 4.65-6.00 all-in on IndiaMART,
# which already carries the manufacturer's and the trader's margin. A 12g sachet at volume:
COGS = {
    "powder (dextrose, salts, acidulant, flavour, vits)": 1.15,
    "sachet laminate + fill": 0.55,
    "outer box of 100 + carton": 0.22,
    "inward freight + wastage": 0.18,
}
COGS_TOTAL = sum(COGS.values())

# No brand royalty. Jesse, 7 Aug 2026: BGV owns Everest Power outright, so the Bear
# Grylls mark is not licensed in from anyone and there is no royalty line. Earlier
# versions of this model carried a 5% placeholder (HISTORICAL, 6-7 Aug 2026).
SECONDARY_FREIGHT = 0.15  # per sachet, to distributor
TRADE_SPEND = 0.30        # per sachet, distributor incentives + scheme + app rewards


def chain(mrp, gst_rate, use_superstockist=False):
    """Work backwards from MRP to our ex-factory price."""
    net_mrp = mrp / (1 + gst_rate)
    retailer_buys = net_mrp * (1 - RETAILER_MARGIN)
    distributor_buys = retailer_buys * (1 - DISTRIBUTOR_MARGIN)
    if use_superstockist:
        our_price = distributor_buys * (1 - SUPERSTOCKIST_MARGIN)
    else:
        our_price = distributor_buys
    return net_mrp, retailer_buys, distributor_buys, our_price


def pnl(mrp, gst_rate, use_superstockist=False):
    net_mrp, ret, dist, ours = chain(mrp, gst_rate, use_superstockist)
    variable = COGS_TOTAL + SECONDARY_FREIGHT + TRADE_SPEND
    contribution = ours - variable
    return {
        "net_mrp": net_mrp, "retailer_buys": ret, "distributor_buys": dist,
        "our_price": ours, "cogs": COGS_TOTAL,
        "freight": SECONDARY_FREIGHT, "trade": TRADE_SPEND,
        "contribution": contribution,
        "margin_pct": contribution / ours * 100 if ours else 0,
    }


if __name__ == "__main__":
    print("=" * 74)
    print("  BEAR GRYLLS EVEREST POWER - unit economics, 6 Aug 2026")
    print(f"  MRP {money(MRP)} per {SACHET_G:.0f}g sachet")
    print("=" * 74)

    print(f"\nCOGS build ({money(COGS_TOTAL)} per sachet):")
    for k, v in COGS.items():
        print(f"    {k:<48} {money(v)}")
    print(f"    {'TOTAL':<48} {money(COGS_TOTAL)}")

    print("\n--- GST classification is worth up to 40 points of margin ---\n")
    print(f"{'Classification':<42}{'We get':>10}{'Contrib':>10}{'Margin':>9}")
    for label, rate in GST_SCENARIOS.items():
        p = pnl(MRP, rate)
        print(f"{label:<42}{money(p['our_price']):>10}"
              f"{money(p['contribution']):>10}{p['margin_pct']:>8.1f}%")

    # Base case: proprietary food at 18%
    base = pnl(MRP, 0.18)
    print("\n--- BASE CASE: proprietary food, 18% GST, no caffeine ---")
    print(f"  Consumer pays                 {money(MRP)}")
    print(f"  Net of GST                    {money(base['net_mrp'])}")
    print(f"  Retailer buys at              {money(base['retailer_buys'])}  (15% to the shop)")
    print(f"  Distributor buys at           {money(base['distributor_buys'])}  (8% to the distributor)")
    print(f"  WE RECEIVE                    {money(base['our_price'])}")
    print(f"    less COGS                  -{money(base['cogs'])}")
    print(f"    less secondary freight     -{money(base['freight'])}")
    print(f"    less trade spend           -{money(base['trade'])}")
    print(f"  CONTRIBUTION                  {money(base['contribution'])}"
          f"   ({base['margin_pct']:.1f}%)")

    # What a box and a distributor look like
    print("\n--- WHAT EACH LINK IN THE CHAIN ACTUALLY EARNS ---")
    box = 100
    print(f"  Box of {box} sachets:")
    print(f"    Retailer pays distributor   {money(base['retailer_buys'] * box)}")
    print(f"    Retailer sells for          {money(MRP * box)} (before GST {money(base['net_mrp']*box)})")
    print(f"    Retailer makes              {money((base['net_mrp'] - base['retailer_buys']) * box)} per box")
    print(f"    Distributor makes           {money((base['retailer_buys'] - base['distributor_buys']) * box)} per box")
    print(f"    We make                     {money(base['contribution'] * box)} per box")

    print("\n--- DISTRIBUTOR VIABILITY: is this a job worth having? ---")
    for outlets, spb in [(150, 2), (300, 3), (500, 4)]:
        boxes_month = outlets * spb
        gp = (base['retailer_buys'] - base['distributor_buys']) * box * boxes_month
        print(f"  {outlets} outlets x {spb} boxes/mo = {boxes_month:,} boxes"
              f"  ->  {money(gp)}/mo gross to distributor "
              f"(GBP {gp/INR_GBP:,.0f})")

    print("\n--- SCALE: what the brand earns ---")
    print("  BASE CASE, 2.5 sachets per outlet per day (75 a month).")
    print("  This is the corrected planning rate from the demand test of 10 Aug 2026.\n")
    for rate_label, per_day in [("BASE  2.5/outlet/day", 2.5), ("BULL 10.0/outlet/day", 10.0)]:
        print(f"  {rate_label}")
        for label, outlets in [("Pilot: 1 state", 5_000),
                               ("Year 1: 5 states", 60_000),
                               ("Year 3: national", 400_000)]:
            sachets = outlets * per_day * 30
            rev = sachets * base['our_price']
            contrib = sachets * base['contribution']
            print(f"    {label:<20} {outlets:>7,} outlets  "
                  f"{sachets/1e6:>6.1f}m sachets/mo  "
                  f"rev {money(rev/1e7)} cr/mo  "
                  f"contrib GBP {contrib*12/INR_GBP/1e6:>5.2f}m/yr")
        print()

    print("  The load-bearing assumption in every line above is the rate of sale.")
    print("  10 a day out of one shop is what the pitch assumed; as a twelve-month")
    print("  average across 60,000 shops it implies a quarter of Electral's business")
    print("  in year one, so it is a bull case and not a plan. Prove or kill the real")
    print("  number in the pilot before anything else in this model matters.")
    print(f"\n  {fx_note()}")
    print()
