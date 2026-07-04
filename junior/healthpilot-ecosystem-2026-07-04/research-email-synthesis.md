# Ted's White-Label Build — Email Research Synthesis (4 Jul 2026, CONFIDENTIAL, never publish)

## What the offering is
Ted's Health (GSET Health Ltd) is pivoting from D2C to a CQC-registered white-label clinical backend for health operators. Jesse to Calvin (8 Apr): "power other clinics under their own brand, rather than compete for consumer attention against Numan and Manual." Stack: TH multi-tenant platform built by Felix (four views: patient, WL clinic owner, TH admin, doctor); SignatureRX (prescribing + meds, best-in-market pricing); Inuvi (blood labs); third-party phlebotomy; Ryft (payments); Tuli + Heim integrations; Dr Jonathan Andrews as CMO; MIAB insurance (MDU malpractice; NO run-off cover — unresolved gap).

WL TRT flow (Filmer, 26 Mar): partner screens patient (blood test or symptoms) → patient buys WL TRT diagnosis package (Baseline Blood Test + consult) → BBT → doctor consult → medication. TH forces its own BBT panel because "most [partners] dont actually test for all the right biomarkers we need to create a prescription." Principle: "the more flexibility we could give the potential partners, the more attractive the offering is… We're going to try and WL pretty much the whole flow."

## Status
Sandbox complete after 150+ bug tickets; go-live planned w/c 1 Jun with Ryft/SignatureRX/Inuvi/Tuli/Heim monitored. WL Service Agreement (from a Rimo Health template) with Ignition Law — contested clauses: controlled drugs 5.3, pricing 7.6, Ryft 8.5, data processing 10.9, indemnities, continuity of care 18.8. NOT finalized. Thomas Filmer (Head of Ops) resigned 23 Jun (~2 months left), still driving pricing/updates. Raemy owns financial model + legals; Johnny clinical; CJ commercial; Calvin's WL marketing strategy still missing. D2C base is small and shrinking: May revenue £5,642 (Apr £10,058), ~50 TRT + 74 ED actives; Cypionate renewal ≈ £480.

## Commercial
Voy (ex-Manual, $650M ARR): 1 Jul call with Max (Head of Men's Health) — wants Bear front-and-centre, open to buying Ted's (cash + equity). Bear's targets: become Voy's B2B arm at 75/25 rev share keeping ownership; or sell; and/or endorse Voy B2C for equity + rev share; "I would market it in India." CJ leads negotiation; NDA pending; Nikhil Kamath India angle floated. Prospect clinics: OM (first go-live candidate), Mint Health Clinic (Maggie Thomas, on hold), GymWolfPT (Ian Worthington, referral ambassador), Mike James. Market comp: Evaro — £250/month platform fee, partner earns 2.5% (branded) to 10% (unbranded) per prescription, Evaro owns the patient and data, integration via a simple script tag, NO blood testing capability. Blood testing is TH's differentiator.

## Pain points an AI intake layer addresses (email-evidenced)
1. Partner screening is broken: WL flow starts with partner screening but partners can't test the right biomarkers — a standardized AI symptom-screening layer routes qualified patients into the BBT+consult package (the paid wedge).
2. Drop-off: Miro board "pink notes to key drop off points"; May revenue fell on "a reduction in new patient intake" and long lag "between initial engagement and reaching the medication phase."
3. Cross-sell gap (Tom, 25 Mar): "missing some marketing opportunities/conversions from ED only to TRT… vital if we decide to push forward with the supplements too." No real CRM (SendGrid transactional only, Klaviyo dormant).
4. Prescriber documentation time: Filmer proposed a "regulated healthcare AI scribe" (£65/user/month Heidi, or Tandem) for consult docs and "legal defensive" transcripts. Structured AI intake feeding the doctor view attacks the same pain upstream.
5. Patient DD at scale (post Daily Mail sting): "aim to do as much DD on patients as we can… Easier said than done to do at scale." Auditable triage records = scalable DD.
6. Integration pattern: Evaro wins partners with a script-tag embed; HealthPilot's embeddable quiz matches the validated pattern, plus blood-test attach Evaro can't do.

## Constraints
- CQC registration is the core asset; regulated activity stays with TH. Data Processing Schedule under legal review — quiz data flows must fit it.
- Quiz screens, never diagnoses; TRT prescriptions require TH's full BBT panel. HealthPilot's own rule: prescription treatments require a HealthPilot-ordered or recognized-partner test.
- Patient/data ownership is the industry fault line (Evaro owns the patient); Ted's must decide where quiz data sits.
- Claims-made insurance, no run-off cover (unresolved). Thin unit economics. LegitScript compliance for content on partner sites.
- CJ has a "Health Pilot + Ted's Health - Marketing and Tech Update" Zoom Thu 9 Jul — this package is ammo for that call.
