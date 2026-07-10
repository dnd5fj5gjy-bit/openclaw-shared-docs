# Line-by-line review — 30 findings, all fixed

Full review of the four go-live commits (landing page, quiz scroll fix,
customisation layer, supplement funnel), 25 files. 30 concrete issues found and
**all 30 fixed** in commit `ea46f54`. Verified: `nest build` + `vite build` +
`tsc` clean; 12 server + 49 frontend tests pass.

## High severity (ship-blockers)

1. **`/dashboard/supplements` crashed on render** — `useCart()` throws when no `CartProvider` is present, and the patient dashboard tree has none. Fix: wrap the route in `<CartProvider>`.
2. **Cross-tenant leak in recommendation sync** — `syncRecommendationsFromSlugs` read the catalogue with no clinic scope on the webhook/clinician paths (no ambient tenant context), returning every clinic's products (and throwing under strict mode). Fix: run the read + writes inside `runWithClinicContext(clinicId)`.
3. **Orphan recommendations** — the upsert bypassed the tenant orphan guard and could store `clinicId = NULL` (invisible to every clinic). Fix: the same context wrap + refuse when no clinic resolves for the patient.

## Medium severity

4. **Re-sync un-dismissed a dismissed supplement** — a patient's dismissal silently reappeared on the next quiz sync. Fix: stop clearing `dismissedAt` on update.
5. **No transaction** around the recommendation upsert loop (partial writes on failure). Fix: one `$transaction`.
6. **`supplementsEnabled` never enforced server-side** — the API served clinics that never opted in. Fix: gate the patient endpoints on the clinic flag.
7. **Missing Patient foreign key** on `PatientSupplementRecommendation` (orphans on patient deletion). Fix: FK to `Patient(uid)` with cascade.
8. **Public homepage text was unbounded/unsanitised** — a clinic admin could store megabytes into `aboutBody`, and `serviceCardOrder` accepted any CSV. Fix: server-side length clamps + validate the card keys.
9. **`recommendationSlugs` unvalidated** — a stray space/uppercase made a slug silently never match. Fix: enforce a snake_case CSV format.
10. **Quiz scroll parked the question under the sticky header** — `scrollIntoView` aligned the iframe top flush with the viewport, hiding the first ~64px behind the dashboard header. Fix: `scroll-margin-top`.
11. **Quiz scroll used a fragile 80ms timer** that raced the height resize. Fix: drive the re-align off the committed frame height (no magic number).
12. **Editor always pinned `serviceCardOrder`** — so a pathway enabled later was forced to the end of the card list. Fix: persist the order only when it differs from natural order.
13. **Editor preview ignored "homepage off"** — toggling it off still showed the landing. Fix: show a placeholder for the off state.
14. **Supplements page had no error UI** — a failed fetch masqueraded as "nothing available". Fix: distinct error state with retry.
15. **Recommendations pop-in / heading flip** on load (layout shift). Fix: gate on both queries loading.
16. **Dangling "More supplements" heading** when there were recommendations but no other catalogue items. Fix: hide the section when empty.
17. **Add-to-basket on an unpriced product** — a variant with no price still showed the buy button. Fix: require both variant and price.
18. **Trust section had no heading** (accessibility h2→h3 gap). Fix: add the section `<h2>`.
19. **Non-6-digit-hex brand colours silently broke the hero wash/borders** (alpha-hex string concat produced invalid CSS). Fix: normalise brand colours to 6-digit hex.
20. **Server test gave false confidence** — the "cross-clinic" test only exercised the null branch. Fix: added tests for the enabled-gate, no-un-dismiss, no-clinic refusal, and dismiss ownership.

## Low severity / polish

21. **Platform logo leaked onto white-label landings** with no clinic logo. Fix: render the clinic name as a wordmark instead of the Ted's logo.
22. **Contrast maths could pick unreadable text** on a light non-hex primary. Fixed via the hex-6 normalisation (#19).
23. **`source` unvalidated** vs its `VARCHAR(32)` column. Fix: constrained to a union type.
24. **No rate-limits** on the supplement routes (the peer module throttles). Fix: `@Throttle` on every route.
25. **Schema index/unique gaps** — redundant `patientId` index; no `unique(clinicId, medusaVariantId)`. Fix: both corrected.
26. **Dismiss was implemented in the API client but not wired** into the UI. Fix: dismiss control + query invalidation.
27. **`formatPence` was naive** (no thousands separator, negatives rendered). Fix: `Intl.NumberFormat` GBP, clamped ≥ 0.
28. **Editor preview ignored the external-homepage URL**. Fix: show an "external redirect" placeholder.
29. **Toggle label not associated** with its control (a11y). Fix: `htmlFor`/`id` wiring.
30. **Hero-image `url()` escaping only handled quotes** — now also escapes backslashes/parens/whitespace as defence in depth (the scheme is already gated). Also documented the preview-only authenticated CTA branch.
