# Modern Savage: does October hold?

**The pre-order re-date decision, and the one week it has to be made in.**

Junior, 14 August 2026. Built overnight.
Model: `workspace/docs/ms-october-decision-2026-08-14/model.py`. Re-run it, do not quote from here
once the pre-order book and Andrew's start date are real numbers.

---

## The answer, in five lines

1. **October holds only if ACF started the 12-week clock on or before 26 July.** That is the
   break-even, worked backwards. Nobody has asked Andrew the question in those words.
2. **Even if the clock starts today, we land on 19 November** and that is survivable, because it
   falls inside the 30-day window where a delay notice runs on silence rather than consent.
3. **We get exactly one cheap notice.** A second one refunds roughly six times as much, by law, no
   matter how good the new date is.
4. **The hard deadline is 31 October.** Not for shipping. For *telling people*. Miss it and the
   remedy stops being a new date and becomes refunding the book.
5. **The cheapest item on the critical path is a $250 barcode purchase** that has been blocked since
   yesterday morning by a deleted draft.

---

## What we have actually promised

Verified live on modernsavage.co at 01:20 this morning, on `/shipping`, `/returns` and `/terms`,
in these words:

> "We are aiming to deliver around October 2026. If that date moves we will email you with the new
> one, and you can either wait or cancel for a full refund at that point."

> "Your card is charged in full when you order, not when we dispatch."

Two things follow that are worth being plain about. The public promise is **October**, not
September, so Andrew's "launch sometime in September" is upside against what customers were told,
not the commitment. And because the card is charged in full at order, **the pre-order book is
already cash on our side of the table**, which makes a cancellation event a treasury event rather
than a customer service one.

Seller of record is Modern Savage Inc., Delaware. Terms last updated 5 August.

---

## The three readings of "12 weeks"

Andrew told Beau on 13 August that it takes **12 weeks to manufacture**, **3 days to ship to
Mississippi**, and that we should still be able to **launch sometime in September** because we were
ready to go in July. Those statements only reconcile if the clock started in July. Worked forward
from each possible start, adding 3 days freight, 5 days for Ships A Lot to receive and put away,
and the 3 to 5 day transit the site itself promises:

| Clock starts | Made | First dispatch | Customer has it | |
|---|---|---|---|---|
| 1 July | 23 Sep | 1 Oct | 6 Oct | holds |
| 15 July | 7 Oct | 15 Oct | 20 Oct | holds |
| **26 July** | 18 Oct | 26 Oct | **31 Oct** | **break-even** |
| 31 July | 23 Oct | 31 Oct | 5 Nov | misses |
| Today, 14 Aug | 6 Nov | 14 Nov | 19 Nov | misses |
| On artwork, ~1 Sep | 24 Nov | 2 Dec | 7 Dec | misses |

**The whole thing turns on one yes/no question:** did ACF begin the 12 weeks on or before 26 July?
Beau has been asked to get the start date in writing and Andrew said he would send an approximate
date by the end of this week. That is the single highest-value answer available to us right now, and
it costs one line of email.

---

## Why the worst case is still survivable

This is the part that turns it from an alarm into a decision.

If the clock only starts today, first dispatch is **14 November**. The end of the promised window is
31 October. The gap is 14 days, and the line that matters sits at 30 days:

```
promised window ends        31 Oct
+ 30 days                   30 Nov   <- the silence-as-consent cliff
worst-case dispatch         14 Nov   <- inside it
```

Under the FTC's Mail, Internet or Telephone Order Merchandise Rule, verified at the FTC's own
business guidance this morning, a **first** delay notice giving a definite revised date **30 days or
less** after the originally promised time may tell customers that **non-response counts as consent
to the delay**. Only people who actively choose to cancel get refunded.

A first notice with a revised date **more than 30 days** later, or with no date at all, flips it:
non-response becomes automatic cancellation and refund. That is the cliff, and on any book size it
is roughly a six-fold difference in refunded cash.

So even on the worst honest reading of Andrew's 12 weeks, a single notice re-dating dispatch to
**30 November** stays on the cheap side of the line.

---

## The two ways this gets expensive

**One: a second notice.** A renewed delay notice cannot use silence as consent. The FTC is explicit:
*"One important difference: the customer's silence may not be treated as a consent to delay."* On a
500-order book, the identical re-date costs about $5,300 as a first notice and about $30,000 as a
second. The lesson is not to re-date early, it is to **re-date once, to a date we will actually
hit.** An optimistic revised date that slips again converts the entire silent majority into refunds.

**Two: going quiet past 31 October.** The notice has to land inside the originally promised time.
The FTC guidance: *"no notification to the customer can take longer than the time you originally
promised... If you cannot ship the order or provide the notice within this time, you must cancel the
order and make a prompt refund."* Waiting to see how it plays out, and then writing in November, is
the one move that turns a manageable slip into refunding the book.

