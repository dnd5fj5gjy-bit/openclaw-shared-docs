# Ted's Health White-Label Platform — Go-Live Architecture & Handover (10 Jul 2026)

**Audience:** Felix (senior engineer, taking this to production next week) and Jesse (founder, exec summary only).
**Status:** Sandbox audited by reading the code. This document records the stable architecture and the honest go-live status. Concrete code changes made in this session are logged separately.

---

## What was built in this session (see BUILD-NOTES.md)

> Placeholder — the concrete code changes from this session are logged separately in `BUILD-NOTES.md` in this same folder. This handover covers only the stable architecture and audited go-live status.

---

## 1. Executive summary (for Jesse)

The Ted's Health white-label platform is already a real, production-grade system, not a prototype. It is a multi-tenant clinic platform: each clinic is an isolated tenant with its own branding, its own patients, and its own data, all served from one codebase. The white-label surface is genuine self-service, clinics can set their logo, colours, fonts, and welcome messaging through a real branding editor, and an AI health quiz (HealthPilot) is embedded per-clinic with real AI, real red-flag safety checks, and real supplement-matching logic. The premium landing page you have been reviewing (Harborview) was a separate standalone demo built on GitHub Pages to show the look and feel; it is not yet wired into the actual product, and bringing that experience into the platform is now pure engineering work. Three things stand between us and go-live: (1) the per-clinic public landing page needs to be wired into the product, (2) the supplement funnel needs a real catalogue and checkout built on top of the matching logic that already exists, and (3) live payments need Felix to connect Ryft's live credentials and pass their compliance checks. Two of those three are code we control; the payment piece needs external providers.

---

## 2. System architecture

Three repositories, all local under `~/agents/junior/workspace/repos`.

### 2.1 `th-whitelabel-sandbox` — the platform (internal name `th-whitelabel`)

A full duplicated copy of the Ted's Health platform that Felix provisioned as a sandbox. Junior holds push access to the sandbox; `main` is protected and untouched. It is a monorepo:

- **`server/`** — NestJS + Prisma + PostgreSQL. ~90 models across a ~3,100-line `schema.prisma`. The system of record and the API.
- **`frontend/`** — Vite + React + TanStack Router. Four surfaces in one app: patient, staff, admin, platform.
- **`medusa/`** — Medusa v2 e-commerce, with a Ryft payments module.
- **`firebase/` + `functions/`** — Firebase Auth and Cloud Functions.

### 2.2 `health-pilot-frontend` — HealthPilot (the AI quiz front-door)

Next.js 16 AI health-quiz application, embedded into the platform as an iframe. Relevant branch: `feat/whitelabel-luxury`.

### 2.3 `health-pilot-backend` — HealthPilot's backend

Express + TypeScript + Prisma. Relevant branch: `feat/product-upgrade`. Runs the AI provider, red-flag detection, supplement matching, and webhook delivery.

### 2.4 How they connect

The platform frontend embeds HealthPilot via an iframe (`components/health-quiz/HealthPilotEmbed.tsx`) pointed at `VITE_HEALTHPILOT_URL`, passing `?clinic=<slug>&locale` and communicating over validated `hp:*` `postMessage` events. HealthPilot's backend talks back to the platform server through a signed (HMAC-SHA256) webhook, and the platform pulls summaries server-side using an encrypted per-clinic `healthPilotApiKey`.

### 2.5 Multi-tenancy model

- **Tenant = `Clinic`** (`server/prisma/schema.prisma`).
- **Resolution:** `ClinicUrlResolverService` (`server/src/core/clinic-url/clinic-url-resolver.service.ts`) resolves the tenant from a custom domain or from `<slug>.<PLATFORM_ROOT_DOMAIN>`.
- **Isolation:** row-level tenant scoping via `AsyncLocalStorage` (`server/src/core/database/tenant-context.ts`) auto-injects `WHERE clinicId` on queries. Super-admin paths use `@BypassTenantFilter()`.
- **Special tenant:** the `isPlatform` flag marks the Ted's-owned tenant. Clinic `status` (`DRAFT` / `LIVE`) gates whether real payments can run.

This tenancy layer is production-grade.

### 2.6 The core principle: Clinic = single source of truth for brand

The clean architecture, and the one this handover recommends holding to, is that **the sandbox `Clinic` record is the single source of truth for brand.** The platform stores the branding tokens; HealthPilot should *inherit* them by having the clinic forward its brand tokens into the embed (via the `data-hp-*` / `hp:init` path that the `feat/whitelabel-luxury` work already provides) rather than maintaining its own brand store. HealthPilot's own brand config currently has no persistence, which is exactly why it should not own brand state.

---

## 3. Feature-by-feature go-live status

