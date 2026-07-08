# HealthPilot — The Ted's Health Front Door
### Demo walkthrough for CJ · 8 July 2026

---

## The one line

**HealthPilot is the AI front door for every clinic on the Ted's Health white-label platform.** A patient lands on a clinic's own website, answers a 2-minute intelligent health quiz under that clinic's brand, gets a personalised summary, and is routed straight to a revenue event: a blood panel, a consultation, a treatment. The clinic gets a qualified, pre-triaged patient and structured intake data it never had to collect by hand.

Ted's pivoted from selling direct to running the backend clinics build on. That backend is mature: per-clinic theming, pricing, feature flags. **HealthPilot is the top of the funnel that platform was missing** — the piece that turns a clinic's website visitor into a booked patient.

---

## Why this matters to Ted's (in plain terms)

1. **It completes the product.** A white-label backend with no patient-acquisition layer is half a sell. HealthPilot is the half that gets a clinic excited on the first call.
2. **It makes the platform stickier.** Once a clinic's intake, triage and patient record run through the quiz, switching away is painful.
3. **It's a second revenue line.** On top of the platform SaaS fee: per-intake usage plus a share of the blood panels and consultations the quiz drives. Roughly half of HealthPilot's revenue grows without signing a single new clinic.
4. **It strengthens the Ted's story** at the exact moment a large digital-health player is circling. An AI intake layer with a data flywheel is precisely the kind of asset that improves that conversation.

---

## The problem it solves

Today a clinic's "intake" is a contact form or a receptionist taking history by phone. Cold website traffic leaks away. There's no triage before the first appointment, no structured data, no upsell. HealthPilot replaces that with a premium digital first impression that qualifies the patient and books the revenue before a clinician spends a minute.

---

## The flow — what CJ will see

*(Five stops. Screenshots on the following pages.)*

**1. The clinic's branded quiz.** Patient arrives on the clinic's site — the clinic's logo, colours, tone. Not "powered by someone else". This is the white-label promise made visible.

**2. The intelligent assessment.** Goal-driven questions that branch on the answers. Two minutes, feels concierge, not a form. Clinical red-flag detection runs underneath: emergency symptoms trigger a 999/NHS-111 interstitial, under-18s are gated out. Safety is built in, not bolted on.

**3. The personalised summary.** The patient gets a clear, second-person health summary written by the model, mapped to the clinic's own catalogue of treatments and tests.

**4. The revenue moment — the blood-panel CTA.** A patient who says "no recent blood test" is offered a clinic-branded panel then and there. This is the first attributable pound: a vague concern becomes a £150 panel. The click flows back to the clinic's system.

**5. The clinic side.** Staff see the structured intake in the patient record, urgent cases flagged for escalation, a clinician pre-brief ready before the consultation, and an owner console showing funnel analytics — how many started, completed, converted. The clinic gets a conversion funnel it never had to build.

---

## The business model

Sold to Ted's platform clinics as one extra line on the invoice — quiz on by feature flag, no separate contract.

- **Base SaaS:** £199 / £449 / £899 per month by intake volume.
- **Overage:** £0.60 per completed intake beyond tier.
- **Conversion share:** 10% of net revenue on quiz-driven blood panels and consultations, plus affiliate on supplements.
- **Setup:** £750 one-off — **waived** for Ted's platform clinics (zero-friction activation is worth more than the fee).

**Worked example — a clinic doing 500 intakes/month:** ~£1,209/month to HealthPilot; the clinic keeps roughly **4.5x what it pays**. That ratio is the pitch. At 30 clinics that's ~£435k ARR — and about half of it is usage and share that grows without new logos. For context, all of Ted's D2C was doing £6k MRR at the pivot.

**The one number that decides it:** the model leans on **8% of blood-panel CTAs converting.** That's a hypothesis, not data. First job after launch is to prove it with two design-partner clinics over 30 days. Everything else is priced off that number.

---

## Where we honestly are

- **Built and demo-ready.** Security hardened, red-flag safety added, embed SDK, per-clinic branding, clinic-side triage and analytics, three languages, a full end-to-end test harness.
- **Not live yet.** It sits on two sandbox pull requests and patch sets waiting on Felix to merge, apply, migrate and run one live AI test. Until then it isn't in production. Thursday is a demo, not a launch.
- **Next after the demo:** merge and deploy, get a clinical/regulatory eye on the AI safety layer, and run the 30-day conversion validation with two clinics.

*This is a feature that makes the Ted's platform materially more sellable, with a clean path to being its own revenue line. It is not yet a proven standalone business — and we shouldn't pitch it as one until the conversion number is real.*

---

## Talk track — what to say at each stop

- **Open:** "This is the front door for every clinic on the Ted's platform. Watch it turn a website visitor into a booked, paid patient in two minutes."
- **At the quiz:** "Everything you see is the clinic's brand. To the patient this is their clinic, not ours."
- **At the assessment:** "It branches on the answers, and it's watching for red flags — anything urgent gets pushed to emergency care. Safety's built in."
- **At the summary + CTA:** "Here's the money. No recent blood test becomes a £150 panel, attributed to the quiz, before a doctor's even involved."
- **At the clinic side:** "The clinic gets a qualified patient, structured notes, urgent cases flagged, and a funnel dashboard they never had to build."
- **Close:** "Clinic keeps about four and a half times what it pays us. It's an add-on line on a bill they already get. The one thing we need to prove is the conversion rate — two clinics, thirty days."
