# Modern Savage — GDPR / PECR consent audit (UK side)

**Built:** May 2, 2026 (Pulse 56)
**For:** Jesse + Raemy
**Risk level:** LOW for launch send. MODERATE for ongoing marketing past launch. One easy fix.

---

## What I checked
The 170-person waitlist will receive Email 1 on July 1. Under UK GDPR + PECR the lawful basis for that send must be either (a) explicit consent freely given for that purpose, or (b) "soft opt-in" (existing customer relationship). Modern Savage has not sold anything, so it must be (a).

I pulled the live landing page (modernsavage.co), the privacy policy, the terms page, and walked through the consent chain.

## What's working

**Privacy policy is solid.**
- Names UK GDPR + Data Protection Act 2018 + US state privacy laws.
- Names lawful basis explicitly: Article 6(1)(a) consent.
- Frames form submission as the unambiguous affirmative act of consent.
- Lists withdrawal rights, one-click unsubscribe, ICO complaints route.
- Confirms no sale of data, no cross-context behavioural advertising.
- States "We do not rent or trade your email address to third parties."

**Form purpose is clear at submit.**
The CTA reads "Notify Me at Launch" / "Join the waitlist to be first." Combined with the privacy link, this is defensible as consent for launch notifications.

## Three gaps to fix before July 1

### 1. Data controller field is blank in the privacy policy
The policy says: *"The data controller for personal data collected through this site is [blank]."* Under UK GDPR Article 13, the controller's identity and contact details must be transparent at the point of collection. Empty controller field = formal defect.

**Fix:** Once Modern Savage UK Ltd is registered (the Pulse 41 / Monday item 5 question for Raemy), insert: *"The data controller is Modern Savage [UK] Limited, [registered office address], registered in England & Wales under company number [XXXXX]."* Add a UK postal address (Bear Witness's Isle of Man one is wrong here — need a UK one, even a virtual office).

**Until UK Ltd exists**, a short-term defensible fix: name "Bear Witness Limited (Isle of Man company XXXXX)" as the controller for waitlist data, and migrate to UK Ltd post-registration with a notice email to the list.

### 2. The form CTA does not name "marketing emails" explicitly
"Notify Me at Launch" covers the launch send. It does **not** cover ongoing promotional emails post-launch. Once the launch email goes out, sending Email 6+ to that same list under the original consent is on shaky ground.

**Fix (30 seconds, Calvin can do it):** add micro-copy under the input field:
> *"By joining, you agree to receive launch notifications and occasional product news from Modern Savage. Unsubscribe anytime."*

This converts the consent from "launch-only" to "launch + ongoing marketing," which is what the launch playbook actually relies on.

### 3. Email 5 (launch day, July 1) should include a reconfirmation prompt for the original 170
Belt-and-braces: the 170 originals signed up before the new micro-copy is added. Their consent was "launch-only" by the strictest reading. Email 5 — the moment they get the founding-member offer — is the natural place to ask them to reconfirm for ongoing comms.

**Fix:** add one line near the bottom of Email 5: *"Want to hear from us beyond launch? You're already on the list. If not, tap unsubscribe — no hard feelings."* This creates an audit trail of continued consent for anyone who stays on the list after that send.

## What I'm not flagging

- PECR (UK ePrivacy Regs) — covered. PECR for B2C marketing requires either consent or soft-opt-in; consent route is established here.
- Cookie consent — site uses minimal cookies pre-launch. Will need a banner once Klaviyo + analytics fire on the post-launch site, but not blocking for July 1.
- Right to be forgotten plumbing — Klaviyo's standard suppression workflow handles this. Calvin to confirm in setup.
- US state laws (CCPA / CPRA / Virginia / Colorado / Connecticut / Utah / Texas) — covered in the policy at sufficient depth for pre-launch.

## The asks

**Raemy (or Jesse to forward):**
- Confirm Modern Savage UK Ltd registration (Monday's question).
- Once registered, fill the data controller field.
- Provide a UK postal address for the policy.

**Calvin:**
- Add the micro-copy under the waitlist form (30 seconds, hardcoded text in the next.js component).
- Add the reconfirmation line to Email 5.
- Confirm Klaviyo's unsubscribe + suppression workflow is enabled before July 1.

## Why this is worth doing
ICO fines for marketing-without-consent under PECR run £500K+ for repeat offenders. Bear Grylls's name on the brand makes Modern Savage a higher-visibility target than its size suggests — same dynamic flagged in the claims-guide ASA risk note. The launch-day send is fine. The post-launch programme isn't, without these two micro-fixes. Doing them now costs 30 minutes total.

---
*Junior, May 2 2026. Cross-references: modern-savage-claims-guide-2026-04-24.md (ASA), modern-savage-compliance-check-2026-04-30.md (FDA/FSA), modern-savage-uk-entity-status-2026-04-30.md (entity), modern-savage-email-deliverability-audit-2026-05-02.md (DNS).*
