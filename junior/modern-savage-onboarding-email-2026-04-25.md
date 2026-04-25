# Modern Savage — Post-Purchase Onboarding Email
**Prepared:** April 25, 2026
**Author:** Junior
**Trigger:** Fires automatically when a customer completes Stripe checkout / subscription
**Timing:** Immediately on purchase (or within 5 minutes via email automation)
**Goal:** Confirm the decision, set expectations, invite into the community, reduce day-1 churn risk

---

## Part 1 — Why This Email Matters More Than Most

The most dangerous moment in a subscription is the 24-48 hours after purchase. The customer has paid. They haven't received anything yet. The enthusiasm that drove the purchase starts cooling. Buyer's remorse is a real biochemical phenomenon — it's triggered by the transition from anticipation to waiting.

The onboarding email exists to bridge that gap. Its job is not to sell anything further — the sale is done. Its job is to:

1. **Validate the decision.** Make the subscriber feel like they made the right choice. Not with hype. With specifics.
2. **Set expectations.** Tell them exactly when the product ships, what to expect when it arrives, how to use it.
3. **Start the relationship.** Invite them into the community before the product arrives. First impressions of the brand happen now, not when the box lands.
4. **Create a low-stakes action.** Give them something to do (join the WhatsApp, bookmark the recipe page) so they engage with the brand before the product exists in their hands.

Supplement subscription churn research: brands with a strong Day-0 onboarding email reduce 30-day cancellations by 15-20%. At 170 founding members, that's 25-34 people who might otherwise cancel in the first month.

---

## Part 2 — The Email

### SUBJECT LINE
`You're in. Here's what happens next.`

### PREVIEW TEXT
`Your founding member subscription is confirmed. A few things worth knowing before it arrives.`

---

### FULL BODY COPY

---

**From:** Bear Grylls / Jesse Grylls, Modern Savage
**From email:** hello@modernsavage.com

---

You just became a founding member of Modern Savage.

That means something — not as a marketing phrase, but as a factual description. You're in the first group of people in the world to take what I've been taking for years and finally put into a product. Thank you.

Here's what happens next.

---

**Your first shipment.**

Your first box ships [within 5-7 business days / expected [DATE]]. You'll get a separate shipping confirmation with tracking when it's on its way.

In the box: [X] capsules — approximately [30 days] supply at the standard serving. Everything is labelled. The insert card inside has our contact details if you have questions.

---

**How to take them.**

I take mine with breakfast. Four capsules, water, done. There's no wrong time — some people prefer evenings — but morning works better for most because it becomes part of an existing routine rather than something you have to remember later.

If you've never taken organ supplements before: in the first week you might notice a slight difference in energy or digestion as your body adjusts to the nutrient density. This is normal. It fades within a few days. After that, you'll likely stop noticing anything specific — which sounds like a bad thing but isn't. Nutrition that's working in the background is what you want.

---

**You're now in the founding tribe.**

There are 170 of you. I want to keep this group tight and genuinely useful.

We have a WhatsApp Community for founding members: [LINK].

This isn't a broadcast channel. It's where I'll share what I'm learning — from the field, from the research, from what you're all reporting back. Bear drops in occasionally. Jesse's there. It's the real version of "let us know how you get on."

---

**Recipes.**

The website has a recipe section: [modernsavage.co/recipes].

The organ content in these recipes is genuine — not a marketing add-on. If you want to build these foods back into your actual diet rather than relying on capsules, this is where to start. The liver pâté recipe is Bear's. Start there.

---

**One more thing: bring someone with you.**

Share your referral link below and when a friend subscribes, you both get a free month. This isn't a referral scheme — it's the founding member version of something we'll build properly at scale. For now: share it if you believe in it.

**Your personal referral link: [REFERRAL LINK]**

---

Any questions before your box arrives — reply here.

Welcome.

Bear

---

## Part 3 — Implementation Notes for Calvin

**Automation trigger:** This email sends automatically when Stripe marks a subscription as "active." If using Klaviyo, this fires on the "Subscription Created" event. If using another ESP, trigger on first successful charge.

**Placeholders to fill before launch:**
- `[within 5-7 business days / expected DATE]` — confirmed once Ships A Lot shipping timeline is locked
- `[LINK]` — WhatsApp Community invite link (Jesse or Calvin creates the Community and generates the invite URL)
- `[REFERRAL LINK]` — personalized via ReferralCandy or manual code if using Option C from the Founding Savage program brief

**Tone note:** This email is short by design. The subscriber just made a decision — they don't want to read 600 words. They want confirmation, a timeline, and a reason to feel good. The three practical sections (how to take them, WhatsApp, recipes) give them three low-friction actions before the product arrives.

**Do not add:** product upsells, discount codes, social follow prompts, review requests. All of these are premature at Day 0. They belong in the Month 1 or Month 2 sequence.

**Personalization:** If the ESP supports it, personalize the opening: "You just became a founding member of Modern Savage, [FIRST NAME]." Even low-cost personalization increases engagement 10-15% on transactional emails.

---

## Part 4 — What Comes After Onboarding (The Full Post-Purchase Sequence)

| Email | Trigger | Subject | Goal |
|---|---|---|---|
| **Onboarding (this email)** | **Immediately on purchase** | **"You're in. Here's what happens next."** | **Validate, set expectations, community** |
| Shipping confirmation | When tracking number created | "Your Modern Savage order is on its way." | Logistics + anticipation |
| Week 2 check-in | Day 14 after subscription | "How are you getting on?" | Engagement, feedback, identify potential churners |
| Month 1 refill notice | Day 25 | "Your next shipment ships in 5 days." | Reduce surprise, manage expectations |
| 60-day review ask | Day 60 | "You've been taking these for 2 months. Honest question:" | Social proof collection, NPS, referral reactivation |

The shipping confirmation is transactional and Calvin/Ships A Lot likely generates this automatically. The Week 2 check-in and 60-day review are the highest-value follow-up emails after onboarding — they catch churners before they cancel and build the testimonial bank for launch press.

---

## Part 5 — The Harder Question: What If They Cancel Before the Box Arrives?

Stripe allows cancellations. If someone subscribes and cancels before receiving their first shipment (this happens — 3-8% of supplement subscribers), you need a win-back email within 24 hours of cancellation.

Subject: `Before you go — one question.`

Body: "I saw you cancelled. I'd rather know why than guess. One question: what put you off? Reply here and I'll read it personally. If there's something we got wrong, I want to know."

This email recovers 10-15% of cancellations in the pre-shipment window and — more importantly — it gives you real market intelligence from the people most likely to give you honest feedback. The ones who cancel before receiving the product are often price-sensitive or trust-uncertain; their reasons tell you what the pre-purchase sequence still needs to address.
