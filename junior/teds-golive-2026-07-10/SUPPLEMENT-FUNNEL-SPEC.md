# Supplement Funnel — Implementation Spec (go-live gap #2)

Implementation-ready design to build the supplement upsell funnel INTO the
platform at the same standard as the TRT/ED commerce, reusing what already
exists. Scope split explicitly into **code we build** vs **Felix connects**.

Business model and partner research already done: see
`workspace/docs/2026-07-09-teds-supplement-operating-model.{md,pdf}` (merchant-
of-record + blind dropship own-label; platform takes an override on every
clinic's supplement sales). Regulatory guardrails there are load-bearing —
firewall the supplement lane from TRT prescribing; permitted GB NHC claims only.

## What already exists (do not rebuild)

- **Matching brain** (HealthPilot backend, `services/supplement` + `matching`):
  `calculateSupplementScore` scores supplements against the intake + bloods with
  real eligibility gates. This produces the *recommendation*; it does not sell.
- **Commerce spine** (sandbox `medusa/` + Ryft module): real catalogue, cart,
  orders and Ryft payments already power TRT/ED checkout. Reuse it.
- **Per-clinic economics**: `Clinic.platformFeePercent` + Ryft sub-accounts
  already split money platform↔clinic. The supplement override rides the same rail.
- **The toggle**: `Clinic.supplementsEnabled` already exists and is surfaced in
  `getPublicConfig`. The landing page (built this session) already shows a
  "Clinician-matched supplements" service card when it is on.

## What to build (code we own)

### 1. Catalogue — per-clinic supplement products
Represent supplements as **Medusa products** (SKU, price, inventory, subscription
option) in a dedicated `supplements` sales channel / product category, so they
reuse cart + Ryft + order lifecycle. Curate per clinic with a thin server table:

```
// server/prisma/schema.prisma  (tenant-scoped via existing AsyncLocalStorage)
model ClinicSupplement {
  id                String   @id @default(cuid())
  clinicId          String
  medusaProductId   String   // variant/SKU in Medusa
  displayName       String
  retailPriceGBP    Decimal  @db.Decimal(10,2)  // clinic's chosen retail (>= MAP)
  subscriptionEligible Boolean @default(true)
  active            Boolean  @default(true)
  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt
  @@unique([clinicId, medusaProductId])
  @@index([clinicId, active])
}
```
Plus a NestJS domain module `server/src/domain/supplements/` mirroring
`domain/health-quiz/`: `supplements.service.ts`, `supplements.controller.ts`,
DTOs, tenant-scoped repo. Admin CRUD for the clinic to curate its stack;
public `GET /clinic/supplements` (active only) for the funnel.

### 2. Recommendation link — quiz/bloods → clinic catalogue
On the existing signed HealthPilot summary webhook (`health-quiz-webhook.service`),
map HP's recommended supplement identifiers → this clinic's `ClinicSupplement`
rows and persist a `SupplementRecommendation` (per intake/patient) with the
clinical reason string (already produced by HP). Surfaced as "Recommended for
you" on the patient dashboard and on the public results screen — the care-plan-
not-store framing from `project_harborview_demo` (monthly-led pricing, one
recommended protocol, transparent opt-out subscribe, NO buyer/revenue language
on patient surfaces).

### 3. Basket + checkout — reuse the commerce spine
Add a supplement cart flow (patient portal + public results) on the existing
Medusa cart + Ryft hosted checkout. Subscribe-and-save = Medusa subscription /
scheduled order. No new payment code; it is the TRT/ED path with supplement line
items. Platform override applied via `platformFeePercent` on the split.

### 4. Fulfilment — a clean adapter seam (this is Felix's plug)
Define an interface and inject it, so the funnel is real end-to-end in code and
Felix only drops in credentials + the supplier's transport:

```
// server/src/domain/supplements/fulfilment/fulfilment-provider.ts
export interface FulfilmentProvider {
  createOrder(input: FulfilmentOrder): Promise<{ providerOrderId: string }>;
  getStatus(providerOrderId: string): Promise<FulfilmentStatus>;
  // inbound shipment/tracking webhook -> normalized event
  parseWebhook(req: RawWebhook): FulfilmentEvent;
}
```
Ship a `NoopFulfilmentProvider` (logs + marks pending) as the default so the
whole funnel runs in the sandbox without a live supplier. Felix implements
`DropshipFulfilmentProvider` against the chosen UK partner (Specialist
Supplements / Amrita — outreach already sent, see `project_healthpilot_supplements`).

## What Felix connects (external — cannot be coded now)
- Dropship supplier **API credentials + transport** (CSV/middleware bridge if no
  API), behind `DropshipFulfilmentProvider`.
- **Live Ryft** for supplement charges (same go-live as TRT/ED: live keys +
  KYB/KYC + `ryftChargesEnabled`).
- Real **product data + inventory** seeded into Medusa (SKUs, MAP, images).
- FBO registration / own-label compliance sign-off (business, not code).

## Build order
1. Prisma `ClinicSupplement` + migration; Medusa `supplements` category + seed a
   couple of demo SKUs.
2. `domain/supplements` module (admin CRUD + public read) + tenant scoping tests.
3. Recommendation mapping on the HP webhook + "Recommended for you" surfaces.
4. Cart/checkout wiring on the Medusa+Ryft spine; subscribe-and-save.
5. `FulfilmentProvider` interface + `NoopFulfilmentProvider`; wire order → fulfilment.
6. Hand `DropshipFulfilmentProvider` + live keys to Felix.

Estimate: steps 1–5 are ~1–2 focused build sessions (all verifiable in the
sandbox with the Noop provider). Step 6 is Felix + supplier lead time.
