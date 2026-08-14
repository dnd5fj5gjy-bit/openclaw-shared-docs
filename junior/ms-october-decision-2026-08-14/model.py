#!/usr/bin/env python3
"""
Modern Savage - does "around October 2026" hold, and what does a re-date cost?
Built 14 Aug 2026, 01:00-03:00 BST.

Every input is tagged:
  VERIFIED - read at primary source, with the source named
  QUOTED   - a counterparty put it in writing to us
  ESTIMATE - my number, reasoned, labelled as such
  UNKNOWN  - nobody has priced or counted it. These are the dangerous ones.

Re-run this. Do not quote the numbers out of the write-up once the two UNKNOWNs
(the pre-order book, and Andrew's written start date) become real.
"""

from datetime import date, timedelta

# ---------------------------------------------------------------------------
# THE PUBLIC PROMISE - VERIFIED live on modernsavage.co, 14 Aug 2026 01:20 BST
# ---------------------------------------------------------------------------
# /shipping, /returns and /terms all say, in these words:
#   "We are aiming to deliver around October 2026."
#   "If that date moves we will email you with the new one, and you can either
#    wait or cancel for a full refund at that point."
#   "Your card is charged in full when you order, not when we dispatch."
# Seller of record: Modern Savage Inc., Delaware. Terms last updated 5 Aug 2026.
PROMISE_WINDOW_START = date(2026, 10, 1)   # VERIFIED - "around October 2026"
PROMISE_WINDOW_END   = date(2026, 10, 31)  # VERIFIED - the generous reading

# ---------------------------------------------------------------------------
# THE MANUFACTURING CLOCK - QUOTED, Andrew Kouvel (ACF) to Beau, 13 Aug 2026
# ---------------------------------------------------------------------------
# "it will take 12 weeks to manufacture the product. And 3 days to ship to
#  Mississippi. He says though that because we were all ready to go in July that
#  we should be able to launch sometime in September. He's going to send us an
#  approximate date sometime end of week."
MANUFACTURE_WEEKS = 12   # QUOTED 13 Aug
FREIGHT_DAYS      = 3    # QUOTED 13 Aug - ACF (Pompano Beach FL) to Olive Branch MS
RECEIVING_DAYS    = 5    # ESTIMATE - Ships A Lot inbound receipt, check-in, putaway.
                         # No receiving SLA anywhere in the rate card. See UNKNOWNS.
TRANSIT_US_DAYS   = 5    # VERIFIED - site states 3-5 business days after dispatch

TODAY = date(2026, 8, 14)

# ---------------------------------------------------------------------------
# PRICES - VERIFIED 2 Aug 2026 from modernsavage.co, unchanged since
# ---------------------------------------------------------------------------
US_SUB_SINGLE    = 69.00
US_ONEOFF_SINGLE = 79.00
US_SUB_STACK     = 180.00

# ---------------------------------------------------------------------------
# THE TWO UNKNOWNS THAT DECIDE EVERYTHING
# ---------------------------------------------------------------------------
# 1. The pre-order book. It is on Felix's dashboard and I have never been given a
#    number. Every refund figure below is therefore a SHAPE, not a forecast.
# 2. Andrew's written start date for the 12 weeks. Asked for; not yet received.
BOOK_SIZES_TO_TEST = [100, 250, 500, 1000, 2000]  # UNKNOWN - orders placed to date
ORDERS_PER_WEEK    = 60      # UNKNOWN - run rate. Placeholder to show the slope.
US_SHARE           = 0.65    # ESTIMATE - US-led launch, UK site live too
STACK_SHARE        = 0.30    # ESTIMATE - shop page leads with singles, hides bundle

# ACF balance due on delivery - VERIFIED, invoice S1825, $164,075 total, 50% paid
ACF_BALANCE_DUE = 82082.50

# Cancellation behaviour - ESTIMATE, and the single most important assumption here
ACTIVE_CANCEL_RATE   = 0.10  # ESTIMATE - people who read a delay email and act
NON_RESPONSE_RATE    = 0.80  # ESTIMATE - people who ignore a delay email entirely
STRIPE_FEE           = 0.029 # VERIFIED - Stripe standard; fees are NOT returned on refund