| Feature | Status | Where it lives | Notes |
|---|---|---|---|
| Multi-tenant clinic isolation | Real | `server/src/core/database/tenant-context.ts`, `clinic-url-resolver.service.ts` | Row-level `WHERE clinicId` via AsyncLocalStorage; `@BypassTenantFilter()` for super-admin. |
| Brand tokens on the tenant | Real | `Clinic` model in `schema.prisma`; `GET /clinic/config` (`clinic.controller.ts` `getPublicConfig`, `clinic.service.ts:885`) → `contexts/clinic-brand.tsx` | logoUrl, primaryColor, accentColor, buttonColor, fontFamily, customCss, faviconUrl, logoScale, welcomeMessage. |
| Self-service branding editor | Real | `staff/_mainNav/clinic-settings.*`, `components/branding/*` | Clinic admins edit only whitelisted fields (`CLINIC_ADMIN_ALLOWED_FIELDS` in `clinic.service.ts`); platform-only fields locked. |
| Clinic onboarding wizard | Real | `platform.signup.tsx`, `staff/onboarding.tsx`, `clinic-signup.service.ts` | Real self-service signup path. |
| Embedded AI health quiz | Real | `components/health-quiz/HealthPilotEmbed.tsx`; gated by `healthQuizEnabled` + `publicHealthQuizEnabled` | iframe to `VITE_HEALTHPILOT_URL`, origin-validated `hp:*` postMessage, auto-resize. Public lead-capture route `_app.health-assessment.tsx`. |
| Health-quiz server domain | Real | `server/src/domain/health-quiz/` | Analytics, reassessment, signed-HMAC webhook ingestion, encrypted per-clinic summary export. |
| HealthPilot AI | Real (stub-swappable) | `health-pilot-backend` provider factory | OpenAI `gpt-4o` via provider factory; `AI_PROVIDER=stub` for CI. |
| Red-flag / emergency detection | Real | `health-pilot-backend` | Regex, 7 emergency categories, blocks AI + supplement recs. |
| Supplement matching logic | Real | `calculateSupplementScore` (`health-pilot-backend`) | Eligibility + weighted symptom/goal/biomarker scoring. |
| Quiz content | Real | `health-pilot-backend` | Dynamic, versioned, i18n (en-GB / es-ES / de-DE). |
| Webhooks (platform ↔ HealthPilot) | Real | `health-pilot-backend` | HMAC-SHA256 with a delivery ledger. |
| HealthPilot brand-token engine | Real (not persisted) | `src/lib/brand/tokens.ts`, `embed-provider.tsx`, `src/components/owner/branding-studio.tsx` | Sanitised hex/font/radius/logo, color-mix palette, WCAG on-color. Live `/embed-preview` + copy-paste snippet. **Config is NOT persisted — "the snippet IS the configuration."** |
| Public per-clinic landing page | Demo-only | Fields exist in `Clinic`; editor unwired (`clinic-settings.homepage.tsx` redirects to Branding) | `_app.index.tsx` unconditionally redirects to `/login` or `/dashboard`. Premium landing is the separate Harborview GitHub Pages SPA, not in-product. |
| Supplement commerce funnel | Partial (matching only) | `supplementsEnabled` toggle in schema/config; `SupplementMatch.status` flips in `health-pilot-backend` | No catalogue module, no route, no cart/checkout/dropship. Commerce is affiliate-stub level (click/purchase recording). |
| Live payments | Needs-Felix | `medusa/` Ryft module; Ryft client | Real client but points at `sandbox.ryftpay.com`. Needs live creds + KYB/KYC + `ryftChargesEnabled` flip. Clinic stuck in `DRAFT` until then. |
| Build / tests (HealthPilot FE) | Real | `feat/whitelabel-luxury` | `next build` passes; 163/176 tests pass. 13 failures are pre-existing intake-wizard tests unrelated to white-label. |

---

## 4. The three go-live gaps

### Gap 1 — Public per-clinic landing page

**What's missing:** In the real app, `_app.index.tsx` unconditionally redirects to `/login` or `/dashboard`, so there is no public marketing page for a clinic. The homepage fields (`homepageEnabled`, `homepageExternalUrl`, `heroTitle`, `heroSubtitle`, `heroImageUrl`, `showServicesSection`, `showTrustSection`) already exist on the `Clinic` model, but the editor was deliberately unwired: `clinic-settings.homepage.tsx` redirects to Branding with a comment noting it is "fully built but never wired... avoid exposing an untested surface at go-live." The premium landing Jesse has been reviewing is the standalone Harborview GitHub Pages SPA, not the product.

**Pure code vs needs-Felix:** 100% pure code. No external dependency.

**Recommended approach:** Wire the existing homepage fields end-to-end rather than inventing a new surface. (a) Add a public branch in `_app.index.tsx`: when `homepageEnabled` is true for the resolved clinic, render the landing instead of redirecting; when `homepageExternalUrl` is set, honour it. (b) Re-enable the already-built `clinic-settings.homepage.tsx` editor behind the same `CLINIC_ADMIN_ALLOWED_FIELDS` whitelisting used everywhere else, and QA it before exposing. (c) Port the Harborview design into a real landing component that reads brand tokens from `contexts/clinic-brand.tsx`, so the page inherits each clinic's brand automatically. This keeps the Clinic as the single source of truth and reuses the field schema that already ships.

### Gap 2 — Supplement funnel

