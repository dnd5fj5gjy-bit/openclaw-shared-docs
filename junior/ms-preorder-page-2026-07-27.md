# The Founding 800 page: built, not described

**27 July 2026. The cap, the price and the compliance copy were all settled by Friday and Saturday's documents. What did not exist was the page. This is it, plus everything around it that has to exist before it opens.**

There is a working prototype to look at:
`https://dnd5fj5gjy-bit.github.io/openclaw-shared-docs/junior/ms-preorder-page-2026-07-27.html`

It is an internal preview, not a live store. It runs the real copy, the real prices and the real cap, and it has a small control strip at the top so you can flip between the states without me rebuilding it: **open**, **nearly gone**, **sold out**, and the two payment mechanics. Look at it on your phone, that is where it will be bought.

---

## Why this and not another memo

Saturday's sizing document ended with five actions. Four are questions for other people (Raemy on the bridge, Sarah on the price hold, Calvin on the countdown creative, Felix on capture-later). The fifth was mine: **commission the sold-out state and the run-two waitlist at the same time as the main page, not the morning it sells out.**

That last one is the one everybody skips, and it is the one that costs money. On the conversion numbers in the sizing doc the list alone clears 800 without a penny of paid spend. So the sold-out state is not a defensive edge case, it is a page that a large share of your traffic will see. It should be as well built as the buy page.

The other reason to build rather than brief: the page has to work **whichever way Raemy answers**. Both versions are in here, and the only difference between them is one paragraph and one payment setting. That means the page is not blocked on the treasury question. Build it now, flip the setting when the answer comes.

---

## 1. The offer, as it appears

| | Price | Notes |
|---|---|---|
| **Founding bundle (hero)** | **$125** | Adult + Summit default, Adult + Mini as the family option |
| Full set | $180 | Adult + Summit + Mini |
| Adult only | $79.99 | Available, deliberately not the hero |

Included at no cost to us, and stated on the page because they are the actual reason to buy now rather than in October:

- **Price locked for twelve months.** Whatever we do to pricing, a founding place holds.
- **Hand-numbered insert.** One of 800, with the number on it.
- **Founding community access from the moment of order**, not from delivery. This matters: it is the only thing a customer receives immediately, and it is what makes an eight-week wait feel like membership rather than a delay.

**No discount.** The founding benefit is the lock, the number and the access. Discounting a capped product that will likely sell out is paying for demand you already have.

---

## 2. The compliance block

This sits directly above the buy button, not in a footer and not in the confirmation email. Two versions. Pick one when Raemy answers the $80,000 bridge question.

**Version A - charge on despatch** (recommended if BGV Global can carry the ACF balance):

> **This is a pre-order, and you will not be charged today.**
> We are making the first run now. Your place is reserved and your card is charged only when your order leaves the warehouse, on or before **[DATE]**. If anything slips we will email you before that date and you can cancel with one reply.

**Version B - charge now** (if the bridge is not available):

> **This is a pre-order. You are paying today for a product that ships on or before [DATE].**
> We are making the first run now. Your order is reserved and we will email you tracking the moment it leaves the warehouse. If we miss that date we will email you before it with a new one, and you can cancel for a full refund, no questions and no chasing.

`[DATE]` is whatever we honestly expect **plus two weeks**. On the current chain, artwork to Belmark in mid-August means stock shippable end of September, so the honest date is early October. Put **12 October** on the page and ship in September. Shipping early costs nothing. Shipping late costs a delay notice, a refund queue and a story, in launch week, on a Bear-fronted brand.

---

## 3. The counter, and how to be honest with it

The page states a number and counts it down. **Count real orders.** No inflation, no "only 40 left" that stays at 40 for a week, no fake reservation timer. The reason is not squeamishness: this audience is 57,620 people who trust Bear specifically, and a fake scarcity mechanic is the single most recognisable thing in D2C. It reads as someone else's brand.

Three states, all built up front:

1. **Open.** "X of 800 founding places remaining."
2. **Nearly gone**, below 100. Same page, the counter becomes the headline, and the run-two waitlist form appears below the buy button rather than replacing it.
3. **Sold out.** The buy button is replaced by the run-two waitlist with a stated ship month. Not a dead page, not a 404, not a "sign up for updates" with no date on it.

The sold-out headline is written and in the prototype: *"All 800 founding places are gone. Run two ships in [MONTH]."* Say the month. A waitlist with no date is a mailing list; a waitlist with a date is a queue.

---

## 4. The three emails

These have to exist before the page opens, for the same reason the sold-out state does.

**Confirmation, sends immediately.** Reserves the place, states the date, states the charge mechanic in plain words, and delivers the one thing they get today: the community link and their number. "You are founding member 0341." That is the email people screenshot.

**Delay notice, drafted now, sends only if needed.** Written in advance and kept ready, because the moment you actually need it is the moment you have the least time to write it well. It states the new date, offers the cancel in the first two lines rather than the last, and does not explain the supply chain. Nobody wants the reason, they want the date and the exit.

**Sold-out / run-two, sends to the waitlist.** Confirms the position in the queue and the ship month.

Full copy for all three is in the prototype page under the tab marked "emails", so Calvin can lift it straight into Klaviyo.

---

## 5. What each person now needs

**Jesse.** One decision only: the `[DATE]` on the page. I recommend **12 October**, for the reason in section 2. Everything else on this page is already settled by your own earlier calls.

**Raemy.** The unchanged question from Saturday: can BGV Global carry roughly $80,000 for four to eight weeks? Yes selects version A, no selects version B. Nothing else on the page moves either way.

**Felix.** Does the backend support authorise-now, capture-on-despatch? That is the same question in engineering terms. Also: the counter must decrement on paid or authorised orders only, and must hard-stop the checkout at 800 rather than merely hiding the button.

**Calvin.** The creative is built around a countdown from a fixed number, not an open door. He needs the cap and the hero price to start, and both are in this document. The sold-out state needs its own creative too, and it is the asset most likely to be forgotten.

---

## 6. The thing I would get wrong if I were doing this quickly

The temptation is to treat 12 September as the launch and the pre-order as the warm-up. On the numbers, the opposite is true: the pre-order likely sells out weeks before Bear is on that stage.

That is not a problem to be managed, it is the better position. "Run one sold out in 40 hours. Run two opens tonight" is a materially stronger thing to say from a stage than "please visit our website." But it only works if run two exists as a page on the night, with a date on it, and that has to be built in August rather than sketched in September.

Which is the whole argument of this document, applied one level up.

---

**Verified for this document:** the cap of 800, the $125/$180/$79.99 price grid, the 46-day artwork-to-shippable chain and the mid-August drop-dead, the ~$80,000 ACF balance due on ship, list sizes of 57,620 and ~1,800, and both regulatory positions (FTC Mail Order Rule, UK Consumer Contracts Regulations) as set out in the 25 July compliance document.

**Not verified:** whether the backend supports authorise-now-capture-later, which decides A or B but blocks neither. The prototype is a static preview with no payment path and no data capture, and is not connected to anything.
