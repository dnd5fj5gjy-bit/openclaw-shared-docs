# Amazon FBA Automation Catalog — Jim Reed Brands
**Brands:** Newgate World, London Mole Eyewear, Funkstar Hardware  
**Date:** 2026-03-26  
**Audience:** Felix / engineering handoff

## Executive summary
The highest-ROI automations are the ones that push more qualified traffic into hero ASINs while protecting stock and margin: auto-built Sponsored Products structures, placement-aware bid/budget rebalancing, top-of-search rules, review-driven copy/keyword loops, and promo scheduling. Start with **Newgate** because the catalogue is search-led, visual, and easier to scale on Amazon; roll the same stack into **Funkstar** next; keep **London Mole** selective around proven reading-glasses SKUs. Build the system as a thin decision layer on top of Amazon Ads API + SP-API + a small warehouse, with manual approval for write-backs in phase 1. Priority is sales lift first, cost control second.

## Prioritized automation opportunities

| Opportunity | Impact | Effort | Dependencies |
|---|---|---|---|
| Auto-campaign builder for new/live hero ASINs | H | S | Ads API credentials, ASIN master, keyword seeds |
| Auto-bid & budget rebalancer with placement logic | H | M | Ads API reporting/write access, target ACOS/ROAS, stock feed |
| Top-of-search rule engine | H | S | Placement reports, stock cover thresholds |
| Search-term harvesting + negation automation | H | M | Ads reports, query mapping, approval workflow |
| Review sentiment detection feeding ads/listings | H | M | Public review capture or exported reviews, NLP pipeline |
| Coupon/discount scheduler | H | M | Promotions data, seasonal calendar, margin floors |
| Bundling & cross-sell automation | M/H | M | Catalogue graph, Brand Store/PDP mapping, bundle rules |
| DTC sync and Amazon demand-to-site optimization | M/H | M | Shopify/DTC data, attribution model, product mapping |
| Inventory & FBA inbound automation | M/H | M | SP-API credentials, lead times, MOQ/carton metadata |
| Repricer with floor/ceiling and stock-age logic | M | M | Pricing feed, margin data, competitor snapshots |
| Returns & A-to-Z issue triage automation | M | M | Returns/cases export, templates, escalation paths |
| Refund detection & stock recovery | M | M | Finance events, return status, reconciliation logic |
| Customer service auto-responses with escalation | M | S/M | Case feed, templates, policy guardrails |

## Detailed automation patterns

