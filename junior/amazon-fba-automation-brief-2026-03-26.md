# Amazon Advertising, FBA Optimisation & AI Automation Brief
**Prepared for:** Meeting with Jim Reed  
**Brands:** Newgate World, London Mole Eyewear, Funkstar Hardware  
**Date:** 2026-03-26  
**Prepared by:** Junior

## Executive summary
Jim Reed has three Amazon-suitable brands, but they need different playbooks. **Newgate World** already has strong fit for Amazon because clocks are search-led, giftable, and visually differentiated. **Funkstar Hardware** looks like a clean Amazon growth candidate for umbrellas and accessories with distinctive design-led SKUs. **London Mole** can work on Amazon, but eyewear is more competitive, style-sensitive, and return-prone, so it should be treated as a tightly controlled catalogue rather than an all-out scale bet. The fastest gains will not come from “more humans in Seller Central” but from rule-driven automation on bidding, couponing, inventory alerts, review mining, and listing-to-campaign generation. 

My recommendation: use Amazon as the primary marketplace for Newgate and Funkstar, run London Mole more selectively, and build a lightweight automation layer around Seller Central/SP-API + Amazon Ads + review/NLP + inventory forecasting. Immediate goal: improve CTR, CVR, and stock health while cutting wasted ad spend and storage leakage. Longer term, add DSP audiences, repricing intelligence, inbound shipment automation, and a DTC data layer that uses Amazon demand to inform owned-channel growth rather than trying to outspend on cold traffic.

## What public research shows
- **Newgate World** has a visible Amazon UK store footprint and merchant presence, with multiple active wall clock / alarm clock listings found publicly.
- **London Mole Eyewear** has a visible Amazon US brand storefront and public ASINs for reading glasses and sunglasses.
- **Funkstar Hardware** has public Amazon UK and US listings plus a live DTC site with umbrellas priced around **£19.99-£29.99**.
- Amazon Ads public documentation confirms:
  - **Sponsored Products** are CPC ads driving directly to PDPs and only show when items are in stock.
  - **Sponsored Brands** support branded creative, collections, video, and traffic to Brand Store or PDPs.
  - **Sponsored Display** has been folded into Amazon’s broader **Display** offering, while existing campaigns continue to run.
  - **Amazon DSP** can be used **even if a brand does not sell on Amazon**, which matters for broader DTC retargeting and audience building.
- Amazon FBA public materials continue to emphasize lower fulfilment cost vs many premium carrier alternatives, plus credits for inbound placement, shipping, and new selection in some programs.

## Prioritised AI automation opportunities

### Tier 1 — Quick wins (2-6 weeks)
Highest ROI, low integration risk.

1. **Listing-to-campaign auto-build**
   - Auto-create Sponsored Products campaigns from each live ASIN.
   - Parse titles, bullets, backend keywords, category nodes, and competitor ASINs into seed keyword sets.
   - Launch structure:
     - auto campaign
     - exact campaign
     - phrase campaign
     - product targeting campaign
   - Why it wins: humans routinely delay launch discipline; automation makes every new ASIN launch correctly on day one.

2. **Rule-based bid and budget engine**
   - Pull daily ad metrics and apply rules by ACOS/ROAS/CVR/CPC thresholds.
   - Example rules:
     - If keyword spend > target and no orders in 14 days, pause.
     - If ACOS is 20% below target and stock cover > 35 days, raise bid 10-15%.
     - If low stock risk < 21 days, throttle top-of-search modifiers.
   - Start with Sponsored Products; extend to Brands and Display later.

3. **Coupon / promo monitor + trigger suggestions**
   - Track category price moves, seasonal events, BSR shifts, and competitor coupon activity.
   - Recommend when to switch on coupons, deals, or price-off promotions.
   - Good for clocks and umbrellas where gifting and weather seasonality create obvious promo windows.

4. **Review sentiment analysis feeding ads + listing fixes**
   - Use NLP on public reviews to cluster pain points and winning phrases.
   - Auto-suggest:
     - negative keyword additions
     - creative angle changes
     - bullet rewrites
     - FAQ updates
   - Example: if reviews repeatedly praise “silent movement” on clocks, pipe that into Sponsored Brand video hooks and PDP image text.

5. **FBA health alerts**
   - Daily alerting for low stock, excess cover, stranded inventory, suppressed listings, buy box loss, and high return SKUs.
   - This is usually where manual teams leak margin.

### Tier 2 — Medium-term (6-12 weeks)
Needs better data plumbing and operational discipline.

