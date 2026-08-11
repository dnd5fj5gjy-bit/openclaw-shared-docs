#!/usr/bin/env python3
"""
Modern Savage - US unit economics, first complete build.
Built 11 Aug 2026, the night the Ships A Lot rate card arrived.

WHY THIS EXISTS
The 2 Aug pre-order model had fulfilment as UNKNOWN - Ships A Lot had never sent a rate card,
despite being the assumed US 3PL since July. Susan U's card arrived 10 Aug 2026 inside Beau
Bennett's status email. This is the first time every US cost line can be filled in.

EVERY INPUT IS TAGGED. Do not quote a number out of this file without reading its tag.
  VERIFIED - read off a primary document or a live page, with a date
  QUOTED   - a counterparty put it in writing but it is not contracted
  ESTIMATE - my arithmetic or my assumption, stated so it can be attacked
  UNKNOWN  - nobody has priced it. These are the dangerous ones.

Run:  python3 model.py
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# 1. REVENUE  (US market)
# ---------------------------------------------------------------------------
# VERIFIED 2 Aug 2026, modernsavage.co US storefront.
# NOTE: re-checked 11 Aug 2026 but the fetch resolves to the UK storefront from here
# (UK confirmed unchanged: GBP 55/mo, GBP 65 one-off, GBP 140/mo bundle, "save GBP 55").
# The US figures below therefore carry a 2 Aug verification date, not tonight's.
US_SUB_SINGLE      = 69.00   # VERIFIED 2 Aug - per SKU per 28 days, subscribed
US_ONEOFF_SINGLE   = 79.00   # VERIFIED 2 Aug
US_SUB_STACK       = 180.00  # VERIFIED 2 Aug - all three, 60.00 each
US_DELIVERY        = 7.99    # VERIFIED 2 Aug
US_FREE_SHIP_OVER  = 100.00  # VERIFIED 2 Aug - free delivery above ~$100

# ---------------------------------------------------------------------------
# 2. COGS  (per pouch, per SKU)
# ---------------------------------------------------------------------------
# VERIFIED 9 Aug 2026 from ACF invoice S1825 dated 20 Apr 2026 (Lightning Labs DBA ACF Pharma).
# 7,500 units total, $164,075. These are the ACTUAL per-SKU line prices, which are better
# than the blended $21.33 that has been in circulation since 2 Aug.
COGS = {
    "adult":  24.45,  # VERIFIED - Modern Savage 28sv, 2,500 @ 24.45 = 61,125
    "mini":   22.28,  # VERIFIED - Mini Savage 28sv,   2,500 @ 22.28 = 55,700
    "summit": 18.90,  # VERIFIED - BG Summit 28sv,     2,500 @ 18.90 = 47,250
}
ACF_TOTAL          = 164075.00  # VERIFIED - invoice S1825
ACF_BALANCE_DUE    = 82082.50   # VERIFIED - 50% due on completion; deposit 81,992.50 paid 24 Apr
RUN_UNITS_PER_SKU  = 2500       # VERIFIED - invoice S1825

# ---------------------------------------------------------------------------
# 3. FULFILMENT  (Ships A Lot rate card)
# ---------------------------------------------------------------------------
# QUOTED 10 Aug 2026 - Susan U rate card, images in workspace/evidence/beau-status-2026-08-10/.
# QUOTED not VERIFIED on purpose: THERE IS NO SIGNED SHIPS A LOT CONTRACT. Searched junior@
# and jesse@ on 10 Aug - no executed agreement, no signed proposal. A rate card is an offer.
SAL_ORDER_FEE      = 1.50   # QUOTED - per order shipped
SAL_PICK           = 0.50   # QUOTED - "Per Unit Picked", note "Charged Per Handled Unit"
SAL_CARTON_MED     = 0.61   # QUOTED - Carton 10x8x6 Medium. Card says application "Per Unit" (see AMBIGUITY)
SAL_CARTON_SML     = 0.37   # QUOTED - Carton 6x5x5 Small
SAL_POLY_MAILER    = 0.28   # QUOTED - Poly Bubble Mailer #1
SAL_ADMIN_WEEK     = 15.00  # QUOTED - weekly admin fee, "Waived 90 Days from Shipping Start"
SAL_PALLET_STORE   = 5.50   # QUOTED - per pallet per week
SAL_BIN_STORE      = 0.65   # QUOTED - per bin per week
SAL_RECV_PALLET_1  = 15.00  # QUOTED - single-SKU pallet
SAL_RECV_PALLET_N  = 30.00  # QUOTED - multi-SKU pallet
SAL_RECV_CASE_1    = 5.00   # QUOTED - per case, single SKU
SAL_RECV_CASE_N    = 30.00  # QUOTED - per case, multi SKU
SAL_LABOR_HR       = 45.00  # QUOTED - project labour, FOUR HOUR MINIMUM = $180 floor
SAL_LABOR_MIN_HRS  = 4      # QUOTED
SAL_SHIP_LABEL     = 3.00   # QUOTED - charged when a non-SAL carrier is used (carrier lock-in)

# Ships A Lot Priority Postage Ground, QUOTED 10 Aug. Rows are shipped weight.
POSTAGE = {
    "8oz":  [5.02, 5.02, 5.13, 5.19, 5.24, 5.30, 5.40, 5.51, 7.80],
    "12oz": [5.83, 5.83, 5.83, 5.87, 5.92, 6.06, 6.11, 6.41, 8.25],
    "1lb":  [5.87, 5.87, 6.02, 6.10, 6.20, 6.20, 6.36, 6.51, 8.79],
    "2lb":  [5.96, 5.96, 6.24, 6.38, 6.53, 6.67, 6.94, 7.18, 9.25],
    "3lb":  [6.73, 6.73, 7.13, 7.31, 7.52, 7.74, 8.10, 8.45, 10.05],
    "4lb":  [7.48, 7.48, 7.99, 8.24, 8.50, 8.76, 9.26, 9.67, 11.37],
    "5lb":  [8.22, 8.22, 8.83, 9.15, 9.45, 9.77, 10.38, 10.89, 12.65],
}
DEFAULT_ZONE = 5   # ESTIMATE - mid-zone. Zone spread is shown separately.

def postage(row, zone=DEFAULT_ZONE):
    return POSTAGE[row][zone - 1]

# ---------------------------------------------------------------------------
# 4. WEIGHTS  -- the weakest inputs in this model
# ---------------------------------------------------------------------------
# ESTIMATE. 28 servings x 23.5g scoop = 658g of powder for the adult pouch (VERIFIED serving
# size, modernsavage.co). Summit fill is ~336g (ESTIMATE from the ACF spec). Packaging adds
# an unknown amount. ACF figures are FILL weights, not gross shipped weights.
# I asked Beau on 10 Aug to get PACKED weights from Drew. Until they land, every postage row
# below is an assumption and the postage line is the single biggest cost in the stack.
SHIPPED_ROW = {
    "adult":  "2lb",   # ESTIMATE - 658g fill + pouch + carton
    "mini":   "2lb",   # ESTIMATE - assumed same as adult; Mini fill weight UNKNOWN
    "summit": "1lb",   # ESTIMATE - ~336g fill; sits near the 12oz boundary
}
ROW_2PACK  = "4lb"  # ESTIMATE - adult + mini
ROW_3PACK  = "5lb"  # ESTIMATE - all three. NOTE the postage table STOPS at 5lb.

# ---------------------------------------------------------------------------
# 5. PAYMENT PROCESSING
# ---------------------------------------------------------------------------
STRIPE_PCT   = 0.029   # VERIFIED - Stripe US standard card rate
STRIPE_FIXED = 0.30    # VERIFIED

# ---------------------------------------------------------------------------
# 6. FX
# ---------------------------------------------------------------------------
GBPUSD = 1.348598      # VERIFIED 11 Aug 2026, open.er-api.com
SCEND_PER_ORDER_GBP = 5.01  # VERIFIED 23 Jul 2026 - Jack Crumpton in writing, all-in, box + one insert


# ---------------------------------------------------------------------------
# ENGINE
# ---------------------------------------------------------------------------
@dataclass
class Order:
    name: str
    skus: list
    revenue: float
    delivery_charged: float
    postage_row: str
    carton_cost: float
    carton_note: str

    def units(self):
        return len(self.skus)

    def gross(self):
        return self.revenue + self.delivery_charged

    def stripe(self):
        return self.gross() * STRIPE_PCT + STRIPE_FIXED

    def cogs(self):
        return sum(COGS[s] for s in self.skus)

    def fulfilment(self, zone=DEFAULT_ZONE):
        return (SAL_ORDER_FEE
                + SAL_PICK * self.units()
                + self.carton_cost
                + postage(self.postage_row, zone))

    def contribution(self, zone=DEFAULT_ZONE):
        return self.gross() - self.stripe() - self.cogs() - self.fulfilment(zone)

    def cash_after_processing(self):
        """Pre-order treasury measure. COGS is deliberately NOT deducted: the ACF balance
        we are trying to cover IS the COGS. Fulfilment is not deducted either - it is not
        paid until dispatch, which is after the ACF balance falls due."""
        return self.gross() - self.stripe()


def delivery_for(revenue):
    return 0.0 if revenue >= US_FREE_SHIP_OVER else US_DELIVERY


# The carton line is the one genuine ambiguity in the rate card. See AMBIGUITY below.
def build_orders(carton_per_unit: bool):
    def carton(row, units):
        base = SAL_CARTON_MED
        cost = base * units if carton_per_unit else base
        note = f"{units} x {base:.2f}" if carton_per_unit else f"1 x {base:.2f}"
        return cost, note

    out = []
    # Single adult, subscribed
    c, n = carton(SHIPPED_ROW["adult"], 1)
    out.append(Order("Single pouch (adult), subscribed", ["adult"], US_SUB_SINGLE,
                     delivery_for(US_SUB_SINGLE), SHIPPED_ROW["adult"], c, n))
    # Single adult, one-off
    c, n = carton(SHIPPED_ROW["adult"], 1)
    out.append(Order("Single pouch (adult), one-off", ["adult"], US_ONEOFF_SINGLE,
                     delivery_for(US_ONEOFF_SINGLE), SHIPPED_ROW["adult"], c, n))
    # Single summit
    c, n = carton(SHIPPED_ROW["summit"], 1)
    out.append(Order("Single pouch (Summit), subscribed", ["summit"], US_SUB_SINGLE,
                     delivery_for(US_SUB_SINGLE), SHIPPED_ROW["summit"], c, n))
    # Hypothetical 2-pack - DOES NOT EXIST ON THE SITE TODAY
    two_price = 128.00   # ESTIMATE - a proposed step, $64 each. Not offered today.
    c, n = carton(ROW_2PACK, 2)
    out.append(Order("2-pack (adult + mini), PROPOSED $128", ["adult", "mini"], two_price,
                     delivery_for(two_price), ROW_2PACK, c, n))
    # Full stack
    c, n = carton(ROW_3PACK, 3)
    out.append(Order("Full stack (all three), subscribed", ["adult", "mini", "summit"],
                     US_SUB_STACK, delivery_for(US_SUB_STACK), ROW_3PACK, c, n))
    return out


def hr(ch="-", n=94):
    print(ch * n)


def main():
    print()
    hr("=")
    print("MODERN SAVAGE - US UNIT ECONOMICS".center(94))
    print("first complete build, 11 Aug 2026".center(94))
    hr("=")
    print()
    print("Fulfilment inputs are QUOTED, not contracted: there is no signed Ships A Lot")
    print("agreement anywhere in junior@ or jesse@ as of 10 Aug 2026. Postage rows are")
    print("ESTIMATES until Drew supplies packed weights.")
    print()

    for carton_per_unit in (False, True):
        label = ("READING B - carton charged PER UNIT (what the card literally says)"
                 if carton_per_unit else
                 "READING A - carton charged PER ORDER (what a carton physically is)")
        hr("=")
        print(label)
        hr("=")
        print(f"{'Order type':<38}{'Gross':>9}{'Stripe':>8}{'COGS':>9}{'Fulfil':>9}"
              f"{'Contrib':>10}{'Margin':>8}")
        hr()
        for o in build_orders(carton_per_unit):
            print(f"{o.name:<38}{o.gross():>9.2f}{o.stripe():>8.2f}{o.cogs():>9.2f}"
                  f"{o.fulfilment():>9.2f}{o.contribution():>10.2f}"
                  f"{o.contribution()/o.gross()*100:>7.1f}%")
        print()

    orders_a = {o.name: o for o in build_orders(False)}
    single = orders_a["Single pouch (adult), subscribed"]
    two    = orders_a["2-pack (adult + mini), PROPOSED $128"]
    stack  = orders_a["Full stack (all three), subscribed"]

    hr("=")
    print("THE BASKET LEVER - fulfilment cost per POUCH, Reading A, zone 5")
    hr("=")
    for o in (single, two, stack):
        per = o.fulfilment() / o.units()
        print(f"  {o.units()} pouch(es): ${o.fulfilment():>6.2f} per order  =  ${per:>5.2f} per pouch"
              f"   ({(1 - per/single.fulfilment())*100:>5.1f}% vs a single)")
    print()
    print("  The order fee and the carton are per ORDER. Only the pick and the postage scale.")
    print("  Nothing negotiable off Susan's card comes close to this. The basket is the lever.")
    print()

    hr("=")
    print("CONTRIBUTION PER ORDER vs PER POUCH - they point in opposite directions")
    hr("=")
    for o in (single, two, stack):
        print(f"  {o.name:<40} ${o.contribution():>7.2f}/order   "
              f"${o.contribution()/o.units():>6.2f}/pouch")
    print()
    print(f"  The stack earns {stack.contribution()/single.contribution():.2f}x a single PER ORDER")
    print(f"  but only {stack.contribution()/stack.units()/single.contribution()*100:.0f}% as much PER POUCH,")
    print("  because the bundle discounts $69 to $60. Which number matters depends on")
    print("  whether the scarce thing is customers or pouches. Right now it is customers:")
    print(f"  the run is {RUN_UNITS_PER_SKU:,} of each SKU and a bundle draws one from each,")
    print("  so a bundle customer and a single customer consume the SAME adult-pouch cover.")
    print()

    hr("=")
    print("TREASURY - covering the ACF balance of $82,082.50 due on completion")
    hr("=")
    print("  COGS is NOT deducted here. The ACF balance we are covering IS the COGS.")
    print()
    for o in (single, two, stack):
        n = ACF_BALANCE_DUE / o.cash_after_processing()
        print(f"  {o.name:<40} ${o.cash_after_processing():>7.2f} kept   "
              f"{n:>7.0f} orders to cover")
    print()
    ratio = (ACF_BALANCE_DUE / single.cash_after_processing()) / \
            (ACF_BALANCE_DUE / stack.cash_after_processing())
    print(f"  Single-led needs {ratio:.2f}x the ORDERS of stack-led for the same cash.")
    print("  Same customer count, same draw on the scarce adult SKU, same marketing spend.")
    print()
    print("  CAVEAT THAT LIMITS ALL OF THE ABOVE: pre-order cash is a refundable deposit.")
    print("  modernsavage.co states in three places that the customer may cancel for a full")
    print("  refund any time before dispatch. And roughly half the book is UK, where nothing")
    print("  dispatches this year. This is US-side arithmetic only.")
    print()

    hr("=")
    print("ZONE SENSITIVITY - postage is the largest single line")
    hr("=")
    print(f"{'Order type':<38}" + "".join(f"{'Z'+str(z):>7}" for z in range(1, 10)))
    hr()
    for o in (single, stack):
        print(f"{o.name:<38}" + "".join(f"{o.contribution(z):>7.2f}" for z in range(1, 10)))
    print()
    print(f"  Zone 1 to zone 9 swings a single by "
          f"${single.contribution(1) - single.contribution(9):.2f} and a stack by "
          f"${stack.contribution(1) - stack.contribution(9):.2f}.")
    print("  Warehouse location vs customer distribution is worth real money and nobody")
    print("  has looked at where the pre-order book actually lives.")
    print()

    hr("=")
    print("THE RECEIVING TRAP - a 2x to 6x swing decided by how Drew packs the truck")
    hr("=")
    # ESTIMATE: 12 pouches per case; 40 cases per pallet.
    CASES = 7500 / 12
    PALLETS = CASES / 40
    print(f"  ESTIMATE: {CASES:,.0f} cases of 12, about {PALLETS:.0f} pallets, for the whole 7,500-unit run.")
    print()
    print(f"  Palletised, single SKU per pallet : {PALLETS:>5.0f} x ${SAL_RECV_PALLET_1:.2f} = "
          f"${PALLETS*SAL_RECV_PALLET_1:>9,.2f}")
    print(f"  Palletised, mixed SKU per pallet  : {PALLETS:>5.0f} x ${SAL_RECV_PALLET_N:.2f} = "
          f"${PALLETS*SAL_RECV_PALLET_N:>9,.2f}")
    print(f"  By the case, single SKU per case  : {CASES:>5.0f} x ${SAL_RECV_CASE_1:.2f} = "
          f"${CASES*SAL_RECV_CASE_1:>9,.2f}")
    print(f"  By the case, mixed SKU per case   : {CASES:>5.0f} x ${SAL_RECV_CASE_N:.2f} = "
          f"${CASES*SAL_RECV_CASE_N:>9,.2f}")
    print()
    print(f"  Worst case minus best case: ${CASES*SAL_RECV_CASE_N - PALLETS*SAL_RECV_PALLET_1:,.2f}.")
    print("  The instruction to Drew - single SKU per pallet AND per case - costs nothing and")
    print("  has to be given BEFORE the run is packed. The identical trap was already caught")
    print("  and fixed at SCEND, where it saved about GBP 650.")
    print()

    hr("=")
    print("FIXED AND PERIODIC COSTS NOBODY HAS MODELLED")
    hr("=")
    print(f"  Weekly admin fee ${SAL_ADMIN_WEEK:.2f}/wk, waived 90 days from shipping start.")
    print(f"    If dispatch starts 1 Oct 2026 the first charge lands about 1 Jan 2027: "
          f"${SAL_ADMIN_WEEK*52:,.2f}/yr.")
    print(f"  Pallet storage ${SAL_PALLET_STORE:.2f}/pallet/week. At {PALLETS:.0f} pallets that is "
          f"${PALLETS*SAL_PALLET_STORE:,.2f}/wk")
    print(f"    = ${PALLETS*SAL_PALLET_STORE*52:,.2f} for a full year of holding, "
          f"about ${PALLETS*SAL_PALLET_STORE*26:,.2f} on an average half-held run.")
    print(f"  Project labour ${SAL_LABOR_HR:.2f}/hr with a {SAL_LABOR_MIN_HRS}-hour minimum = "
          f"${SAL_LABOR_HR*SAL_LABOR_MIN_HRS:.2f} floor EVERY time it is invoked.")
    print("    This matters precisely because we are about to lead on bundles. If SAL treat a")
    print("    bundle as a pre-kitted work order rather than a multi-unit pick, that floor lands")
    print("    repeatedly. Get it in writing that a bundle picks as 3 units at $0.50.")
    print()

    hr("=")
    print("UK vs US, same single order")
    hr("=")
    scend_usd = SCEND_PER_ORDER_GBP * GBPUSD
    print(f"  SCEND (UK) : GBP {SCEND_PER_ORDER_GBP:.2f} all-in, box and one insert included")
    print(f"               = ${scend_usd:.2f} at GBP/USD {GBPUSD:.4f} (11 Aug 2026)")
    print(f"  Ships A Lot: ${single.fulfilment():.2f} built from five separate lines, mid-zone")
    print(f"  US runs {(single.fulfilment()/scend_usd - 1)*100:.0f}% above the UK for the same order.")
    print()
    print("  CORRECTION to my own 10 Aug note, which said 44%. That was computed against a")
    print("  stale FX rate. On tonight's rate it is the figure above. Mostly geography, not")
    print("  a negotiating stick - but it is a P&L number that belongs in the plan.")
    print()

    hr("=")
    print("AMBIGUITY - one line on the card is worth an email tonight")
    hr("=")
    a = build_orders(False)[-1]
    b = build_orders(True)[-1]
    print(f"  The three carton lines and the poly mailer are all marked application 'Per Unit'.")
    print(f"  A carton is physically per ORDER. If SAL mean it literally, a 3-pack carries")
    print(f"  3 x ${SAL_CARTON_MED:.2f} of carton instead of 1.")
    print(f"    Full stack, carton per order : ${a.fulfilment():.2f} fulfilment")
    print(f"    Full stack, carton per unit  : ${b.fulfilment():.2f} fulfilment")
    print(f"    Difference: ${b.fulfilment()-a.fulfilment():.2f} per bundle order.")
    print(f"  At 800 bundle orders a month that is ${(b.fulfilment()-a.fulfilment())*800:,.2f}/mo, "
          f"${(b.fulfilment()-a.fulfilment())*800*12:,.2f}/yr.")
    print("  It is one question to Susan and it should be asked before anything is signed.")
    print()

    hr("=")
    print("STILL UNPRICED - the UNKNOWN tags, which are the ones that bite")
    hr("=")
    for line in [
        "Returns / RMA: NO line on the card at all, while Beau writes the returns SOP this week.",
        "Carton and mailer supplies: all marked 'Will Review when product received'. Not agreed.",
        "Packed shipped weights: ACF give FILL weights. Every postage row here is an estimate.",
        "Setup, onboarding, minimum monthly, integration, exit/removal: absent from the card.",
        "  Absent is not the same as zero when there is no contract to record the absence.",
        "Postage table stops at 5 lb. A 3-pack is already at the last row.",
        "$3.00 ship-label fee for any non-SAL carrier - that is carrier lock-in, priced.",
        "The actual pre-order book: Felix's dashboard has it, this model does not.",
    ]:
        print(f"  - {line}")
    print()

    hr("=")
    print("THE ONE THAT OUTRANKS EVERY NUMBER ABOVE")
    hr("=")
    print("  There is no Ships A Lot contract. No executed agreement, no signed proposal, and")
    print("  no rate card at all until 10 Aug - and SAL has been the assumed US 3PL since July.")
    print("  Every good SCEND term (zero minimum, no setup fee, the GBP 15 pallet rate) was")
    print("  agreed BEFORE signature. Order: contract, then onboard, then PO.")
    print("  Beau wants to book onboarding now to be 'locked and loaded'. That is the wrong way round.")
    print()
    hr("=")


if __name__ == "__main__":
    main()
