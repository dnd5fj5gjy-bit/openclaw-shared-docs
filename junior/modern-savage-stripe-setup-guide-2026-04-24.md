# Modern Savage — Stripe Setup Guide
**Prepared:** April 24, 2026
**Author:** Junior
**For:** Jesse or whoever sets up payment infrastructure
**Purpose:** Step-by-step. From zero Stripe account to accepting subscription payments. Estimated time: 60-90 minutes.

---

## Why This Matters

Without Stripe, Modern Savage cannot accept a single payment. No launch. No waitlist conversion. No revenue. This is the one technical blocker that sits entirely with Jesse (requires the business bank account and company details for Bear Witness Ltd or the operating entity).

---

## CRITICAL — ENTITY DECISION (READ BEFORE ANYTHING ELSE)

**Bear Witness Limited (Isle of Man) CANNOT set up a Stripe account.**

Stripe explicitly does not support Isle of Man registered companies. The Isle of Man is a Crown Dependency, not part of the UK, and is not on Stripe's supported countries list. If you try to register Stripe under Bear Witness Ltd (IoM), it will be rejected.

**The solution: use a UK Ltd company.**

Three options, in order of speed:

### Option A — Incorporate a new UK Ltd today (RECOMMENDED)
- Cost: ~£100-150 via a formation agent (e.g. 1stformations.co.uk, Rapid Formations)
- Time: same-day if submitted before noon, next-day otherwise
- Name options: "Modern Savage Ltd", "Bear Witness UK Ltd", or "Bear Witness Digital Ltd"
- Jesse can do this from his phone in 15 minutes: go to 1stformations.co.uk, fill in name + director details, pay £100
- Certificate of Incorporation arrives same day → Stripe setup Tuesday with a clean UK entity

### Option B — Use BGV Global Ltd (already exists as UK company)
- No incorporation needed, available immediately
- Risk: conflates Jesse's personal brand business with BGV Global (Bear's corporate entity)
- Only suitable as a temporary measure while a proper entity is set up