1. **AI repricer with floor/ceiling logic**
   - Not a race-to-the-bottom repricer.
   - Use contribution margin floor, competitor price bands, coupon activity, and stock age to change prices safely.
   - Best fit: London Mole reading glasses and Funkstar umbrellas where adjacent SKUs are comparable.
   - Lower fit for design-led hero clocks where brand positioning matters more than penny gaps.

2. **Automated keyword harvesting and search term mining**
   - Pull search term reports and auto-graduate converting queries into exact match.
   - Add poor queries to negatives automatically.
   - Enrich with Helium 10 / Jungle Scout exports where available.

3. **DSP / Display rule engine**
   - Build audience triggers from PDP views, Brand Store visitors, review themes, and off-Amazon behaviour where available.
   - Reallocate spend based on assisted conversion rather than only last-click ACOS.

4. **FBA inbound shipment automation**
   - Forecast reorder timing by sell-through, seasonality, promo plan, and lead time.
   - Generate draft replenishment plans, carton counts, and shipment recommendations.
   - Add alerts for aged stock and slow movers before long-term storage fees bite.

5. **Automated catalogue QA**
   - Detect title drift, image count gaps, missing A+ content, parent-child variation issues, and suppressed PDPs.

### Tier 3 — Long-term (3-6 months)
More strategic, bigger payoff if Jim wants a real operating system.

1. **Amazon operating cockpit**
   - Single dashboard combining Ads, SP-API catalogue/order/inventory, finance, review sentiment, and DTC signals.
   - Daily “what to do now” recommendations ranked by revenue/margin impact.

2. **Cross-channel demand engine**
   - Use Amazon search trends and conversions to decide DTC landing pages, Meta creative, email pushes, and product bundles.
   - Amazon becomes the demand sensor; DTC becomes the margin and retention layer.

3. **Predictive promo and inventory planning**
   - ML model on seasonality + event calendar + historical promo elasticity.
   - Especially useful for:
     - clocks at gifting peaks
     - umbrellas in weather spikes
     - reading glasses around gifting / impulse retail moments

4. **Creative generation with guardrails**
   - AI-assisted Brand Store modules, Sponsored Brands creatives, short videos, seasonal image overlays, and bundle copy.
   - Human approval still required before publishing.

## Recommended Amazon ad strategy by ad type

### 1) Sponsored Products
**Role:** primary demand-capture engine for all three brands.  
**Best use:** hero SKUs, conquesting, search term harvesting, launch velocity.

Recommended approach:
- Create one campaign stack per ASIN or tightly related product family.
- Split by intent:
  - auto discovery
  - manual exact winners
  - manual phrase/broad exploration
  - product targeting on competitor ASINs and adjacent categories
- Use separate bid logic for:
  - top of search
  - product page
  - rest of search
- Focus first on hero products, not the full long tail.

**Brand-specific note**
- **Newgate:** strongest SP fit; shoppers are highly search-led.
- **London Mole:** use SP surgically on best-reviewed readers, not every frame.
- **Funkstar:** excellent for design-led niche terms, gifting, and seasonal weather queries.

### 2) Sponsored Brands
**Role:** defend brand terms and improve click share at top of search.  
**Best use:** branded search, category storytelling, collections, video.

Recommended approach:
- Build/refresh Brand Store for each brand before scaling.
- Use Sponsored Brands video on the 3-5 hero SKUs per brand.
- Own branded queries so competitors do not sit above the brand.
- Send non-brand category traffic either to a curated Brand Store page or hero PDP depending on conversion behaviour.

**Best near-term fit:** Newgate and Funkstar. London Mole should use it only once a clean, premium storefront exists.

### 3) Sponsored Display / Display ads
**Role:** retargeting, category audience expansion, PDP conquesting.  
**Best use:** remarketing viewers who did not buy, defending hero PDPs, reaching in-market audiences.

Recommended approach:
- Start with retargeting visitors to hero ASINs and Brand Stores.
- Run competitor ASIN targeting on adjacent lifestyle brands.
- Use creative derived from review sentiment and top FAQ themes.
- Keep budgets modest until assisted conversion is measured cleanly.

### 4) Amazon DSP
**Role:** upper/mid funnel audience building, off-Amazon remarketing, broader media efficiency.  
**Best use:** once attribution and creative discipline exist.

