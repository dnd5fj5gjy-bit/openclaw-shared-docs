# Modern Savage — Klaviyo Setup Specification
**Prepared:** April 28, 2026
**Author:** Junior
**For:** Calvin Manik — build before June 25
**Purpose:** Complete technical setup guide for Klaviyo. All email content already exists in docs — this is the implementation map.

---

## Overview

Modern Savage has two distinct email workflows in Klaviyo:

1. **Pre-launch sequence** — sent to the 170-person waitlist before July 1. Manual campaign sends, not flows. Already built (Emails 1-5).
2. **Post-purchase onboarding flow** — triggered automatically when a customer subscribes. Automated Klaviyo flow. Built in `workspace/docs/modern-savage-post-purchase-sequence-2026-04-24.md`.

These are separate. The pre-launch sequence ends when the waitlist converts to customers. The post-purchase flow begins.

---

## 1. Account Setup

### Lists to Create

| List Name | Who Goes In | Source |
|-----------|-------------|--------|
| `Waitlist - Founding Members` | 170 pre-launch signups | Upload manually from waitlist CSV |
| `Active Subscribers` | Paying subscribers | Klaviyo-Stripe integration (auto) |
| `Kids Blend Interest` | People who expressed interest in kids blend | Tag from waitlist form if possible |
| `Influencer Seeds` | 20 gifted influencers | Add manually, exclude from campaign metrics |

### Segments to Create

| Segment Name | Logic | Use |
|--------------|-------|-----|
| `Founding Members` | Subscribed before August 1, 2026 | VIP comms, testimonial asks |
| `Adult Blend Only` | Subscribed to adult SKU only | Family upsell targeting |
| `High Engagers` | Opened 3+ emails in last 60 days | Social proof collection, ambassador outreach |
| `At Risk - Month 2` | Active subscriber, Day 40-55, low open rate | Retention intervention |
| `Referrers` | Has referred at least 1 subscriber | Loyalty programme |

---

## 2. Pre-Launch Sequence (Campaigns, Not Flows)

These are one-time manual sends to the `Waitlist - Founding Members` list. Not automated. Calvin schedules and sends each one.

| Email | Subject | Send Date | From Name | From Email |
|-------|---------|-----------|-----------|------------|
| Email 1 | `I owe you an update.` | When Stripe live (target: May 15) | Bear Grylls | hello@modernsavage.com |
| Email 2 | `What's actually in it.` | 3-4 days after Email 1 | Bear Grylls | hello@modernsavage.com |
| Email 3 | `What I do before anything hard.` | 10-14 days after Email 1 | Bear Grylls | hello@modernsavage.com |
| Email 4 | `7 days.` | June 24 | Bear Grylls | hello@modernsavage.com |
| Email 5 (waitlist) | `Before we open the doors.` | June 29, 7am UK | Bear Grylls | hello@modernsavage.com |
| Email 5 (launch day) | `It's live.` | July 1, 7am UK | Bear Grylls | hello@modernsavage.com |

**Note:** Email 5 is actually two separate sends — the June 29 soft launch (waitlist only, 170 people) and the July 1 public launch (all subscribers + wider list).

**Template settings for all pre-launch emails:**
- Plain text or minimal HTML — no header images, no heavy branding
- Unsubscribe footer: required by law, but keep plain ("Unsubscribe" link only, no elaborate footer)
- Preview text: set explicitly for each email (see content docs)
- A/B subject line test: set up for Emails 1, 3 — 50/50 split, pick winner after 4 hours by open rate

---

## 3. Post-Purchase Flow (Klaviyo Automation)

**Trigger:** `Placed Order` event from Stripe → Klaviyo integration, where subscription type = Modern Savage Adult or Kids Blend.

**CRITICAL:** OB-1 must fire within 5 minutes of purchase. Klaviyo's default flow check interval is fine for this if the Stripe integration is webhooks-based (real-time). Confirm this with Stripe setup.

### Flow Map

