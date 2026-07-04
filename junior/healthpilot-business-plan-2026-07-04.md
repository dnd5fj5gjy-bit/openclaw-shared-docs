# HealthPilot - Business Plan & Monetisation Strategy
**Prepared:** 4 July 2026
**Author:** Junior
**Status:** Internal, decision-ready. All pricing figures are working hypotheses to be validated with design partners, not finance-approved.

---

## 1. The Concept, Sharpened

**HealthPilot is the AI front door for health brands and clinics.** It is an embeddable intake, triage and conversion layer: a patient arrives at a clinic's website, answers an intelligent, goal-driven quiz under the clinic's own brand, gets a personalised health summary, and is routed to the right revenue event - a blood panel, a consultation, a treatment pathway, a product. The clinic gets structured intake data written straight into its patient record, plus a conversion funnel it never had to build.

Today HealthPilot is an AI health quiz with a DB-driven recommendation engine and affiliate tracking already built in. That last part matters: the revenue seam exists in the code, not just the pitch. What turns it from a demo into a product is the embed SDK now being built - identity in (clinic slug, patient reference, theme), results out (completed intake pushed to the host system), per-clinic feature flags, and clinic-branded output. Before the SDK, HealthPilot was a standalone quiz that happened to sit in an iframe. After it, HealthPilot is infrastructure any health brand can drop into its own site in an afternoon, with the results landing in its own systems. That is the difference between "a nice form" and "a distribution product". Security hardening and red-flag safety handling have been completed as prerequisites.

The strategic fit is clean. Ted's Health has pivoted from D2C to a white-label backend for clinics, and that platform is genuinely mature: per-clinic theming, pricing overrides, feature flags. HealthPilot becomes the top of every clinic's funnel on that platform - and, separately, a product that can be sold to health brands that are not on the platform at all.

## 2. Who Pays, and Why

**Buyer 1: Clinic operators on the Ted's white-label platform.** Independent men's health clinics, private GPs, sports medicine practices. Their job-to-be-done: "Turn my website visitors into booked, qualified patients without my front desk doing triage by phone." Today their intake is a contact form or a receptionist. HealthPilot gives them a premium digital first impression, pre-qualified patients, structured intake data before the first consultation, and a built-in upsell path (blood panel before you even see the doctor). For these buyers HealthPilot is a feature toggle on a platform they already pay for - lowest friction sale in the book.

**Buyer 2: Health and wellness brands wanting a smart quiz funnel.** Supplement brands, blood-testing companies, longevity clinics, corporate wellness providers. Their job-to-be-done: "Convert cold traffic into buyers with a personalised recommendation, and capture consented first-party data doing it." They currently duct-tape Typeform to a spreadsheet. HealthPilot gives them AI-personalised recommendations mapped to their own catalogue, affiliate/attribution tracking out of the box, and their brand on every pixel. This is the bigger long-term market but the harder sale - it needs self-serve onboarding that does not exist yet. Sequence it second.