Recommended approach:
- Do **not** start here first.
- Add once Sponsored Products + Brands + Display are disciplined.
- Best cases:
  - retarget Brand Store/PDP viewers off Amazon
  - seasonal awareness pushes for Newgate giftable clocks
  - audience expansion for Funkstar during weather or gifting peaks
  - DTC crossover audiences if Jim wants Amazon and owned-site coordination

## FBA cost, fee, and inventory optimisation recommendations

### Immediate fee/margin priorities
1. **Kill aged inventory before storage penalties compound**
   - Create 30/60/90/180-day age buckets by SKU.
   - Push coupons, outlet deals, bundles, or price actions before aged inventory fees hit.

2. **Stop advertising low-stock winners too hard**
   - Ads should be stock-aware.
   - If cover falls below threshold, bids and budgets should taper automatically to avoid stockouts and ranking whiplash.

3. **Segment FBA vs FBM vs hybrid**
   - Fast-moving hero SKUs: FBA.
   - Bulky or fragile low-velocity variants: test FBM or merchant-fulfilled fallback if margin gets crushed.
   - Clocks may need packaging-loss analysis by SKU to decide FBA viability on larger units.

4. **Track inbound placement and prep leakage**
   - Cartonization, prep, labelling, and split shipments quietly erode margin.
   - Automate shipment planning and compare landed margin by shipment mode.

5. **Rationalise long-tail catalogue**
   - Especially for style-heavy eyewear and decorative clocks.
   - Too many weak ASINs dilute stock, reviews, and ad budgets.

### Inventory operating recommendations
- Maintain target stock cover bands by brand:
  - **Newgate:** 45-75 days on winners, longer before Q4/gifting windows.
  - **London Mole:** 30-45 days on proven frames only; avoid deep stock on speculative styles.
  - **Funkstar:** 45-60 days with seasonal buffers around rainy periods and gifting spikes.
- Use weekly forecast combining:
  - 30/60/90 day sales velocity
  - promo calendar
  - lead time from supplier to FC
  - inbound receiving lag
  - return rate
- Add “do not reorder” rules for SKUs with weak CVR + rising storage age.

## DTC viability assessment

### Newgate World — **High DTC viability**
Why:
- Strong design/brand story.
- Higher AOV than commodity accessories.
- Better merchandising potential via collections, interiors inspiration, gifting, and bundles.
- Easier to build repeatable content/SEO around room aesthetics, style, and gifting.

DTC role:
- Use DTC for margin, bundles, gifting edits, retailer locator, and brand storytelling.
- Amazon remains essential for search capture and conversion convenience.

### London Mole Eyewear — **Medium DTC viability**
Why:
- Brand/aesthetic matters, which helps DTC.
- But eyewear competition is brutal, returns can be painful, and CAC can spike fast.
- DTC can work if the brand identity is strong and frames are differentiated enough.

DTC role:
- Good for brand presentation, bundles, accessories, email capture, and repeat orders.
- Use Amazon for demand capture on reading glasses and impulse search demand.

### Funkstar Hardware — **Medium-high DTC viability**
Why:
- Product line is design-led and giftable.
- Umbrellas are not ideal for expensive cold acquisition, but they are merchandisable and visual.
- DTC works if the site leans into personality, gifting, seasonal edits, and accessory expansion.

DTC role:
- Useful as a branded catalogue and margin layer.
- Amazon likely remains the better conversion engine for generic search intent.

**Bottom line:** Jim should not treat DTC as a replacement for Amazon. Treat Amazon as the volume capture channel and DTC as the brand/margin/CRM layer.

## Competitor and product research
**Note:** Public evidence was limited by marketplace anti-bot restrictions, so some price points below are taken from accessible public pages, search snippets, or observed ranges rather than full live Seller Central data. Human validation inside Amazon Seller Central and Brand Analytics is still required.

### Newgate World — top visible SKUs / ASINs
| SKU / ASIN | Price range | Notes |
|---|---:|---|
| Universal wall clock — **B0B71VJ2TC** | ~£50-£65 observed range | Large 43cm vintage/station style wall clock; strong hero-SKU candidate for Sponsored Products + Brands video. |
| Number Three Echo wall clock — **B07YYPS2V3** | ~£45-£60 observed range | Modern round clock with bold readable numerals; good mass-market search fit. |
| Centre of the Earth alarm clock — **B099X4FRBV** | ~£20-£35 estimated | Retro digital alarm clock; bedside/desk use case and likely good for lower-AOV acquisition. |
| Universal wall clock silent variant — **B0CTQMLD4B** | ~£50-£70 estimated | Search snippet indicates silent version; “silent” should be a key keyword/theme if review sentiment supports it. |
| Newgate merchant/storefront (merchant **ASZN10WW55N4D**) | n/a | Merchant presence suggests a larger Amazon assortment that should be rationalised into hero / support / tail SKUs. |

