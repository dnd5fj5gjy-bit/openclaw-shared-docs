#!/usr/bin/env /usr/bin/python3
"""Single source of truth for exchange rates across the Everest Power model.

WHY THIS FILE EXISTS. On 11 Aug 2026 setup_costs.py was corrected from INR_GBP 106.0
to the real rate, and economics.py and downside.py were not. For several hours the
set-up cost was in real pounds and every contribution figure was 21% too high, in the
same pack. One constant, imported everywhere, so they cannot drift apart again.

RE-VERIFIED 12 Aug 2026 (01:00 BST) against api.frankfurter.dev (ECB reference rates),
quote date 2026-08-11:
    GBP -> INR   128.84   (was 128.70 on the 10th, +0.11%)
    GBP -> USD     1.35
    USD -> INR    95.44    (derived, 128.84 / 1.35)

These are volatile. Re-verify before any pack that goes to a human, and stamp the date.
"""

FX_DATE = "2026-08-11"
FX_SOURCE = "api.frankfurter.dev (ECB reference rates)"

INR_GBP = 128.84   # rupees per pound
INR_USD = 95.44    # rupees per dollar
USD_GBP = 1.3500   # dollars per pound


def gbp(rupees):
    """Rupees -> pounds."""
    return rupees / INR_GBP


def fx_note():
    return f"FX {INR_GBP:.2f} INR/GBP, {INR_USD:.2f} INR/USD, verified {FX_DATE}, {FX_SOURCE}."


if __name__ == "__main__":
    print(fx_note())
