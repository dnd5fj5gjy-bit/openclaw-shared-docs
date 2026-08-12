#!/usr/bin/env /usr/bin/python3
"""
BGEP - the fill weight decision, 12 August 2026.

Answers the OPEN line in section 9 of the product spec: 12 g or 21 g, and at what MRP.

WHAT IS QUOTED AND WHAT IS MODELLED. Nothing here is a manufacturer quote, because no
manufacturer has quoted. The Rs 2.10 at 12 g is Junior's build from Indian trade prices
(9 Aug). Every 21 g figure is that build re-scaled by the rules in scale_cogs() below,
which are stated so they can be argued with and replaced the moment Hindustan Foods
comes back with a real number.

Competitor MRPs ARE verified at source (PharmEasy / 1mg, 10 Aug 2026).

Re-run:  /usr/bin/python3 fill_weight.py
"""

import fx

# ----------------------------------------------------------------------------------
# 1. The trade structure. Unchanged from economics.py - same chain, same margins.
# ----------------------------------------------------------------------------------
GST = 0.18            # proprietary food, HSN 2106. Base case.
RETAILER_MARGIN = 0.15
DISTRIBUTOR_MARGIN = 0.08

# ----------------------------------------------------------------------------------
# 2. COGS at the 12 g reference, from economics.py
# ----------------------------------------------------------------------------------
COGS_12G = {
    "powder":    1.15,   # dextrose, salts, acidulant, flavour, vitamin C, sucralose
    "laminate":  0.55,   # film + fill/seal
    "outer":     0.22,   # box of 100 + shipper carton
    "freight":   0.18,   # inward freight + wastage
}
SECONDARY_FREIGHT_12G = 0.15
TRADE_SPEND_PCT = 0.03   # 3% of MRP - Rs 0.30 at Rs 10, scales with price not weight


def scale_cogs(grams):
    """Re-scale the 12 g cost build to another fill weight.

    Each line scales differently and the reason matters more than the number:

      powder    90% of the cost is dextrose and salts, which are bought by the kilo,
                so that part scales linearly with fill. The other 10% (flavour,
                vitamin C, sucralose, anticaking) is a DOSE, fixed per sachet
                whatever the fill, so it does not scale.

      laminate  A sachet is a flat 2D object. Film cost tracks AREA, not mass, so it
                scales at roughly the 0.7 power of the weight ratio. The fill/seal
                half of this line is machine time per sachet, which is flat - a
                21 g sachet does not take longer to make than a 12 g one.

      outer     Board on a box of 100 scales with surface area of a bigger volume,
                so weight ratio to the 2/3 power. Same 100 sachets either way.

      freight   Inward freight and wastage are both mass-driven. Linear.
    """
    r = grams / 12.0
    return {
        "powder":   COGS_12G["powder"] * (0.90 * r + 0.10),
        "laminate": COGS_12G["laminate"] * (0.50 * r ** 0.7 + 0.50),
        "outer":    COGS_12G["outer"] * r ** (2 / 3),
        "freight":  COGS_12G["freight"] * r,
    }


def unit_economics(grams, mrp):
    """Full chain from shelf price back to our contribution, per sachet."""
    cogs = scale_cogs(grams)
    cogs_total = sum(cogs.values())

    net_of_gst = mrp / (1 + GST)
    retailer_buys = net_of_gst * (1 - RETAILER_MARGIN)
    we_receive = retailer_buys * (1 - DISTRIBUTOR_MARGIN)

    secondary_freight = SECONDARY_FREIGHT_12G * (grams / 12.0)
    trade_spend = mrp * TRADE_SPEND_PCT

    contribution = we_receive - cogs_total - secondary_freight - trade_spend

    return {
        "grams": grams, "mrp": mrp,
        "cogs_lines": cogs, "cogs": cogs_total,
        "net_of_gst": net_of_gst,
        "retailer_buys": retailer_buys,
        "we_receive": we_receive,
        "secondary_freight": secondary_freight,
        "trade_spend": trade_spend,
        "contribution": contribution,
        "margin_on_receipt": contribution / we_receive,
        "margin_on_mrp": contribution / mrp,
        "rs_per_gram": mrp / grams,
        "retailer_earns_per_box": (net_of_gst - retailer_buys) * 100,
        "distributor_earns_per_box": (retailer_buys - we_receive) * 100,
        "we_earn_per_box": contribution * 100,
    }