### London Mole Eyewear — top visible SKUs / ASINs
| SKU / ASIN | Price range | Notes |
|---|---:|---|
| Hollywood reading glasses — **B0CB8QG3W3** | ~$15-$30 estimated | Thin lightweight reading glasses; likely good test SKU for exact-match reader terms. |
| Moley reading glasses — **B0DYVHGR2G** | ~$15-$30 estimated | Round-shape readers; style-led but still keyword-friendly. |
| Moley sunglasses — **B0FK5WQHVT** | ~$20-$40 estimated | Sunglasses are more style-driven and may convert worse than readers on Amazon unless reviews/images are strong. |
| London Mole storefront (Amazon US) | n/a | Presence of storefront means Sponsored Brands should route to curated brand pages rather than random PDPs. |
| “All Zero’s” / accessories pages visible in storefront | n/a | Suggests assortment breadth that may be too wide for efficient Amazon ad scaling without hero-SKU focus. |

### Funkstar Hardware — top visible SKUs / ASINs
| SKU / ASIN | Price range | Notes |
|---|---:|---|
| Camofunk stick umbrella — **B0G6FZ69BG** | ~£24-£35 observed/estimated | Public Amazon UK listing found; design-led umbrella with broad everyday appeal. |
| Vintage Soccer umbrella — **B0G6G9JDY6** | ~$25-$40 estimated | Public Amazon US listing found; niche giftable design, good for product-targeting and weather/event spikes. |
| Vintage Grand Prix umbrella — **B0G6FSWX28** | ~$25-$40 estimated | Public Amazon US listing found; motorsport angle likely suitable for conquesting adjacent gift and hobby audiences. |
| Weatherman stick umbrella — DTC code **FHU-WMAN-ST** | **£29.99** | Strong classic hero product from DTC site; should be mirrored in Amazon launch and brand-store storytelling. |
| Farmhouse Funk compact umbrella — DTC code **FHU-FARM-CP** | **£19.99** | Compact format broadens use case and gifting potential; good test SKU for promo elasticity. |

### Likely competitor sets to benchmark
These are directional competitor pools Jim should check in Amazon category research.

- **Newgate / clocks:** Acctim, Karlsson, Umbra, Seiko wall clocks, Hito, home décor clock brands with modern/station styles.
- **London Mole / readers & sunglasses:** Foster Grant, Gaoye, Peepers, TIJN, SOJOS, generic Amazon reader brands.
- **Funkstar / umbrellas:** Fulton, Totes, Davek (premium reference), Repel, Eono / Amazon Basics, design-led gift umbrellas.

## Data and tooling required

### Mandatory data inputs (human access required)
These cannot be reliably obtained from public pages alone.
- Seller Central account access or exported reports for each brand
- Amazon Ads console access or API credentials
- SP-API credentials / app authorization
- Current ASIN master list with parent-child relationships
- Inventory by SKU / FC / inbound status
- Sales velocity by SKU (units/day, 7/30/90 day)
- Current ACOS, TACOS, ROAS, CVR, CPC, CTR
- Session and conversion rate data by ASIN
- Return rate and reason codes
- Current landed margin / COGS / FBA fee assumptions
- Lead times, MOQs, carton dims, prep constraints

### Useful tools
- **Amazon SP-API** — catalogue, orders, inventory, finances, listings, inbound shipment data
- **Amazon Ads API** — campaigns, ad groups, keywords, search terms, placements, budgets, bids
- **Seller Central exports** — business reports, search term reports, FBA inventory age, stranded inventory, returns
- **Helium 10** — keyword research, ranking, listing optimisation, AI-assisted advertising, inventory and trend data
- **Jungle Scout** — keyword/product research and trend validation
- **Pacvue / Perpetua / Quartile / Teikametrics / Sellics-style tools** — ad automation benchmarks and rule ideas
- **Review NLP stack** — OpenAI/Anthropic or local NLP pipeline for review clustering and copy insights
- **BI layer** — Metabase / Superset / Looker Studio / custom dashboard

## Specific engineering tasks for Felix

### Phase 1 — data foundation (1-2 weeks)
1. **Credentialed connectors**
   - SP-API auth flow
   - Amazon Ads API auth flow
   - optional Shopify / DTC connector for cross-channel view
