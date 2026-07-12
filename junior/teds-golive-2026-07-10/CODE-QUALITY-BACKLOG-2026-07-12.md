# Code-Quality / Perf / Coverage Backlog — th-whitelabel-sandbox @ feat/supplement-commerce
Date: 2026-07-12 · Read-only survey (agent a955483b). Excludes security audit findings, the any-sweep, the 2 test/eslint items.

## Top items (ranked)
1. **[FUNCTIONAL GAP - biggest] Recommendation funnel has NO production input.** `syncRecommendationsFromSlugs`
   (supplements.service.ts:208) is the ONLY creator of `PatientSupplementRecommendation`, and it's referenced only by
   tests. `health-quiz.service.ts` storeResult (hp:completed ingestion ~L467-573) never calls SupplementsService. => the
   "Recommended for you" UI, analytics funnel, seeded recs will all be EMPTY in prod. Effort M. NEEDS DECISION: wire into
   health-quiz results ingestion, but only once HealthPilot summary-export actually EMITS supplement slugs (sender may not
   yet). Confirm both ends (likely a Felix/HealthPilot-side item).
2. **[CORRECTNESS] Order line snapshot stores mixed units.** supplements.service.ts:384-395: `retailPricePence` per-UNIT
   but `tradeCostPence`/`marginPence` per-LINE-TOTAL. Integration test (supplement-funnel.integration.spec.ts:214-221)
   wrongly asserts the mismatch as correct. Order-level totals happen to be right, so latent. Any per-line consumer
   (invoice/refund/dispute) gets nonsense. Effort S, fix code + test together; guard legacy rows.
3. **[PERF] Missing indexes for analytics.** groupBy(['supplementProductId']) (service.ts:560) unindexed; every
   SupplementFulfilmentOrder query bounds on createdAt with no index. Add `@@index([clinicId, supplementProductId])` on
   PatientSupplementRecommendation and `@@index([clinicId, createdAt])` on SupplementFulfilmentOrder. Add NOW (empty tables
   = free lock); later needs CREATE INDEX CONCURRENTLY. Effort S.
4. **[SCHEMA SAFETY] New models: missing FK / dangling id / wrongly-nullable / cascade conflict.**
   - SupplementFulfilmentOrder.patientId (schema.prisma:3204) bare String, NO FK (sibling rec model has one) -> orphaned orders.
   - healthQuizResultId Int? (3179) dangling, no relation.
   - clinicId String? nullable on all 3 new models (3136,3171,3202) though service refuses null -> should be NOT NULL.
   - PatientSupplementRecommendation.product onDelete:Cascade (3184) vs deactivateProduct soft-delete -> hard delete wipes
     history. Prefer Restrict/SetNull. Effort M. Confirm order-FK omission isn't a deliberate financial-retention choice.
5. **[DUPLICATION] Staff-analytics scaffolding copy-pasted 3x** (analytics.supplements.tsx <-> analytics.health-quiz.tsx <->
   analytics.trt.tsx): searchSchema, STAFF-gate beforeLoad, formatCount, quickRanges, stat-tile grid, funnel bars. Extract
   `staffAnalyticsBeforeLoad` + <QuickRangePicker>/<StatTile>/<ProportionBar>. Effort M.
6. **[COMPLEXITY] SupplementsService = 670-line 5-concern God-service.** Split into Catalogue/Recommendation/Fulfilment/
   Analytics services. Effort M, lower urgency. (Worst overall are pre-existing/out-of-scope: ecommerce.service.ts 2409,
   reports.service.ts 2370, platform-admin.service.ts 1879.)
7. **[DEPS] Vuln counts high.** npm audit: frontend 36 (3 critical/18 high); server 68 (4 critical/25 high). Triage
   criticals individually; do NOT blanket `audit fix --force` on a go-live branch (major Vite/Nest/Medusa bumps risky).
   NEEDS DECISION.
8. **[DEAD CODE] quick wins.** `placeFulfilment` (service.ts:330) orphaned - remove/fold. Drop module-internal `export`s
   (EmbedFontKey/EmbedThemeSource/EmbedTheme/HealthPilotEmbedProps in HealthPilotEmbed.tsx; SupplementProductWithStock in
   supplements.ts). Effort S. (Do NOT delete syncRecommendationsFromSlugs - unfinished, not dead.)
9. **[DUPLICATION] Money helpers fragmented.** penceToPounds/poundsToPence identical in clinic-settings.supplements.tsx:64-73
   and clinic-settings.pricing.tsx:156-165; formatPence (supplements.ts:182-194) is a 4th GBP formatter. Consolidate into
   lib/utils/price.ts. Effort S.
10. **[RESILIENCE/BUG] Order/storefront path.** dashboard/supplements.tsx:142 recommended cards never get `stock` -> OOS
    recommended item still shows "Add to basket" (minor bug). listOrdersNeedingReview (service.ts:624) findMany no take ->
    unbounded queue. FulfilmentProvider interface has no timeout/retry/AbortController contract (forward-looking for Amrita
    HTTP). Effort S each.

## Coverage gaps
- No controller-level tenant-isolation test for supplement endpoints (isolation proven via Prisma extension in audit, but no
  supplement-specific test). M.
- Margin-unit test validates a BUG (#2). createFulfilmentOrder payment-gate untested (= security #1).

## Accessibility (new UI) - largely clean (labels, aria, aria-hidden present). Small: ClinicHomepage inkSoft 0.72 alpha +
0.24em uppercase eyebrows can fail AA on adverse palettes (add contrast floor like the CTA band's readableOn); "Not linked
to checkout yet" badge text-[10px] text-amber-600 likely fails AA.

## Quick wins to batch (safe, mechanical)
Remove placeFulfilment + unneeded exports; consolidate money helpers; add the 2 indexes (empty tables); pass stock to
recommended cards; contrast floor on inkSoft/eyebrow + fix amber badge; flip 3 clinicId String? -> NOT NULL.

## DO-NOT-TOUCH / risky
- Do NOT delete syncRecommendationsFromSlugs (unfinished funnel input, wire it).
- Do NOT fix margin snapshot by only editing the assertion (change persisted shape + test together; guard legacy rows).
- Do NOT blanket npm audit fix --force on go-live branch.
- Do NOT add indexes non-concurrently once tables grow.
- Do NOT change onDelete:Cascade without checking soft-delete guarantee; confirm missing order->patient FK isn't deliberate.
- Leave tenant-isolation layer, webhook HMACs, postMessage origin-pinning alone (verified good).
