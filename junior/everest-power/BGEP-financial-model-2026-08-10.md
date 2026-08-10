# Bear Grylls Everest Power - financial model and downside

**For Raemy Singh, CFO. 10 August 2026.**

Everything here is an estimate. **No manufacturer has quoted and no distributor has signed.**
That is not a caveat on the model, it is the model's main finding: the two numbers that decide
this business are the two we do not yet own.

---

## 1. The unit

12g sachet, MRP Rs 10, sold wholesale into kirana shops, street vendors and petrol pumps.

| | Rs per sachet |
|---|---|
| Consumer pays (MRP) | 10.00 |
| Less GST at 18% | 8.47 |
| Retailer buys at (15% to the shop) | 7.20 |
| Distributor buys at (8% to the distributor) | **6.63 - we receive this** |
| Less COGS | (2.10) |
| Less secondary freight | (0.15) |
| Less trade spend | (0.30) |
| **Contribution** | **4.08 (61.5%)** |

COGS build, Rs 2.10: powder 1.15, laminate and fill 0.55, outer box and carton 0.22,
inward freight and wastage 0.18.

**GST classification is worth up to 13 points.** Proprietary food (HSN 2106) at 18% is the
prudent read and the one used throughout. An ORS/drug classification (HSN 3004) would give us
Rs 7.82 rather than Rs 6.63, but FSSAI has banned the word "ORS" on labels, so we do not plan
on it. A caffeinated classification would cost us, and we have no caffeine.

---

## 2. The volume correction, made 10 August

The pitch assumed **10 sachets a day in each of 60,000 outlets**. The 60,000 outlets are
conservative, being 0.5% of India's 13m kirana shops. **The rate of sale is roughly four times
too high as a twelve-month average.**

At 10 a day, year one revenue is Rs 143 crore. That is **25% of Electral**, India's number one
ORS brand, selling since the 1970s, and **22-27% of the entire Rs 800-1,000 crore ORS category
in our first year**. It passes the shopkeeper test in a good outlet in May. It does not survive
as the average of 60,000 shops over twelve months.

**Planning case is now 2.5 sachets/outlet/day = 4.5m sachets/month.**

One thing the lower forecast does not change: we are planning conservatively and **buying
capacity optimistically**. The factories have been asked to price at 1.5m, 6m and 18m sachets a
month, and for **peak** monthly capacity rather than average, because this product sells into
the Indian summer. On our own numbers a normal seasonal curve is ~108 tonnes in the peak month
against 22 in the trough, and a line sized to the average cannot serve that. Specifying the
headroom costs nothing today.

---

## 3. The downside you asked for

Flexing only the three you named - cost of goods, contribution margin, distribution costs -
and holding volume at the corrected Base case.

| # | Case | COGS | We get | Contribution | Margin | Year at Base |
|---|---|---|---|---|---|---|
| 1 | Plan, as pitched | 2.10 | 6.63 | 4.08 | 61.5% | GBP 2.08m |
| 2 | COGS only (Rs 2.75) | 2.75 | 6.63 | 3.43 | 51.7% | GBP 1.75m |
| 3 | Trade terms only (18% / 10%) | 2.10 | 6.25 | 3.45 | 55.2% | GBP 1.76m |
| 4 | Both | 2.75 | 6.25 | 2.80 | 44.8% | GBP 1.43m |
| 5 | Stress (Rs 3.25, 20% / 12%) | 3.25 | 5.97 | 1.87 | 31.3% | GBP 0.95m |

Margin is stated as contribution over **what we receive**, the same basis as page 8 of the
pitch. On a shelf-price basis the plan case reads 48% rather than 61.5%; that is a change of
denominator, not a change in the business.

**Volume x margin, annual contribution, GBP m**

| Volume | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Plan, 10/outlet/day (18m/mo) | 8.31 | 6.98 | 7.04 | 5.71 | 3.80 |
| **Base, 2.5/day (4.5m/mo)** | **2.08** | 1.75 | 1.76 | **1.43** | 0.95 |
| Low, 1.5/day (2.7m/mo) | 1.25 | 1.05 | 1.06 | 0.86 | 0.57 |

Margin alone moves contribution from Rs 4.08 to Rs 1.87 a sachet, a 54% cut. Crossed with
volume, year one runs **GBP 0.57m to GBP 8.31m**. The honest planning number is the Base row,
and within it I would work to case 4, **GBP 1.4m**, until a factory has quoted.

---

## 4. What would actually move these numbers, in order

1. **The manufacturer's price.** Rs 2.10 is our estimate. Every 50 paise of error is 12% of
   contribution at the plan margin. Nobody has quoted. This is the critical path.
2. **What the distributor takes.** 8% is assumed, not agreed. At 8% a distributor earns
   Rs 0.58 a sachet and cannot live on us alone in year one, which is why we want to be one
   line in an existing distributor's book rather than have a dedicated one.
3. **GST classification.** Covered above. Prudent read already taken.

## 5. Set-up cost

Separately modelled at roughly **GBP 66k lean, GBP 86k with the unique-code system and retailer
scan-and-collect app built**. Most lines are still estimates; the trade mark is now quoted at
GBP 810. The app is GBP 20k of the difference and the pilot does not need it - 300 outlets can
be run on WhatsApp and UPI by hand.

Workings: `docs/everest-power/economics.py`, `downside.py`, `setup_costs.py`, and the demand
test at `docs/bgep-demand-test-2026-08-10/`.
