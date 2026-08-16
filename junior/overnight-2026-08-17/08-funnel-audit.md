# I walked the pre-order funnel. Here is where it leaks.

**Done in a real browser on 16-17 Aug 2026, all the way from the homepage to the point just before
payment. I did not place an order.**

---

## First, the good news, because it is genuinely good

**Checkout works and it is well built.** I want to say that plainly, because for about twenty minutes
I thought it was broken and I was wrong.

The Checkout button fires no network request when clicked, produces no navigation, and logs no error.
That looks exactly like a dead button, and "the site cannot take money" would have been a dramatic
thing to report. It is not what is happening. Checkout opens an **inline panel** requiring an email
address and a ticked terms box, and only then hands off to **Stripe**. My earlier tests were failing
the terms validation silently. The lesson is mine, not the site's.

**The pre-order disclosure is better than most brands manage.** Verbatim from the checkout panel:

> Aiming to deliver around October 2026. Charged today to reserve your place. Cancel any time before
> dispatch for a full refund. This is a subscription. It renews automatically at £55 every 28 days
> until you cancel. Because this is a pre-order, **the next payment is 28 days after your first order
> is dispatched, not 28 days from today.**

That last clause is a thoughtful piece of work. It closes the trap where a customer pre-orders in
August, waits until October for delivery, and gets billed three times in the meantime. Somebody
thought about that, and it is the kind of detail that avoids chargebacks and complaints.

The currency switcher works properly too: UK/GBP and US/USD, each priced independently rather than
converted.

---

## Now the leaks, in order of how much they cost

### 1. The product page has almost nothing on it

The homepage runs to about **7,600 characters** of copy. The product page for the £65 adult blend is
about **1,400**.

That is the wrong way round. The homepage is where people browse. The product page is where they
decide to hand over £65 for something that arrives in two months. It currently contains a
one-sentence description, the price, a quantity selector, and the pre-order terms.

**What is not on it:** no reviews, no testimonials, no FAQ, no founder story, no ingredient detail
beyond a link, nothing about who made it or why. Every one of those exists elsewhere on the site or in
the press. None of it is at the point of decision.

### 2. There is no social proof anywhere on the site. None.

No reviews, no ratings, no testimonials, no press logos, no follower counts.

This is the single cheapest fix available and probably the highest-return. **The press coverage
already exists** and is running right now: Hello, AOL, Plant Based News, Spectrum FM, and Bear's
Health Optimisation Podcast appearance with Tim Gray. A row of publication logos under the product,
with nothing more than "as featured in", would cost an hour of somebody's time.

For a pre-order in a category with the Liver King and Ancestral history sitting behind it, trust
signals are not decoration. They are the product.

### 3. The two-delivery minimum is the real friction, and it is buried

The headline is **"£55 / MONTH"**. What the customer actually commits to is:

> There is a **minimum of two deliveries**, after which you can cancel at any time from your account.

So the real minimum commitment is **£110**, not £55. It is disclosed, in the checkout panel and in
small text on the product page, so I am not calling this a compliance problem. But it is the single
biggest reason someone reaches Stripe and does not complete, and it is discovered late, at the
moment of payment, which is the worst possible place to discover it.

Two options worth weighing: drop the minimum entirely and rely on the product, or state it much
earlier and confidently as part of the offer. What does not work is a customer meeting it for the
first time with their card out.

**One thing genuinely worth a legal glance rather than my opinion:** UK distance-selling rules give a
14-day cancellation right, and how a two-delivery minimum interacts with that is not something I
should be guessing at. The product page does preserve full pre-dispatch cancellation, which is the
part that matters most for pre-orders, so this may well be fine. It is a question for CJ, not an alarm.

### 4. Non-UK, non-US visitors are greeted with a rejection

The very first line on the page, above the pre-order message, above the brand, is a geo-detected
notice. From here it reads:

> We don't deliver to Switzerland yet, but you can still order to a UK or US address.

**Bear's nine million followers are global.** A large share of anyone arriving from his feed is
neither in the UK nor the US, and the first thing the brand says to them is that it cannot serve them.

The recovery offered is an email capture, which is right. But it is currently framed as an apology
rather than an invitation, and it sits above everything else on the page. Moving it below the hero,
and rewriting it as "we're coming to Switzerland, be first to know", would turn the single largest
category of visitor from a bounce into a list entry.

---

## What I would do, in order of return per hour

1. **Add press logos to the product page.** One hour. The coverage already exists.
2. **Move the product story onto the product page.** The copy is already written elsewhere on the site.
3. **Decide on the two-delivery minimum** and, if it stays, surface it early and confidently.
4. **Reframe the geo notice** from apology to waitlist, and move it below the hero.
5. **Add an FAQ to the product page**, using the questions already answered in the checkout panel.

None of these requires new photography, new creative, or anyone on holiday to approve anything.

---

## What I could not test, stated plainly

- **I did not complete a purchase**, so everything past the Stripe hand-off is unverified.
- **My browser geolocates to Switzerland**, which is why the Swiss banner appears. I tested UK and US
  by switching currency manually, which changes prices but may not change everything a real UK or US
  visitor sees.
- **I have no analytics access**, so none of the above is measured against real drop-off. These are
  structural observations about the journey, not evidence about where users actually leave. Felix's
  dashboard would settle it, and the pre-order book size is still a number I have never been given.