### Option C — Use Braintree (PayPal subsidiary) as interim
- Braintree does support Isle of Man companies
- Higher fees (~2.9% + 30¢ vs Stripe's 1.4% + 20p for UK cards)
- Gets you live faster but suboptimal long-term

**Recommended path:** WhatsApp Raemy Monday morning: "Quick question — for Modern Savage Stripe, I need a UK entity. Easiest options: (a) incorporate a new Modern Savage Ltd today for ~£100, or (b) use BGV Global temporarily. Which do you prefer?" If no response before noon, go with Option A — incorporate Modern Savage Ltd. It's £100 and the right structure anyway.

**VAT note:** IOM and UK are treated as a single VAT area (1979 agreement). IoM VAT registration covers UK sales. No separate UK VAT number needed. Stripe Tax handles this automatically once configured.

---

## Before You Start — What You'll Need

- **UK Ltd company** (Modern Savage Ltd or BGV Global Ltd) — company number and registered address
- Business bank account details — Equals Money (Bear Witness) or BGV Global account
- Jesse's ID (passport) — Stripe requires identity verification for the account owner
- UK company registration number (Companies House)
- The website domain (modernsavage.co)

---

## Step 1 — Create the Stripe Account

1. Go to stripe.com/register
2. Email: use modern-savage@beargryllsventures.com (or jesse@beargryllsventures.com if no separate address exists)
3. Password: use a strong unique password, save to 1Password or equivalent
4. Business type: select **Company**
5. Country: **United Kingdom** (must be UK entity — NOT Isle of Man)
6. Business name: **Modern Savage** (trading name of whichever UK entity you're using)

**Note on entity:** Use the UK Ltd company confirmed with Raemy. Do NOT use Bear Witness Ltd (Isle of Man) — Stripe will reject it.

---

## Step 2 — Verify the Business

Stripe will ask for:
- Business registration number
- Registered address
- Type of business (select: Health & Fitness / Supplements / Consumer Goods)
- Website URL — enter the Modern Savage site URL
- Business description: "Premium organ supplement subscription for health-conscious consumers"
- Estimated monthly volume: be honest — $5K-$50K initially

---

## Step 3 — Add Bank Account (for payouts)

1. Navigate to Settings > Bank accounts and scheduling
2. Add the bank account that will receive payouts
3. For Isle of Man entity: may need to use a UK or international account — confirm with Raemy
4. Stripe pays out within 2-7 days of charge by default. Change to daily payouts once volume starts (Settings > Payouts > Schedule)

---

## Step 4 — Create the Products in Stripe

This is where the subscription is defined. Do this carefully — it sets the billing logic.

### Product 1 — Modern Savage Adult Blend (Monthly Subscription)
1. Go to Products > Add product
2. Name: **Modern Savage Adult Blend**
3. Description: 28-serving monthly supply
4. Pricing model: **Recurring**
5. Price: **$65.00 USD** per month
6. Billing period: Monthly
7. Save

### Product 2 — Modern Savage Kids Blend (Monthly Subscription)
Same process:
1. Name: **Modern Savage Kids Blend**
2. Price: **$[confirm price] USD** per month
3. Billing period: Monthly

### Product 3 — Family Bundle (if launching)
If combining Adult + Kids at a bundled rate:
1. Name: **Modern Savage Family Bundle**
2. Price: **$[95-100] USD** per month (confirm with Calvin)
3. Billing period: Monthly

---

## Step 5 — Set Up the Customer Portal

Stripe has a built-in subscription management portal. Enable it so customers can update cards, cancel, or pause without emailing support.

1. Settings > Billing > Customer portal
2. Enable the portal
3. Configure what customers can do:
   - Update payment method: YES
   - Cancel subscription: YES (don't hide this — it builds trust)
   - Pause subscription: YES (offer 1-month pause before cancellation — reduces churn)
   - Update quantity: NO (keep simple at launch)
4. Add your branding (logo, brand colour)
5. Set cancellation flow: Before cancelling, ask "How can we improve?" — captures churn reasons

---

## Step 6 — Connect to the Website

**If using Shopify:**
- Install the Stripe payment app from the Shopify App Store
- Or use Shopify Payments (which runs on Stripe infrastructure) — simpler

**If using a custom site / Webflow / other:**
- Use Stripe Checkout (hosted payment page) — no coding required
- Or Stripe Payment Links — generate a direct payment URL for each product
- Payment Links are the fastest option: Products > [Product name] > Create payment link → share the URL in Email 4 (launch day)

**Payment Links are the launch MVP.** No developer needed. Generate a payment link for the Adult Blend subscription and drop it in Email 4 and the landing page CTA. Stripe handles everything else.

---

## Step 7 — Test Before Launch

1. Stripe has a test mode — toggle it in the dashboard header
2. Use test card: 4242 4242 4242 4242, any future expiry, any CVC
3. Run a test subscription: check that the payment goes through, the confirmation email fires, and the subscription appears in the dashboard
4. Turn off test mode before going live

---

## Step 8 — Tax Configuration

1. Settings > Tax
2. Enable Stripe Tax (automatic tax calculation) — $0.50 per transaction
3. For US customers: configure Nexus states (where Modern Savage has sales tax obligations — initially minimal but grows with volume)
4. For UK/EU customers: VAT may apply — Stripe Tax handles this automatically once configured

**Get Raemy to confirm the tax setup requirements before launch.** She's back next week.

---

## After Setup — What Calvin Needs from Jesse

Once Stripe is set up, Jesse or CJ should give Calvin:
1. The Stripe Payment Links for each product (so Calvin can embed in the email sequence and landing page)
2. Access to the Stripe dashboard (read-only) so Calvin can see conversion data
3. Confirmation of which email address gets transaction notifications

Calvin does NOT need admin access to Stripe. Payment link URLs are enough to launch.

---

## Stripe Costs

- Standard: 1.4% + 20p per European card transaction / 2.9% + 30¢ per US card
- No monthly fees
- Stripe Tax: $0.50 per transaction (optional but recommended)
- Payout: free to bank accounts

At $65/transaction: Stripe takes $2.19 (US) or £1.11 (UK). Already factored into the contribution margin model.

---

## The 90-Minute Version

If Jesse has 90 minutes before sailing:
1. Register the account and verify the business — 30 min
2. Add bank account — 10 min
3. Create the Adult Blend subscription product — 10 min
4. Generate a Payment Link — 5 min
5. Send the Payment Link URL to Calvin — 1 min
6. Modern Savage can take payments

Everything else (portal, tax, Kids Blend product) can follow. The Adult Blend Payment Link is all that's needed to convert the 170 waitlist.