**What's missing:** Only a `supplementsEnabled` boolean exists in schema/config. There is no supplement catalogue module, no supplement route, no cart/checkout/dropship in Medusa or the frontend. HealthPilot's backend has real supplement *matching* (`calculateSupplementScore`), but commerce is affiliate-stub level: it records clicks/purchases by flipping `SupplementMatch.status`, with no real SKUs, cart, checkout, or fulfilment.

**Pure code vs needs-Felix:** Catalogue + funnel + cart/checkout wiring is code we can build. Dropship *fulfilment* and *live payment capture* need Felix and an external provider.

**Recommended approach:** Build the catalogue as Medusa v2 products (Medusa is already in the monorepo) so SKUs, pricing, and cart/checkout come from an existing, battle-tested commerce engine rather than a bespoke store. Surface the matched supplements from `calculateSupplementScore` as a real product route in the frontend, mapping each `SupplementMatch` to a Medusa SKU. Keep checkout on the same Ryft payments module the rest of the platform uses, so payment go-live (Gap 3) unlocks supplements automatically. Leave the dropship/fulfilment handoff as a clean integration seam for Felix to connect to a fulfilment partner API.

### Gap 3 — Payments go-live

**What's missing:** The Ryft client is real but points at `sandbox.ryftpay.com`. Live payments require live Ryft credentials, Ryft Connect KYB/KYC completion, and the `ryftChargesEnabled` webhook flip. Until then a clinic stays in `DRAFT` and cannot take real money.

**Pure code vs needs-Felix:** Needs Felix + external (Ryft). The code path exists.

**Recommended approach:** No new architecture. Felix provisions live Ryft credentials, completes Ryft Connect KYB/KYC per clinic, and confirms the `ryftChargesEnabled` webhook transitions the clinic from `DRAFT` to `LIVE`. Verify with a real low-value transaction on a single pilot clinic before flipping others.

---

## 5. Felix integration checklist (external providers)

These require credentials, contracts, or infra only Felix can provision. Field/env names are given where the audit surfaced them.

| Item | Config field / env var | Notes |
|---|---|---|
| Live Ryft payment credentials | `ryftApiKey` | Currently sandbox; swap for live key. |
| Ryft Connect KYB/KYC + charge enablement | `ryftChargesEnabled` (webhook-driven) | Gates `DRAFT` → `LIVE`; per-clinic compliance. |
| Supplement dropship / fulfilment partner API | *(new integration seam)* | Needed for Gap 2 fulfilment; not yet wired. |
| Custom domain DNS / SSL provisioning | `domainVerified`, `sslProvisioned` | Backs custom-domain tenant resolution. |
| Wearable device APIs (Terra) | *(env TBD)* | For wearable ingestion. |
| Managed Postgres + Redis | *(connection env)* | Production data + cache/queue infra. |
| Live OpenAI key | `AI_PROVIDER` (set to live provider; `stub` for CI) | HealthPilot AI runs `gpt-4o`. |
| Embed origin allow-list | `EMBED_ALLOWED_ORIGINS`, `VITE_HEALTHPILOT_URL` | Origin-pins the HealthPilot iframe + postMessage. |
| Per-clinic HealthPilot API key | `healthPilotApiKey` | Encrypted at rest; used for server-side summary export. |
| Notification / verification transport | SendGrid, Onfido, notification keys *(env TBD)* | Email, identity verification, notifications. |

---

## 6. Recommended deploy order / sequencing

1. **Provision infra first (Felix).** Managed Postgres + Redis, live OpenAI key (`AI_PROVIDER`), SendGrid/Onfido/notification keys. Nothing else runs reliably in production without these.
2. **Lock the embed and domains.** Set `EMBED_ALLOWED_ORIGINS` and `VITE_HEALTHPILOT_URL`, provision custom-domain DNS/SSL (`domainVerified`, `sslProvisioned`) so tenant resolution works on real hostnames.
3. **Wire brand inheritance.** Confirm the Clinic forwards its brand tokens into the HealthPilot embed via `hp:init` / `data-hp-*`, so HealthPilot inherits the clinic brand and needs no store of its own. This closes the persistence gap without new storage.
4. **Ship Gap 1 (landing page).** Pure code: wire `_app.index.tsx` + the existing homepage editor, port the Harborview design onto brand tokens. QA the previously-unwired surface before exposing.
5. **Ship Gap 2 catalogue (code portion).** Build the supplement catalogue on Medusa v2 and the frontend supplement route, mapping `SupplementMatch` results to SKUs, checkout on the shared Ryft module. Leave the fulfilment seam stubbed.
6. **Payments go-live (Gap 3, Felix).** Swap `ryftApiKey` to live, complete Ryft Connect KYB/KYC, confirm the `ryftChargesEnabled` webhook flips a pilot clinic `DRAFT` → `LIVE`. Test with one real low-value transaction.
7. **Connect fulfilment + wearables last.** Wire the dropship/fulfilment partner API into the Gap 2 seam and the Terra wearable APIs once transactional core is proven live.
8. **Pilot then roll out.** Take a single pilot clinic fully live, verify payments, quiz, brand, and landing end-to-end, then enable the rest.
