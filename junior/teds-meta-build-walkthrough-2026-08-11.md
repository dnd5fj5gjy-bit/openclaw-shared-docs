# Building it in Ads Manager
## Ted's Health, weight management. Every screen, every setting.

**11 August 2026. Companion to the setup document.**

Meta merged the manual and Advantage+ flows in February 2026, so there is now one build path rather
than two. Everything below is that path. Where a default is right, I say take it. Where the default
will cost you money, I say why.

---

### Before you open Ads Manager

Three things, or the build is wasted.

1. **Conversions API live.** Since April 2026 the conversion-leads goal *requires* it. Not optional,
   not a nice-to-have. Pixel plus CAPI, deduplicated on event ID.
2. **Domain verified** in Business Settings, and Aggregated Event Measurement configured with your
   deepest event ranked first.
3. **Your 30 ads renamed** before upload, in the convention at the bottom of this document. Thirty
   files called `final_v3_NEW.mp4` is how a test becomes unreadable.

---

## LEVEL 1 — THE CAMPAIGN

You build one. Not one per concept, not one per angle.

| Setting | What to choose | Why |
|---|---|---|
| **Buying type** | Auction | Reservation is for reach buys, not this |
| **Objective** | **Leads** | Not Traffic, not Engagement. Traffic buys you clicks from people who never convert, and it is the most common way to waste a health budget |
| **Special ad category** | **Leave it OFF** | Health is not a special ad category in the UK. Ticking it wrongly strips your targeting and reporting for no reason. Only credit, employment, housing and social issues belong there |
| **Campaign name** | `TEDS_WM_PROSPECTING_2026-08` | Date it. You will run several |
| **Advantage campaign budget** | **ON** | Budget lives at campaign level and Meta moves it to the ad set that is working. This is the setting that stops you hand-feeding a loser |
| **Campaign budget** | Your daily number | See the arithmetic in the setup document. Whatever it is, it goes here, not at ad set level |
| **A/B test toggle** | OFF | You are not running a formal split test. You are running concepts against each other inside one ad set |

Set the campaign spending limit if you want a hard ceiling. It is worth doing on a first campaign in a
regulated category.

---

## LEVEL 2 — THE AD SETS

This is where the real decisions are. Build **one** to start. Add a second only when the first is
funded to 50 conversions a week and still has headroom.

### Conversion location — the decision that matters most

Meta will offer you **Website** or **Instant form**. Take **Website**.

Instant forms are seductive. They prefill name, email and phone from the profile, so the cost per lead
looks superb and you will be tempted to celebrate. In a medical funnel they are usually a trap:
someone taps twice without reading, never completes screening, never gives bloods, never becomes a
patient. You buy a spreadsheet, not a caseload.

Website sends them to a real eligibility screener. Fewer leads, dramatically better ones, and the
screener does qualifying work that your care team would otherwise do by phone.

**Use instant forms only if** your team has capacity to call every lead within minutes. If they do,
instant forms plus fast phone follow-up genuinely wins. If they do not, it is a lead graveyard.

### The rest of the ad set

| Setting | What to choose | Why |
|---|---|---|
| **Performance goal** | Maximise number of conversions | Not link clicks. Not landing page views |
| **Conversion event** | The **deepest** event you can generate 50 of a week | "Consultation booked" or "screening complete" beats "form submitted". If you cannot hit 50 a week on the deep one, step back one event, not five |
| **Ad set name** | `AS_BROAD_UK_18+_v1` | |
| **Budget** | Nothing here — it sits at campaign level | Because you turned on Advantage campaign budget |
| **Schedule** | Start tomorrow 00:00, no end date | Never start mid-afternoon. You get a partial first day and a distorted first read |
| **Location** | United Kingdom | Then open the dropdown and pick **"People living in this location"**, not the default "People living in or recently in". Tourists do not start a course of treatment |
| **Age** | **25 to 65+** | 18 is the legal floor and it must never be lower. 25 is the commercial floor: under-25s convert badly on a paid medical programme |
| **Gender** | See note below | |
| **Advantage+ audience** | **ON, with no suggestions** | Leave the interest box empty. There is no usable health interest targeting any more, so anything you type in is a worse guess than Meta's. An empty box is a decision, not laziness |
| **Placements** | Advantage+ placements, then **manually exclude Audience Network** | Advantage+ is right for about 90% of campaigns, but regulated categories are the recognised exception. Audience Network puts a CQC-registered clinic next to whatever a third-party app is showing. Exclude it |
| **Attribution setting** | 7-day click, 1-day view | The default, and correct here. Note Meta removed the 7-day and 28-day view windows on 12 January 2026, so one day is the longest view window that exists now. A medical decision takes more than a day to make, which is exactly why you keep the 7-day *click* |

