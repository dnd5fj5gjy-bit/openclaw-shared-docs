# Ted's Health — weight loss ads on Meta
## How to set it up, and the one rule that decides the creative

**11 August 2026. For Jesse.**

---

### Read this bit first, because it rewrites your 30 ads

**In the UK you cannot advertise a prescription-only medicine to the public. Not the brand, not the
molecule, not a picture of the pen.** That is the Human Medicines Regulations, and it is not dormant.
The MHRA, the GPhC and the Advertising Standards Authority issued a joint enforcement notice and
updated it in 2026, the ASA is running AI monitoring that scans specifically for these ads, and named
online clinics including Bolt Pharmacy, Cured and Simple Online Pharmacy have already been made to
pull and rewrite theirs.

This is not a compliance footnote. It is the creative brief.

**Out of your 30 variations, anything with these in it is dead on arrival:**

- Mounjaro, Wegovy, Ozempic, Saxenda, tirzepatide, semaglutide, liraglutide
- "jab", "pen", "injection", "skinny jab", "the weight loss injection"
- an image or silhouette of an injector pen, a needle, a dose dial
- implication without naming: "the one everyone is talking about", "you know the one", a pen-shaped
  object, a winking reference
- the same applies to the landing page the ad points at, and to your organic Page content

**What you are allowed to advertise is the service, and that is a real product:**

- a clinician-led weight management programme
- a CQC-registered clinic with a named medical director
- a free eligibility check or consultation
- ongoing medical supervision, monitoring, aftercare
- the outcome in general terms, without attaching it to a medicine

The clinics winning this category right now are not the ones sneaking the drug name past the filter.
They are the ones selling **the clinic**: supervision, safety, a doctor who knows your bloods, and a
programme you do not do alone. That is a stronger position for Ted's than for a pill-shop competitor,
because you already have the CQC registration, the medical director and the patient care team. Lean on
it.

**One non-obvious trap.** Comments on your own ad can be treated as your advertising. Someone will
reply "is this Mounjaro?" within the hour. Set up comment moderation with a blocked-word list covering
every drug name and slang term above, and have someone actually watching. An unmoderated comment
thread is how a compliant ad becomes a non-compliant one.

---

### Meta's own rules, which sit on top of UK law

- **18+ targeting is mandatory** for anything weight related. Set it, do not rely on defaults.
- Weight loss now sits in Meta's **Weight Management** sub-category with extra targeting limits.
- **Before and after images:** since 22 July 2026 these are no longer auto-rejected, but they are
  violative if paired with a prohibited claim. Given the POM position above, I would not use them.
  The upside is small and the downside is a Page restriction.
- **No negative self-perception.** No "before" bodies framed as a problem, no shame angles, no
  targeting language that implies you know the viewer is overweight.
- Detailed health interest targeting does not exist any more. You cannot target "weight loss
  interest". This matters for the structure below: since you have no targeting lever, creative is the
  only lever, which is why the 30 variations are the right instinct.

---

### The account structure

Three campaigns. Not thirty.

| Campaign | Budget | Purpose |
|---|---|---|
| **Advantage+ , objective Leads** | 70 to 80% | The engine. Broad, no interest stacking, let Meta find them |
| **Retargeting** | 15 to 20% | Site visitors, video viewers over 50%, form abandoners |
| **Testing** | 5 to 10% | New concepts only, never new executions of a proven concept |

**The single biggest mistake in Meta right now is budget fragmentation.** One campaign at £500 a day
beats five campaigns at £100 a day, every time, because the algorithm needs consolidated signal.
Resist the urge to split by angle, by gender, by age band. You are buying one thing: a qualified
consultation.

Meta merged manual and Advantage+ into one flow in February 2026, so Advantage+ is the default rather
than a special mode. Take the default.

---

### What to actually do with 30 variations

**Do not upload 30 ads into one ad set.** This is the mistake that wastes the whole budget. Delivery
concentrates on three or four within 48 hours, the other 26 never accumulate enough impressions to be
judged, and you finish the month having learned nothing about 26 of them while having paid for all 30.