```
[TRIGGER: First subscription order placed]
         |
         v
    OB-1: "You're in."
    Send: Immediately (0 min delay)
    From: Bear Grylls <hello@modernsavage.com>
         |
    Wait: 2 days
         |
    OB-2: "What to expect in week one."
    Send: Day 2
         |
    Wait: 5 days
         |
    OB-3: "Why this exists."
    Send: Day 7
    From: Bear Grylls (not "The Modern Savage Team" — this is Bear's personal story)
         |
    Wait: 7 days
         |
    OB-4: "What people are saying."
    Send: Day 14
    NOTE: Requires real quotes from Email 1 replies — see below
         |
    Wait: 14 days
         |
    OB-5: "Month one done."
    Send: Day 28
    CTA: Referral link (requires referral setup — see Section 5)
         |
    Wait: 32 days
         |
    OB-6: "Two months in."
    Send: Day 60
         |
    [Flow ends — subscriber enters ongoing "Active Subscriber" list]
```

### Flow Settings
- Flow name: `Modern Savage — Post-Purchase Onboarding`
- Status: Draft until tested, then Live by June 25
- Smart sending: OFF for OB-1 (send immediately regardless of prior sends). ON for OB-2 through OB-6.
- Recipient activity filter: none — all post-purchase subscribers get this regardless of prior email engagement

---

## 4. OB-4 Quote Collection Protocol

OB-4 (Day 14) uses real quotes from Email 1 replies. Without real quotes, the email cannot send as designed.

**Calvin's action after Email 1 sends:**
1. Export all replies to hello@modernsavage.com from the Email 1 send date through Day 14
2. Select 3-4 quotes: genuine, specific, not generic ("This is great!"). Best are: specific outcome noticed, specific time reference, first-person voice
3. Strip to first name + general descriptor (e.g., "David, firefighter" or "Sarah, London") — no surnames, no email addresses
4. Insert into OB-4 template before it sends
5. If fewer than 3 replies received: use 2 quotes and add one paraphrase from social if available. Do not fabricate.

---

## 5. Referral Program Technical Setup

OB-5 (Day 28) includes a referral link. This requires infrastructure before OB-5 sends.

**Recommended tools:**
- **Referral Hero** (referralhero.com) or **Friendbuy** — both integrate with Klaviyo and Stripe
- Budget: Referral Hero starts at ~$49/month; Friendbuy is enterprise-priced. Referral Hero is right for this stage.

**Programme logic:**
- Referrer: gets 1 month free credit when referred friend completes first month
- Referred friend: first month free (zero financial risk at checkout)
- Implementation: unique referral link per subscriber, tracked in Referral Hero, credit applied to Stripe subscription automatically

**Timing:** This must be live before OB-5 sends. OB-5 sends Day 28 after first customer order (target: first orders July 1, so OB-5 lands late July). Setup deadline: June 25.

**Flag for Jesse/Raemy:** Referral program requires decision on whether "1 month free" credit is against recurring subscription or shipped product. If product is manufactured-to-order (not infinite stock), credit model is simpler than free shipment.

---

## 6. Stripe → Klaviyo Integration

**Required before any post-purchase flow works.**

Setup steps:
1. In Klaviyo: Integrations → Stripe → Connect (OAuth)
2. Map events: `charge.succeeded` → `Placed Order`, `customer.subscription.deleted` → `Cancelled Subscription`
3. Map subscriber properties: email, first name, subscription plan, order date, subscription status
4. Test with a real £1 test charge before go-live

**Key Klaviyo properties to map from Stripe:**

| Klaviyo Property | Stripe Source |
|-----------------|---------------|
| `$email` | customer.email |
| `$first_name` | customer.name (first word) |
| `Subscription Plan` | subscription.items.data[0].price.nickname |
| `Subscription Start Date` | subscription.created (Unix timestamp → datetime) |
| `Subscription Status` | subscription.status |
| `Order Value` | charge.amount / 100 |

---

## 7. Suppression and Compliance

