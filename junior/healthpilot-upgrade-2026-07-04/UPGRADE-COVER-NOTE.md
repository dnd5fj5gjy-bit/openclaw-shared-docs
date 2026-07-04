# HealthPilot Product Upgrade - Cover Note
**Junior - 4 July 2026**

Jesse asked for a full pass on HealthPilot: improve the concept, functionality, business plan and monetisability, then build it. This package is the result. It builds on top of the 4 July security fixes (already delivered; sandbox PR #1).

---

## What was built today

### 1. Embed SDK - the integration is now real
The iframe demo is now a product integration. HealthPilot's quiz runs in embed mode with a strict origin-validated postMessage protocol:
- **Identity in:** clinic slug, patient reference and brand theme (colour, logo, name) flow from the clinic platform into the quiz. HealthPilot now knows who is taking the quiz and for which clinic.
- **Results out:** on completion the host platform is notified, fetches the full summary export server-side with a capability token, and writes it into the clinic's patient record. PHI never passes through the browser bridge.
- Auto-resize, step tracking, red-flag notification (category slug only, no PHI), navigation escape hatches sealed, HealthPilot chrome hidden, clinic branding applied.

### 2. Goal-driven question branching
Picking "Hormone Balance" now unlocks hormone-specific questions (libido, morning energy, body composition, mood); "Energy & Sleep" asks about caffeine, shift work and wind-down; "Weight" asks about appetite and previous approaches. Answered branch questions flow into the AI prompt and the matching engine. This is the "it really understood me" upgrade.

### 3. Blood-test wedge - the first revenue loop
Patients who answer "no recent blood test" now see a clinic-branded "Get a full blood panel" CTA on their summary. Inside a clinic embed, the click routes to that clinic's own panel purchase page. This is the funnel moment: quiz completion becomes panel revenue.

### 4. Streaming generation stages
The 5-18 second AI wait now shows real pipeline progress ("Analysing your health profile", "Matching recommendations", "Running safety checks", "Composing your plan") driven by actual backend stages, not fake timers.

### 5. Per-clinic feature flag
Health Quiz is now an opt-in pathway toggle on ClinicBrandConfig, default OFF, super-admin controlled - same pattern as TRT/ED. The referral programme becomes a commercial term, not a default.

### 6. AI output quality
- Summaries address the patient as "you", never "the user"
- Fabricated "85% compatibility score" removed everywhere (it was a formula, not a measurement)
- Section headings are now authored by the model with its content, validated, so "Digestive Patterns" can no longer contain sleep advice
- Generic "What This May Mean" boilerplate removed; concern-specific or absent
- CMS-internal voice stripped from patient-facing step descriptions
- Recommendation catalogue deepened (9 new supplements, new provider, goal-driven matching rules) and the matching bug that gave everyone the same 3 supplements fixed

### 7. Embedding security
X-Frame-Options replaced with an env-driven CSP frame-ancestors allowlist (EMBED_ALLOWED_ORIGINS), so HealthPilot embeds only where it is told to. Unset = current locked-down behaviour.

---

## Where the code is

| Repo | Delivery | Contents |
|---|---|---|
| th-whitelabel-sandbox | **PR #2** (stacks on PR #1, main untouched) | Embed component, feature flag, results-to-patient-record ingestion, 2 DB migrations |
| health-pilot-backend | **health-pilot-backend-upgrade.patch** (applies on top of the 4 July security patch) | Summary-export endpoint, clinic identity, stages, branching seed, prompt fixes, catalogue, frame-ancestors |
| health-pilot-frontend | **health-pilot-frontend-upgrade.patch** (applies on top of the 4 July security patch) | Embed SDK, stage labels, blood-panel CTA, score removal |

Apply order for Felix: 4 July security patches first, then these. `git am` each file. New env vars: `EMBED_ALLOWED_ORIGINS` (HealthPilot backend), `HEALTHPILOT_API_URL` (white-label server).

## Verification
TypeScript clean on all three repos. Test suites: zero regressions vs base branches; 60+ new tests added across the three repos, all passing. Not yet run: a live end-to-end AI generation (needs OpenAI key + DB + Redis) and the DB migrations against a real database - both are Felix's environment.

## The business plan
Separate document: **HealthPilot Business Plan & Monetisation Strategy**. Headline: three-part hybrid model (SaaS tiers £199/£449/£899 + £0.60 per-intake overage + 10% rev share on quiz-attributed panels and consultations). A 500-intake clinic yields ~£1,209/month; 30 clinics = ~£435k ARR at 80%+ gross margin. The load-bearing assumption to validate first is the 8% intake-to-panel conversion; the 90-day plan starts with 2 Ted's clinics live as design partners.