**Step 1. Sort the 30 into concepts, not executions.**
Thirty variations is almost never thirty ideas. It is usually five or six ideas with five or six
executions each. A concept is the *argument*: "you have tried everything and it was never a willpower
problem", "a doctor should be watching this", "your bloods, not a guess". An execution is the hook,
the actor, the caption, the format. **You test concepts. You refresh executions.**

**Step 2. Three to five ads per ad set. That is the number.**
Enough for the algorithm to find a pattern, few enough that each gets real delivery. Pick the single
strongest execution of each concept and launch six. Hold the other 24.

**Step 3. Work out how many ad sets you can actually afford, because it is fewer than you think.**
An ad set needs roughly **50 optimisation events a week** to get out of learning and stop wasting
money. Do the arithmetic before you build anything:

> If a qualified consultation lead costs £25, one ad set needs 50 × £25 = **£1,250 a week, about £180
> a day**, to learn properly.
> At £360 a day you can run **two** ad sets properly. Not eight.

If you cannot fund an ad set to 50 events a week, do not launch it. A starved ad set does not give
you a slow answer, it gives you a wrong one.

**Step 4. Feed the rest in as replacements, not additions.**
Every week or two, kill the bottom performer and promote the next execution of the winning concept.
The 24 held back are your refresh pipeline for the next two months. Creative fatigue, not audience
exhaustion, is what kills these accounts, so having 24 in the bank is an asset if you release them
slowly and a liability if you dump them on day one.

---

### What you optimise for, which is not leads

A lead is cheap and it lies. In a medical funnel the cheapest leads are the least eligible: people
who will not pass screening, will not complete bloods, will not convert to a prescription.

- Optimise for the deepest event you can generate **50 of per week**. Usually "consultation booked"
  or "screening completed", not "form submitted".
- Send the real outcome back to Meta. **Offline conversions through the Conversions API**, so Meta
  learns what a patient looks like rather than what a form-filler looks like. This is the single
  highest-leverage technical step and most clinics skip it.
- Exclude existing patients from targeting. You have around 97 active. Paying to re-acquire them is
  pure waste, and they are also your best lookalike seed.
- Judge on **cost per first prescription**, not cost per lead. Given July's revenue was refills rather
  than new acquisition, that is the number that tells you whether this channel is actually solving the
  problem you have.

---

### Before anything goes live

1. Pixel and Conversions API both firing, deduplicated.
2. Domain verified, aggregated event measurement configured, the deep event prioritised.
3. 18+ on every ad set.
4. Blocked-word list on comments covering every drug name and slang term.
5. Landing page checked against the same POM rules as the ad.
6. One person named as responsible for reviewing every variation against the drug-name list before
   upload. Thirty ads is thirty chances to get the Page restricted.

---

### Two things I do not know, and they change the answer

**Is weight management inside Ted's CQC registration and statement of purpose yet?** There was a
statutory notification of a change to the statement of purpose on 30 July. If that was this, good. If
not, that comes before any spend, because advertising a service you are not registered to provide is a
bigger problem than any ad policy.

**What is the monthly budget?** Everything in the structure section above is arithmetic driven by it.
Tell me the number and I will tell you exactly how many ad sets you can run and how to split the 30.

---

**One commercial note, since you have not asked for it but it is the reason this matters.** July was
Ted's best month on record at £11,114, but only three TRT packages sold against twelve in June. The
revenue is refills. This channel is not a nice-to-have experiment, it is the acquisition fix, and
weight management is the highest-demand category in UK private health right now. Worth funding
properly or not at all.

*Prepared by Junior, 11 August 2026.*

**Sources:** [GPhC enforcement notice on weight management prescription medicine ads](https://www.pharmacyregulation.org/about-us/news-and-updates/updated-enforcement-notice-issued-weight-management-prescription-medicine-ads) · [MHRA advertising investigations, July 2026](https://www.gov.uk/government/publications/advertising-investigations-july-2026/medicinal-treatment-services-for-weight-loss-july-2026) · [ASA/CAP: weight control, prescription-only medicines](https://www.asa.org.uk/advice-online/weight-control-prescription-only-medicines.html) · [Meta Transparency Center: health and wellness ad standards](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness/) · [Meta: advertising policy on personal health](https://www.facebook.com/business/help/2489235377779939)