| Pattern | Inputs | Outputs | Triggers | Rule examples | Required APIs / endpoints | Data needed (fields) | Compliance notes |
|---|---|---|---|---|---|---|---|
| **Ads automation: auto-campaign builder** | ASIN, SKU, brand, title, bullets, category node, price, hero flag, seed keywords, competitor ASINs | Draft or live campaigns, ad groups, keyword lists, product targets, negatives, default bids | New ASIN goes live; existing ASIN tagged `launch_pending`; weekly refresh for missing campaign coverage | Create 4-pack structure per hero ASIN: auto, exact, phrase, product-targeting. Set launch budgets by price band; if Newgate wall clock > £45, start higher TOS multiplier than bedside alarm clocks. | Amazon Ads API: campaign/adGroup/keyword/productTarget create + report endpoints; internal `POST /amazon/campaigns/generate`, `POST /amazon/campaigns/apply` | asin, sku, brand, title, bullets, search terms, browse node, price, margin band, default bid curve, competitor asins | Requires Ads API credentials; human approval advised before first write-back; avoid trademarked competitor keywords in copy. |
| **Ads automation: DSP rule-bidding** | Audience performance, view-through conversions, PDP visit pools, Brand Store traffic, seasonality tags | Bid multipliers, line-item budget shifts, audience inclusion/exclusion changes | Daily or intraday performance job; event window before gifting/weather periods | If Funkstar weather audience CTR > target and CVR positive, increase audience bid 10%; if assist-to-spend ratio weak for 7 days, cut budget 15%. | Amazon DSP API or managed DSP export ingestion; internal `POST /amazon/dsp/bids/recommend` | audience_id, spend, impressions, clicks, detail_page_views, purchases, NTB ratio, view-through conv, season tag | DSP access required; privacy-safe audience usage only; no off-policy customer-level targeting. |
| **Ads automation: auto-bid & budget rebalancer** | Daily keyword/target metrics, stock cover, margin band, target ACOS/ROAS | Bid changes, campaign budget increases/decreases, pause/resume list | Daily scheduled run; emergency run on spend spike | If ACOS < target by 20% and stock cover > 35 days, raise bid 12%; if spend > 2x order value with zero orders in 14 days, pause target; if low stock < 21 days, reduce budget 30%. | Amazon Ads API reports + mutation endpoints; internal `POST /amazon/bids/recommend`, `POST /amazon/bids/apply` | campaign_id, ad_group_id, keyword_id, target_id, spend, sales, orders, acos, roas, cvr, cpc, ctr, stock_days_cover | Keep approval gate in phase 1; rate-limit writes; maintain audit log for every change. |
| **Ads automation: top-of-search rules** | Placement-level performance, stock cover, review count/rating, margin band, event calendar | Placement multipliers by campaign/ad group | Daily run; event-based boost before Prime-style or gifting windows | If top-of-search CVR > rest-of-search CVR by 30% and ACOS within target, raise TOS multiplier from 35% to 55%; if stock at risk or returns spike, cut TOS modifier. | Amazon Ads API placement reports; internal `POST /amazon/placements/recommend` | placement_type, placement_spend, placement_sales, placement_orders, stock_days_cover, review_rating, season tag | Requires Ads API reporting granularity; throttle changes to avoid oscillation. |
| **Repricer logic** | Current offer price, min margin floor, competitor observed price band, Buy Box status, stock age, sales velocity | Recommended or applied price change, coupon alternative suggestion | Daily run; immediate on Buy Box loss or aged stock trigger | If Buy Box lost and competitor within 3-5%, reduce price within floor; if aged stock > 120 days and CVR stable, prefer coupon over base price cut; if hero Newgate SKU has strong TOS ROAS, hold premium. | SP-API Product Pricing / Listings Items / Notifications where available; internal `GET /amazon/repricing/recommendations` | asin, sku, current_price, min_price, max_price, cogs, fees, contribution_margin, buy_box_status, inventory_age_days | Seller Central/SP-API required; must respect MAP/brand strategy; no race-to-bottom automation without floor controls. |
| **Inventory & FBA inbound automation** | On-hand inventory, reserved, inbound, sell-through, lead time, MOQ, carton dims, seasonality | Replenishment recommendations, reorder date, shipment draft, alerts | Daily forecast job; immediate on stockout-risk threshold | If Funkstar umbrella cover < 28 days during rainy season and lead time 35 days, generate reorder now; if London Mole style velocity low and returns high, block reorder. | SP-API FBA Inventory, inbound/replenishment endpoints; internal `GET /amazon/replenishment/recommendations`, `POST /amazon/inbound/draft` | asin, sku, fnsku, available_qty, reserved_qty, inbound_qty, sell_through_30d, lead_time_days, moq, carton_qty, dimensions | SP-API credentials required; no logged-in scraping; validate shipment rules and hazmat/prep constraints manually at first. |
| **Automated coupon / discount scheduling** | Margin floors, event calendar, stock age, competitor coupon snapshots, ad performance | Coupon schedule, deal recommendation, off/on toggle list | Weekly scheduler; event windows; aged inventory threshold | Turn on 5-10% coupon for Newgate giftable hero SKUs before payday/gifting windows; trigger Funkstar compact umbrella coupon when weather spike + stock age > 60 days; avoid discounts if organic rank rising without promo. | SP-API promotions support where available plus operator action; internal `GET /amazon/promotions/recommendations`, optional create/apply endpoint | asin, sku, current_price, min_margin, inventory_age_days, seasonality flag, CTR, CVR, TACOS, competitor_coupon_flag | Promotions often need Seller Central or approved API path; keep human approval; ensure promo claims comply with Amazon policy. |
| **Review sentiment detection + targeted ads** | Public reviews or exported review text, rating, date, ASIN, topic clusters | Theme dashboard, copy suggestions, keyword seeds, negative keyword suggestions, escalation list | Daily/weekly NLP batch; alert on sudden negative-theme spike | If Newgate reviews repeatedly mention “silent”, add exact keywords and image copy; if London Mole complaints mention fit/slippage, suppress broad style traffic and push clearer PDP copy; if Funkstar praise durability, raise bids on “windproof umbrella”. | Public page capture where allowed, Brand Analytics/export ingestion, internal NLP `POST /reviews/analyze` | asin, review_id, rating, headline, body, verified_purchase, date, topic, sentiment, issue_type | Public data only unless seller export provided; do not fabricate reviews; use only aggregate insights for ad/copy decisions. |
| **Bundling & cross-sell automation** | Catalogue relationships, attachment graph, frequently bought together, margin bands, brand rules | Bundle recommendations, cross-sell widgets, product-targeting campaigns, Brand Store links | Weekly merchandising job; new SKU relation detected | Pair Newgate bedside alarms with batteries/accessories where allowed; pair Funkstar compact + stick umbrella variants in Brand Store flows; cross-sell London Mole readers by frame family only on proven return-safe styles. | SP-API catalog/listings + DTC catalog API; internal `GET /catalog/bundle-recommendations`, `POST /amazon/product-targets/generate` | asin, parent_child, category, price, rating, return_rate, attach_rate, margin_band | Bundle claims must reflect real offers; Amazon virtual bundles depend on account eligibility; avoid misleading compatibility. |
| **DTC sync and conversion optimization** | Amazon demand trends, DTC product data, sessions, conversion, email capture performance | Product/page priority list, landing page briefs, DTC retargeting audiences, stock sync alerts | Daily trend sync; weekly planning | If Amazon search demand for “silent wall clock” rises and Newgate PDP converts, prioritize matching DTC landing page and email feature; if Funkstar Amazon best-seller spikes, feature same SKU on site and paid social. | Shopify/storefront API, Ads API exports, internal `GET /channel-sync/opportunities` | asin, product_id, search_term trends, ad CVR, DTC CVR, inventory by channel, top review themes | DTC/customer data handling must follow privacy policy; keep channel attribution probabilistic, not overclaimed. |
| **Returns & A-to-Z issue triage automation** | Return reason codes, buyer messages, case type, order metadata, ASIN risk score | Suggested response draft, escalation queue, defect trend alerts | New case/return event; daily case summary | Auto-tag “damaged in transit” vs “not as described”; escalate A-to-Z, chargeback, or repeated defective-ASIN cases to human; trigger packaging QA alert if Newgate breakage exceeds threshold. | SP-API orders/returns/cases where accessible, email/helpdesk ingestion; internal `POST /cases/triage` | order_id, asin, sku, return_reason, case_type, buyer_message, delivery_issue_flag, refund_amount | Do not auto-send unsupported claims; human review for A-to-Z and policy-sensitive cases. |
| **Refund detection & stock recovery** | Financial events, return status, warehouse reconciliation, disposal/removal status | Missing-refund alerts, reimbursement claim queue, stock recovery opportunities | Daily reconciliation job | If return marked received but no sellable stock or reimbursement after threshold, queue claim; if unsellable recoverable units rise, recommend removal/rework. | SP-API Finances, FBA Inventory, reimbursements/returns feeds; internal `GET /finance/refund-recovery` | order_id, shipment_id, return_received_date, reimbursement_status, disposition, quantity, fee_type, amount | Requires SP-API finance access; claims should be operator-reviewed before submission. |
| **Customer service auto-responses with escalation** | Buyer message intent, order status, policy templates, risk flags | Draft replies, SLA queue, escalation tags | New buyer message; after-hours queue | Auto-draft “where is my order” using shipment status; escalate refund/legal/threatening tone; send safe FAQ replies for sizing/compatibility only when confidence high. | Buyer-Seller Messaging or helpdesk integration; internal `POST /support/draft-response` | message_id, order_id, asin, buyer_intent, shipment_status, confidence_score, policy_tag | Human approval required before sending if channel/policy risk exists; do not impersonate unsupported guarantees. |

