# Modern Savage Launch Model

**Date:** 2026-04-03  
**Prepared by:** Junior

> This is the missing operator layer for Modern Savage: a simple commercial model Jesse can use to pressure-test launch economics before paid traffic scales.

---

## Executive take

Modern Savage now has positioning, copy, and conversion direction. The next thing it needs is **commercial discipline**.

This model gives Jesse a clean way to answer the questions that matter:
- what CAC still works?
- what AOV do we need?
- what gross margin protects us?
- when does subscription make paid media safer?
- what does month 1 vs month 3 look like if performance is good, base, or weak?

The practical goal is to stop Modern Savage from becoming a brand that sounds premium but is economically soft.

---

## What this model is designed to do

Use it to sanity-check:
1. first-order profitability
2. contribution margin after ad spend
3. breakeven CAC
4. 90-day LTV sensitivity
5. bundle and subscription impact

This is intentionally simple enough to use fast.

---

## Recommended starting assumptions

These are directional launch assumptions, not final truths.

### Base product assumptions
- Single bottle price: **$59**
- 2-bottle bundle price: **$109**
- 3-bottle bundle price: **$149**
- Subscribe & save price: **$52**

### COGS assumptions
- Product COGS per bottle: **$15**
- Pick/pack + payment + variable ops per order: **$6**
- Shipping contribution by brand: **$5** average per order

### Mix assumptions
- 1 bottle share: **45%**
- 2 bottle share: **30%**
- 3 bottle share: **10%**
- subscription first-order share: **15%**

### Paid media assumptions
- Base CAC: **$42**
- Good CAC: **$32**
- Weak CAC: **$55**

### Retention assumptions
- Month-2 reorder / subscription continuation rate: **45%**
- Month-3 continuation rate: **35%**

### Margin target
- Target contribution margin after ad spend on first order: **15%+**

---

## Core formulas

### 1. Gross revenue per order
Weighted average order value:

`AOV = Σ(price x order mix)`

### 2. Weighted bottles per order
`Bottles per order = Σ(bottles in offer x order mix)`

### 3. Variable cost per order
`Variable cost = (weighted bottles x COGS per bottle) + ops + shipping contribution`

### 4. Gross profit before CAC
`Gross profit pre-CAC = AOV - variable cost`

### 5. Contribution after CAC
`Contribution = gross profit pre-CAC - CAC`

### 6. First-order contribution margin
`Contribution margin = contribution / AOV`

### 7. Breakeven CAC
`Breakeven CAC = gross profit pre-CAC`

---

## Base-case output

Using the assumptions above:

### Weighted AOV
- 1 bottle: 45% x $59 = **$26.55**
- 2 bottle: 30% x $109 = **$32.70**
- 3 bottle: 10% x $149 = **$14.90**
- subscription: 15% x $52 = **$7.80**

**Weighted AOV = $81.95**

### Weighted bottles per order
- 1 bottle: 0.45 x 1 = **0.45**
- 2 bottle: 0.30 x 2 = **0.60**
- 3 bottle: 0.10 x 3 = **0.30**
- subscription: 0.15 x 1 = **0.15**

**Weighted bottles per order = 1.50**

### Variable cost per order
- Bottle cost: 1.50 x $15 = **$22.50**
- Ops + payment: **$6.00**
- Shipping contribution: **$5.00**

**Total variable cost = $33.50**

### Gross profit before CAC
**$81.95 - $33.50 = $48.45**

### Contribution by CAC scenario
- Good CAC ($32): **$16.45 contribution** / **20.1% margin**
- Base CAC ($42): **$6.45 contribution** / **7.9% margin**
- Weak CAC ($55): **-$6.55 contribution** / **-8.0% margin**

### Read on that
At the current base assumptions, Modern Savage is:
- **healthy** if CAC lands around low 30s
- **fragile** in the low 40s
- **soft/unacceptable** if CAC drifts into the mid-50s

That means the business cannot rely on vague premium branding alone. It needs either:
1. stronger AOV through bundles,
2. better gross margin,
3. lower CAC through creator and creative fit,
4. or stronger retention economics.

---

## Breakeven guardrails

### Breakeven CAC
**$48.45**

