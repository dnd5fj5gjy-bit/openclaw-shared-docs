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

---

## Session 2 — full build ("do everything properly, no half measures")

Two further pillars were then built into the real codebase and verified.

### Pillar A — schema-backed clinic customisation layer (commit `d4810f7`)

Deepens per-clinic control of the landing page end to end, backend included.

- **Schema + migration** (`add_clinic_homepage_customisation`): adds
  `heroCtaLabel`, `showAboutSection`/`aboutHeading`/`aboutBody`,
  `showTestimonial`/`testimonialQuote`/`testimonialAttribution`/`testimonialRole`,
  and `serviceCardOrder` to `Clinic` (additive, nullable). All added to
  `CLINIC_ADMIN_ALLOWED_FIELDS` and returned by `getPublicConfig` (with
  structural-access defaults). `ClinicPublicConfig` + frontend `ClinicBrandConfig`
  extended.
- **Render**: hero CTA-label override, an "our approach" block, a testimonial,
  and a clinic-defined service-card order (stable reorder; unlisted cards keep
  natural position).
- **Editor**: controls for all of the above incl. an arrow-based service-card
  reorder, feeding the same live preview and the standard `PUT /clinic/:id`.
- **Verified**: tsc + vite build + nest build clean; 9/9 homepage tests.

### Pillar B — supplement upsell funnel (commit `dcdba44`)

Built into the platform at its own standard, reusing the existing Medusa + Ryft
commerce so it goes live by *connecting* a supplier + SKUs, not rebuilding.

- **Server**: `SupplementProduct` (per-clinic catalogue; SKU/price/inventory
  stay in Medusa via `medusaVariantId`) + `PatientSupplementRecommendation`,
  both tenant-isolated (`CLINIC_SCOPED_MODELS`); additive migration
  `add_supplement_funnel`. New `domain/supplements` NestJS module —
  `SupplementsService` (tenant-scoped catalogue CRUD with a cross-tenant
  ownership guard, recommendation-slug → catalogue mapping, soft-delete) +
  `SupplementsController` (patient reads, clinic-STAFF CRUD) + DTOs. A
  `FulfilmentProvider` seam with a `NoopFulfilmentProvider` bound via a DI token,
  so the funnel runs fully in the sandbox and Felix swaps in a real dropship
  adapter by changing one `useClass`. 8 unit tests.
- **Frontend**: `lib/api/supplements` client; a `/dashboard/supplements`
  catalogue route (recommendations first with the clinical reason, then
  catalogue; add-to-basket via the existing `useCart`; "Available soon" when a
  variant isn't seeded); a gated Explore nav entry on `supplementsEnabled`.
- **Verified**: nest build + vite build + tsc clean; 8 server + 44 frontend
  tests pass.

**Felix connects (seamed + documented, cannot be coded without external access):**
- Real dropship adapter behind `FulfilmentProvider` (supplier API/credentials).
- Live Medusa supplement SKUs + prices + inventory; confirm Ryft covers
  supplement charges + the platform/clinic split.
- Extend the HealthPilot summary-export contract to emit supplement
  recommendation slugs, mapped to each `SupplementProduct.recommendationSlugs`.
- Live payments go-live (shared with TRT/ED: live Ryft creds + KYB/KYC).

### Still recommended, not built (needs the other repo deployed)

**HealthPilot brand inheritance** — the sandbox `Clinic` forwarding brand tokens
into the HP embed so the quiz matches each clinic. Not built because the
consuming side lives in the separate, not-yet-deployed `health-pilot-frontend`
`feat/whitelabel-luxury` branch, so it can't be verified end-to-end. Low-risk to
add once HP deploys.

### Full commit list (branch `feat/golive-landing-supplements`)

- `23ca4db` per-clinic public landing page in the product
- `02565aa` quiz scroll-to-top fix + landing review hardening/polish
- `d4810f7` schema-backed clinic customisation layer
- `dcdba44` supplement upsell funnel
