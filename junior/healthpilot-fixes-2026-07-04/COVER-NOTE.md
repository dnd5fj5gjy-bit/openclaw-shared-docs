# HealthPilot Fixes - Patch Package
**Junior - 4 July 2026**

Every critical finding from the 3 July report is fixed. Three patch files, one per repo, each a clean git format-patch series against main. TypeScript checks pass on backend and frontend; test suites show zero regressions against baseline (the handful of failures that exist were already failing on main). The sandbox patch could not be type-checked locally (no installed deps) but is a single contained method change.

## What is fixed

### 1. whitelabel-server.patch (th-whitelabel-sandbox, 1 commit)
- **THWL super-admin backdoor removed.** The public signup endpoint no longer accepts the hardcoded "THWL" secret (which granted super-admin, and all-clinic clinician via the sibling endpoint, in every environment). It now only accepts `PLATFORM_ADMIN_SIGNUP_SECRET` from the environment, minimum 24 chars, compared in constant time. If the var is unset, self-signup is disabled entirely (fail closed).
- **Action needed:** if deliberate self-signup is still wanted, set `PLATFORM_ADMIN_SIGNUP_SECRET` (24+ chars) in the environment. **Check the live th-whitelabel repo for the same backdoor** - the report flagged it likely predates the sandbox.

### 2. health-pilot-backend.patch (5 commits)
- **PHI lockdown.** Anonymous intakes now get a one-time 256-bit access token on creation (only its SHA-256 hash is stored). All reads/mutations of an intake - detail, complete, summary status, all three plan endpoints, and link-anonymous-intake - require the token or an authenticated owner. Non-owners get 403. Legacy anonymous intakes become inaccessible (intended lockdown).
- **AI can no longer invent answers.** Unanswered questions are omitted from the AI payload instead of defaulted (no more phantom "7 hours sleep" or "never smoked"). Prompts render missing data as "Not provided" and explicitly forbid inventing it. Safety checks no longer treat "never asked" as "patient confirmed none" - supplements with listed interactions are excluded when medication questions were not answered.
- **Red-flag handling.** New detection service (chest pain, self-harm, stroke, breathing difficulty, anaphylaxis, severe bleeding, loss of consciousness) scans all answers on submission. Flagged intakes get a structured urgent-care payload (999 / NHS 111), never recommendations. 14 unit tests included. Under-18s (when DOB given) get a "see a GP" response and AI generation is blocked - note DOB is still optional, product decision whether to require it.
- **Fake blood tests gated.** Fabricated demo results now sit behind `DEMO_FAKE_BLOODTESTS` (defaults OFF). When off, ordered tests stay ORDERED with no results feeding the AI.
- **Quick wins:** AI temperature actually set from config (was dead code running at 1.0), model output schema-validated (malformed JSON now fails the generation instead of dumping raw text at the patient), intake endpoint capped at 1MB.

### 3. health-pilot-frontend.patch (5 commits)
- **Skip no longer lies.** Skipped required questions show amber on the review screen with a jump-back link, and Generate is blocked until they are answered.
- **Retry no longer double-bills.** Retrying a failed generation reuses the same intake and job instead of creating a duplicate paid AI run.
- **Refresh/back no longer destroys the quiz.** Answers, step and access token persist to sessionStorage with resume-on-return, plus a leave warning mid-quiz.
- **Urgent-care and GP screens.** Red-flagged intakes render a full-screen 999 / NHS 111 / Samaritans interstitial (checked at create, poll and fetch - flagged intakes never queue an AI job); under-18s get a softer "see a GP" screen. Shapes matched exactly to the new backend payloads.
- **Token integration.** Frontend captures the new access token from intake creation and sends it as a Bearer header on all guarded endpoints; logged-in users use their JWT as before.
- Also fixed: slider default-value validation quirk.

## Apply order and deployment notes
1. Sandbox patch is standalone - apply any time.
2. **Backend and frontend must ship together.** The backend locks down endpoints the old frontend calls unauthenticated; deploying backend alone breaks the live quiz for anonymous users.
3. Backend has **two SQL migrations** (access token hash, red-flag columns) - run before deploy.
4. New env vars: `PLATFORM_ADMIN_SIGNUP_SECRET` (sandbox server, optional, fail-closed), `DEMO_FAKE_BLOODTESTS` (backend, default off - set true in demo envs to keep fake labs).

## Left open (deliberate)
- Rotate anything real in the sandbox git history (CA private keys, old .env tokens) and repoint `.firebaserc` away from live Ted's Firebase projects - config changes, not code, so not in these patches.
- Whether DOB should be required (currently optional, so age gating only fires when given).
- Red-flag pattern list is deliberately broad (historic "seizure" will flag); single list, easy to tune.
- Blood-test rows have no "demo" source column (needs a migration if wanted).
- The embed SDK / identity integration from the report is a feature build, not a fix - not included.

Apply with `git am <file>.patch` on a branch off main in each repo.
