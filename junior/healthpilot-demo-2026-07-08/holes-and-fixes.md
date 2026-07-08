# HealthPilot — Holes, Fixes & Honest Risks
### Internal memo · 8 July 2026 · confidential (never publish)

I ran a deep review of the product and the Ted's integration, then fixed what was safe to fix in our sandbox tonight. Below is the honest picture: what I improved, what still needs Felix, and the things we should NOT overstate to CJ.

---

## 1. What I fixed tonight (in our sandbox, verified)

These went into the demo and are live once the stack reboots:

- **Harborview now has its own logo.** The demo clinic was falling back to the Ted's Health logo on the patient's first screen, which quietly undercut the whole white-label story. Generated a clean Harborview wordmark and seeded it. The white-label promise is now visible at screen one.
- **Clinician stops are now shown, not described.** Seeded a scheduled consultation so the clinician "pre-brief" panel renders live, and stamped quiz content versions on the results so the clinician progress view shows its cross-version caveat. These are the "clinical infrastructure" proof points and they were previously narration.
- **Repeatable one-command demo bring-up (`demo-up.sh`).** Stands up fresh tunnels and boots the whole stack clean, then restores the demo clinic to its intended state. This is what you (or Felix) run shortly before the call to get a live link. The old link was 3 days stale and dead.

## 2. Holes that still need Felix (read-only repos — I can't touch these)

Ranked by how much they matter:

- **[High, operational cost] The AI rate limiters are dead code.** The limiters that are supposed to cap the AI endpoints exist but are wired to nothing, so the paid AI endpoints are effectively uncapped per IP. One-line fix each, but it's in the HealthPilot repo Felix owns. Left unfixed, a bad actor can run up a real OpenAI bill.
- **[High, PHI] Lab-result webhooks are unauthenticated.** The endpoint that writes blood-test results into a patient record accepts any/empty signature ("skip for demo"). Anyone who guesses an ID could write fake results to a real patient. Not demo-visible, but a genuine hole before real patients. Needs the real lab-partner signing scheme.
- **[High, before real data] Clinic API keys fall back to a publicly-known encryption key** if an env var is unset. Fine locally; must be set on the server before any real clinic key is stored.
- **[Med] Anonymous-intake claim can hijack tokenless intakes** on legacy paths. Fresh intakes are safe.

I've packaged these for Felix. None of them affect Thursday's demo; all matter before a real clinic goes live.

## 3. Things we must NOT overstate to CJ (talk-track honesty)

- **It runs on GPT-4o today, not Claude.** Some internal docs imply Claude + prompt caching + versioned prompts. That isn't wired up - it's GPT-4o, no caching, and the "prompt version" is a hardcoded string. The engine is provider-swappable, so the honest line is "GPT-4o today, provider-agnostic by design." Don't let anyone tell CJ it's Claude.
- **The red-flag safety net is a keyword backstop, not intelligent triage.** It catches emergency phrases in English and the escalation wiring around it is solid, but it's regex: it can misread "no chest pain," it's evadable by paraphrase, and it's English-only while we're pitching Spanish/German clinics. Sell it as "a safety backstop with clinician escalation," never as "AI that diagnoses." Pushing it toward "it can tell the patient they have low testosterone" tips it into medical-device (MHRA) territory - that's a hard line.
- **Recommendations can look similar for similar patients.** The catalogue has real depth now, but the quiz captures one goal and few structured symptoms, so two patients who pick the same goal and skip bloods get near-identical output. For the demo, use two clearly different personas (or one with a blood upload) so the "AI-matched" claim visibly holds.
- **The conversion economics are instrumented, not proven.** The click-to-purchase attribution is wired, but there is zero real attributed revenue yet. The whole model rests on an assumed 8% blood-panel conversion. Frame as "instrumented, awaiting design-partner data," never as a proven number.

## 4. Demo-prep checklist (before the call)

- Run `demo-up.sh` shortly before the call - the tunnel link changes each run and goes stale within a day or two.
- Do NOT run the e2e test between reseed and demo (it mutates two demo patients). The bring-up handles the reseed for you.
- Keep the public/patient browser window off any `/platform/*` path - it clears the clinic branding.
- Keep dev tools closed (harmless console noise from the local-only ecommerce stub).
- Deferred cosmetics (not worth touching pre-demo): owner-console "median completion time" reads low on same-instant seeded data; the 6-step signup claim funnel is worth shortening later (it's likely capping the lead→claim conversion).

## 5. Two things I did NOT do tonight, on purpose

- **Did not remove the `production` Firebase alias** from the sandbox working tree, though it's a real footgun (a stray deploy from this tree could hit real Ted's prod). It's a deploy-config change - Felix should confirm and make it.
- **Did not seed anything that could break a working demo.** Every change I made was verified against the live schema and the consultation seed is guarded so it can't take the rest of the demo down with it.
