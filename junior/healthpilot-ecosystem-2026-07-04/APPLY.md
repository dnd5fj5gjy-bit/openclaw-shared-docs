# HealthPilot 4 July Build — Apply Guide

Everything built on 4 July, consolidated. The two FULL patch files replace every incremental patch sent earlier today (security fixes, upgrade round 1, round 2, analytics, webhooks, progress tracking, owner console). If you already applied earlier patches, start from a clean main instead - the FULL patches contain those same commits.

## 1. HealthPilot backend (health-pilot-backend)

```
git checkout main        # must be at ad11218 (current origin/main)
git checkout -b feat/product-upgrade
git am health-pilot-backend-FULL.patch    # 20 commits, verified clean on a fresh clone
npm install              # no lockfile changes, install as normal
npx prisma migrate deploy
npx prisma generate
npx tsc --noEmit         # verified clean
npx jest                 # 236 pass, 4 pre-existing failures in matching.service (present on main)
```

New migrations (all 20260704_*): intake_access_token, intake_red_flags, intake_clinic_identity, intake_funnel_events, clinic_api_keys, clinic_webhooks, intake_repeat_linkage.

New/changed env vars:
- `EMBED_ALLOWED_ORIGINS` - comma-separated partner origins allowed to iframe the quiz (CSP frame-ancestors). Required for any embedding.
- `DEMO_FAKE_BLOODTESTS=false` - keep false in production; true fabricates demo lab results.
- Redis (`REDIS_URL`) is now load-bearing for webhook delivery (BullMQ queue) as well as existing jobs.

Owner console: create an admin account with `npx ts-node scripts/create-admin.ts`, log in at `/owner` on the frontend. Clinic API keys can now be issued from the UI (the `create-clinic-api-key.ts` script still works).

## 2. HealthPilot frontend (health-pilot-frontend)

```
git checkout main        # must be at 9ad70eb (current origin/main)
git checkout -b feat/product-upgrade
git am health-pilot-frontend-FULL.patch   # 26 commits, verified clean on a fresh clone
npm install
npm run build            # prebuild emits public/embed/hp-embed.js + hp-embed.v1.js
npx tsc --noEmit         # verified clean
npx vitest run           # 87 pass, 13 pre-existing failures (present on main)
```

Partner embed docs are in `EMBED.md` in the repo root after applying. Webhook partner docs are in `docs/WEBHOOKS.md` on the backend.

## 3. Ted's white-label sandbox (th-whitelabel-sandbox)

No patches - everything is pushed. Merge PR #1 (security) then PR #2 (the full Health Quiz integration, waves 1-6 documented in the PR body). Then:

```
npx prisma migrate deploy   # 5 new migrations: healthQuizEnabled, health_quiz_results,
                            # publicHealthQuizEnabled, health_quiz_events, healthQuizReassessmentWeeks
```

New env var on the sandbox server: `HEALTHPILOT_API_URL` (see `server/env.healthpilot.example`). Optional: `CLINICAL_ALERT_EMAIL` override for urgent-escalation alerts.

## 4. Suggested smoke test order

1. Backend + frontend up, `EMBED_ALLOWED_ORIGINS` includes the sandbox origin.
2. Sandbox: enable Health Quiz on a clinic via the new clinic-settings > Health Quiz setup page - the checklist tells you what is missing.
3. Run a quiz in-portal: completion should ingest a result, show the clinician brief in the staff Health Quiz tab, and populate the analytics view.
4. Answer with an urgent red flag: escalation created, clinician email sent, dashboard chip appears.
5. Public flow: enable the public flag, complete a quiz logged out, sign up, confirm the result attaches (claim) and the Recommended-for-you card shows.
6. Retake a quiz with the same patient: Health Report shows "Your progress"; sandbox history shows trajectory chips.
7. Owner console at `/owner`: clinic appears with usage; issue a key; register a webhook endpoint via API and watch the test event deliver.

Not run in my environment (needs your stack): live AI generation end-to-end, DB migrations against real data, SendGrid sends, webhook delivery to a real endpoint. Everything else is typecheck + test verified per patch.

Junior, 4 July 2026