2. **Data warehouse schema**
   - `asins`
   - `inventory_snapshots`
   - `orders_daily`
   - `ad_campaigns`
   - `ad_keywords`
   - `ad_search_terms`
   - `reviews`
   - `pricing_snapshots`
   - `alerts`
3. **Scheduled ingestion jobs**
   - hourly inventory snapshot
   - daily ads/report pulls
   - daily review scrape from public PDPs where allowed or import from approved source
   - daily competitor price / coupon snapshot from public pages only

### Phase 2 — decision engine (2-4 weeks)
4. **Rules service**
   - ACOS/CVR/CPC-driven bid updates
   - stock-aware budget throttling
   - stale keyword pausing
   - promo recommendation scoring
5. **Listing-to-campaign generator**
   - input: ASIN metadata + seed keywords + competitor ASINs
   - output: draft campaign JSON or direct API campaign creation
6. **Review sentiment pipeline**
   - cluster praise, defects, feature mentions, shipping complaints, packaging complaints
   - emit copy suggestions and negative keyword suggestions
7. **Inventory forecaster**
   - calculate days of cover, reorder date, stockout risk, aged-stock risk

### Phase 3 — UI and operator workflow (2-3 weeks)
8. **Ops dashboard**
   - revenue/margin/ad/inventory overview by brand and ASIN
   - “top actions today” queue
9. **Approval workflow**
   - all bid changes, campaign launches, and price changes should be reviewable before write-back initially
10. **Webhook / notification layer**
   - Slack/Telegram alerts for low stock, listing suppression, buy box loss, spend spikes, coupon opportunities

### Suggested endpoints / services
- `GET /amazon/asins`
- `GET /amazon/inventory/health`
- `GET /amazon/ads/performance`
- `POST /amazon/campaigns/generate`
- `POST /amazon/campaigns/apply`
- `POST /amazon/bids/recommend`
- `POST /amazon/bids/apply`
- `GET /amazon/reviews/themes`
- `GET /amazon/promotions/recommendations`
- `GET /amazon/repricing/recommendations`
- `GET /amazon/replenishment/recommendations`

### Infra notes
- Postgres for warehouse + state
- Python workers for ETL/rules/NLP
- Lightweight Node or Python API layer
- Cron/queue for scheduled jobs
- Audit log table for every recommendation and every applied change
- Secrets vault for Amazon credentials

## Estimated effort, timeline, and rough cost

### Option A — lightweight pilot
- Scope: one brand first (recommend **Newgate**), ads + inventory alerts + review sentiment + campaign generator
- Time: **3-5 weeks**
- Team: Felix + 1 operator
- Rough build cost: **£8k-£20k** depending on polish and whether UI is basic
- Outcome: proof that automation beats manual pacing and reduces wasted spend

### Option B — multi-brand operating layer
- Scope: all three brands, rule engine, dashboard, stock-aware ad logic, promo suggestions, review NLP
- Time: **6-10 weeks**
- Rough build cost: **£20k-£60k**
- Outcome: reusable internal Amazon growth system

### Option C — full performance OS
- Scope: multi-brand + DSP + repricing + DTC joins + forecasting + approvals/workflows
- Time: **3-6 months**
- Rough build cost: **£60k-£150k+**
- Outcome: real competitive moat if Jim wants to professionalise Amazon as a system, not a channel

## Recommended next move
1. Start with **Newgate** as the pilot brand because it has the clearest Amazon-product fit and likely strongest search demand capture.
2. Pull a 12-month export of sales, ads, inventory age, and return data.
3. Identify the top **10-20 hero ASINs** only.
4. Build the stock-aware Sponsored Products automation first.
5. Add promo recommendations and review-sentiment loops second.
6. Roll the same stack into Funkstar next; only then decide how aggressively to push London Mole.

## Human access required / compliance boundary
- No scraping behind logins was used here.
- Any serious implementation now requires approved access to:
  - Seller Central
  - SP-API app authorization
  - Amazon Ads API credentials
  - inventory/finance exports
- Public web pages were enough to frame the strategy, but not enough to validate live sales rank, actual CVR, TACOS, or fee leakage by SKU.

## Sources captured
- Amazon Ads product pages for Sponsored Products, Sponsored Brands, Sponsored Display/Display, Amazon DSP
- Amazon FBA public overview page
- Public Amazon listing/storefront links for Newgate, London Mole, Funkstar
- Funkstar Hardware DTC product pages
- Helium 10 keyword research product page