## Top 6 automation implementation specs for Felix

### 1) Hero-ASIN campaign generator
- **Goal:** Ensure every approved hero ASIN launches with complete Sponsored Products coverage on day one.
- **Core endpoints:**
  - Internal: `POST /amazon/campaigns/generate`, `POST /amazon/campaigns/apply`, `GET /amazon/asins?hero=true&missingCampaign=true`
  - Amazon Ads API: campaign creation, ad group creation, product ads, keywords, negative keywords, product targets, campaign state endpoints, report endpoints.
- **Data flow:**
  1. Nightly job scans ASIN master for `hero=true` and `campaign_status IS NULL`.
  2. NLP/regex parses title/bullets/search terms into seed keywords.
  3. Generator emits campaign JSON templates by brand + price band.
  4. Operator approves in dashboard.
  5. Apply service writes to Ads API and logs IDs.
- **Rate limits:** Respect Ads API quotas by batching per brand/account and capping writes per minute; retry with backoff on 429.
- **Webhook/event design:** Event bus topic `asin.approved_for_launch`; consumer generates campaign package; optional dashboard notification.
- **Infra:** Lambda or container worker, SQS/Kafka queue, Postgres state, S3 for raw payload snapshots.
- **Storage:** `asins`, `campaign_templates`, `campaign_apply_jobs`, `audit_log`.
- **Monitoring:** Missing campaign coverage %, apply failures, 429 count, median time from ASIN approval to campaign live.
- **Security:** Store Ads credentials in AWS Secrets Manager; sign internal apply actions; RBAC for apply vs approve.
- **Estimated build:** 5-8 engineering days.
- **Estimated cost:** £3k-£7k.