def aov() -> float:
    """Blended order value. ESTIMATE built on VERIFIED prices."""
    single_blend = 0.5 * US_SUB_SINGLE + 0.5 * US_ONEOFF_SINGLE
    return STACK_SHARE * US_SUB_STACK + (1 - STACK_SHARE) * single_blend


def chain(start: date) -> dict:
    """Given the date the 12-week clock starts, when does the customer get it?"""
    made = start + timedelta(weeks=MANUFACTURE_WEEKS)
    at_3pl = made + timedelta(days=FREIGHT_DAYS)
    dispatch = at_3pl + timedelta(days=RECEIVING_DAYS)
    delivered = dispatch + timedelta(days=TRANSIT_US_DAYS)
    return {"start": start, "made": made, "at_3pl": at_3pl,
            "dispatch": dispatch, "delivered": delivered}


def latest_start_for(target: date) -> date:
    """Work backwards: the last day the clock can start and still deliver by target."""
    lead = timedelta(weeks=MANUFACTURE_WEEKS) + timedelta(
        days=FREIGHT_DAYS + RECEIVING_DAYS + TRANSIT_US_DAYS)
    return target - lead


def book_at(weeks_from_now: int, base: int) -> int:
    return base + ORDERS_PER_WEEK * weeks_from_now


def refund_exposure(orders: int, within_30_days: bool, is_first_notice: bool) -> dict:
    """
    The FTC mechanic, VERIFIED at primary source 14 Aug 2026:
    ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-
    telephone-order-merchandise-rule

      - First notice, definite revised date 30 days or less after the originally
        promised time: "you must inform customers that their non-response will be
        treated as a consent to the delay." Only active cancellations refund.
      - First notice, definite revised date MORE than 30 days later, or indefinite:
        "if they do not respond, the order will be cancelled automatically."
        Non-response refunds. This is the cliff.
      - ANY renewed (second) notice: "the customer's silence may not be treated as
        a consent to delay." Non-response refunds, regardless of the new date.

    UK orders do not carry this mechanic at all - see uk_note().
    """
    us_orders = orders * US_SHARE
    uk_orders = orders * (1 - US_SHARE)

    if is_first_notice and within_30_days:
        us_cancel_rate = ACTIVE_CANCEL_RATE
        mechanic = "silence = consent"
    else:
        # non-responders cancel automatically, plus those who actively cancel
        us_cancel_rate = NON_RESPONSE_RATE + ACTIVE_CANCEL_RATE * (1 - NON_RESPONSE_RATE)
        mechanic = "silence = CANCELLED"

    # UK: consumer must act. CRA 2015 s.28(7) - they specify a further period first.
    uk_cancel_rate = ACTIVE_CANCEL_RATE

    refunded_orders = us_orders * us_cancel_rate + uk_orders * uk_cancel_rate
    refunded_cash = refunded_orders * aov()
    # Stripe keeps its processing fee on a refunded charge - a real, unrecoverable cost
    sunk_fees = refunded_orders * aov() * STRIPE_FEE

    return {"orders": orders, "mechanic": mechanic,
            "us_cancel_rate": us_cancel_rate,
            "refunded_orders": refunded_orders,
            "refunded_cash": refunded_cash,
            "sunk_fees": sunk_fees,
            "cash_retained": orders * aov() - refunded_cash}


def rule(title=""):
    print("\n" + "=" * 78)
    if title:
        print("  " + title)
        print("=" * 78)


