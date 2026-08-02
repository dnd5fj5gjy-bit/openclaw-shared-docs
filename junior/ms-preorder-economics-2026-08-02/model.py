#!/usr/bin/env python3
"""
Modern Savage founding pre-order: unit economics and cash model.
Built 2 Aug 2026 (overnight). Junior.

EVERY input is tagged with where it came from. Read the tags before trusting a number.
  [VERIFIED]  read from a primary source on the date shown
  [QUOTED]    stated in writing by the counterparty
  [ESTIMATE]  my assumption, and the number most likely to be wrong
  [UNKNOWN]   nobody holds this figure. Shown as a band, not a point.

Re-run with real COGS and the Ships A Lot rate card and this stops being a band
and becomes an answer:  python3 model.py
"""

FX_GBPUSD = 1.345489   # [VERIFIED] open.er-api.com, 1 Aug 2026 00:02 UTC

# ---------------------------------------------------------------- REVENUE
# [VERIFIED] modernsavage.co, read 2 Aug 2026 01:30 BST (UK) / 31 Jul 2026 (US)
UK = dict(
    sub_price      = 55.00,   # per pouch per month, subscribed. All 3 SKUs same price.
    onetime_price  = 65.00,   # "Subscribing saves you £10"
    bundle_price   = 139.98,  # all three, per month (= £46.66 each; "Save £55" is vs 3x£65)
    delivery       = 4.99,
    vat            = 0.20,    # [VERIFIED] HMRC VFOOD2040 - powder supplements are standard-rated
)
US = dict(
    sub_price      = 69.00,
    onetime_price  = 79.00,
    bundle_price   = 180.00,  # $60 each
    delivery       = 7.99,    # free over ~$100, so the bundle ships free to the customer
    vat            = 0.00,    # US sales tax is added on top at checkout, not carved out of price
)

# ---------------------------------------------------------------- COSTS
# Payment processing
UK_FEE_PCT, UK_FEE_FIX = 0.020, 0.20   # [ESTIMATE] Stripe UK 1.5%+20p domestic, 3.25% intl. Blended.
US_FEE_PCT, US_FEE_FIX = 0.029, 0.30   # [ESTIMATE] Stripe US standard card

# Fulfilment
UK_PICKPACK = 5.01   # [QUOTED] SCEND, Jack Crumpton, 23 Jul + reconfirmed 30 Jul 2026.
                     #          Confirmed in writing to include one insert/flyer.
UK_COURIER  = 3.60   # [ESTIMATE] UK tracked, ~700g single pouch
UK_COURIER_BUNDLE = 5.50  # [ESTIMATE] ~2kg, three pouches
US_LOGISTICS = 15.00      # [UNKNOWN] Ships A Lot rate card has never been received.
US_LOGISTICS_BUNDLE = 18.00  # [UNKNOWN] same

# Cost of goods per pouch
# [UNKNOWN] There is no current COGS. The only quotes held are ACF Pharma's, and the ACF/US
# route is superseded - the site now says Made in the UK and no UK manufacturer is confirmed
# contracted. ACF for reference only: Adult $24.45, Kids $22.28, Adult+creatine $27.03 @2,500u.
COGS_BAND_USD = [18.00, 21.00, 24.00, 27.00]


def gbp(x): return f"£{x:,.2f}"
def usd(x): return f"${x:,.2f}"


def order(market, kind, cogs_local):
    """Contribution from one order, in that market's own currency."""
    m = UK if market == "UK" else US
    if kind == "bundle":
        goods, units = m["bundle_price"], 3
        delivery = 0.0 if market == "US" else m["delivery"]   # US bundle clears the free-ship threshold
        logistics = (UK_PICKPACK + UK_COURIER_BUNDLE) if market == "UK" else US_LOGISTICS_BUNDLE
    else:
        goods = m["sub_price"] if kind == "sub" else m["onetime_price"]
        units, delivery = 1, m["delivery"]
        logistics = (UK_PICKPACK + UK_COURIER) if market == "UK" else US_LOGISTICS

    gross = goods + delivery
    net   = gross / (1 + m["vat"])          # VAT is inside the UK price, added on top of the US one
    fees  = gross * (UK_FEE_PCT if market == "UK" else US_FEE_PCT) \
          + (UK_FEE_FIX if market == "UK" else US_FEE_FIX)
    cogs  = cogs_local * units
    return dict(gross=gross, net=net, fees=fees, logistics=logistics,
                cogs=cogs, contribution=net - fees - logistics - cogs, units=units)


print("=" * 74)
print("  MODERN SAVAGE - FOUNDING PRE-ORDER ECONOMICS      built 2 Aug 2026")
print(f"  GBP/USD {FX_GBPUSD:.4f} (1 Aug 2026)")
print("=" * 74)

# ---- 1. The price correction ------------------------------------------
print("\n1. WHAT THE TWO MARKETS ACTUALLY EARN (the correction to the model)\n")
uk_net = UK["sub_price"] / 1.2
print(f"   UK  £55.00 subscribed  ->  {gbp(uk_net)} net of VAT  =  {usd(uk_net*FX_GBPUSD)}")
print(f"   US  $69.00 subscribed  ->  {usd(US['sub_price'])} net (sales tax sits on top)")
gap = (US["sub_price"] - uk_net * FX_GBPUSD) / US["sub_price"]
print(f"   A US subscriber is worth {gap*100:.0f}% more per month than a UK one, on goods alone.")
print(f"   Raemy's model prices the US sub at $59.99. It is $69.00, so that model")
print(f"   understates US subscription revenue by {(69/59.99-1)*100:.1f}% on every line it touches.")

