# BG 55K Email List - Modern Savage Launch Strategy
*Prepared by Junior | May 17, 2026 | Strictly Private - BGV Internal*

---

## THE ASSET

Adam Hassan exported 55,000 BG website subscribers and purchasers in May 2025. CJ shared with EBG in July 2025 - nothing was done with it. CJ now wants to use it for BGV direct marketing. Jesse has asked Felix to create a new BG website mailing list, add these 55K, and market Modern Savage to them.

This is Bear's most direct route to 55,000 people who have already raised their hand for his world. Done right, it's worth 300-600 launch orders on July 1. Done wrong, it creates an ICO complaint or a wave of spam flags that destroys deliverability before launch.

This brief covers: what you can legally do, how to segment the list, and the exact email sequence to get from cold archive to paying customer.

---

## GDPR REALITY CHECK

### The legal question
These subscribers opted in at some point to receive content from Bear Grylls. The key question: can you now email them about a product (Modern Savage) they've never heard of, from a brand that didn't exist when they signed up?

### Short answer: Yes, with conditions

**Purchasers** (people who bought something from Bear's website or signed up in connection with a purchase): You have an existing customer relationship. Under PECR s.22, you can email them about "similar products" without fresh consent - provided the original sign-up included a clear opt-out and you offer opt-out in every email. Modern Savage = Bear Grylls family brand supplement = clearly similar to Bear Grylls brand activity. **Strongest legal basis. Email these first.**

**Engaged subscribers** (people who signed up for BG content and have opened emails in the last 24 months): Arguable legitimate interest for a soft re-engagement email. Best practice is to lead with Bear's personal message rather than a product email. If they re-engage, they've signalled consent to hear more. **Reactivate before pitching.**

**Dormant** (never opened or silent 3+ years): Highest legal and deliverability risk. Industry guidance says do not cold-email after 24 months without re-consent. Send a single "do you still want to hear from us?" email only. Do not add to the main sequence unless they opt in.

### What you must always include
- 1-click unsubscribe in every email (PECR mandatory)
- Sender name "Bear Grylls" or "Bear Grylls Ventures" (not "Modern Savage" - they don't know that name yet)
- Physical address in email footer (BGV Global Ltd or Bear Witness Ltd registered address)
- No misleading subject lines

### One action item before launch
Felix / Raemy: confirm BGV Global Ltd (or whichever entity is sending) is registered with ICO as a data controller and that the privacy policy on the BG website clearly states subscriber data may be used for marketing of associated brands. If not, update the policy before June 1.

---

## SEGMENT THE LIST - THREE BUCKETS

| Segment | Est. Size | Legal Basis | Approach |
|---------|-----------|-------------|----------|
| A: Purchasers | ~5,000-8,000 | PECR s.22 existing customer | Email directly with Bear's personal message |
| B: Engaged subscribers | ~12,000-18,000 | Legitimate interest + soft opt-in | Reactivation email first, then MS sequence |
| C: Dormant (3+ years silent) | ~25,000-30,000 | Weak - re-consent required | Single opt-in email only, no sequence |

### How to identify each bucket
Felix needs these flags in Klaviyo on import:
- `list_type = purchaser / subscriber`
- `last_open_date` (if available from previous email platform)
- `last_click_date`
- `source = bg_website_2025_export`

If open/click history is not in the export, treat all non-purchasers as Bucket C until they re-engage.

---

## THE EMAIL SEQUENCE

### Segment A: Purchasers (Start June 2)

**Email A1 - Bear's Personal Message (June 2)**
Subject: "Something I've been building with my family..."
From: Bear Grylls / Bear Grylls Ventures
No Modern Savage branding. Just Bear. Tells the origin story in Bear's voice:
"A couple of years ago, my family and I started thinking about what we were actually putting in our bodies. Not supplements designed for athletes. Something whole. Something real. Something you could give your kids..." Ends with: "We're almost ready. And I wanted you to be the first to know."
CTA: "Stay in the loop" (click to add to Modern Savage pre-launch list in Klaviyo)

**Email A2 - The Product (June 9)**
Subject: "Meet Modern Savage - our family's daily blend"
Introduce the brand. Bear + Jesse + family. Why organ blend. Why powder. Why once daily. Show the bag. No hard sell.
CTA: "Learn more at modernsavage.co"

**Email A3 - Founding Member (June 22)**
Subject: "Founding Member price - only until July 1"
$69/month. What's in it. The family insert card (Bear wrote it sitting around their kitchen table). Genuine scarcity (manufacturing run = 2,500 units first batch). Auto-ship from July 1.
CTA: "Secure my bag" (Shopify/Stripe checkout)

---

### Segment B: Engaged Subscribers (Start June 8)

**Email B1 - Reactivation (June 8)**
Subject: "It's been a while - Bear wanted to share this"
Very short. "We haven't been in touch much lately. Bear wanted to share something personal before it becomes public. No pitch, just a message." Links to Bear's 60-second voice note or written message about why he built Modern Savage.
CTA: "I'm curious" (click to segment into active sequence)

*Anyone who clicks goes into Segment A sequence at Email A2 onwards. Anyone who doesn't open: no further emails.*

**Those who engage** follow A2 + A3 schedule.

---

### Segment C: Dormant (One email only, June 1)

**Email C1 - Re-consent (June 1)**
Subject: "Do you still want to hear from Bear?"
Brutally simple: "We have something new from Bear's family launching this summer. If you want to hear about it, click below. If not, no hard feelings - you'll be removed from our list."
CTA: "Yes, keep me in the loop" / "No thanks, unsubscribe"

*Only those who click "yes" join the Segment B flow. Everyone else is suppressed permanently.*

This one email done well could yield 2,000-3,000 re-opted subscribers from the dormant pool - without legal exposure.

---

## EXPECTED IMPACT

Conservative scenario (10% reactivation of full list):
- Deliverable after bounce removal: ~42,000
- Segment A (purchasers): 6,000, 35% open rate = 2,100 reading
- Segment B (engaged): 15,000, 15% reactivation = 2,250 re-engaged
- Segment C (dormant re-opt): 21,000 x 12% opt-in = 2,520 new subscribers
- Total active list from this exercise: ~6,870 people who've heard the story by June 15

Purchase conversion (2.5% of active list):
- ~172 founding member orders from this channel before July 1
- At $69/month autoship: $142,000 ARR from this channel alone if they stay 12 months

Optimistic (25% reactivation):
- 12,000 active engaged by June 15
- 300-500 Founding Member orders
- $250,000-$415,000 ARR contribution

This is a material number for a first-batch run of 2,500 units.

---

## DELIVERABILITY PROTECTION

The list is 7 years old. If you blast all 55K with one email, expect 30-40% hard bounces and multiple spam complaints - which will tank domain reputation and hurt *all* Bear Grylls email (marketing, Running Wild newsletter, BGSA, everything).

The sequence above protects this. Calvin must:
1. Import list with suppression file (anyone who previously unsubscribed from any BGV list)
2. Start with Segment C re-consent email (lowest engagement = highest bounce risk - send to this group first to clean the list before it matters)
3. Warm up the sending domain with Segment A first (small, high-quality, most likely to engage)
4. Move to B and C in weeks 2-3

If Klaviyo sending domain is new, warm it up over 3 weeks before hitting full volume. Max 500 emails/day week 1, 2,000/day week 2, full volume from week 3.

---

## INTEGRATION WITH EXISTING LAUNCH PLAN

| Existing asset | Connection |
|----------------|------------|
| Pre-launch email sequence (Emails 1-5, Klaviyo) | These are for new sign-ups via modernsavage.co. BG list is a parallel track - distinct audience, needs Bear's personal framing, not generic MS branding |
| Founding Savage program (brief April 25) | BG purchasers = ideal Founding Savages. Offer them the same 20% discount + founding status |
| Calvin/Ku Creatives Bear IG arc | Timing should coordinate: A2 (product email June 9) runs same week as Bear IG post on organ blend rationale |
| Ships a Lot fulfillment | No change - US orders fulfil regardless of source |

---

## ACTION LIST

| # | Action | Owner | Deadline |
|---|--------|-------|----------|
| 1 | Confirm ICO registration and BG website privacy policy covers associated brand marketing | Raemy | May 22 |
| 2 | Import full list to Klaviyo, flag by segment (purchaser / subscriber), validate and remove bounces | Felix | May 24 |
| 3 | Build suppression list from all previous BGV unsubscribes | Felix/Calvin | May 24 |
| 4 | Warm sending domain if new (Klaviyo domain setup) | Calvin | May 18-June 1 |
| 5 | Write email C1 (re-consent, June 1) | Junior drafts, Jesse approves | May 25 |
| 6 | Write email A1 (Bear's personal message) | Junior drafts, Bear/Jesse approves | May 28 |
| 7 | Write emails A2, A3, B1 | Junior drafts, Jesse approves | June 1-5 |
| 8 | Schedule in Klaviyo per sequence above | Calvin | June 7 |
| 9 | Send C1 re-consent first (clean the dormant pool) | Calvin | June 1 |
| 10 | Monitor open rates, flag if below 8% (domain issue) | Calvin | Ongoing |

---

## BOTTOM LINE

55,000 people already trust Bear. They signed up for his world. Modern Savage is Bear's family brand. This channel is warm, underused, and sits outside the CPM/algorithm risk of paid social. Executed properly, it's worth 200-500 day-1 orders with $0 ad spend.

The only risk is mishandling GDPR and torching deliverability. The segmented approach above neutralises both.

**Estimated incremental revenue from this channel (year 1):** $100K-$400K depending on reactivation rate. Warranting the 2 weeks of Felix/Calvin setup time.

---

*Files: workspace/docs/bg-email-list-modern-savage-strategy-2026-05-17.md*
*Next step: Junior drafts email C1 and A1 for Jesse's approval*
