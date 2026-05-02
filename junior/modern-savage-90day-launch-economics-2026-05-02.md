# Modern Savage — 90-Day Launch Economics Model

**Built:** May 2, 2026 (overnight build)
**For:** Jesse, Monday May 4 morning
**Companion to:** modern-savage-financial-model-2026-04-28.md (Year 1 view) and modern-savage-launch-date-reality-check-2026-05-02.md (Model A/B decision)
**Status:** Decision-grade. Validate COGS and Calvin retainer split before betting on absolutes.

---

## Why this model exists

The April 28 model answered "is Modern Savage a viable business by Year 1." The April 28 model assumed product is in hand, no float, no pre-order, USD pricing, monthly average churn.

Three things have changed since:

1. Lightning Nutra ship date is uncertain (Pulse 57). Launch is now either Model A (pre-order with explicit ship date) or Model B (delayed launch). Each has different week-by-week economics.
2. Pricing is being set in GBP for UK launch (£59 / £47 founding / £39 kids / £89 family) pending Raemy reply Monday.
3. Cohort behavior matters more than monthly averages. The 170 founding members are not the same animal as the August acquisition cohort — they self-selected, they are warmer, they will churn differently.

This model fills those gaps. It runs week-by-week for the first 12 weeks (July 1 to September 22) — the period that determines whether Modern Savage breaks out or stalls.

---

## Section 1: Core economics in GBP

Re-baselining the April 28 model in GBP using the recommended pricing.

### Per-subscriber unit economics

| Line item | Founding member | Adult standard | Kids | Family bundle |
|---|---|---|---|---|
| Subscription price | £47 | £59 | £39 | £89 |
| Cadence | Monthly | Monthly | Monthly | Monthly |
| Stripe fees (2.5% + 20p UK card avg) | £1.38 | £1.68 | £1.18 | £2.43 |
| COGS — product (est. £14/bottle, validate with Chris Liming) | £14 | £14 | £14 | £28 (2 bottles) |
| COGS — UK fulfilment (est. £6/order via Ships A Lot UK) | £6 | £6 | £6 | £6 |
| Free shipping over £40 — eaten by MS | -£4 | -£4 | included | included |
| **Gross profit per subscriber per month** | **£21.62** | **£33.32** | **£17.82** | **£52.57** |
| **Gross margin %** | 46% | 56% | 46% | 59% |

**Validate before launch:**
- COGS estimate of £14/bottle is industry-typical for premium organ supplement at <500 unit batches. Could be £11-£18 range. Chris Liming knows the real number — his April 27 email did not include cost detail. CJ to extract this in the Wednesday May 7 written ship-date reply.
- Ships A Lot UK pick/pack cost was on the Susan U Qwilr (still unsigned). Junior estimate is £6 — could be £4-£8.
- Stripe UK card mix assumes ~70% debit (1.5% + 20p) / 30% credit (2.5% + 20p). Founding 170 may skew higher-quality cards; adjust if Klaviyo data shows otherwise post-launch.

### Subscriber-level lifetime value

LTV = monthly gross profit ÷ monthly churn rate.

| Cohort | Monthly churn assumption | LTV (£) |
|---|---|---|
| Founding 170 (high intent, brand attached) | 5% | £21.62 ÷ 0.05 = **£432** |
| Adult standard new acquisition (organic Bear) | 9% | £33.32 ÷ 0.09 = **£370** |
| Adult standard new acquisition (paid) | 12% | £33.32 ÷ 0.12 = **£278** |
| Kids tier | 8% | £17.82 ÷ 0.08 = **£223** |
| Family bundle | 6% | £52.57 ÷ 0.06 = **£876** |

**Implication:** Family bundle is structurally the highest-LTV product. If the launch optimises for adult-standard subscribers and ignores family, you leave the best customer on the table. Calvin's email sequence and the homepage hierarchy should not bury the family bundle.

---

## Section 2: Model A vs Model B — week-by-week launch economics

The launch operates under one of two models. The economics differ.

### Model A — Pre-order launch July 1, ship date disclosed

Stripe charges July 1 for everyone who orders. Product ships when Lightning Nutra delivers (best estimate: July 7-14). Customer waits 7-14 days for product.

