#!/usr/bin/env /usr/bin/python3
"""Everest Power - what it costs to get going. 7 Aug 2026.
EVERY LINE IS MY ESTIMATE, not a quote. The three manufacturer RFQs and three
incorporation RFQs sent 7 Aug replace lines marked [RFQ] when they come back."""
INR_GBP = 106.0

# Pilot shape, from the deck: one distributor, 300 outlets, 90 days.
OUTLETS, BOXES_PER_OUTLET_MO, SACHETS_PER_BOX, MONTHS = 300, 3, 100, 3
pilot_demand = OUTLETS * BOXES_PER_OUTLET_MO * SACHETS_PER_BOX * MONTHS

# First production run. Bigger than 90 days of demand - you do not run a line for
# 270k units, and a printed laminate has its own minimum.
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
 # QUOTED 10 Aug 2026. Intepat: search + written opinion USD 50, then USD 225 prof
 # + USD 100 official per class = USD 1,025 for 3 classes. At USD 1.27/GBP ~ GBP 810.
 # Anand and Anand for the same scope: search USD 250 PER CLASS (750) + filing USD 1,215
 # = USD 1,965, and their schedule shows a further USD 730 of acceptance, publication and
 # registration-certificate stages that Intepat's does not mention. Hence the line below.
 ("Trade mark: clearance search + filing, 3 classes (Intepat quote)",  810, ""),
 ("Trade mark: prosecution to registration certificate",               600, "[RFQ]"),
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
APP = ("Unique-code system and retailer scan-and-collect app",      20_000, "")

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
    print(f"\n  The app is £{APP[1]:,} of the difference and the pilot does not need it.")
    print(f"  300 outlets can be run on WhatsApp and UPI by hand.")
    print(f"\n  Sensitivity: COGS at Rs 2.10 (the model's volume price) instead of Rs "
          f"{COGS_PILOT} would take £{round(FIRST_RUN*(COGS_PILOT-2.10)/INR_GBP):,} off.")
