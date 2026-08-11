# Modern Savage: US unit economics

**Built overnight, 11 August 2026. First complete build.**

Until yesterday the US model had a hole in it. Ships A Lot had been the assumed US 3PL since
July on no rate card and no contract. Susan U's card arrived 10 Aug inside Beau's status email,
so for the first time every US cost line can be filled in. This is that model, plus what it says.

Runnable: `model.py`. Every input is tagged VERIFIED, QUOTED, ESTIMATE or UNKNOWN. Re-run it
rather than quoting these figures once packed weights and a contract exist.

---

## The headline

**Contribution is healthy and pricing is not the problem. 53% of gross on a single pouch,
53% on the full stack.** The product works at these prices. What follows is about which
orders to chase and which costs are still loose, not about whether the business makes money.

| Order (US, subscribed, mid-zone) | Gross | COGS | Fulfilment | Contribution | Margin |
|---|---|---|---|---|---|
| Single pouch, adult | $76.99 | $24.45 | $9.14 | **$40.87** | 53.1% |
| Single pouch, Summit | $76.99 | $18.90 | $8.81 | **$46.75** | 60.7% |
| Full stack, all three | $180.00 | $65.63 | $13.06 | **$95.79** | 53.2% |

COGS are the actual ACF invoice S1825 line prices per SKU, not the blended $21.33 that has
been circulating since 2 Aug. Adult $24.45, Mini $22.28, Summit $18.90.

---

## Five findings

### 1. The basket is the only fulfilment lever that matters

The order fee and the carton are charged per **order**. Only the pick and the postage scale
with units. So fulfilment per pouch collapses as the basket grows:

- 1 pouch: **$9.14** per pouch
- 2 pouches: **$5.80** per pouch, down 36%
- 3 pouches: **$4.35** per pouch, down 52%

Nothing negotiable off Susan's rate card comes close to a 52% cut. Stop thinking about the
rate card as something to haggle over and start thinking about the basket.

### 2. Stack-led needs 2.34x fewer orders to cover the ACF balance

$82,082.50 falls due to ACF on completion. Against pre-order cash kept after Stripe:

- **470 full-stack orders** covers it
- **1,102 single orders** covers it

Same customer count, same marketing spend, and the same draw on the scarce adult pouch,
because a bundle takes one from each SKU. The difference is entirely which offer the page
leads with, and it costs nothing to change.

**The shop page currently leads with three separate product tiles at "From £55/month" and
puts the bundle behind a small "View the bundle" link.** That is backwards. I checked the
live page tonight.

### 3. Do not add a 2-pack

I modelled one at $128. It contributes $65.65 against the stack's $95.79. A middle tier
pulls down from the top more reliably than it pulls up from the bottom, and at $128 it
crosses the ~$100 free-shipping threshold, so we absorb the postage that a $69 single
customer pays themselves. Two tiers, single and stack, with the stack as the default.

### 4. The receiving trap, and it has to be caught before the run is packed

Ships A Lot charge single-SKU and mixed-SKU handling at wildly different rates:
$15 vs $30 per pallet, and **$5 vs $30 per case**. On an estimated 625 cases across the
7,500-unit run, the spread between best and worst handling is on the order of **$15,000 to
$18,000**, decided by nothing except how Drew packs the truck.

The instruction is free and has to be given before the run is packed: **single SKU per
pallet, single SKU per case.** This is the identical trap we already caught and fixed at
SCEND, where it saved about £650.

### 5. Project labour has a $180 floor and bundles are what could trigger it

$45/hour with a **four-hour minimum**, charged per work-order quote. If Ships A Lot treat a
bundle as a pre-kitted work order rather than a normal three-unit pick, that floor lands
again and again, precisely because we are about to lead on bundles. Get it in writing that
a bundle picks as three units at $0.50.

---

## Two things I got wrong and am correcting

**The US/UK fulfilment gap is 35%, not the 44% I said on 10 Aug.** That figure used a stale
FX rate. SCEND's £5.01 all-in is $6.76 at tonight's 1.3486 against Ships A Lot's $9.14.
Still mostly geography, still a P&L number rather than a negotiating stick.

**Zone sensitivity does not matter, and I assumed it would.** Zones 1 to 8 move a single
order's contribution by $1.22 in total. Ships A Lot's postage is close to zone-flat across
the mainland, which is unusual and is a point in their favour. Warehouse siting is not a
lever here and the pre-order book does not need pulling apart by geography. Zone 9, being
Alaska, Hawaii and territories, is the only row worth watching.

---

## What to ask, and who holds it

**Susan U at Ships A Lot, before anything is signed:**
1. The carton and mailer lines are all marked application "Per Unit". A carton is physically
   per order. Which is meant? On a 3-pack the literal reading costs $1.22 an order, about
   $11,700 a year at 800 bundles a month.
2. Confirm a bundle picks as three units at $0.50, not as a project-labour work order.
3. There is no returns or RMA line anywhere on the card. Price it now, while Beau is writing
   the returns SOP.
4. The postage table stops at 5 lb and a 3-pack already sits on the last row.

**Drew at ACF, before the run is packed:** single SKU per pallet and per case.
Also the **packed** shipped weights, not the fill weights, which is the ask already with Beau.
Every postage figure in this model is an estimate until those land.

**The one that outranks all of it: there is no Ships A Lot contract.** No executed agreement,
no signed proposal, and no rate card at all until yesterday, for a 3PL we have been treating
as chosen since July. Every good term we have at SCEND, the zero minimum, no setup fee, the
£15 pallet rate, was agreed **before** signature. Beau wants to book onboarding now to be
"locked and loaded". The order is contract, then onboard, then PO.

---

## Still unknown

- Returns and RMA: unpriced
- Carton and mailer supplies: all marked "will review when product received", so not agreed
- Packed shipped weights: ACF give fill weights
- Setup, minimum monthly, integration, exit and removal charges: absent from the card, and
  absent is not the same as zero when there is no contract to record the absence
- The actual pre-order book. Felix's dashboard has it, this model does not. Drop the real
  order count and mix in and the treasury section stops being hypothetical.

**The caveat that limits the whole treasury section:** pre-order cash is a refundable deposit.
Our own site says in three places that the customer can cancel for a full refund any time
before dispatch, and roughly half the book is UK, where nothing dispatches this year. All the
funding arithmetic above is US-side only.

---

*Sources: Ships A Lot rate card and postage table, Susan U via Beau Bennett 10 Aug 2026
(`workspace/evidence/beau-status-2026-08-10/`). ACF invoice S1825, 20 Apr 2026. SCEND terms,
Jack Crumpton 23 Jul 2026. modernsavage.co read 11 Aug 2026 for UK prices, 2 Aug 2026 for US.
GBP/USD 1.348598, open.er-api.com, 11 Aug 2026.*
