#!/usr/bin/env /usr/bin/python3
"""Everest Power - the downside Raemy asked for, 10 Aug 2026.

She asked (10 Aug 17:34): "the contribution margin / cost of goods / distribution costs
are the matters we will firm up on once we've had calls from manufacturers / distributors
etc. I think it would be useful just to do a downside and take the margin down a bit."

So this flexes exactly those three, and nothing else. Volume is held at the corrected
planning case (2.5 sachets/outlet/day) except in the last table, which crosses the two.

EVERY COGS AND MARGIN FIGURE HERE IS AN ESTIMATE. No manufacturer has quoted and no
distributor has signed. That is the whole reason for the exercise.
"""
INR_GBP = 106.0
MRP     = 10.00
GST     = 0.18      # proprietary food, HSN 2106, no caffeine

def contribution(cogs, retailer_pct, dist_pct, freight, trade):
    """Rs of contribution per sachet, working down from the shelf price."""
    net_of_gst  = MRP / (1 + GST)
    retail_buy  = net_of_gst * (1 - retailer_pct)
    we_receive  = retail_buy * (1 - dist_pct)
    return we_receive - cogs - freight - trade, we_receive

#            label                       COGS  retail  dist  freight trade
CASES = [
    ("Plan, as pitched",                  2.10, 0.15, 0.08, 0.15, 0.30),
    ("Downside 1 - COGS only",            2.75, 0.15, 0.08, 0.15, 0.30),
    ("Downside 2 - trade terms only",     2.10, 0.18, 0.10, 0.20, 0.50),
    ("Downside 3 - both",                 2.75, 0.18, 0.10, 0.20, 0.50),
    ("Stress - both, harder",             3.25, 0.20, 0.12, 0.25, 0.60),
]

VOLUMES = [   # sachets/month, and where the number comes from
    ("Plan  10/outlet/day",  18_000_000),
    ("Base   2.5/day",        4_500_000),
    ("Low    1.5/day",        2_700_000),
]

def money(rs_per_sachet, per_month):
    return rs_per_sachet * per_month * 12 / INR_GBP

if __name__ == "__main__":
    print("EVEREST POWER - MARGIN DOWNSIDE".center(78))
    print(f"MRP Rs {MRP:.2f} per 12g sachet, GST {GST:.0%} (proprietary food, no caffeine)\n")

    print(f"  {'Case':<32}{'COGS':>6}{'We get':>9}{'Contrib':>9}{'Margin':>8}"
          f"{'  Yr at Base':>13}")
    print("  " + "-" * 76)
    base_vol = VOLUMES[1][1]
    for label, cogs, r, d, f, t in CASES:
        contrib, we_receive = contribution(cogs, r, d, f, t)
        print(f"  {label:<32}{cogs:>6.2f}{we_receive:>9.2f}{contrib:>9.2f}"
              f"{contrib/(MRP/(1+GST)):>7.0%}"
              f"{'  GBP ' + format(money(contrib, base_vol)/1e6, '.2f') + 'm':>13}")

    print("\n  Base = 2.5 sachets/outlet/day across 60,000 outlets = 4.5m sachets/month.")
    print("  'Margin' is contribution over the GST-exclusive shelf price, not over what we receive.\n")

    print("  VOLUME x MARGIN - annual contribution, GBP m")
    print(f"  {'':<22}" + "".join(f"{lbl.split()[0]:>12}" for lbl, _, _, _, _, _ in CASES))
    print("  " + "-" * 76)
    for vlabel, vol in VOLUMES:
        row = f"  {vlabel:<22}"
        for label, cogs, r, d, f, t in CASES:
            c, _ = contribution(cogs, r, d, f, t)
            row += f"{money(c, vol)/1e6:>12.2f}"
        print(row)

    plan, _  = contribution(*[c for c in CASES[0][1:]])
    worst, _ = contribution(*[c for c in CASES[4][1:]])
    print(f"\n  The spread on margin alone is Rs {plan:.2f} to Rs {worst:.2f} per sachet, "
          f"a {1 - worst/plan:.0%} cut.")
    print(f"  Crossed with volume, the range on year-one contribution is "
          f"GBP {money(worst, VOLUMES[2][1])/1e6:.2f}m to GBP {money(plan, VOLUMES[0][1])/1e6:.2f}m.")
    print("\n  What would actually move these numbers, in order:")
    print("   1. The manufacturer's price. Rs 2.10 is our estimate; nobody has quoted.")
    print("      Every 50 paise of error is 12% of contribution at the plan margin.")
    print("   2. What the distributor takes. 8% is what we have assumed, not agreed.")
    print("   3. GST classification. Proprietary food at 18% is the prudent read;")
    print("      an ORS/drug classification would be worth ~6 points of margin and")
    print("      FSSAI has banned 'ORS' on labels anyway.")