# ---- 2. Contribution per order ----------------------------------------
print("\n2. CONTRIBUTION PER FOUNDING ORDER, ACROSS THE COGS BAND\n")
print(f"   {'COGS/pouch':>12} | {'UK single':>22} | {'US single':>22}")
print("   " + "-" * 62)
for c_usd in COGS_BAND_USD:
    c_gbp = c_usd / FX_GBPUSD
    u = order("UK", "sub", c_gbp)
    s = order("US", "sub", c_usd)
    print(f"   {usd(c_usd):>12} | {gbp(u['contribution']):>9} ({u['contribution']/u['net']*100:4.0f}% of net) "
          f"| {usd(s['contribution']):>9} ({s['contribution']/s['net']*100:4.0f}% of net)")

print("\n   Same, for the three-product bundle (the founding offer worth leading with):\n")
print(f"   {'COGS/pouch':>12} | {'UK bundle':>22} | {'US bundle':>22}")
print("   " + "-" * 62)
for c_usd in COGS_BAND_USD:
    c_gbp = c_usd / FX_GBPUSD
    u = order("UK", "bundle", c_gbp)
    s = order("US", "bundle", c_usd)
    print(f"   {usd(c_usd):>12} | {gbp(u['contribution']):>9} ({u['contribution']/u['net']*100:4.0f}% of net) "
          f"| {usd(s['contribution']):>9} ({s['contribution']/s['net']*100:4.0f}% of net)")

# ---- 3. Break-even against committed cash -----------------------------
# This is a TREASURY question, not a margin one, so it compares cash in against cash out.
# COGS does not appear: the ACF balance inside the committed figure IS the cost of the run.
# Deducting it again here would double-count it.
#
# [ESTIMATE / STALE] The last committed-cash figure is ~$106,000 from the 26 Jul sizing doc,
# and it was built on the ACF/US route which is now superseded. Nobody has restated it.
COMMITTED = 106_000


def cash_retained(market, kind):
    """Cash actually kept from one order: gross, less processing, less VAT owed to HMRC."""
    o = order(market, kind, 0)
    keep = o["gross"] - o["fees"] - (o["gross"] - o["net"])   # last term is the VAT
    return keep * FX_GBPUSD if market == "UK" else keep


print(f"\n3. HOW MANY ORDERS SELF-FUND THE RUN  (against the last stated {usd(COMMITTED)},")
print("   itself from 26 Jul and built on the superseded ACF route. Cash in vs cash out;")
print("   COGS is deliberately absent - it is already inside the committed figure.)\n")
for market in ("US", "UK"):
    for kind, label in (("sub", "single"), ("bundle", "bundle")):
        k = cash_retained(market, kind)
        print(f"   {market} {label:6}  keeps {usd(k):>8} of cash per order  ->  "
              f"{COMMITTED/k:5.0f} orders to cover the run")
print(f"\n   Rescale for any other committed figure: divide it by the cash-per-order above.")
print(f"   Each $10,000 of committed cash needs {10_000/cash_retained('US','bundle'):.0f} more US bundles"
      f" or {10_000/cash_retained('US','sub'):.0f} more US singles.")
print("\n   Against the 800-place cap this is the whole commercial point:")
b800 = 800 * cash_retained("US", "bundle")
s800 = 800 * cash_retained("US", "sub")
print(f"     800 bundles raise {usd(b800)}  -> covers the run with {usd(b800-COMMITTED)} spare")
print(f"     800 singles raise {usd(s800)}  -> leaves {usd(COMMITTED-s800)} to find elsewhere")
print("   Same 800 customers, same 800 units of the scarce Adult SKU. The mix is the difference")
print("   between a launch that pays for itself and one that needs a cheque.")

# ---- 4. UK refund exposure --------------------------------------------
print("\n4. UK CASH IS NOT YET EARNED CASH\n")
print("   The 1 Aug campaign takes payment now, promises delivery around Oct 2026, and offers")
print("   a full refund any time before it ships. Until a UK pouch can lawfully ship, every")
print("   pound of UK pre-order money is a refund liability, not revenue.")
print("   Four things must exist before one UK order can be fulfilled. None is confirmed held:")
for i, g in enumerate([
        "a contracted UK manufacturer (last record: 3 leads at NDA stage, 13 Jul)",
        "a UK VAT number - SCEND cannot ship without it (Jack Crumpton, 30 Jul, unanswered)",
        "an EORI number, to import the goods (same email, same silence)",
        "FBO registration and a UK-address back-of-pack, which is a separate print run"], 1):
    print(f"     {i}. {g}")
print("\n   Cost of the UK half of day one being wrong is not margin. It is the whole ticket back,")
print("   plus the processing fee, which Stripe does not return on a refund.")
print("\n" + "=" * 74)
print("  The four numbers that turn this from a band into an answer:")
print("   (a) real cost per pouch from the actual manufacturer")
print("   (b) the Ships A Lot rate card")
print("   (c) a restated committed-cash figure for the UK route")
print("   (d) the UK/US split of orders taken so far - Felix's dashboard, 2 Aug")
print("=" * 74)