### 2) Placement-aware bid and budget rebalancer
- **Goal:** Reallocate spend daily toward winners, especially top-of-search, while preventing stock-driven overspend.
- **Core endpoints:**
  - Internal: `POST /amazon/bids/recommend`, `POST /amazon/bids/apply`, `POST /amazon/placements/recommend`, `GET /amazon/ads/performance?granularity=placement`
  - Amazon Ads API reporting + campaign/keyword/target bid mutation endpoints.
- **Data flow:**
  1. Pull daily keyword/target/placement reports.
  2. Join inventory snapshot and margin band table.
  3. Rules engine scores actions: increase, decrease, pause, budget up/down, TOS multiplier change.
  4. Operator reviews deltas above threshold; low-risk changes can auto-apply later.
- **Rate limits:** Single daily batch write is enough; serialize apply jobs; enforce per-campaign cool-down (e.g. no more than 1 placement change/24h).
- **Webhook/event design:** Nightly scheduler; urgent event `spend.spike_detected` triggers an extra run for flagged campaigns.
- **Infra:** Python rules worker, Postgres, queue, dashboard approvals.
- **Storage:** `ad_metrics_daily`, `placement_metrics_daily`, `bid_recommendations`, `budget_changes`, `inventory_snapshots`.
- **Monitoring:** ROAS delta, ACOS delta, stockout incidents on advertised SKUs, approval/apply latency.
- **Security:** Immutable audit table; signed operator identity on approvals; segregated read vs write credentials.
- **Estimated build:** 8-12 engineering days.
- **Estimated cost:** £5k-£12k.

### 3) Search-term harvesting + review-sentiment loop
- **Goal:** Turn converting queries and review language into better keywords, negatives, copy hooks, and product targeting.
- **Core endpoints:**
  - Internal: `POST /reviews/analyze`, `GET /reviews/themes`, `POST /amazon/search-terms/process`, `GET /amazon/search-terms/actions`
  - Amazon Ads API search term reports; review ingestion from public pages or exported review feed.
- **Data flow:**
  1. Daily search-term ingest marks winners, losers, irrelevant queries.
  2. Weekly review NLP clusters benefit/pain-point themes.
  3. Merger service outputs exact keyword adds, negative keywords, copy suggestions, and issue alerts.