**Buyer 3: Ted's Health itself, as first customer.** Ted's uses HealthPilot as the intake layer across its own white-label clinic deployments. This matters commercially in three ways: it is proof (live clinics, real conversion data), it is pipeline (every Ted's clinic is a warm HealthPilot upsell), and it strengthens the Ted's story at exactly the moment a large digital health player is showing acquisition and partnership interest in Ted's. An AI intake layer with a data flywheel is precisely the kind of asset that improves that conversation - whether HealthPilot ends up inside a deal or deliberately held outside it.

## 3. Monetisation Model

Four levers are available. Assessment of each, then the recommendation.

**(a) SaaS per-clinic monthly fee.** Predictable MRR, easy to buy, easy to forecast. Weakness: caps upside on high-volume clinics and undercharges the ones getting the most value.

**(b) Per-completed-intake pricing.** Aligns price to usage, and each AI generation has a real marginal cost (LLM calls), so this also protects gross margin. Weakness: clinics dislike unpredictable bills; needs a cap or tier structure.

**(c) Revenue share on conversions the quiz drives.** Blood panels, consultation bookings, supplement affiliate revenue. The attribution plumbing already exists in the engine. This is where the real money is long-term, because a quiz that reliably converts is worth a percentage of what it converts, not a flat fee. Weakness: requires trusted attribution and enough volume to matter; useless as the only model in month one.

**(d) Setup / white-label fee.** One-off cash, filters out tyre-kickers, funds onboarding effort. Weakness: friction for pilots.

### Recommendation: a three-part hybrid

1. **Base SaaS fee per clinic** - covers the platform, keeps MRR predictable:
   - **Starter: £199/month** - up to 200 completed intakes, standard theming, blood-panel CTA
   - **Growth: £449/month** - up to 750 completed intakes, full branding, results-to-record integration, results PDF/email
   - **Scale: £899/month** - up to 2,500 intakes, priority support, custom question sets
2. **Overage: £0.60 per completed intake** beyond tier allowance. Anchors the per-intake value and protects AI cost margin.
3. **Conversion revenue share: 10% of net revenue on quiz-attributed blood panels and consultation bookings, plus existing affiliate commission on supplement sales.** This is the growth engine and the number that scales with proof.
4. **Setup fee: £750 one-off** for clinics off the Ted's platform (custom domain, theme, catalogue mapping). **Waived for Ted's platform clinics** - the platform relationship has already paid for onboarding, and zero-friction activation there is worth more than the fee.

For Ted's platform clinics, HealthPilot is sold as an add-on line on the existing Ted's invoice - one contract, one bill, quiz enabled by feature flag. Consistent with the existing Ted's partner economics framing (setup + platform fee + revenue share), so the two products sell in the same language.

### Worked example: a clinic doing 500 intakes/month

Assumptions, stated as assumptions: 500 completed intakes/month; 60% answer "no recent blood test" and see the panel CTA; 8% of those buy a panel at £150 net (24 panels); 5% of all intakes book a paid consultation at £80 (25 consultations); supplement affiliate revenue averages £0.40 per intake. Every one of these numbers is a guess until design partners produce real data - the 8% panel conversion is the load-bearing one.

| Line | Calculation | HealthPilot revenue |
|---|---|---|
| Growth tier base | flat | £449 |
| Overage | none (500 < 750) | £0 |
| Blood panel rev share | 24 x £150 x 10% | £360 |
| Consultation rev share | 25 x £80 x 10% | £200 |
| Affiliate supplements | 500 x £0.40 | £200 |
| **Total per clinic/month** | | **£1,209** |

Clinic side of the ledger: roughly £5,600/month in quiz-attributed gross revenue (panels + consultations) plus downstream treatment revenue from better-qualified patients, against £449 + £560 in fees. The clinic keeps about 4.5x what it pays. That ratio is the pitch.

At 10 clinics on this profile: **~£12k MRR / £145k ARR**. At 30 clinics: **~£36k MRR / £435k ARR**. For context, the entire Ted's D2C business was doing £6k MRR at the April pivot decision. A modest clinic count on an honest conversion rate beats it comfortably - and roughly half the revenue is usage and share, which grows without a single new logo.

Marginal cost per intake (AI generation, infra) is pennies against £0.60 overage and the rev share, so gross margin stays software-shaped at 80%+ even with heavy AI usage. Assumption to monitor: model costs per generation at production prompt sizes.

## 4. The Wedge Sequence

**Wedge 1 - blood-test upsell (now).** The quiz already asks about recent blood tests; the upgrade being built turns "no" into a clinic-branded panel CTA, with the click event flowing back to the host. This is the first attributable pound: a patient who arrived with a vague concern leaves having bought a £150 panel. It is also the easiest revenue to attribute cleanly - one CTA, one purchase, one event. Prove this first because everything else is priced off it.

**Wedge 2 - consultation booking (next quarter).** Panel results plus intake data make "book a consultation to review your results" the natural next step. Decision required on build-vs-partner for booking itself (see 90-day plan) - HealthPilot does not need to own the calendar, only the routed, attributed handoff.

**Wedge 3 - the referral network (12+ months).** Once multiple clinics run HealthPilot, intakes that do not fit the host clinic's services can, with consent, be referred across the network - a patient whose profile screams sports medicine gets routed to a sports medicine partner, with a referral fee attached. This is where HealthPilot stops being a tool and becomes a marketplace. Do not build it yet; do design the data model so it is possible.

**Why the data compounds.** Every completed intake plus its downstream outcome (panel bought or not, consultation booked or not, plan followed or not) is a labelled training example for the matching engine. Better matching means better conversion, better conversion justifies the rev share, and the aggregate conversion benchmarks become sales collateral no new entrant has. Hard constraint: this only works within GDPR consent limits. Improvement of matching must run on properly consented, minimised data, with per-clinic data segregated by default and any cross-clinic learning done on anonymised or aggregated data under a lawful basis stated at intake. The flywheel is real but it spins inside the consent envelope, not around it.

## 5. Competitive Frame

**Generic quiz builders (Typeform, Jotform health templates).** Cheap, ubiquitous, dumb. They capture answers; they do not reason about them, recommend against a live catalogue, track conversion attribution, or route to clinical pathways. HealthPilot competes with them on outcome, not on form-building.

**US medical intake tools (Phreesia, IntakeQ).** Serious products, but they are administrative intake - insurance, consents, scheduling paperwork - built for the US system. They optimise the clipboard, not the funnel. No AI personalisation, no conversion orientation, thin UK presence.

**Symptom checkers (Ada, the Babylon-era tools).** Clinically deep, consumer-branded, and commercially adrift - Babylon's collapse showed that clinical AI without a revenue-routing model burns cash. They also sit deliberately on the medical-device side of the line, which is expensive. HealthPilot is the inverse: wellness-side triage whose entire purpose is converting intent into the host brand's revenue.

**The category HealthPilot actually occupies:** embedded, brand-native, conversion-oriented AI intake. Nobody credible in the UK sells "the AI front door for your clinic, under your brand, paid partly on the revenue it drives". The rev-share model itself is a differentiator - none of the above will price on conversion because none of them can attribute it.

**Honest read on defensibility: thin today.** The quiz, the AI layer and the embed SDK are all replicable by a competent team in a quarter. Numan or Manual could build this if they decided the white-label market mattered. Real defensibility arrives from exactly two things: the **data flywheel** (intake-to-outcome data that makes matching measurably better than a cold start) and the **clinic network** (distribution through the Ted's platform plus, later, cross-referral economics that make leaving costly). Neither exists yet. Until they do, the moat is speed and the Ted's distribution channel - which is why the 90-day plan is about getting live clinics generating outcome data, not adding features.

## 6. Risks and Gates

**Clinical safety and liability.** Red-flag handling now exists - urgent symptoms halt the quiz and route to emergency services, with age gating. But the boundary must be actively policed, not assumed: the product gives wellness guidance and routes to clinicians; it must never diagnose, and prompt/output changes need a safety review step so drift does not creep in through model updates. Contractually, clinic agreements must state that clinical responsibility sits with the clinic's registered clinicians, and HealthPilot is a triage and information tool.

**MHRA software-as-medical-device boundary.** This is the sharpest regulatory line. Wellness triage and lifestyle recommendation is outside SaMD scope. The moment the software's stated purpose includes diagnosis, or it drives treatment decisions ("your answers indicate low testosterone, start TRT"), it is a medical device under UK MDR and needs UKCA marking, a quality management system and clinical evidence. Gate: every new pathway and every marketing claim gets checked against intended-purpose wording before ship. The blood-panel CTA is fine (it sells a test, not a diagnosis); interpreting results back to the patient in diagnostic language is where it would tip. If the roadmap ever wants diagnostic features, that is a deliberate, costed decision - likely 12+ months and six figures - not a drift.

**GDPR and special category data.** Health answers are special category data: explicit consent at intake, encryption at rest (built), strict access control (built), data minimisation in AI prompts (built - only answered fields are passed), UK data residency for processing, DPIA before scaled launch, and per-clinic controller/processor agreements defining who owns the patient record. The referral network and any cross-clinic learning need their own consent language from day one - retrofitting consent is how the flywheel dies.

**UK ASA claims rules on supplement recommendations.** Recommendations tied to affiliate revenue are advertising. No medicinal claims for supplements, only authorised health claims per the GB nutrition and health claims register, and affiliate relationships disclosed. The recommendation catalogue needs a claims-compliance pass and a rule that AI output cannot generate claims not present in approved product copy. An ASA ruling against a clinic embed would poison the B2B pipeline overnight.

**Platform dependence on Ted's.** HealthPilot's first distribution channel is the Ted's white-label platform, and Ted's is in acquisition/partnership conversations with a large digital health player. Two scenarios to plan for: an acquirer wants HealthPilot bundled in (fine, priced in), or an acquirer's ownership complicates selling HealthPilot to clinics outside their orbit. Mitigation: keep HealthPilot a separate product with its own repos, its own commercial identity and at least one non-Ted's design partner within 90 days, so it has standalone option value whatever happens to Ted's. This also strengthens Jesse's hand in the Ted's conversation - a separable asset is worth more than an entangled one.

## 7. 90-Day Plan

**Days 1-30: live and instrumented.**
- Embed SDK, goal branching, blood-panel CTA and per-clinic feature flag shipped and stable (in build now).
- Two Ted's platform clinics live as design partners on founder terms (free base fee, rev share only) in exchange for data access and a case study.
- Attribution pipeline verified end to end: quiz CTA click → panel purchase → revenue event logged. Baseline KPIs recording from day one.

**Days 31-60: pricing and proof.**
- First quiz-attributed blood-panel revenue booked. This is the milestone that matters most - one attributed pound beats any deck.
- Pricing tested in real conversations with 5 clinics (mix of platform and off-platform): present the tier structure, log objections, find the price that closes without discounting. Target: 3 signed at or near list.
- DPIA completed; clinic data processing agreement and claims-compliance pass on the recommendation catalogue done.
- One non-Ted's design partner signed (a testing brand or longevity clinic) to prove the product travels beyond the platform.

**Days 61-90: decide and double down.**
- Build-vs-partner decision on consultation booking: if the Ted's platform booking flow can take an attributed handoff, integrate; if not, partner with an existing UK booking layer rather than building calendars. Decision criterion: whichever gets attributed consultation revenue live within 30 days of the decision.
- 5+ clinics live, first full month of cohort data on completion and conversion rates.
- Rewrite the worked example in section 3 with real numbers and re-cut pricing if the assumptions were wrong.
- Go/no-go on raising HealthPilot's profile in the Ted's acquisition conversation, based on whether the numbers make it an asset or a distraction.

## 8. KPIs That Matter

| KPI | Definition | Working target (assumption) |
|---|---|---|
| **Completion rate** | Completed intakes / started intakes | >65%. Below 50%, fix the quiz before selling anything. |
| **Intake → panel conversion** | Panel purchases / intakes shown the CTA | 5-10%. This validates the core wedge and the rev-share model. |
| **Revenue per intake** | Total HealthPilot revenue / completed intakes | £2+ blended at maturity (base fee + overage + share). |
| **Clinic activation** | Clinics with 50+ completed intakes in their first 30 days live | >70% of signed clinics. A signed clinic with no traffic is a churn event in waiting. |

Secondary, tracked but not steered by yet: intake → consultation rate, red-flag rate (safety monitoring, expect 1-3%), per-clinic month-2 retention, AI cost per intake.

Everything upstream of these four numbers is activity. These four are the business.

---

**Bottom line:** HealthPilot is a real product with a real revenue seam, sitting on top of a mature distribution platform, at the exact moment that platform has strategic attention on it. The model is base SaaS for predictability, per-intake for margin protection, and conversion share for upside. The next 90 days are about one thing: attributed revenue from live clinics. Prove the 8% panel conversion and everything else in this document is conservative.