**Float dynamics:** between July 1 and ship date, MS holds customer cash without delivered product. Useful for working capital. Risky for refunds — UK Distance Selling Regulations give a 14-day cooling-off period from delivery, so refund exposure is full ticket value through ~July 28-Aug 7.

Assumed July 1 conversion: 130 of 170 founding members order on day one (76% conversion rate — high because list was warmed for ~10 weeks).

| Week | Founding orders | New (organic) | Cumulative subs | Cash in (£) | Cash out (COGS+ship+Calvin+ad) | Net cash | Notes |
|---|---|---|---|---|---|---|---|
| W1 (Jul 1-7) | 130 | 5 | 135 | £6,403 | £2,810 | +£3,593 | Float starts. Email 5 sent Jul 1. |
| W2 (Jul 8-14) | 25 | 12 | 172 | £1,849 | £3,580 | -£1,731 | Product ships. Refund clock starts. |
| W3 (Jul 15-21) | 8 | 18 | 198 | £1,438 | £3,020 | -£1,582 | First product reviews land. NPS gate. |
| W4 (Jul 22-28) | 4 | 20 | 222 | £1,368 | £3,420 | -£2,052 | Mid-month replenishment ping. |
| W5 (Jul 29-Aug 4) | 0 | 22 | 244 | £1,298 | £3,160 | -£1,862 | First real churn check. |
| W6 (Aug 5-11) | 0 | 25 | 269 | £1,475 | £3,360 | -£1,885 | Family bundle conversion push. |
| W7 (Aug 12-18) | 0 | 28 | 297 | £1,652 | £3,580 | -£1,928 | Bear post 2 (Modern Savage). |
| W8 (Aug 19-25) | 0 | 30 | 327 | £1,770 | £3,800 | -£2,030 | Repeat billing cycle 2 starts. |
| W9 (Aug 26-Sep 1) | 0 | 32 | 359 | £1,888 | £4,020 | -£2,132 | Ship date reality check. |
| W10 (Sep 2-8) | 0 | 35 | 394 | £2,065 | £4,260 | -£2,195 | First sustained CAC test. |
| W11 (Sep 9-15) | 0 | 38 | 432 | £2,242 | £4,520 | -£2,278 | Q3 close. |
| W12 (Sep 16-22) | 0 | 40 | 472 | £2,360 | £4,780 | -£2,420 | 90-day retention readout. |

**12-week totals (Model A):**
- Cumulative cash in: £25,808
- Cumulative cash out: £44,310
- **Net cash position end of W12: -£18,502**
- Subscribers at end W12: 472
- MRR at end W12: ~£18,500

This is before founding-member retention shows up in cash. Most founding members renewed on Aug 1 are still showing in cash-in for W2-W4 of August. The W12 number is the "burn before economy works" figure — recoverable through October as MRR rolls.

### Model B — Delayed launch (e.g., July 22 once product confirmed in UK)

Three weeks of preparation lost on the front end, but no pre-order float. The 170 are warmed for an extra three weeks. Risk: list fatigue. Some will drop off.

Assumed July 22 conversion: 105 of 170 founding members order (62% — drop from 76% reflects list cooling).

| Week | Founding orders | New (organic) | Cumulative subs | Cash in (£) | Cash out | Net cash |
|---|---|---|---|---|---|---|
| W1 (Jul 1-7) | 0 | 0 | 0 | £0 | £1,500 (Calvin retainer half) | -£1,500 |
| W2 (Jul 8-14) | 0 | 0 | 0 | £0 | £1,500 | -£1,500 |
| W3 (Jul 15-21) | 0 | 0 | 0 | £0 | £1,500 | -£1,500 |
| W4 (Jul 22-28) | 105 | 5 | 110 | £5,170 | £2,500 | +£2,670 |
| W5 (Jul 29-Aug 4) | 25 | 12 | 147 | £1,883 | £2,940 | -£1,057 |
| W6 (Aug 5-11) | 12 | 18 | 177 | £1,646 | £3,420 | -£1,774 |
| W7 (Aug 12-18) | 4 | 20 | 201 | £1,368 | £3,560 | -£2,192 |
| W8 (Aug 19-25) | 0 | 22 | 223 | £1,298 | £3,800 | -£2,502 |
| W9 (Aug 26-Sep 1) | 0 | 25 | 248 | £1,475 | £4,000 | -£2,525 |
| W10 (Sep 2-8) | 0 | 28 | 276 | £1,652 | £4,200 | -£2,548 |
| W11 (Sep 9-15) | 0 | 30 | 306 | £1,770 | £4,440 | -£2,670 |
| W12 (Sep 16-22) | 0 | 32 | 338 | £1,888 | £4,640 | -£2,752 |