- **Rate limits:** Mostly read-heavy; batch keyword writes weekly to reduce churn.
- **Webhook/event design:** `reviews.negative_theme_spike` to alert ops; `search_term.winner_detected` to queue exact-match recommendation.
- **Infra:** NLP worker, embeddings optional, Postgres + S3 raw text archive.
- **Storage:** `search_terms_daily`, `review_raw`, `review_themes`, `keyword_recommendations`, `listing_copy_suggestions`.
- **Monitoring:** Adoption rate of recommendations, CTR/CVR lift on applied changes, theme drift by ASIN.
- **Security:** Strip PII from buyer messages if mixed inputs ever added; keep raw review snapshots internal.
- **Estimated build:** 7-10 engineering days.
- **Estimated cost:** £4k-£10k.

### 4) Inventory forecast + inbound shipment draft automation
- **Goal:** Keep hero SKUs in stock without over-ordering tail SKUs.
- **Core endpoints:**
  - Internal: `GET /amazon/replenishment/recommendations`, `POST /amazon/inbound/draft`, `GET /amazon/inventory/health`
  - SP-API inventory and inbound shipment/replenishment endpoints (account-dependent), listings/catalog data.
- **Data flow:**
  1. Daily inventory snapshot + rolling sell-through calculation.
  2. Forecast service computes cover, reorder date, stockout probability, aged-stock risk.
  3. Shipment draft builder groups SKUs by supplier / carton / destination rules.
- **Rate limits:** Snapshot polling hourly or daily is sufficient; no tight loops.
- **Webhook/event design:** `inventory.low_cover`, `inventory.aged_stock_risk`, `inventory.reorder_due` events.
- **Infra:** Scheduled ETL worker, queue for alert fan-out, Postgres.
- **Storage:** `inventory_snapshots`, `supplier_lead_times`, `shipment_drafts`, `forecast_runs`.
- **Monitoring:** Stockout rate, days of cover accuracy, aged inventory %, forecast error MAPE.
- **Security:** SP-API tokens in secret store; supplier cost sheets encrypted at rest.
- **Estimated build:** 8-14 engineering days.
- **Estimated cost:** £5k-£14k.

### 5) Promo/coupon scheduler with margin guardrails
- **Goal:** Switch discounts on where they lift rank/conversion, not everywhere.
- **Core endpoints:**
  - Internal: `GET /amazon/promotions/recommendations`, `POST /amazon/promotions/schedule`, `GET /calendar/events`
  - Promotion creation/apply path depends on Seller Central/API access; otherwise generate operator-ready actions.
- **Data flow:**
  1. Weekly scheduler reads seasonality, stock age, rank trends, ad efficiency.
  2. Scoring model recommends coupon type, value, window, and ASIN set.
  3. Operator approves and system either writes or produces execution checklist.
- **Rate limits:** Low-frequency weekly writes.
- **Webhook/event design:** `seasonal.window_open`, `inventory.aged_stock_risk`, `rank.slipping` trigger recommendation refresh.
- **Infra:** Simple scheduler + dashboard card; little compute.
- **Storage:** `promo_recommendations`, `promo_calendar`, `margin_floors`, `competitor_coupon_snapshots`.
- **Monitoring:** Promo ROI, rank delta, TACOS delta, margin impact.
- **Security:** Protect margin-floor table; approvals required for any price-affecting action.
- **Estimated build:** 4-7 engineering days.
- **Estimated cost:** £2k-£6k.

### 6) Refund recovery + returns/A-to-Z triage
- **Goal:** Recover hidden margin leakage and route risky cases fast.
- **Core endpoints:**
  - Internal: `GET /finance/refund-recovery`, `POST /cases/triage`, `GET /cases/escalations`
  - SP-API finance/returns/orders/case-related feeds where available; helpdesk/email ingestion if needed.
- **Data flow:**
  1. Daily finance reconciliation joins orders, returns, reimbursements, inventory disposition.
  2. Rules flag missing reimbursements, repeated damage patterns, escalatable case types.
  3. Triage UI shows draft replies and claim queue.