**The UK book does not carry either mechanic.** Under the Consumer Rights Act 2015 section 28, where
a delivery period has been agreed, a consumer who does not get the goods must specify a further
reasonable period and only then may treat the contract as at an end. Silence changes nothing. The
legal exposure is concentrated almost entirely in the US orders, and that asymmetry is worth knowing
before anyone panics about the whole book.

---

## What it costs, by size of book

I have never been given the pre-order count. It sits on Felix's dashboard. So these are shapes, not
forecasts. Blended order value $105.80, built on the verified site prices, 65% US.

| Book | First notice, 30 days or less | First notice, more than 30 days |
|---|---|---|
| 250 orders | $2,645 refunded | $15,024 refunded |
| 500 orders | $5,290 refunded | $30,047 refunded |
| 1,000 orders | $10,580 refunded | $60,094 refunded |
| 2,000 orders | $21,160 refunded | $120,189 refunded |

Against that, **$82,082.50 is due to ACF on delivery**. The book has to clear that number. On the
cheap notice it does so from about 900 orders. On the expensive one it needs roughly 1,800. That
gap, between one kind of email and another, is the difference between the run funding itself and
needing money from somewhere else.

Two things get worse every week we say nothing: the book grows, so the same percentage refunds more
cash, and the 31 October deadline gets closer. They multiply.

---

## The testing decision, before it silently costs a month

Andrew strongly recommends **full panel testing and accelerated stability testing** on the first
batch, and wants to send batch one to a lab and come back with pricing. He is right on the substance.
If we want to make strong claims we need the panel.

The trap is sequencing, and nobody has drawn it yet:

- **Full panel** (identity, potency, heavy metals, microbiological) is the one that should gate
  dispatch. It runs while the pallet is in freight and being received. Book the lab slot **now**,
  not when the batch is made, because the queue is the long pole, not the assay.
- **Accelerated stability does not gate dispatch and must not be allowed to.** It validates the
  best-by date, and it reports on one, two and three month pulls by design. Gate shipping on it and
  we add a quarter to the launch for a number we can set conservatively today.

This connects to Beau's own open task, to find the temperature limits and set a best-by for each
SKU. Same decision, two places.

---

## What has to happen this week

Regardless of which reading of the clock turns out to be true:

1. **Get Andrew's start date in writing.** One line. It decides everything above. He offered it by
   the end of this week, so this is a reminder, not an ask.
2. **Buy the GS1 barcodes.** $250 for a prefix covering ten products, about $50 a year to maintain,
   in Modern Savage Inc's name because GTINs are valid worldwide. Andrew independently recommended
   the same thing. The pouch artwork cannot be finished without the numbers, and the pouch is the
   gate. This is blocked on a draft to Raemy that was deleted yesterday morning.
3. **Ask Belmark for their print lead time.** Still unasked since 7 August, and it is the last
   unmeasured link in the US chain. If printing runs after the blend rather than alongside it, every
   date in this document moves right.
4. **Book the lab slot for the full panel.** Ahead of the batch, not after it.
5. **Decide the re-date posture now, so it can be executed on the day the start date lands.** My
   recommendation is below.

---

## Recommendation

**Do not re-date yet, and do not wait past the answer.** Andrew's start date arrives this week. It
resolves the question completely, and re-dating before it arrives spends our one cheap notice on a
guess.

**When it lands, one of two things happens.** If the clock started on or before 26 July, October
holds, we say nothing publicly, and the site copy stands. If it started later, we send **one** delay
notice, immediately, giving a definite dispatch date of **30 November** rather than the earliest date
we can defend. That date is inside the 30-day window on every reading of the clock including the
worst, which means silence counts as consent, and it is conservative enough that we will not need a
second notice. The whole cost of this decision sits in that word "second".

**If the start date has not arrived by Friday next week, treat the silence as the answer** and
proceed as though the clock starts now. A 30 November notice sent in late August against a small book
is cheap. The same notice in late October, against the largest book we will ever have, is not, and
one sent in November is not a notice at all.

---

*Sources opened for this: modernsavage.co /shipping, /returns, /terms and homepage metadata, live at
01:20 on 14 Aug 2026. Beau Bennett's "Major Updates" email of 13 Aug 19:43 for everything attributed
to Andrew Kouvel. FTC business guide to the Mail, Internet or Telephone Order Merchandise Rule.
Consumer Rights Act 2015 section 28 on legislation.gov.uk. ACF invoice S1825 for the balance due.*

*Not verified, and flagged as such: the pre-order book size, Andrew's actual start date, Belmark's
print lead time, and Ships A Lot's inbound receiving time. The first two decide the answer.*
