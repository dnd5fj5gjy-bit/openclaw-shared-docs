# HealthPilot AI-Logic Upgrade — Build Plan
Date: 2026-07-12 · Read-only design (agent a1d9ee36). Drives Jesse's AI workstream: smarter recommendations, API cost savings via "if functions", Dr AI support, patient personalization. CONFIDENTIAL/local.

## Key findings
- ALL LLM spend is in **health-pilot-backend** (th-whitelabel server has ZERO LLM calls). 9 gpt-4o call sites via AIProviderFactory (`AI_PROVIDER=openai|stub`). Anthropic is a name-constant only — no impl (provider choice = Jesse/Felix decision).
- **Biggest waste:** detail-page calls (#3 supplement-plan, #4 provider-plan, #5 symptom-category-plan, #6 explanation) fire PER VIEW, UNCACHED, with deterministic inputs. Caching = 60-85% of detail-page spend. Highest ROI.
- Guaranteed per intake: #1 analyzeHealth (biggest single call, ~1.5-2k static system prompt) + #2 rerank.
- **Funnel unwired** (= our biggest functional weakness): `recommended-solutions` emits `supplementMatches[].slug`, `summary-export` ships it, but NOTHING calls `syncRecommendationsFromSlugs` -> clinic reco funnel has no live input. Stage 1 fixes this.
- Strong deterministic assets already exist to build on: red-flag gate (regex, i18n, server-side), age gate (fail-closed), calculateSupplementScore, `buildIntakeScoringContext` (613-line weighted domain scoring - the "thinking" foundation, currently only feeds LLM prompt), matching.service (deterministic), finalizeClinicianBrief (Dr-AI safety spine), cacheOrFetch (Redis, used for ref data, NEVER for LLM).

## Target architecture: 4-layer pipeline, deterministic "if" layer in front of every LLM call
- L0 SAFETY GATE (detectRedFlags + isUnderMinimumAge) — blocking, deterministic, upstream of everything. No cost lever can reach it.
- L1 DETERMINISTIC ENGINE (no LLM): buildIntakeScoringContext + calculateSupplementScore v2 + NEW treatment-eligibility rules -> ranked candidates + confidence + "obvious?" verdict.
- L2 ROUTER (NEW `ai-router.service.ts`, single chokepoint): obvious/high-confidence -> short-circuit (template, no LLM); ambiguous -> cache lookup -> model-tier (mini vs 4o) -> schema-validate.
- L3 OUTPUT: schema validation + finalizeClinicianBrief overrides + red-flag re-detect + persist -> emit slugs -> syncRecommendationsFromSlugs.

## Cost levers (verify OpenAI pricing before quoting numbers)
- A. CACHE detail-page calls #3-6 keyed (id+intakeId+model+promptVersion) -> 60-85% detail spend. LOW risk. SHIP FIRST.
- B. MODEL-TIER to gpt-4o-mini for explanations/OCR/detail pages -> ~90%/call. MED risk (needs eval). Flagged, provider choice = Jesse.
- C. DETERMINISTIC SHORT-CIRCUIT: skip #2 rerank on high-confidence single-domain no-blood intakes -> eliminates #2 on 30-50%. LOW-MED.
- D. PROMPT SLIM: buildBaseSystemPrompt ~1.5-2k tok every call #1; wire unused AI_TASK_CONFIG max_tokens (stop defaulting 4096) -> 15-30% input on #1. LOW.
- E. OpenAI prompt-prefix caching (stable prefix ≥1024 tok, ~50% input discount). LOW. Stacks with D.
- F. BATCH pre-generate top-N detail pages on completion (shifts cost, guarantees cache hits). LOW.

## Staged build (smallest-highest-value first). Repo per stage. Safety non-negotiable throughout.
- S0 INSTRUMENTATION (hp-backend): ai-usage.service.ts logging {task,model,tokens,cachedHit,intakeId,clinicSlug} at all 9 sites. Measure first.
- S1 WIRE FUNNEL (hp-backend + th-whitelabel) = our backlog item A: emit `recommendationSlugs[]` on summary.ready; th-whitelabel webhook consumer calls syncRecommendationsFromSlugs. Make supplement-funnel.integration.spec pass e2e. No LLM/PHI change.
- S2 CACHE detail calls (hp-backend, Lever A): wrap #3-6 in cacheOrFetch + CACHE_KEYS incl promptVersion. Huge win, low risk.
- S3 ROUTER + PROMPT SLIM (hp-backend, D/E): ai-router.service.ts chokepoint; slim system prompt; wire AI_TASK_CONFIG; stable prefix. Golden-fixture regression.
- S4 SHORT-CIRCUIT + TIERING (hp-backend, B/C): router selectModel + isObviousCase; EVAL HARNESS required; flag AI_ROUTER_TIERING=off default. Needs Jesse sign-off on mini quality + provider choice. Test: flagged intake never builds a router request.
- S5 RECO ENGINE v2 (hp-backend, Ask 1): rewrite calculateSupplementScore (weighted evidence-graded, explainable rationale[]) + NEW treatment-eligibility.service.ts (treatment-agnostic config rules: trt/hair_loss/weight_loss/peptides/blood_panel -> {eligible,confidence,requiredNextStep,blockingReasons,rationale}). Eligibility = additive gates never relaxations.
- S6 DR AI (hp-backend, Ask 3): extend clinician-brief.service — triage priority (risk bucket+red-flag), draft consult notes (LLM drafts, finalizeClinicianBrief authoritative, containsDiagnosticLanguage guard), history/wearables summary. Doctor reviews not authors.
- S7 PATIENT PERSONALIZATION (hp-backend + FE contract, Ask 4): patient-guidance.service — "why these recs" from S5 rationale (optional mini polish), education, progress nudges. Gated by diagnostic-language + health-claims-lexicon filters; blocked for flagged/underage. "Information not diagnosis".

## Reco-algo spec (implementable) — see agent output; core:
Hard eligibility gate (keep isEligible incl conditions/meds UNKNOWN fail-closed) -> weighted match (symptom Σsev×conf×20, goal prio×25, biomarker abnormal30/target15, scoringContext ±15/exclude, evidence bonus only if base>0) -> normalize 0-100 + rationale[] -> LLM rerank advisory only (40/60 blend, deterministic floor). Treatment layer declarative config so new treatments = data not code.

## OPEN QUESTIONS for Jesse/Felix (surface at next milestone):
1. Provider: stay OpenAI + gpt-4o-mini tiering, OR add real Anthropic/Claude provider (Haiku cheap / Sonnet reasoning)? Router built provider-agnostic either way. [Note: house guidance favors Claude for new AI apps, but this is Jesse/Felix's call - it's an existing OpenAI system.]
2. Confirm current OpenAI pricing before quoting savings %.
3. gpt-4o-mini quality bar acceptable for explanations/detail pages (pending eval)?
4. PHI-to-LLM: OpenAI DPA in place? Caching LLM outputs keyed on intake data + any new provider must respect consent/DPA.
5. Wearables: source/schema, live or roadmap? (S6/S7 reserve a slot, don't build ingestion until answered.)
6. Which th-whitelabel service receives summary.ready webhook (for S1 landing point)?
7. Detail-page cache TTL/invalidation (1hr ok? invalidateSupplementsCache hook exists).

## S1 CONTRACT (SHIPPED — backend sender half) — `recommendationSlugs`
The `summary.ready` webhook now carries the supplement funnel input. The platform-side `syncRecommendationsFromSlugs` consumer must match this exactly:
- **Field:** `recommendationSlugs`
- **Type:** `string[]`
- **Event:** `summary.ready` (webhook `data.recommendationSlugs`)
- **Semantics:** de-duplicated, rank-ordered supplement slugs (highest-ranked first) from `recommendedSolutions.supplementMatches[].slug`. Always present. `[]` when there are no matches.
- **Safety:** flagged / underage intakes throw upstream of the emit (intake-summary.service ~L553) and never fire `summary.ready`, so slugs are only ever populated for eligible intakes; the list can only be empty for them.
- **Parity channel:** the GET summary-export pull payload (`SummaryExportPayload`) also carries `recommendationSlugs: string[]` (same derivation), so the platform can read slugs from either the webhook or the pull.
- Source: `extractRecommendationSlugs()` in `src/services/intake/summary-export.service.ts`.

## S3 STATUS (PARTIAL — landed the safe half, deferred the risky half)
Landed:
- `src/services/ai/ai-router.service.ts` — single chokepoint every one of the 9 LLM chat-completions now routes through (analyzeHealth, generateExplanation, analyzeImage, generateReport, rerank, the 3 plan-detail services, blood-test interpretation). Pure pass-through: it owns the provider call + the S0 usage-emit; behaviour/outputs byte-identical. It does NOT cache (S2 stays at service level; router only runs on a cache miss, always cachedHit:false) and does NOT pick models/short-circuit. This is the clean seam **S4 (tiering/short-circuit) plugs into** — add `selectModel()` / `isObviousCase()` in the router; a flagged intake already never reaches it (gate throws upstream). `resolveTaskMaxTokens(task)` reads per-task budgets from `AI_TASK_CONFIG`.
- Per-task `max_tokens` wiring: the 5 detail/rerank/explanation literals now come from `AI_TASK_CONFIG` (values codified to the de-facto budgets; identical on the wire).

DEFERRED (logged, not shipped):
- **Aggressive prompt-slim of `buildBaseSystemPrompt`** and the **`AI_PROMPT_VERSION` v1->v2 bump**. Reason: the acceptance bar is "summary-quality unchanged via golden-fixture regression", which needs live-provider output to verify. This environment has no outbound/creds, so quality cannot be validated, and the base prompt's boilerplate is largely SAFETY spine (red-flag severity rules, injection delimiters, non-diagnostic register) that must not be trimmed blind. AI_PROMPT_VERSION stays 'v1' (no prompt change => no S2 cache bust). Prefix-caching (Lever E) note: the base system prompt is already a stable, byte-identical prefix for default-locale traffic (buildOutputLanguageInstruction returns '' for en-GB and is appended only for non-default locales), and system-message-first ordering is already in place — so same-locale traffic already gets the prefix-cache discount without restructuring.
- max_tokens REDUCTION on analyzeHealth (still config.openai.maxTokens = 4096) — the actual Lever D saving. Same reason: needs an eval to confirm no truncation of the large combined summary payload.

## SAFETY NON-NEGOTIABLES
L0 red-flag+age stays deterministic/server-side/upstream of all cost+routing (S4 adds a test enforcing no cost lever reaches it). LLM outputs schema-validated. Prompt-injection delimiters preserved. Personalization gated by diagnostic-language + claims filters. Cost-saving NEVER bypasses a gate.
