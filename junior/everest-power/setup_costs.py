#!/usr/bin/env /usr/bin/python3
"""Everest Power - what it costs to get going. 7 Aug 2026.
EVERY LINE IS MY ESTIMATE, not a quote. The three manufacturer RFQs and three
incorporation RFQs sent 7 Aug replace lines marked [RFQ] when they come back."""
# FX corrected 11 Aug 2026 (was 106.0, ~21% wrong) and now imported from fx.py so it
# cannot drift out of step with economics.py and downside.py again.
from fx import INR_GBP, USD_GBP, fx_note

# Pilot shape, from the deck: one distributor, 300 outlets, 90 days.
# RATE OF SALE CORRECTED 11 Aug 2026. This ran on 3 boxes per outlet per month, i.e.
# 10 sachets a day, which the demand test of 10 Aug found to be ~4x too high. The
# planning rate is 2.5/day. It matters here because it is what the first run is sized
# against.
OUTLETS, SACHETS_PER_BOX, MONTHS = 300, 100, 3
SACHETS_PER_OUTLET_DAY = 2.5
pilot_demand = int(OUTLETS * SACHETS_PER_OUTLET_DAY * 30 * MONTHS)
pilot_demand_bull = OUTLETS * 10 * 30 * MONTHS

# First production run. A printed laminate carries its own minimum and you do not run a
# line for a few tens of thousands of units, so the run is set by the factory, not by
# the pilot. That is a real working capital point, not a rounding one - see the note
# printed at the end.
FIRST_RUN = 500_000
# COGS at pilot volume is NOT the Rs 2.10 in the model. That is a volume price.
COGS_PILOT = 3.25   # ASSUMPTION - the single biggest unknown until quotes land. [RFQ]