**12-week totals (Model B):**
- Cumulative cash in: £18,150
- Cumulative cash out: £38,000
- **Net cash position end of W12: -£19,850**
- Subscribers at end W12: 338
- MRR at end W12: ~£13,300

### Headline comparison

| Metric | Model A (pre-order) | Model B (delayed) | Difference |
|---|---|---|---|
| W12 subscriber count | 472 | 338 | +134 (+40%) |
| W12 MRR | £18,500 | £13,300 | +£5,200 (+39%) |
| W12 cumulative net cash | -£18,500 | -£19,850 | +£1,350 (better) |
| Founding cohort conversion | 76% | 62% | +14 pts |
| Refund risk window | Jul 1 - Aug 7 | Jul 22 - Aug 28 | A is more compressed |
| Brand risk | Pre-order communication failure | Launch slip optics | Different |

**Recommendation: Model A unless Chris Liming's confirmed ship date slips beyond July 21.** The pre-order model produces a meaningfully larger subscriber base by W12 (472 vs 338) and gets to MRR break-even faster. The risk is execution on customer communication (the refund clock + the Email 5 explicit ship date language). Both are within Calvin's competence if briefed correctly.

The April 28 brief said: "Model A if confirmed ship date is on or before July 14. If it slips beyond July 14 (more than two weeks late), Model B is cleaner." This week-by-week analysis backs that — the specific cutoff is "ship date on or before July 21" because the marginal subscriber gain compounds for 8 weeks before the next billing cycle resets.

---

## Section 3: The single lever that moves outcomes most

Modern Savage has three controllable economic levers. Sensitivity analysis on each:

### Lever 1: Founding cohort conversion rate
- Base assumption: 76% of 170 = 130 conversions
- Each +5 percentage points = +9 customers = +£300/mo gross profit = +£3,600 LTV total
- Worth fighting for: yes, but ceiling is ~85% (some signups will inevitably ghost)

### Lever 2: Monthly churn rate
- Base assumption: 9% standard, 5% founding
- Each -1 percentage point on standard cohort = LTV jumps from £370 to £416 = **+12.5%**
- At W12 with 472 subscribers, every 1pt of churn reduction is worth £4,720 cumulative gross profit over 12 months
- Lever pulled by: product quality, replenishment UX, NPS at delivery, the 7-step retention email flow

### Lever 3: New acquisition velocity
- Base assumption: 5-40 organic adds per week, ramping
- Each +10 organic adds per week sustained = +120 new subs over 12 weeks = +£4,000 MRR by W12
- Lever pulled by: Bear posts, Running Wild MGK ep, content cadence, the July 9 book launch overlap

**Highest-leverage lever: churn.** A 1-point churn reduction is worth more cumulative profit than a 10-customer-per-week acquisition increase. And churn is cheaper to influence (the existing retention playbook stub is mostly free).

**What this means operationally:** Calvin's Modern Savage SOW currently emphasises new content and new subscribers. If the SOW does not have a specific churn KPI baked in, it is mis-targeted. The negotiation brief should add: "Calvin's monthly KPIs include a stated 90-day cohort retention target of 70%+."

---

## Section 4: Operator dashboard — what Jesse watches weekly

12 weeks of Modern Savage launch lives or dies on six numbers. Everything else is noise.