That is the hard ceiling at the base model. Realistically Jesse should not run near ceiling.

### Recommended operating bands
- **Green zone:** CAC under **$35**
- **Yellow zone:** **$35–$42**
- **Red zone:** above **$42** unless retention is proving out quickly

### Why this matters
If CAC comes in at $44–$48, the brand can fool itself because revenue still looks exciting. But it is buying volume without enough economic protection.

---

## Highest-leverage improvements

## 1. Push bundle mix up fast
If Jesse increases 2- and 3-bottle share, the model gets safer quickly.

### Example improved mix
- 1 bottle: 30%
- 2 bottle: 40%
- 3 bottle: 20%
- subscription: 10%

With the same pricing, weighted AOV rises materially and CAC tolerance improves.

### Takeaway
The page should sell **consistency and stocking up**, not just trial.

---

## 2. Protect gross margin before traffic scales
If real fully loaded bottle COGS lands above $15, paid media tolerance drops hard.

### Rule
Before scaling traffic, Jesse should know the real numbers for:
- bottle landed cost
- pack-out cost
- card fees
- shipping subsidy
- refund rate

The brand should not guess here.

---

## 3. Treat subscription as margin protection, not just retention theater
A subscription box checked by default helps only if the subscriber actually sticks.

The important metric is not initial opt-in rate alone.
It is:
- first renewal rate
- second renewal rate
- pause/cancel reasons

### Good early target
- first-order subscription share: **15–20%**
- first renewal rate: **45%+**

If that happens, CAC in the high 30s becomes much safer.

---

## 4. Use creator seeding to beat platform CAC
If Modern Savage relies only on cold paid traffic from day one, the model is exposed.

The smart move is to blend:
- direct-response Meta creative
- creator UGC
- seeded testimonials
- founder/operator-style content

That gives the brand a better shot at sub-$35 CAC before serious scaling.

---

## 90-day LTV snapshot

This is a rough directional view using the base assumptions.

### Month 1
- Weighted revenue: **$81.95**
- Variable cost: **$33.50**
- Gross profit pre-CAC: **$48.45**

### Month 2 retained cohort economics
Assume 45% of buyers generate one additional order at a net realized revenue of **$55** with **$26** variable cost.

- Month-2 retained gross profit per retained customer: **$29**
- Weighted across whole cohort: 0.45 x $29 = **$13.05**

### Month 3 retained cohort economics
Assume 35% of original cohort generates another order with same gross profit profile.

- Weighted month-3 cohort gross profit: 0.35 x $29 = **$10.15**

### Rough 90-day gross profit per acquired customer before fixed overhead
**$48.45 + $13.05 + $10.15 = $71.65**

### Implication
If the retention assumptions are real, CAC can stretch above first-order comfort **somewhat**. But Jesse should not assume this until real data confirms it.

---

## Decision rules Jesse can use immediately

### Scale paid traffic if:
- CAC is under **$35** consistently
- bundle mix is improving
- subscription share is **15%+**
- refund signals are clean

### Hold and refine if:
- CAC is **$35–$42**
- CVR is decent but AOV is soft
- bundle take rate is weak
- creator content is not yet integrated

### Stop pretending and fix the machine if:
- CAC is above **$42**
- 1-bottle mix dominates
- subscription opt-in is weak or cancels fast
- actual contribution after refunds is near zero or negative

---

## Best immediate actions

1. Build the landing page so the **2-bottle bundle is the merchandising hero**.
2. Keep **subscription selected by default**, but make the value obvious rather than gimmicky.
3. Create a simple weekly dashboard with these six numbers:
   - CAC
   - CVR
   - AOV
   - bundle mix
   - subscription share
   - refund rate
4. Do not scale spend aggressively until real breakeven math is verified with live order economics.
5. Treat creator UGC as a CAC tool, not just a branding extra.

---

## Final call

Modern Savage can work.

But it will work because the brand combines **strong identity + strong economics**, not because premium language hides weak numbers.

The safest launch posture is:
- premium brand
- bundle-led merchandising
- subscription as margin support
- strict CAC discipline
- creator content to lower acquisition cost

That is the version with the best shot at becoming a real business instead of an expensive aesthetic.
