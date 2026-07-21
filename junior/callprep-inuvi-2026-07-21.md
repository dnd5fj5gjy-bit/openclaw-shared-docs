# Inuvi — diagnostics partner intro
**Tue 21 Jul, 14:00 UK, Zoom.** Harry Patey, Account Executive, Inuvi. Felix (bgvai@) also on the invite.

---

## WHO THEY ACTUALLY ARE

Not a home-test-kit reseller. Inuvi is a **B2B clinical diagnostics business**: phlebotomy, pathology, cardio-respiratory testing, audiology, wellbeing assessments, and services to life and health insurers.

Four UK sites: Wokingham, London (their own diagnostic centre), Gloucester, Plymouth. **UKAS-accredited lab, ISO 9001, ISO 27001, CQC registered.**

That accreditation stack is the interesting part, and I will come back to it.

Thomas Filmer, Head of Operations at Ted's Health, made the introduction. Harry has spoken to Felix once before, a while ago. **Harry asked what the projects were and nobody replied, so he is coming in blind.** Expect him to spend the first ten minutes on a capability overview. That is fine; let him.

---

## THE ONE DECISION TO MAKE BEFORE YOU DIAL

**How much do you tell him?**

Harry is an account executive at a supplier that already sits inside the Ted's Health environment. What you say travels, both inside Inuvi and around the market. Meanwhile Ted's is in a live conversation with Voy.

My recommendation: **describe the shape, not the plan.** He needs enough to quote and to know this is worth his attention. He does not need names, timelines, or the sale context.

Say this much:

> "Short version. We run a men's health platform in the UK. We are building the technology so that it runs multiple clinics on one back end rather than just our own, and every one of those clinics needs blood work as the front door of the patient journey. So I am not really looking at this as ordering some panels. I am looking for a diagnostics partner who can sit underneath a platform and scale with it.
>
> I will keep the commercial detail light today because some of it is confidential, but if this looks like a fit I am happy to put an NDA in place and go properly into it."

Do not say Voy. Do not give a go-live date. Do not name the other clinics.

---

## THE THREE ANSWERS THAT DECIDE WHETHER INUVI IS A REAL PARTNER

Everything else is price. These decide it.

**1. Structured results, or PDFs? (read aloud)**
> "When a result comes back, how do we receive it? Is there an API where we order a panel and get back structured results, analyte by analyte with the reference ranges as data, or do we get a PDF report?"

- **Good:** they have an API or HL7/FHIR feed, and can talk about it without fetching someone.
- **Red flag:** "we email a PDF to the clinic." A PDF is a dead end. Our whole product is reading results and personalising what happens next, and you cannot do that to a scanned document without a human retyping it.

This is the single most important question on the call. If the answer is bad, everything else is academic.

**2. Nationwide draw, or come-to-us? (read aloud)**
> "Our patients are all over the country. Can you collect from them wherever they are, at home or at a partner site, or does it depend on being near one of your four locations?"

- **Why it matters more than it sounds:** if Inuvi can collect anywhere, then a clinic joining our platform does not need its own phlebotomy capability. That removes the single biggest physical barrier to onboarding a new clinic. It turns a hard operational problem into a line item.
- **Red flag:** coverage limited to their own sites. Workable for a London brand, useless as national platform infrastructure.

**3. One relationship, or one per clinic? (read aloud)**
> "Here is how our side is structured. All the clinics run on our back end, one clinical pathway, one compliance framework, with our CMO as the responsible clinician throughout. Only the front end differs, the branding and the landing pages. So can you contract with us once, with our clinician as the requesting doctor across all of it, or would every clinic need its own account and its own requester with you?"

- **Good:** one master agreement, our prescriber as requester, sub-accounts underneath.
- **Red flag:** each clinic contracts separately. That makes us an introducer instead of a platform and kills the commercial model.

This is the same framing that worked with Amrita, and it is genuinely our strongest card. A supplier only has to assess **one** clinical relationship, not twenty. Lead with it as a strength, not a request.

---

## SECONDARY QUESTIONS

- **Turnaround.** "Sample collected Monday morning, results in our system when?" Two to three working days is normal. Anything over five breaks the patient experience.
- **Panels.** Do they have standard men's health and hormone panels off the shelf, or do we specify our own? Ask for their catalogue and price list.
- **Volume pricing.** Do not name our numbers. Ask: "How does your pricing move with volume, and what tiers do you work in?" Let him show the shape of the curve.
- **White label.** "Can results reach the patient under the clinic's brand rather than Inuvi's?"
- **Their CQC registration.** Worth one question: "What is your CQC registration for, and what does it cover us for as a client?" Regulatory cover is the hardest part of our build, and understanding what they already carry is worth more than a discount.
- **Data.** They hold ISO 27001. Ask who is controller and who is processor for patient results. Felix will want this in writing.

---

## FIRST, ONE HOUSEKEEPING QUESTION

Thomas Filmer introduced you, which means Inuvi may already be doing something with Ted's Health. Open with it so you do not accidentally renegotiate a deal Thomas has already done:

> "Before we get going, Harry, what do you already do with Ted's Health today? I want to make sure I am building on that rather than talking across it."

---

## LET FELIX TAKE THE TECHNICAL HALF

Felix is on the invite and has spoken to Harry before. The API, data flow and integration questions are his ground and he will get more out of them than a general conversation will. Take the commercial and structural questions, hand him the plumbing.

---

## CLOSE (read aloud)

> "This is useful, thank you. Two things to take away. Send me your panel catalogue and pricing with the volume tiers, and put me in touch with whoever owns the API so Felix can look at the integration properly. If it holds up technically, I would like to get an NDA signed and have a more specific conversation about what we are building."

---

## WHAT NOT TO DO

- **Do not commit to volumes.** Our clinic pipeline is not signed, and a number said out loud becomes the basis of every quote afterwards.
- **Do not mention Voy or the Ted's sale conversation.** Harry sits inside the Ted's supplier network.
- **Do not agree an exclusive.** It will sound harmless in an intro call and it will cost us later.

---

## AFTER THE CALL — WHAT I NEED

Just the answer to question one: API or PDF. If it is an API, I will draft the diagnostics section of the platform build with Inuvi as the assumed partner, and get Felix a technical contact. If it is PDFs, I will bring you two alternative UK labs before the end of the week, because that answer disqualifies them as platform infrastructure no matter how good the price is.

---
*Junior, 21 Jul 2026*
