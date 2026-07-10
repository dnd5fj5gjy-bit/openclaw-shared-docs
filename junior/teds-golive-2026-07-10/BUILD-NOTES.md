# Build Notes — Ted's Health go-live (10 Jul 2026 overnight)

Concrete code built this session, in the real platform codebase (not a demo).
Companion to `HANDOVER-ARCHITECTURE.md`.

Repo: `th-whitelabel-sandbox`
Branch: `feat/golive-landing-supplements` (off `feat/embed-integration`, the real
integration branch that carries the health-quiz work; `main` is untouched).
Commit: `23ca4db` — "feat(homepage): per-clinic public landing page in the product".

---

## What shipped: the public per-clinic landing page, IN the product

This directly closes go-live gap #1 and answers the core problem — the premium
landing had only ever existed as a throwaway static demo (the Harborview
GitHub Pages SPA). It now lives inside the platform, driven entirely by each
clinic's stored config, so every clinic gets its own branded landing with zero
per-clinic code.

### Files

| File | Change |
|---|---|
| `frontend/src/components/homepage/ClinicHomepage.tsx` | **New.** The landing component. Reads the clinic config (colours, logo, hero copy/image, section toggles, pathway flags) and renders a premium, fully brand-driven marketing page: hero + adaptive CTAs, "how it works", auto-generated service cards (only for enabled pathways), trust/credibility, closing CTA band. Accepts an optional `clinic` override + `previewMode` so the settings editor can preview unsaved edits with inert CTAs. |
| `frontend/src/components/homepage/ClinicHomepage.test.tsx` | **New.** 5 regression tests (all pass): hero copy, brand-safe default headline, quiz-led CTA gating, pathway-derived service cards, section-visibility toggles. |
| `frontend/src/routes/_app.index.tsx` | **Changed.** `/` used to unconditionally redirect anonymous visitors to `/login`. Now: authed → `/dashboard` (unchanged); anonymous visitor of a `homepageEnabled` clinic → the branded landing; `homepageExternalUrl` set → redirect out; platform apex / unresolved clinic / homepage disabled → historical `/login` redirect (no regression). |
| `frontend/src/routes/staff/_mainNav/clinic-settings.homepage.tsx` | **Changed.** Was a redirect stub (the homepage editor had been retired). Re-wired as a real self-service editor: visibility toggle, external-URL override, hero headline/sub-headline (length-limited), hero image upload, and section toggles — with a **live, brand-accurate preview** rendered by the same `ClinicHomepage` component the public site uses. Saves via the standard `PUT /clinic/:id` path. |
| `frontend/src/routes/staff/_mainNav/clinic-settings.tsx` | **Changed.** Added the "Homepage" tab to the settings rail (clinic-owner-facing, hidden from platform super-admins, same rule as Branding). |

### Why this fits the platform's standard (not a bolt-on)

- **No new backend was needed.** `GET /clinic/config` (`clinic.service.ts:getPublicConfig`) already serves every homepage field (`homepageEnabled`, `homepageExternalUrl`, `heroTitle`, `heroSubtitle`, `heroImageUrl`, `showServicesSection`, `showHowItWorks`, `showTrustSection`), and all of them are already in `CLINIC_ADMIN_ALLOWED_FIELDS`, so a clinic admin can already save them. The gap was purely that nothing rendered them and the editor tab had been unwired. This build closes exactly that gap and nothing else.
- **Config-driven, multi-tenant by construction.** The landing reads only the resolved `Clinic` config through the existing `useClinicBrand()` context, so it inherits tenant resolution, brand CSS, and isolation for free. Zero per-clinic branching.
- **Respects the original guardrail.** The homepage editor was deliberately unwired in May "to avoid exposing an untested surface at go-live." This build re-exposes it *with* a regression test and a real render path, which is the condition that guardrail implied.

### Verification

- `npx tsc --noEmit` (frontend): **clean, 0 errors.**
- `npx vitest run src/components/homepage`: **5/5 pass.**
- Production build (`npm run build`): see `fe-build-result.txt` in this folder.
- Pre-existing unrelated failure: `clinic-settings-pricing.test.tsx` has one failing
  assertion (MAP tooltip trigger count 5 vs 4). It renders the Pricing route, which
  this build never touches; it fails on the base branch too. Flagged, not caused here.

### How to see it live (for Felix)

1. Boot the stack (`KEEP_UP=1 DEMO_RESEED=1 ./e2e/run.sh` from the sandbox root, or `npm run local:start`).
2. Ensure a demo clinic has `homepageEnabled = true` (default) and some hero copy.
3. Visit the clinic's host (e.g. `?clinic=<slug>`) while logged out → the branded landing renders. Log in → straight to dashboard (unchanged).
4. Staff → Clinic Settings → **Homepage** → edit hero copy / toggles, watch the live preview, Save, reload `/` to confirm.

---

## What was deliberately NOT hand-built overnight (and why)

**The supplement funnel (go-live gap #2).** It is fully designed in
`SUPPLEMENT-FUNNEL-SPEC.md` (this folder), ready to build. It was not
hand-written tonight because doing it *properly* means a Medusa v2 commerce
module + Ryft checkout reuse + a fulfilment adapter seam — commerce code that,
built unverified against live payment/fulfilment paths overnight, would be
exactly the fragile "surface-level" work this effort is meant to avoid. The
spec makes it a mechanical build for the next session or for Felix, with the
external pieces (dropship supplier API, live Ryft) clearly seamed off.

**HealthPilot brand inheritance.** Recommended and specced in the handover
(the sandbox `Clinic` should forward brand tokens into the HP embed so the quiz
matches each clinic). Not built tonight because the consuming side lives in the
separate, not-yet-deployed `health-pilot-frontend` `feat/whitelabel-luxury`
branch, so it could not be verified end-to-end. Low-risk to add once HP deploys.
