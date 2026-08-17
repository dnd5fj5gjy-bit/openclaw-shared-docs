#!/usr/bin/env python3
"""
Modern Savage - Australasia: LICENCE vs EXPORT
Runnable model. Junior, 17 August 2026.

Every input is tagged. Re-run this rather than quoting the numbers from memory.

  VERIFIED - opened the primary source myself, on the date shown
  QUOTED   - a counterparty put it in writing to us
  ESTIMATE - my assumption, defensible, not sourced. Change it and re-run.
  UNKNOWN  - load-bearing and nobody has it. Listed at the end.

Usage:  python3 model.py
        python3 model.py --royalty 0.10 --rrp 129
"""

import argparse

# ---------------------------------------------------------------------------
# FX
# ---------------------------------------------------------------------------
GBP_AUD = 1.9114        # VERIFIED 17 Aug 2026 01:15 BST, frankfurter/ECB, rate dated 14 Aug
USD_AUD = 1.412876      # VERIFIED 17 Aug 2026 01:15 BST, open.er-api.com, dated 16 Aug
GBP_USD = 1.3537        # VERIFIED same call

# ---------------------------------------------------------------------------
# What the product costs us to make, today, in Florida
# ---------------------------------------------------------------------------
# VERIFIED - Lightning Nutra / ACF invoice S1825, per-SKU, not the blended $21.33
COGS_USD = {"adult": 24.45, "mini": 22.28, "summit": 18.90}
SKU = "adult"                       # the adult pouch is the launch SKU and the worst of the three
COGS_AUD = COGS_USD[SKU] * USD_AUD

# ---------------------------------------------------------------------------
# What it should retail for in Australia
# ---------------------------------------------------------------------------
# UK subscribed price is GBP 55 (VERIFIED on modernsavage.co, 16 Aug 2026).
# At 1.9114 that is A$105.13. AG1 in Australia is A$120/mo for 30 servings
# (SOURCED, secondary - thebircherbar.com.au review, Aug 2026).
# A$109 inc GST sits at UK parity and ~9% under AG1. This is the model's RRP.
RRP_INC_GST = 109.00                # ESTIMATE, anchored on two verified reference points
GST = 0.10                          # VERIFIED - Australian GST, statutory
NET_SALES = RRP_INC_GST / (1 + GST)  # royalties are struck on net sales, ex-GST

# ---------------------------------------------------------------------------
# ROUTE A - EXPORT. We make it in Florida, an Australian partner buys and sells it.
# ---------------------------------------------------------------------------
# What the partner pays us, as a share of net RRP. Two channel shapes:
PARTNER_BUYS_AT_D2C    = 0.42       # ESTIMATE - partner sells direct, one margin to fund
PARTNER_BUYS_AT_RETAIL = 0.32       # ESTIMATE - partner must also fund a retailer's 40%+

# Cost of getting a pouch from Pompano Beach to an Australian warehouse.
FREIGHT_AUD    = 1.20               # ESTIMATE - FCL sea, FL->Sydney, ~11k pouches/20ft at
                                    #   USD 4,500-7,000 (SOURCED range, no quote obtained)
IMPORT_AUD     = 1.60               # ESTIMATE - BICON permit, US health certification,
                                    #   border inspection as a risk food, broker, amortised
EXPORT_ADMIN_AUD = 0.50             # ESTIMATE - insurance, docs, FX spread

LANDED_COST_AUD = COGS_AUD + FREIGHT_AUD + IMPORT_AUD + EXPORT_ADMIN_AUD

# ---------------------------------------------------------------------------
# ROUTE B - LICENCE. They make it in Australia. We take a royalty on net sales.
# ---------------------------------------------------------------------------
ROYALTY = 0.08                      # ESTIMATE - food & beverage trademark licensing runs
                                    #   2.5%-6% of sales (SOURCED, RoyaltyRange / Goldstein).
                                    #   8% reflects a named founder, not just a mark.
LOCAL_COGS_AUD = 36.00              # ESTIMATE - AU co-packer, 658g pouch, this deck, low volume.
                                    #   No quote held. This is the number to replace first.

# What it costs us to support a licensee, per year, either way
BRAND_SUPPORT_AUD = 25_000          # ESTIMATE - QA, artwork, Bear asset access, one paid
                                    #   Australian food-law opinion in year one

# ---------------------------------------------------------------------------
# Volumes to test
# ---------------------------------------------------------------------------
VOLUMES = [500, 1500, 4000]         # pouches per month. UNKNOWN - no AU demand data exists.


def money(x):
    return f"A${x:,.2f}"