# ----------------------------------------------------------------------------------
# 3. Serve size. This is the half of the decision that is not financial.
# ----------------------------------------------------------------------------------
# From the product spec, 11 Aug: per 12 g sachet the finished drink carries approx.
# 355 mg sodium and 9.1 g glucose, targeted at 200-240 mOsm/kg in 400 ml.
NA_MG_PER_12G = 355.0
GLUCOSE_G_PER_12G = 9.1
OSMO_AT_400ML = 220.0     # midpoint of the 200-240 spec target

PLASMA_OSMO = 285.0       # mOsm/kg - below this is hypotonic
WHO_ORS_NA_MMOL = 75.0    # mmol/l - the therapeutic benchmark we deliberately sit under
SPORTS_DRINK_NA_MMOL = 20.0


def serve(grams, volume_ml):
    """What the drink actually is at a given fill and a given volume of water."""
    r = grams / 12.0
    na_mg = NA_MG_PER_12G * r
    na_mmol_l = (na_mg / 23.0) / (volume_ml / 1000.0)   # 23 g/mol sodium
    # Osmolality is proportional to solute mass and inversely to water volume.
    osmo = OSMO_AT_400ML * r / (volume_ml / 400.0)
    return {
        "grams": grams, "volume_ml": volume_ml,
        "na_mg": na_mg, "na_mmol_l": na_mmol_l,
        "glucose_pct": (GLUCOSE_G_PER_12G * r) / volume_ml * 100,
        "osmo": osmo,
        "hypotonic": osmo < PLASMA_OSMO,
    }


# ----------------------------------------------------------------------------------
# 4. The shelf, verified at source 10 Aug 2026
# ----------------------------------------------------------------------------------
COMPETITORS = [
    ("Electral (FDC)",        21.8, 23.05),
    ("Electral unit dose",     4.4,  4.65),
    ("Cipla Prolyte",         21.0, 22.26),
]

# Base-case planning volume from the 10 Aug demand test: 2.5 sachets/outlet/day across
# 60,000 outlets = 4.5m sachets/month.
YEAR1_SACHETS_PER_MONTH = 4_500_000
YEAR1_SACHETS_PER_YEAR = YEAR1_SACHETS_PER_MONTH * 12


def rs_cr(rupees):
    """Rupees -> crore (10 million), how Indian counterparties will read it."""
    return rupees / 10_000_000


def line(ch="-", n=86):
    print(ch * n)