**On gender.** Ted's is a men's health clinic. If the weight management service only treats men, that
is not a targeting preference, it is a service constraint, and it belongs in the creative and the
screener as well as the setting. Do not rely on Advantage+ to hold a line that your intake process
should be holding. If the service treats everyone, leave it on All and let the creative do the work.

**Exclusions.** Upload your existing patient list as a Custom Audience and exclude it. You have around
97 active patients. Paying to re-acquire them is money set on fire, and the same list is your best
lookalike seed later.

---

## LEVEL 3 — THE ADS

Six ads in the ad set. One per concept. The other 24 wait.

| Setting | What to choose |
|---|---|
| **Identity** | The Ted's Health Facebook Page and the linked Instagram account. Both, always |
| **Ad name** | `CONCEPT_FORMAT_HOOK_v1` — see convention below |
| **Format** | Single image or single video. Not carousel for cold traffic in this category |
| **Creative source** | Manual upload. Turn **off** Advantage+ creative enhancements |
| **Primary text** | Your copy. Front-load the first line, it is all most people read |
| **Headline** | Short. The clinic promise, not the medicine |
| **Description** | Usually ignored by the placement. Fill it anyway |
| **Call to action** | "Learn more" or "Book now". Not "Shop now" |
| **Website URL** | The screener, with UTM parameters |
| **URL parameters** | `utm_source=facebook&utm_medium=paid&utm_campaign=wm_prospecting&utm_content={{ad.name}}` |

**Turn off Advantage+ creative enhancements.** Normally I would leave them on. Not here. They let Meta
restyle text, add overlays, crop, and generate variations, and in a category where the exact wording
is the difference between a compliant and a non-compliant ad, you do not hand the wording to an
automated system. This is the one place I would take worse performance for control.

**Every ad gets checked against the drug-name list before it is published.** Thirty ads is thirty
chances to get the Page restricted.

---

### Naming convention for the 30

`CONCEPT_FORMAT_HOOK_VERSION`

- `WILLPOWER_VID_MIRROR_v1`
- `WILLPOWER_IMG_MIRROR_v1`
- `DOCTORLED_VID_BLOODS_v1`
- `TRIEDEVERYTHING_IMG_SCALES_v2`

The first token is the only one that matters for reading results. When you look at the report you want
to see whether `DOCTORLED` beat `WILLPOWER`, because that tells you what to make next. Knowing that
`final_v3_NEW` beat `final_v2` tells you nothing.

---

## The first fortnight

**Day 0.** Publish six ads in one ad set. Do not touch anything.

**Days 1 to 3.** Ignore the numbers. You are in learning, the data is noise, and every edit resets it.
The urge to intervene on day two is the most expensive instinct in this whole exercise.

**Day 4.** First look. Check delivery is spread across at least four of the six ads. If one ad has 80%
of spend and the rest are starved, that is Meta having decided early rather than a real result.

**Day 7 to 10.** First real read, once you are out of learning. Kill the bottom two ads. Promote the
next execution of whichever concept is winning. Do not add a new concept yet.

**Week 3.** Now add the second ad set, if and only if the first is funded to 50 conversions a week and
still has room. Otherwise keep consolidating.

**Ongoing.** One creative refresh a week from the 24 held back. Creative fatigue, not audience
exhaustion, is what kills accounts in this category.

---

### The five ways this goes wrong

1. Thirty ads in one ad set on day one. You pay for all thirty and learn about four.
2. Splitting a small budget across many ad sets. Nothing ever leaves learning.
3. Optimising for form fills, then wondering why nobody completes screening.
4. Editing on day two and resetting learning, repeatedly.
5. A drug name slipping through in ad 27 of 30, or in a comment nobody moderated.

*Prepared by Junior, 11 August 2026.*

**Sources:** [Meta: about Advantage+ audience](https://www.facebook.com/business/help/273363992030035) · [Meta Transparency Center: health and wellness ad standards](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness/) · [GPhC enforcement notice, weight management prescription medicine ads](https://www.pharmacyregulation.org/about-us/news-and-updates/updated-enforcement-notice-issued-weight-management-prescription-medicine-ads) · [ASA/CAP: weight control, prescription-only medicines](https://www.asa.org.uk/advice-online/weight-control-prescription-only-medicines.html)
