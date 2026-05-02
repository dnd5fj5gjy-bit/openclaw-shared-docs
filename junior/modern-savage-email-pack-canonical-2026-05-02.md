# Modern Savage — Canonical Email Pack
**Built:** May 2, 2026
**Purpose:** Single source of truth for the 5-email waitlist sequence. Multiple versions exist on disk; this document names the canonical one for each slot and deprecates the rest. Hand this to Calvin.

---

## TL;DR

Five emails to draft into Klaviyo. Use these versions only. Older drafts dated April 24 are superseded.

| Slot | Canonical file | Send trigger | Notes |
|---|---|---|---|
| Email 1 — Waitlist launch | `modern-savage-email1-waitlist-2026-04-29.md` | Day Stripe goes live | The 170-person warm-up. Pricing-locked content; Email 1 will not work until Jesse confirms £59/£47/£39/£89. |
| Email 2 — Proof | `modern-savage-email-2-proof-2026-04-25.md` | 3-4 days after Email 1 | Science + sourcing. Move curious → convinced. |
| Email 3 — Ritual | `modern-savage-email-3-ritual-2026-04-28.md` | 7-10 days after Email 2 (~10-14 days after E1) | The "how." Frames who Modern Savage is for. |
| Email 4 — Countdown | `modern-savage-email-4-countdown-2026-04-28.md` | June 24 (7 days before launch) | Founding member pricing window opens. |
| Email 5 — Launch day | `modern-savage-email-5-launch-2026-04-28.md` | July 1, 7am-9am UK | Doors open. Two sends: June 29 soft (waitlist) and July 1 hard (full list). Same body, different subject + intro. |

Plus one ancillary:
- `modern-savage-onboarding-email-2026-04-25.md` — Post-purchase OB-1 from Klaviyo flow (fires within 5 min of first order, NOT part of the pre-launch sequence). Calvin should set this as a separate Klaviyo automation.

---

## What is deprecated (do NOT use)

These earlier versions sat at April 24 baseline. They were superseded by the dated drafts in the table above. Do not paste any of them into Klaviyo; if Calvin has them in a Drive folder, replace them.

| Deprecated file | Replaced by |
|---|---|
| `modern-savage-email-2-2026-04-24.md` | Email 2 — Proof (Apr 25) |
| `modern-savage-email-3-2026-04-24.md` | Email 3 — Ritual (Apr 28) |
| `modern-savage-email-3-launch-2026-04-25.md` | Email 3 — Ritual (Apr 28) (the "launch" framing was wrong slot — that's Email 5) |
| `modern-savage-email-4-2026-04-24.md` | Email 4 — Countdown (Apr 28) |
| `modern-savage-email4-2026-04-29.html` | Email 4 — Countdown (Apr 28) — the 04-29 HTML is just a styling render, not new copy |

Reason this happened: emails were drafted iteratively as the brand voice + pricing model evolved. The Apr 24 versions were written before the pricing analysis (Apr 28), the founding-savage program (Apr 25), and the 90-day economics model (May 2). Anything dated April 28+ has the right structural assumptions baked in; anything dated April 24 does not.

---

## Pre-flight checks before any email goes into Klaviyo

Run these in order. Each is a hard gate.

1. **Pricing locked** (Jesse Mon May 4). Email 1, 4, 5 all depend on £59/£47/£39/£89 or revised numbers. Do not import to Klaviyo until confirmed.
2. **Sender domain authenticated** (Calvin). SPF, DKIM, DMARC fix from `modern-savage-email-deliverability-audit-2026-05-02.md`. Without this, ~30-40% of the 170-list goes to spam.
3. **GDPR micro-copy in place** (Calvin/Tammy). Per `modern-savage-gdpr-pecr-audit-2026-05-02.md`. The "Notify Me at Launch" form CTA needs the marketing-consent line under it before Email 1 sends.
4. **Reconfirmation prompt in Email 5** (Calvin). The 170-person waitlist signed up for "launch notification" only — Email 5 must include a "stay on the list for ongoing emails?" reconfirmation line. Drafted in the GDPR audit doc.
5. **Ship date locked or pre-order language live** (CJ). Per Pulse 57 / Lightning Nutra brief. If Model A: ship date in Email 1 body. If Model B: launch date pushed and email schedule shifts.
6. **Sender name/email** (Calvin). All five emails are from "Bear Grylls <hello@modernsavage.com>". Confirm Bear is OK with the from-name on emails written in his voice (the email pack is drafted in Bear's voice with Jesse's editorial frame).
7. **Subject line A/B test set up** (Calvin). Klaviyo spec says A/B for Email 1 and 3, 50/50 split, pick winner at 4 hours by open rate. Subject line variants are in each email doc.

---

## What Calvin actually needs (Monday email request)

Add this to the launch-infrastructure email already drafted at `draft-calvin-launch-infrastructure-email-2026-05-02.txt`:

> 6. Email pack import to Klaviyo. Single canonical file pointer at `modern-savage-email-pack-canonical-2026-05-02.md`. All five email bodies are paste-ready in their respective files. Do not use the April 24 versions — they pre-date the current pricing and brand-voice work. Import the five canonical bodies + onboarding email into Klaviyo as drafts, do not schedule until Jesse signs off post-sailing. Reply with: which support tool we're using (for ticket templates) AND confirmed import of these five drafts.

This makes the email pack item an explicit reply gate so Calvin doesn't accidentally pick up an old version off Drive.

---

## What this doc does NOT do

- It does not rewrite any email body. Every paste-ready body is in the file pointed to.
- It does not change pricing, send schedule, or brand voice — those are already locked in the canonical drafts.
- It does not address post-purchase Klaviyo flow (OB-2 onwards) — that's in the Klaviyo setup spec.

---

## File naming hygiene going forward

Going forward Junior will not produce additional Email 1-5 drafts unless Jesse or Calvin explicitly asks for a rewrite. If a rewrite is needed, the new file will start with `modern-savage-email-{slot}-FINAL-{date}.md` and this canonical pointer doc will be updated in the same pulse to point to it. Old drafts will be moved to `workspace/docs/archive/email-versions/` to clear the noise.

(Archive move can happen post-sailing — not blocking.)
