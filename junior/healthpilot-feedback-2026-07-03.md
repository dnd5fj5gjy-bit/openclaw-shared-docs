# HealthPilot x Ted's White-Label - Test Feedback
**Junior - 3 July 2026**
Tested: two full end-to-end runs of the hosted quiz (desktop + 390px mobile) plus edge-case probes, and a full read-only code review of `th-whitelabel-sandbox` (with `health-pilot-frontend`/`health-pilot-backend` as reference).

---

## Verdict

The concept works and the bones are good. Both runs completed with no crashes, the flow is clear, mobile is genuinely solid, the loading states are polished, and the recommendation engine is properly DB-driven with affiliate tracking already built in - the revenue seam is real. But three things need fixing before this goes near a patient or a clinic demo: **the AI fabricates patient data**, **there is no safety net for red-flag symptoms**, and **the security posture has two critical holes**. The integration itself is currently a UI-only prototype (an iframe), so the "referral revenue inside the clinic" story has no plumbing yet. All fixable, and the fixes are mostly cheap.

---

## 1. Must-fix before anything else (critical)

**1.1 The AI invents answers the patient never gave.** I selected 4 hours of sleep; the summary reported "7 hours". I submitted a gibberish concern ("asdf qwerty") and skipped every question; the AI confidently described a patient with "no tobacco or alcohol use, 7 hours sleep, budget sensitivity and preference for home delivery" - none of which are even questions in the quiz. Root cause is visible in the code: the intake mapping hardcodes defaults (`symptoms: []`, `smokingStatus: 'never'`, `alcoholConsumption: 'none'` etc. in `intake.routes.ts:321-361`) and the prompt gets seeded with them. In a health product, reporting 4 hours as 7 changes the interpretation. Fix: only pass the AI what the patient actually answered.

**1.2 No red-flag handling anywhere.** A patient typing "chest pain" or describing suicidal thoughts gets a wellness plan and supplement recommendations. There is zero emergency escalation logic in frontend or backend (no 999/111 interstitial, no crisis copy). This is the single biggest liability for a medical brand. Cheap fix exists: the quiz config schema already supports conditional fields, so a red-flag rule that halts the quiz and shows an urgent-care screen is a small change. Also: no age gating (DOB optional, anonymous intake).

**1.3 Hardcoded super-admin backdoor in the white-label server.** Anyone who sends the literal string `"THWL"` to the public signup endpoint (`platform-admin.service.ts:167-174`) gets a super-admin account, in every environment. The secret is in the source code. This is the worst thing in the codebase and predates the sandbox - if it exists in the live repo too, it needs killing this week.

**1.4 Health data readable without login.** `GET /intakes/:id` returns the fully decrypted intake and recommendation to anyone holding the UUID, no auth required (`intake.routes.ts:404-455`); several plan endpoints have no ownership check at all. Intake IDs will leak via iframe URLs and referrer headers once embedded. Combined with 1.3, this is a GDPR/PHI incident waiting to happen.

**1.5 Fake blood tests treated as real.** "Ordered" blood tests write fabricated demo values to the DB as COMPLETED results, which then feed the AI summary as if they were real labs (`bloodtest.service.ts`). Fine for a demo, but there is no environment gate, so it must be flagged before any production path reuses this code.

---

## 2. Bugs found in live testing

- **Skip bypasses all validation.** "Continue" correctly blocks empty required fields, but "Skip this question" advances anyway. You can skip all five steps and the review screen shows "All sections complete" with every tick green, then generates a summary from nothing.
- **Browser back destroys the session.** The whole quiz lives at one URL. Browser back (or a mobile back-swipe) exits to a blank page and the retry restarts at step 1 with everything lost, including a generated summary. No warning, no restore. Related: refreshing mid-quiz loses all state; the autosave interval exists in config but is never wired up.
- **Retry after an AI failure creates a duplicate intake** and a second paid AI job (`DynamicWizard.tsx:301-348`).
- **Contradictions inside one output.** Run 2: stress slider at 10/10 produced "severe stress" in the warning banner and "moderate stress" in the body of the same summary. "1-2x per week exercise" became "no regular exercise".
- **Canned section headings don't match their content.** "Digestive Patterns" contained sleep advice in both runs; nothing digestive was ever discussed. Looks like a fixed heading list zipped with AI bullets by index.
- **Slider quirk:** a slider left at its default position fails "required" validation even though the thumb is visibly on a value; the user has to wiggle it.
- **Identical "85% compatibility score" in both runs** despite completely different answers. If it is hardcoded, drop it - fake precision damages trust more than no score.
- Minor: recurring aborted prefetch request on the summary page (`/next-steps?_rsc=... ERR_ABORTED`), dead route `ed-old.tsx` still registered, TODO stub on the appointment booking route.

---

## 3. UX and AI quality

**Good:** clear 6-step progress header, per-field validation messages, persistent "not a medical diagnosis" banner, in-app back preserves answers, mobile layout is clean with no horizontal scroll, and the "Analysing Your Health Profile" loading sequence feels premium. AI generation took 5-18 seconds, acceptable.

**AI output:** real personalisation exists - concern, duration, goal, sleep quality, energy and care preference were all correctly reflected, and the two runs produced meaningfully different strategies ("Lifestyle Enhancement for Energy and Sleep" vs "Balanced Hormonal Health"). Advice is conservative and safe in tone, disclaimers are everywhere. But:

- The summary talks about the patient in the third person ("the user expresses concerns...") - it should say "you".
- Run 2's headline complaint (vanished libido) got no libido-specific question, signal, or pathway - the symptom checklist is the same five items regardless of goal, and the only real branch in the whole quiz is the blood-test yes/no. Different goals should unlock different question sets; that is where the "impressively personal" feeling will come from.
- Run 2 said "open to clinical treatment" and still got a lifestyle-only plan.
- Both personas received the same three supplements (D3+K2, Ashwagandha, Magnesium Glycinate) and the same single provider, just reordered. The catalogue needs depth or the "AI-matched" claim collapses on the second use.
- "What This May Mean" is identical generic boilerplate in every run - cut it or personalise it.
- Step descriptions leak internal CMS voice to patients ("Document the symptoms most relevant to the user's current complaint", "Let users upload recent results").
- Answering YES to a recent blood test hits a login wall to upload, but you can continue without uploading and the summary reads as if labs were considered.
- Technical notes for Felix: temperature is never set on any AI call (the whole AI_TEMPERATURE config block is dead code, everything runs at default 1.0), and there is no schema validation on model output - malformed JSON degrades to raw text shown to the patient. The docs claim Claude Sonnet + prompt caching + versioned prompts; reality is gpt-4o only, no caching, hardcoded v1.0.0. Raw quiz answers also go verbatim into the prompt from an unauthenticated endpoint with a 25MB body limit - prompt-injection and cost-abuse surface.

---

## 4. The integration itself (sandbox repo)

The integration is currently three files: a sidebar nav entry, an iframe route pointing at `/intake`, and an env var. Honest prototype, but the seams that make it a product do not exist yet:

- **No identity in:** the iframe passes no patient ID, clinic slug, or token. HealthPilot does not know who is taking the quiz or for which clinic.
- **No results out:** no postMessage bridge, no webhook, no endpoint - quiz results never reach the patient record, so the referral-revenue loop has no mechanism.
- **Framing will break in production:** HealthPilot's backend sends `X-Frame-Options: SAMEORIGIN` and the frontend sets no frame-ancestors policy, so the embed either fails or is open to clickjacking depending on which side gets disabled.
- **Escape hatches:** links inside the quiz can navigate the iframe to HealthPilot's own landing page and login inside the clinic dashboard.
- **No clinic opt-out:** every other pathway (TRT, ED, products) is per-clinic toggled; the Health Quiz renders unconditionally. Clinics must be able to opt in contractually to a partner-referral quiz.
- **HealthPilot is not white-label-ready:** "Health Pilot" wordmark, teal palette, and support@healthpilot.com are hardcoded. The Ted's white-label platform itself, by contrast, is genuinely mature - per-clinic theming, pricing overrides, feature flags all real.

Also worth knowing: the sandbox contains committed CA private keys and old `.env` files in git history (Klaviyo/Storyblok tokens) - rotate anything that was ever real - and `.firebaserc` still points at real Ted's Firebase projects, so a manual `firebase deploy` with credentials present could reach production despite the deploy workflow being removed.

---

## 5. Ideas to make it genuinely impressive

1. **A proper embed SDK (highest leverage, one component).** postMessage events out (`ready`, `height`, `completed {intakeId}`) and config in (`theme`, `patientRef`, `authToken`). This single piece solves identity, auto-resize, theming, and writing results back to the patient record - and turns the iframe from a demo into the product.
2. **Goal-driven question branching.** Pick "Hormone Balance" and get hormone-specific questions (libido, morning erections, body composition); pick "Energy" and get sleep/caffeine/shift-work questions. This is the difference between "a form" and "it really understood me", and the quiz engine's conditional-field schema already supports it.
3. **Red-flag interstitial** (also a safety must-have): urgent symptoms halt the quiz with a "call 999 / NHS 111" screen. Doubles as a trust signal in clinic sales demos.
4. **Autosave + resume.** Wire the existing autosave config to sessionStorage for everyone, and on retry poll the existing intake instead of creating a new one. Kills the two worst data-loss bugs for ~30 lines.
5. **Use the blood-test branch as the wedge.** "No recent blood test" → offer Ted's blood panel right there (real revenue, already in the platform). "Yes" → parse the upload and reference actual markers in the summary. That is the moment the quiz becomes a funnel rather than a questionnaire.
6. **Stream the pipeline stages during generation** ("Comparing 14 providers...", "Checking interactions...") - the status plumbing already exists, and it makes the 15 seconds feel like work being done rather than a spinner.
7. **Clinic-branded results PDF / email** of the summary the patient can take to their GP - shareable artefact, brings the clinic's brand home, and creates the follow-up touchpoint.
8. **Feature-flag the quiz per clinic** in ClinicBrandConfig like every other pathway, so the referral programme is an opt-in commercial term.

---

## Priority order if Felix does nothing else

1. Kill the THWL signup secret (live repo too, if present)
2. Lock down the unauthenticated intake/plan reads
3. Stop seeding the AI with default answers, and pass symptoms/medications/allergies through so the safety checks stop running on empty arrays
4. Red-flag + age gating
5. Skip-validation bypass, autosave, duplicate-intake retry
6. Then the embed SDK, and the integration becomes real

Evidence available on request: 20+ screenshots of both runs and the edge probes, full verbatim AI outputs as JSON, and file/line references for every code finding.