**UK/EU compliance (GDPR + UK PECR):**
- All subscribers must have given explicit email marketing consent at checkout. Stripe checkout confirmation flow must include the consent tick-box. This is a legal requirement.
- Suppression list: anyone who unsubscribes from Klaviyo must be permanently suppressed — Klaviyo handles this automatically if the unsubscribe link is included in every send.
- Kids blend customers: if the purchaser is buying for a child, the marketing target is still the adult purchaser. No marketing addressed to children.
- **Colostrum allergen note:** Any automated email that mentions the Kids Blend must carry the allergen declaration: "Contains Milk (Colostrum)." This applies to all automated emails referencing the Kids SKU.

**US compliance (CAN-SPAM):**
- Physical address must be in the footer of every email
- Unsubscribe must be honoured within 10 business days
- Modern Savage shipping address (Ships A Lot or ACF Pharma) can serve as the physical address once confirmed

---

## 8. Before Go-Live Checklist (Calvin — complete by June 25)

- [ ] Klaviyo account created under modernsavage.com domain (not Bear Witness email)
- [ ] Stripe integration connected and tested with real test charge
- [ ] `hello@modernsavage.com` sending domain authenticated (SPF + DKIM + DMARC) — critical for deliverability
- [ ] `Waitlist - Founding Members` list uploaded and tagged
- [ ] Pre-launch Email 1 template built and test-sent to Calvin + Jesse
- [ ] Post-purchase flow built in draft (all 6 emails)
- [ ] Post-purchase flow tested end-to-end with test subscriber account
- [ ] OB-1 delivery tested: confirm arrives within 5 minutes of Stripe order
- [ ] Referral Hero account created, programme configured, Klaviyo integration live
- [ ] Referral link working: test referral → friend signup → credit allocation
- [ ] UK GDPR consent mechanism confirmed live in checkout flow
- [ ] Physical address confirmed in every email footer
- [ ] All emails viewed in dark mode (Gmail + Apple Mail) — organ blend brand should still read clearly
- [ ] All emails viewed on mobile (60%+ of opens will be mobile)

---

## 9. Deliverability Setup (do this first — before first send)

Klaviyo is only as good as the domain reputation behind it.

**SPF record** — add to modernsavage.com DNS:
```
v=spf1 include:klaviyo.com ~all
```

**DKIM** — Klaviyo generates DKIM keys under Settings → Domains. Add the two CNAME records to modernsavage.com DNS.

**DMARC** — add to modernsavage.com DNS:
```
v=DMARC1; p=quarantine; rua=mailto:dmarc@modernsavage.com; ruf=mailto:dmarc@modernsavage.com; adkim=r; aspf=r
```

**Warm-up plan for new domain:**
- Do not send Email 1 to all 170 people on Day 1 if the domain is brand new
- Send to 50 most-engaged contacts first (those who opened the waitlist confirmation email)
- Wait 24 hours, check bounce/spam rate
- If below 1%: send to remaining 120
- A brand-new domain sending 170 emails at once has a small but real risk of hitting spam filters for first-time recipients

---

## 10. Ongoing Flows to Build Later (not July 1)

These are out of scope for launch but Calvin should have them on the roadmap:

| Flow | Trigger | Purpose | Priority |
|------|---------|---------|---------|
| Cancel-save flow | `Cancelled Subscription` event | Conviction-based retention (not discount) | High — build by August |
| Win-back | 60+ days since last order, no active subscription | Re-engage lapsed customers | Medium |
| Birthday | `$birthday` profile property | Simple relationship touchpoint | Low |
| 90-day milestone | Day 90 post-purchase | Deepen retention, plant ambassador seed | High — build by September |
| Kids blend upsell | Active adult-only subscriber, Day 45 | Family subscription conversion | Medium |

---

*Built April 28, 2026. Technical setup guide for Calvin. All email content exists in separate docs — this is the implementation map. Calvin to complete the checklist by June 25 to ensure post-purchase flow is live before first customer orders on July 1.*