def main():
    print("MODERN SAVAGE - DOES OCTOBER HOLD?")
    print("Built 14 Aug 2026. Blended AOV used throughout: $%.2f (ESTIMATE on VERIFIED prices)"
          % aov())

    # -----------------------------------------------------------------
    rule("1. THE THREE READINGS OF ANDREW'S 12 WEEKS")
    # -----------------------------------------------------------------
    print("  Andrew said 12 weeks AND September in the same breath. Those two only")
    print("  reconcile if the clock started in July. Each row is one reading:\n")
    print("  %-34s %-12s %-12s %-12s" % ("clock starts", "made", "dispatch", "customer has it"))
    print("  " + "-" * 72)
    readings = [
        ("Started 1 Jul (order was ready)",  date(2026, 7, 1)),
        ("Started 15 Jul",                   date(2026, 7, 15)),
        ("Started 26 Jul  <- BREAK-EVEN",    date(2026, 7, 26)),
        ("Started 31 Jul",                   date(2026, 7, 31)),
        ("Starts today, 14 Aug",             TODAY),
        ("Starts on artwork, ~1 Sep",        date(2026, 9, 1)),
    ]
    for label, start in readings:
        c = chain(start)
        flag = "  OK" if c["delivered"] <= PROMISE_WINDOW_END else "  MISSES OCTOBER"
        print("  %-34s %-12s %-12s %-12s%s" % (
            label, c["made"], c["dispatch"], c["delivered"], flag))

    be = latest_start_for(PROMISE_WINDOW_END)
    print("\n  BREAK-EVEN: the 12 weeks must have started on or before %s" % be)
    print("  for a customer to hold the product inside October.")
    print("  That is %d days before Andrew said the words." % (date(2026, 8, 13) - be).days)
    print("  So: 'September' is only true if ACF began in July. It is a yes/no question")
    print("  with a one-line answer, and it is the highest-value question we can ask.")

    # -----------------------------------------------------------------
    rule("2. THE WORST CASE IS SURVIVABLE, AND THAT IS THE REAL FINDING")
    # -----------------------------------------------------------------
    worst = chain(TODAY)
    print("  If the clock starts TODAY - the worst honest reading - the customer")
    print("  receives on %s." % worst["delivered"])
    days_past = (worst["dispatch"] - PROMISE_WINDOW_END).days
    print("  First dispatch %s is %d days after the end of the promised window." % (
        worst["dispatch"], days_past))
    print()
    print("  That matters because of where the 30-day line falls:")
    cliff = PROMISE_WINDOW_END + timedelta(days=30)
    print("    promised window ends      %s" % PROMISE_WINDOW_END)
    print("    + 30 days                 %s   <- the silence-as-consent cliff" % cliff)
    print("    worst-case dispatch       %s" % worst["dispatch"])
    print()
    if worst["dispatch"] <= cliff:
        print("  The worst case lands INSIDE the 30-day window. A single delay notice")
        print("  re-dating dispatch to 30 Nov is therefore a '30 days or less' notice,")
        print("  where non-response counts as consent. The book largely survives.")
    else:
        print("  The worst case lands OUTSIDE the 30-day window. Non-response would")
        print("  auto-cancel. This is the expensive branch.")

    # -----------------------------------------------------------------
    rule("3. WHAT THE TWO KINDS OF NOTICE COST")
    # -----------------------------------------------------------------
    print("  Same book, same slip, two different notices. The gap is the whole point.\n")
    print("  %-8s %-24s %10s %13s %13s" % (
        "book", "notice type", "US cancel", "refunded", "cash kept"))
    print("  " + "-" * 72)
    for b in BOOK_SIZES_TO_TEST:
        a = refund_exposure(b, within_30_days=True,  is_first_notice=True)
        c = refund_exposure(b, within_30_days=False, is_first_notice=True)
        print("  %-8d %-24s %9.0f%% %13s %13s" % (
            b, "<=30d, silence=consent", a["us_cancel_rate"] * 100,
            "$%,.0f".replace(",", ",") % a["refunded_cash"], "$%,.0f" % a["cash_retained"]))
        print("  %-8s %-24s %9.0f%% %13s %13s" % (
            "", ">30d, silence=cancel", c["us_cancel_rate"] * 100,
            "$%,.0f" % c["refunded_cash"], "$%,.0f" % c["cash_retained"]))
        print()

    # -----------------------------------------------------------------
    rule("4. THE TREASURY TEST - CAN WE STILL PAY ACF?")
    # -----------------------------------------------------------------
    print("  The pre-order book is what funds the ACF balance of $%,.2f due on" % ACF_BALANCE_DUE)
    print("  delivery. A forced refund is a treasury event, not a support ticket.\n")
    print("  %-8s %-24s %13s %13s  %s" % (
        "book", "notice type", "cash kept", "ACF due", "covers ACF?"))
    print("  " + "-" * 74)
    for b in BOOK_SIZES_TO_TEST:
        for within, lbl in ((True, "<=30d, silence=consent"), (False, ">30d, silence=cancel")):
            r = refund_exposure(b, within_30_days=within, is_first_notice=True)
            ok = "YES" if r["cash_retained"] >= ACF_BALANCE_DUE else "NO  - short $%,.0f" % (
                ACF_BALANCE_DUE - r["cash_retained"])
            print("  %-8s %-24s %13s %13s  %s" % (
                b if within else "", lbl,
                "$%,.0f" % r["cash_retained"], "$%,.0f" % ACF_BALANCE_DUE, ok))
        print()

    # -----------------------------------------------------------------
    rule("5. THE COST OF WAITING")
    # -----------------------------------------------------------------
    print("  Two things get worse every week we say nothing, and they multiply:")
    print("    (a) the book grows, so the same cancellation rate refunds more cash")
    print("    (b) the FTC notice must land INSIDE the promised time. Miss that and")
    print("        the remedy is not a re-date, it is cancel and refund the lot.\n")
    base = 500  # UNKNOWN placeholder
    print("  Modelled on a %d-order book today growing %d/week (both UNKNOWN):\n" % (
        base, ORDERS_PER_WEEK))
    print("  %-22s %-8s %13s %13s" % ("notify", "book", "refunded (<=30d)", "refunded (>30d)"))
    print("  " + "-" * 62)
    for wk in (0, 2, 4, 6, 8, 11):
        when = TODAY + timedelta(weeks=wk)
        bk = book_at(wk, base)
        a = refund_exposure(bk, True, True)
        c = refund_exposure(bk, False, True)
        late = "  <- PAST THE DEADLINE" if when > PROMISE_WINDOW_END else ""
        print("  %-22s %-8d %13s %13s%s" % (
            when.strftime("%d %b %Y"), bk,
            "$%,.0f" % a["refunded_cash"], "$%,.0f" % c["refunded_cash"], late))

    print("\n  The notice deadline is %s. Not a soft date - it is the point at which" %
          PROMISE_WINDOW_END)
    print("  the FTC remedy stops being 'offer a new date' and becomes 'refund'.")

    # -----------------------------------------------------------------
    rule("6. THE ONE-NOTICE RULE")
    # -----------------------------------------------------------------
    print("  A second delay notice CANNOT use silence as consent. VERIFIED at the FTC:")
    print('    "One important difference: the customer\'s silence may not be treated')
    print('     as a consent to delay."')
    print()
    b = 500
    first = refund_exposure(b, True, True)
    second = refund_exposure(b, True, False)
    print("  On a %d-order book, the same <=30-day re-date costs:" % b)
    print("    as a FIRST notice   $%,.0f refunded" % first["refunded_cash"])
    print("    as a SECOND notice  $%,.0f refunded" % second["refunded_cash"])
    print("    difference          $%,.0f" % (second["refunded_cash"] - first["refunded_cash"]))
    print()
    print("  We get exactly one cheap notice. Spend it on a date we will hit, not on")
    print("  the most optimistic date we can defend. An optimistic re-date that slips")
    print("  again converts the whole silent majority into refunds.")

    # -----------------------------------------------------------------
    rule("7. UNKNOWNS - what would change these numbers")
    # -----------------------------------------------------------------
    for u in [
        "The pre-order book. Never given to me. On Felix's dashboard. Every dollar",
        "  figure above is a shape until that number is real.",
        "Andrew's written start date for the 12 weeks. Promised 'end of week'.",
        "Belmark's print lead time. Unasked since 7 Aug. If print is SERIAL after the",
        "  blend rather than parallel, every date above moves right.",
        "Ships A Lot inbound receiving SLA. No line in the rate card. Modelled at 5 days.",
        "Lab turnaround on the full panel Andrew wants on batch one. Unpriced, unscheduled.",
        "The US/UK split of the book, and the bundle share. Both ESTIMATE.",
    ]:
        print("  - " + u if not u.startswith("  ") else "   " + u.strip())


if __name__ == "__main__":
    main()
