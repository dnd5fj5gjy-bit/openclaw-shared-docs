#!/usr/bin/env /usr/bin/python3
"""Single source of truth for exchange rates across the Everest Power model.

WHY THIS FILE EXISTS. On 11 Aug 2026 setup_costs.py was corrected from INR_GBP 106.0
to the real rate, and economics.py and downside.py were not. For several hours the
set-up cost was in real pounds and every contribution figure was 21% too high, in the
same pack. One constant, imported everywhere, so they cannot drift apart again.

VERIFIED 11 Aug 2026 against api.frankfurter.dev (ECB reference rates), date 2026-08-10:
    GBP -> INR   128.70
    USD -> INR    95.30
    USD -> GBP     0.7405   (so GBP -> USD 1.3505)

These are volatile. Re-verify before any pack that goes to a human, and stamp the date.
"""

FX_DATE = "2026-08-10"
FX_SOURCE = "api.frankfurter.dev (ECB reference rates)"

INR_GBP = 128.70   # rupees per pound
INR_USD = 95.30    # rupees per dollar
USD_GBP = 1.3505   # dollars per pound


def gbp(rupees):
    """Rupees -> pounds."""
    return rupees / INR_GBP


def fx_note():
    return f"FX {INR_GBP:.2f} INR/GBP, {INR_USD:.2f} INR/USD, verified {FX_DATE}, {FX_SOURCE}."


if __name__ == "__main__":
    print(fx_note())