def main():
    print("=" * 86)
    print("  BGEP - FILL WEIGHT DECISION MODEL")
    print("  12 August 2026 ·", fx.fx_note())
    print("=" * 86)

    # --- The options -------------------------------------------------------------
    options = [
        ("A", 12, 10, "The plan of record. Impulse price, street channel."),
        ("B", 21, 10, "21 g held at Rs 10. What the 21 g mockups imply if MRP does not move."),
        ("C", 21, 20, "21 g repriced head-on with Electral's 21.8 g pack."),
        ("D", 21, 15, "21 g at the midpoint. Included for completeness."),
    ]

    print("\n--- THE FOUR WAYS THIS CAN GO ---\n")
    hdr = f"{'':3}{'Fill':>6} {'MRP':>7} {'Rs/g':>7} {'COGS':>7} {'We get':>8} {'Contrib':>9} {'% recpt':>8}"
    print(hdr)
    line()
    results = {}
    for tag, g, mrp, _ in options:
        e = unit_economics(g, mrp)
        results[tag] = e
        print(f"{tag:3}{g:>5}g {mrp:>6.0f} {e['rs_per_gram']:>7.2f} "
              f"{e['cogs']:>7.2f} {e['we_receive']:>8.2f} {e['contribution']:>9.2f} "
              f"{e['margin_on_receipt']*100:>7.1f}%")
    line()
    for tag, g, mrp, note in options:
        print(f"  {tag}: {note}")

    # --- Cost of moving to 21 g at the same price --------------------------------
    a, b = results["A"], results["B"]
    delta = a["contribution"] - b["contribution"]
    print("\n\n--- WHAT 21 g AT Rs 10 ACTUALLY COSTS (option A -> B) ---\n")
    print(f"  Contribution per sachet   Rs {a['contribution']:.2f}  ->  Rs {b['contribution']:.2f}")
    print(f"  Lost per sachet           Rs {delta:.2f}   ({delta/a['contribution']*100:.0f}% of contribution)")
    print(f"  Margin on our receipt     {a['margin_on_receipt']*100:.1f}%  ->  {b['margin_on_receipt']*100:.1f}%")
    print()
    print("  COGS line by line:")
    print(f"    {'':22}{'12 g':>9}{'21 g':>9}{'delta':>9}")
    for k in COGS_12G:
        print(f"    {k:22}{a['cogs_lines'][k]:>9.2f}{b['cogs_lines'][k]:>9.2f}"
              f"{b['cogs_lines'][k]-a['cogs_lines'][k]:>9.2f}")
    print(f"    {'TOTAL':22}{a['cogs']:>9.2f}{b['cogs']:>9.2f}{b['cogs']-a['cogs']:>9.2f}")

    annual = delta * YEAR1_SACHETS_PER_YEAR
    print(f"\n  At the base-case year-one run rate ({YEAR1_SACHETS_PER_YEAR/1e6:.0f}m sachets/yr):")
    print(f"    Rs {rs_cr(annual):.2f} crore of contribution a year, "
          f"GBP {fx.gbp(annual):,.0f}")
    print("    Every sachet sold at 21 g for Rs 10 is a sachet sold at a "
          f"{delta/a['contribution']*100:.0f}% discount to plan.")

    # --- Breakeven on the repriced option ----------------------------------------
    c = results["C"]
    ratio = a["contribution"] / c["contribution"]
    print("\n\n--- OPTION C: 21 g AT Rs 20. MORE PER SACHET, FEWER SACHETS ---\n")
    print(f"  Contribution per sachet   Rs {a['contribution']:.2f} (A)  ->  Rs {c['contribution']:.2f} (C)")
    print(f"  C earns {c['contribution']/a['contribution']:.2f}x per sachet, so it only needs "
          f"{ratio*100:.0f}% of A's volume to match it.")
    print(f"  Per gram we would sit at Rs {c['rs_per_gram']:.2f} against the category's Rs 1.06,")
    print(f"  i.e. {(1 - c['rs_per_gram']/1.06)*100:.0f}% cheaper - against "
          f"{(1 - a['rs_per_gram']/1.06)*100:.0f}% cheaper at option A.")
    print("\n  The catch is not in this table. Rs 20 is not an impulse price in the")
    print("  informal channel, and the entire 60,000-outlet thesis is an impulse thesis.")

    # --- What each link earns ----------------------------------------------------
    print("\n\n--- WHO EARNS WHAT, PER BOX OF 100 ---\n")
    print(f"  {'':3}{'Retailer':>12}{'Distributor':>14}{'Us':>10}")
    line()
    for tag in ("A", "B", "C", "D"):
        e = results[tag]
        print(f"  {tag:3}{e['retailer_earns_per_box']:>12,.0f}"
              f"{e['distributor_earns_per_box']:>14,.0f}{e['we_earn_per_box']:>10,.0f}")
    print("\n  The distributor viability floor from the 6 Aug model is ~Rs 52,000/month.")
    for tag in ("A", "C"):
        e = results[tag]
        boxes = 52_000 / e["distributor_earns_per_box"]
        print(f"    Option {tag}: needs {boxes:,.0f} boxes/month to clear it "
              f"({boxes*100/75:,.0f} outlets at 2.5/day)")

    # --- The serve size question -------------------------------------------------
    print("\n\n--- THE HALF OF THIS THAT IS NOT FINANCIAL: WHAT ONE SACHET MAKES ---\n")
    print(f"  {'Fill':>6}{'Water':>9}{'Sodium':>10}{'Na mmol/l':>12}{'Glucose':>10}{'mOsm/kg':>10}  verdict")
    line()
    cases = [
        (12, 400, "spec target. A bottle."),
        (12, 500, "a standard Indian water bottle."),
        (12, 1000, "what the mockups print. Flavoured water."),
        (21, 700, "a bottle and a half. Awkward."),
        (21, 1000, "a litre jug. The Electral serve."),
    ]
    for g, ml, note in cases:
        s = serve(g, ml)
        print(f"  {g:>5}g{ml:>8}ml{s['na_mg']:>9.0f}mg{s['na_mmol_l']:>12.1f}"
              f"{s['glucose_pct']:>9.2f}%{s['osmo']:>10.0f}  {note}")
    line()
    print(f"  Benchmarks: WHO ORS {WHO_ORS_NA_MMOL:.0f} mmol/l sodium · sports drink "
          f"~{SPORTS_DRINK_NA_MMOL:.0f} · plasma {PLASMA_OSMO:.0f} mOsm/kg")
    print("\n  THE FINDING. 12 g in a litre lands at "
          f"{serve(12,1000)['osmo']:.0f} mOsm/kg and "
          f"{serve(12,1000)['na_mmol_l']:.0f} mmol/l sodium.")
    print("  That is below a sports drink on salt and roughly a third of the spec's own")
    print("  osmolality target. The pack line '1 sachet = 1 litre' and the 12 g fill")
    print("  cannot both be true. Only 21 g makes a credible litre.")

    # --- The shelf ---------------------------------------------------------------
    print("\n\n--- THE SHELF, MRPs VERIFIED AT SOURCE 10 AUG 2026 ---\n")
    print(f"  {'Product':<26}{'Pack':>8}{'MRP':>9}{'Rs/gram':>10}")
    line()
    for name, g, mrp in COMPETITORS:
        print(f"  {name:<26}{g:>7.1f}g{mrp:>9.2f}{mrp/g:>10.2f}")
    for tag in ("A", "C"):
        e = results[tag]
        print(f"  {'BGEP option ' + tag:<26}{e['grams']:>7.1f}g{e['mrp']:>9.2f}"
              f"{e['rs_per_gram']:>10.2f}")
    line()

    # --- The overfill audit line -------------------------------------------------
    print("\n\n--- WHY FILL TOLERANCE IS A MONEY QUESTION, NOT A QA ONE ---\n")
    for g in (12, 21):
        powder_per_g = scale_cogs(g)["powder"] / g
        for pct in (0.02,):
            cost = powder_per_g * g * pct
            print(f"  {g} g fill, {pct*100:.0f}% systematic overfill: "
                  f"Rs {cost:.3f}/sachet = Rs {rs_cr(cost*YEAR1_SACHETS_PER_YEAR):.2f} cr/yr "
                  f"(GBP {fx.gbp(cost*YEAR1_SACHETS_PER_YEAR):,.0f})")
    print("\n  This is why the spec asks the factory to state its fill tolerance and how it")
    print("  is verified in line. At Rs 10 retail nobody notices 2%, and it is a salary.")

    # --- Recommendation ----------------------------------------------------------
    print("\n\n" + "=" * 86)
    print("  RECOMMENDATION")
    print("=" * 86)
    print(f"""
  FILL WEIGHT:  12 g, at Rs 10.  Option A. Unchanged, now with the arithmetic behind it.

    Holding 21 g at Rs 10 costs Rs {delta:.2f} a sachet, {delta/a['contribution']*100:.0f}% of contribution,
    GBP {fx.gbp(annual):,.0f} a year at the base case. That option is simply worse.

    Repricing to Rs 20 (option C) is a real business and a different one. It earns
    Rs {c['contribution']:.2f} a sachet and needs only {ratio*100:.0f}% of the volume, but it buys a fight
    on Electral's shelf, at Electral's pack size, at Electral's price, with no brand
    history and no medical channel - and it abandons the impulse thesis the whole
    60,000-outlet plan is built on. Not for the pilot. Worth revisiting as SKU 2.

  FLAVOUR:  Lime and salt (nimbu). Option A in spec section 6.

    Jesse already chose it once by picking the nimbu pack on 6 Aug. It carries the
    700 mg of salt without the salt reading as a fault, which orange does not, and
    a hypotonic drink has less sugar than the palate expects at this price - so the
    flavour has to do work the sweetness cannot. Order samples of both anyway; the
    sip test is cheap and taste is the repeat-purchase driver.

  THE THING TO FIX TODAY EITHER WAY:

    The artwork in circulation prints NET WT 21 g and '1 sachet = 1 litre'. Both are
    wrong at 12 g. The pack has to read 500 ml, or one bottle. Nobody has started the
    artwork, so this costs nothing now and costs a print run later.
""")
    print("=" * 86)
    print("  Junior · Bear Grylls Ventures · 12 August 2026")
    print("  COGS scaling is MODELLED, not quoted. Replace on the first real factory number.")
    print("=" * 86)


if __name__ == "__main__":
    main()