| Metric | Source | W1 target | W4 target | W12 target | Red flag |
|---|---|---|---|---|---|
| Founding cohort conversion | Stripe | 70% | 78% | 80% | Below 60% W1 |
| New paying subs added | Stripe | 5 | 80 (cumulative) | 300 (cumulative) | Flat W3 to W4 |
| Cohort 1 (Aug billing) retention | Stripe | n/a | n/a | 70%+ | Below 55% |
| Refund rate | Stripe | <2% | <4% | <5% | Above 7% sustained |
| NPS / 5-star reviews | Klaviyo + Trustpilot | 5+ reviews | 25+ reviews | 80+ reviews | Avg below 4.2 |
| Customer support volume | support@ inbox | <20 emails | <80 emails | <250 emails | Spike to 50+/day |

The dashboard fits on one screen. Junior to build the auto-refresh version on the BGV dashboard before July 1. Stripe + Klaviyo APIs both exist for this. Estimated 4 hours work — should be on Felix's queue or my own once Calvin SOW is signed.

---

## Section 5: Cash runway during the 12-week window

The big question: does MS need money to get through W12?

### Fixed costs during launch window (July 1 - Sep 22, ~13 weeks)

| Line item | Per week | 13-week total |
|---|---|---|
| Calvin / Ku Creatives (1/3 allocation to MS, $3K/mo total = $1K/mo MS) | £200 | £2,600 |
| Klaviyo subscription | £80 | £1,040 |
| Stripe subscription billing tooling | £40 | £520 |
| Domain + hosting (Netlify, Cloudflare) | £20 | £260 |
| Regulatory + minor legal | £100 | £1,300 |
| Customer support tooling | £50 | £650 |
| **Total fixed overhead** | **£490/wk** | **£6,370 / 13 wks** |

### Variable costs during launch window (Model A)

| Line item | 13-week total |
|---|---|
| Product COGS (proportional to orders shipped) | £21,000 |
| UK fulfilment | £9,000 |
| Stripe processing | £2,500 |
| Free-shipping subsidy | £2,400 |
| Refunds reserve (5% of revenue) | £1,800 |
| **Total variable** | **£36,700** |

### Cash position needed in MS UK Ltd at July 1

To cover -£18,500 trough at W12 plus a £5,000 buffer = **£23,500 working capital**.

This is not a fundraising number. It is a "do not start the launch with less than this in the entity bank account" number. If the Lightning Nutra deposit was already paid out of Bear Witness funds and not reimbursed, it counts against this.

---

## Section 6: What Jesse decides Monday from this model

1. **Approve the Model A vs B threshold:** "Model A if Chris Liming's written ship date is July 21 or earlier. Model B if it slips beyond July 21." (Currently the April 28 brief says July 14 — this model recommends extending to July 21 based on cohort math.)

2. **Send Raemy a working-capital question:** "What's in the Modern Savage UK Ltd bank account on July 1, and what working capital needs topping up if any?" (£23,500 floor for Model A.)

3. **Add a churn KPI to Calvin's SOW.** Specifically: "Cohort retention 70%+ at month 3 measured on the original 170 founding members." Tie to bonus or trigger renegotiation.

4. **Validate three numbers with Chris Liming and Susan U via CJ this week:**
   - Lightning Nutra COGS per bottle at the order volume committed
   - Ships A Lot UK pick/pack rate
   - Refund handling fee per returned unit (UK side)

If all three numbers come back materially worse than this model's estimates (COGS over £18, fulfilment over £8, refund fees over £3), the gross margin moves from 56% to ~48% and the W12 net cash moves from -£18,500 to roughly -£24,000. Still survivable but reduces buffer.

---

## Why this matters more than the chase-up list

The chase-up list and metricool queue are 24-hour problems. The economics of the launch determine whether Modern Savage becomes a £40K MRR company by Year 1 (April 28 base case) or stalls at £8K MRR (a real downside if churn lands above 12%). The fastest way to lose this business is to launch without a churn target in the operator KPI structure and discover at month 3 that subscribers are leaving faster than they arrive.

Jesse already knows this intuitively. This model converts the intuition into specific decisions and numbers.

---

*Junior, May 2 2026 (overnight build). Cross-references: modern-savage-financial-model-2026-04-28.md, modern-savage-launch-date-reality-check-2026-05-02.md, modern-savage-launch-week-playbook-2026-04-29.md, calvin-sow-negotiation-brief-2026-04-29.md.*