LINES = [
 ("Indian company: incorporation as a WOS, FDI/FEMA filings",      2_000, "[RFQ]"),
 ("Resident director service, 12 months",                          5_000, "[RFQ]"),
 # KNM India (Sandeep Bansal) 10 Aug 2026, in writing: we need a CENTRAL FSSAI licence
 # as brand owner/marketer/relabeller, and the contract manufacturer's own licence covers
 # our product at his address - so no second licence at the factory. Structure settled,
 # fee still not quoted; KNM promised their quotation 11 Aug 2026.
 ("FSSAI central licence, GST, PAN, TAN, bank account",             1_000, "[RFQ]"),
 ("Accounting, statutory audit, company secretarial, 12 months",    3_000, "[RFQ]"),
 # ALL THREE TRADE MARK QUOTES IN. Same scope, 3 classes, restated 11 Aug 2026 at the
 # corrected FX above and at the TRUE statutory fee, which Anand & Anand confirmed in
 # writing 11 Aug: INR 9,000 per class, billed at spot on the day of filing.
 # INR 9,000 = USD 94 = GBP 70. That fee is identical for all three firms, so any gap
 # between a firm's "official fee" line and INR 9,000 is padding, not service:
 #   Intepat        USD 100/class  -> USD 6 over.  Accurate.
 #   Anand & Anand  USD 140/class  -> USD 46 over, 49%. Inflated their headline by USD 138.
 #   S. S. Rana     GBP 105/class  -> INR 13,535, 50% over. GBP 105 of padding over 3 classes.
 # Totals to registration certificate, 3 classes, restated:
 #   Intepat        search + written opinion USD 50; filing USD 225 prof + USD 100 official
 #                  per class = USD 1,025 = GBP 759. INSTRUCTED 9 Aug, search running,
 #                  findings chased 11 Aug 03:12. Certificate stage still unpriced.
 #   Anand & Anand  search USD 300/class (900, was quoted 250 on 10 Aug and re-quoted at 300
 #                  on 11 Aug while described as unchanged) + filing USD 1,077 at true
 #                  official fee + USD 730 acceptance/publication/certificate = USD 2,707
 #                  = GBP 2,004. Confirmed 11 Aug: nothing else falls due in a clean case.
 #                  Now the MOST expensive of the three, not Rana.
 #   S. S. Rana     search GBP 150/class (450) + filing GBP 455/class (200 prof + 105
 #                  official + 150 final formalities) = GBP 1,365. Total GBP 1,815. Only
 #                  firm that refused a view on the EVEREST conflict without being paid.
 # Line below stays at the Intepat number because Intepat is instructed and working.
 ("Trade mark: clearance search + filing, 3 classes (Intepat quote)",  759, ""),
 # NOT IN THE TOTAL, a live decision for Jesse: Anand & Anand quoted 11 Aug for searching
 # the EVEREST wordmark alone in classes 5, 30 and 32 at USD 300 per mark per class, so
 # USD 900 = GBP 666, 4-5 working days, opinion on availability and on the Everest spice
 # brand included in that fee. They are the only firm that raised the enforcement pattern
 # of existing EVEREST rights as the real risk, and they enforced HIMALAYAN. Worth buying
 # only if Intepat's USD 50 opinion comes back thin. Wait for Intepat first.
 # Post-filing. Rana is the only firm to price it: GBP 200 per office-action reply and
 # GBP 200 per hearing, per application - so a 3-class objection is GBP 600-1,200. Rana
 # bundles the registration certificate into its filing fee; Intepat's schedule is silent
 # on it and has been asked. The 600 below is a one-objection-on-one-class assumption.
 ("Trade mark: prosecution to registration certificate",               600, "[RFQ - Intepat]"),
 ("Formula and flavour development, blind sip tests",               6_000, ""),
 ("Lab work: nutritional analysis, stability at 45C/75% RH",        2_000, "[RFQ]"),
 ("Production-ready artwork: sachet, outer box, code layout",       5_000, ""),
 ("Print cylinders and laminate setup",                             2_000, "[RFQ]"),
 (f"First run, {FIRST_RUN:,} sachets at Rs {COGS_PILOT}",
      round(FIRST_RUN * COGS_PILOT / INR_GBP), "[RFQ]"),
 ("Distributor trade scheme and incentives, 90 days",               2_000, ""),
 ("India ground support, part time, 3 months",                      5_000, ""),
 ("Travel, two trips",                                              5_000, ""),
]
APP = ("Unique-code system and retailer scan-and-collect app",           0,
       "[in house - Felix builds it, Jesse 11 Aug 2026. Internal time, no cash line]")

def show(rows, label):
    sub = sum(c for _, c, _ in rows)
    cont = round(sub * 0.15)
    print(f"\n--- {label} ---")
    for n, c, f in rows:
        print(f"  {n:<58} £{c:>7,}  {f}")
    print(f"  {'Subtotal':<58} £{sub:>7,}")
    print(f"  {'Contingency 15%':<58} £{cont:>7,}")
    print(f"  {'TOTAL':<58} £{sub+cont:>7,}")
    return sub + cont

if __name__ == "__main__":
    print("EVEREST POWER - COST TO GET GOING")
    print(f"Pilot: {OUTLETS} outlets x {BOXES_PER_OUTLET_MO} boxes/mo x {MONTHS} months "
          f"= {pilot_demand:,} sachets of demand")
    print(f"First production run: {FIRST_RUN:,} sachets")
    lean = show(LINES, "LEAN PILOT - answers 'does a shop sell ten a day'")
    full = show(LINES + [APP], "WITH THE CODE SYSTEM AND APP BUILT")
    print(f"\n  The app is now built in house (Jesse, 11 Aug 2026), so it is £0 of cash.")
    print(f"  300 outlets can be run on WhatsApp and UPI by hand.")
    print(f"\n  Sensitivity: COGS at Rs 2.10 (the model's volume price) instead of Rs "
          f"{COGS_PILOT} would take £{round(FIRST_RUN*(COGS_PILOT-2.10)/INR_GBP):,} off.")