def run(royalty, rrp_inc_gst):
    net = rrp_inc_gst / (1 + GST)
    landed = LANDED_COST_AUD

    print("=" * 78)
    print("  MODERN SAVAGE - AUSTRALASIA: LICENCE vs EXPORT")
    print("  Junior, 17 Aug 2026.  Adult pouch, 658g, 28 servings.")
    print("=" * 78)

    print(f"\nRRP inc GST                 {money(rrp_inc_gst)}")
    print(f"Net sales (ex 10% GST)      {money(net)}")
    print(f"Per serving                 {money(rrp_inc_gst / 28)}   "
          f"(AG1 Australia: A$4.01)")
    print(f"Our COGS, Florida           {money(COGS_AUD)}   (USD {COGS_USD[SKU]:.2f} @ {USD_AUD})")

    # ---- Route A ----------------------------------------------------------
    print("\n" + "-" * 78)
    print("  ROUTE A - EXPORT finished goods from Florida")
    print("-" * 78)
    print(f"Landed cost to us           {money(landed)}")
    print(f"  COGS {money(COGS_AUD)} + freight {money(FREIGHT_AUD)} "
          f"+ import/permit {money(IMPORT_AUD)} + admin {money(EXPORT_ADMIN_AUD)}")

    export_rows = []
    for label, share in (("partner sells D2C only", PARTNER_BUYS_AT_D2C),
                         ("partner also supplies retail", PARTNER_BUYS_AT_RETAIL)):
        price_to_partner = net * share
        contribution = price_to_partner - landed
        export_rows.append((label, share, price_to_partner, contribution))
        print(f"\n  {label}  (partner buys at {share:.0%} of net)")
        print(f"    They pay us              {money(price_to_partner)}")
        print(f"    We keep                  {money(contribution)}"
              f"   {'  <-- NEGATIVE' if contribution < 0 else ''}")
        print(f"    As % of RRP              {contribution / rrp_inc_gst:.1%}")

    # ---- Route B ----------------------------------------------------------
    print("\n" + "-" * 78)
    print("  ROUTE B - LICENCE, made in Australia, royalty on net sales")
    print("-" * 78)
    for r in (0.05, royalty, 0.10):
        print(f"  Royalty {r:>5.1%}  ->  we keep {money(net * r)} per pouch"
              f"   ({(net * r) / rrp_inc_gst:.1%} of RRP)")

    # ---- The breakeven ----------------------------------------------------
    d2c_contribution = export_rows[0][3]
    breakeven = d2c_contribution / net
    print("\n" + "-" * 78)
    print("  THE BREAKEVEN")
    print("-" * 78)
    print(f"  Exporting to a D2C partner earns us {money(d2c_contribution)} a pouch.")
    print(f"  A licence matches that at a royalty of {breakeven:.1%} of net sales.")
    print(f"  Published food & beverage trademark licensing band: 2.5% - 6%.")
    if breakeven < 0.06:
        print(f"  -> {breakeven:.1%} is INSIDE the ordinary market band, so a")
        print( "     normal licence beats exporting before any risk is priced in.")
    retail = export_rows[1][3]
    if retail < 0:
        print(f"\n  And to reach shelves, export runs at {money(retail)} a pouch.")
        print( "     Export cannot fund the retail channel at all. A licence can.")

    # ---- Annualised -------------------------------------------------------
    print("\n" + "-" * 78)
    print("  ANNUAL, BY VOLUME  (contribution to us, before brand support)")
    print("-" * 78)
    print(f"  {'pouches/mo':>11} {'EXPORT (D2C)':>15} {'LICENCE @' + f'{royalty:.0%}':>15} "
          f"{'cash we tie up':>16}")
    for v in VOLUMES:
        yr = v * 12
        exp = yr * d2c_contribution
        lic = yr * net * royalty
        # cash: one production run of cover, at 3 months, paid before revenue
        cash = v * 3 * COGS_AUD
        print(f"  {v:>11,} {money(exp):>15} {money(lic):>15} "
              f"{money(cash) + ' / 0':>16}")
    print(f"\n  Brand support costs us {money(BRAND_SUPPORT_AUD)}/yr under EITHER route.")
    print( "  The cash column is the point: the licence column is earned on")
    print( "  someone else's balance sheet.")

    # ---- Does the licensee make money? ------------------------------------
    print("\n" + "-" * 78)
    print("  CAN THE LICENSEE LIVE ON IT?  (a deal they lose on will not close)")
    print("-" * 78)
    fulfil = 8.00   # ESTIMATE - AU 3PL, pick/pack/post a 750g parcel
    cac = 25.00     # ESTIMATE - blended acquisition cost per pouch sold
    lic_partner = net - LOCAL_COGS_AUD - (net * royalty) - fulfil - cac
    exp_partner = net - (net * PARTNER_BUYS_AT_D2C) - fulfil - cac
    print(f"  Under a LICENCE (they make it):  {money(lic_partner)} a pouch  "
          f"({lic_partner / net:.0%} of net)")
    print(f"    net {money(net)} - local COGS {money(LOCAL_COGS_AUD)} "
          f"- royalty {money(net * royalty)} - fulfilment {money(fulfil)} - CAC {money(cac)}")
    print(f"  Under EXPORT (they buy from us): {money(exp_partner)} a pouch  "
          f"({exp_partner / net:.0%} of net)")
    print(f"    and they carry the import permit, the border inspection and a 12-week lead.")
    gap = exp_partner - lic_partner
    print(f"\n  Difference to them: {money(abs(gap))} a pouch "
          f"({'export better' if gap > 0 else 'licence better'}).")
    print( "  Close to neutral. We are not asking them to take a worse deal -")
    print( "  we are asking them to take the one that also works for us.")

    # ---- Unknowns ---------------------------------------------------------
    print("\n" + "=" * 78)
    print("  LOAD-BEARING UNKNOWNS - none of these are held today")
    print("=" * 78)
    for u in [
        "Australian local manufacture cost per pouch. Modelled at A$36. No quote.",
        "Australian demand. Every volume above is a scenario, not a forecast.",
        "The formula specification gaps - the 21 Nutrient Blend, the 8 Berry Blend and",
        "  the excipient weights (22.9% of the serving). NO licensee can make the",
        "  product without these. This blocks the licence route in every market.",
        "Whether Bear's name can be sub-licensed for Australasia, and on what terms",
        "  BGV Global / Modern Savage Limited actually control it.",
        "Freight and import permit costs. Estimated, never quoted.",
    ]:
        print(f"  - {u}")
    print()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--royalty", type=float, default=ROYALTY)
    ap.add_argument("--rrp", type=float, default=RRP_INC_GST)
    a = ap.parse_args()
    run(a.royalty, a.rrp)