- **Rate limits:** Daily batch; no high-frequency needs.
- **Webhook/event design:** `case.high_risk_opened`, `refund.missing_detected`, `damage.pattern_spike`.
- **Infra:** ETL job, rules service, queue, dashboard panel.
- **Storage:** `finance_events`, `return_events`, `case_queue`, `reimbursement_claims`, `packaging_issue_flags`.
- **Monitoring:** Recovered £ per month, unresolved case SLA, repeat defect rates by ASIN.
- **Security:** Buyer/order data access limited to support roles; redact sensitive content in analytics tables.
- **Estimated build:** 6-9 engineering days.
- **Estimated cost:** £3k-£8k.

## Data & tooling matrix

| Tool / system | Best use in stack | Strengths | Limits / caveats | Credentials required |
|---|---|---|---|---|
| **Helium10** | Keyword expansion, rank tracking, listing optimization inputs | Fast commercial keyword tooling; good for seed discovery and competitive direction | Third-party estimates, not source of truth for performance writes | Paid account |
| **JungleScout** | Keyword/product trend validation | Useful cross-check on demand and seasonality | Public site blocks some automated access; still directional | Paid account |
| **Sellics / similar retail media tools** | Benchmarking rule ideas and dashboards | Helpful model for automation UX and reporting | Not the underlying data source if building in-house | Paid account |
| **DataLake / warehouse (Postgres/RDS + S3)** | System of record for cross-source joins | Needed for rules, audit, history, and analytics | Requires schema discipline | Internal infra |
| **SP-API** | Listings, inventory, orders, finances, inbound/replenishment | Authoritative operational data | Credentialed; account-specific scopes; quotas apply | Seller Central authorization |
| **Amazon Ads API** | Campaigns, keywords, targets, placements, budgets, reports | Required for serious ad automation | Credentialed; quotas/429s; write safety needed | Ads API authorization |
| **Amazon DSP** | Audience and retargeting automation | Useful after SP/Brands fundamentals are solid | More complex attribution; not phase-1 priority | DSP access |
| **AWS Lambda** | Lightweight scheduled jobs and event consumers | Cheap, easy scaling for batch automations | Long-running ETL may fit containers better | AWS account |
| **S3** | Raw report/archive storage | Cheap durable storage for exports and payloads | Needs lifecycle rules | AWS account |
| **RDS / Postgres** | Structured state, recommendations, audit logs | Strong fit for operational analytics | Needs migrations, backups, retention rules | AWS account |
| **Kafka / queues (or SQS)** | Event-driven workflows, decoupled jobs | Good for launch, alerts, recommendations, apply jobs | Overkill if volume small; SQS simpler for pilot | Internal infra |

## Next steps and recommended pilot

### Recommended pilot
- **Brand:** **Newgate World**
- **Why first:** strongest Amazon fit, clearer search intent, visually distinctive hero ASINs, lower style/fit return risk than eyewear, easier to prove sales lift from placement optimization.

### Pilot scope (30-45 days)
1. Connect Ads API + SP-API for one marketplace first.
2. Tag top 10-20 hero ASINs.
3. Ship these four automations first:
   - campaign generator
   - bid/budget rebalancer
   - top-of-search rules
   - inventory health alerts
4. Add review sentiment loop and coupon scheduler in week 3-4.
5. Keep write actions approval-based for the full pilot.

### KPI targets
- **Sales growth:** +15% to +25% attributed ad sales on pilot ASIN set
- **Visibility:** +20% top-of-search impression share on target hero ASINs
- **Efficiency:** 10% to 20% reduction in wasted spend on zero-conversion targets/queries
- **Stock health:** zero stockouts on pilot hero ASINs; reduce low-cover alerts to <5% of hero catalogue days
- **Conversion:** +5% to +10% PDP CVR improvement on ASINs where review/copy insights are applied

### Rollout after pilot
- **Second brand:** Funkstar Hardware
- **Third brand:** London Mole Eyewear, but only on validated reader SKUs and with stricter return-rate gating.

## Notes on data boundary
- This catalog uses public evidence and Amazon public documentation for framing.
- Any implementation that reads operational data or writes changes requires approved Seller Central / SP-API / Ads API credentials.
- No logged-in scraping should be used; ingest exports or official APIs instead.
