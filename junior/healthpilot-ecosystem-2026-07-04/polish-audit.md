# HealthPilot Frontend — Luxury Polish Audit

Date: 4 Jul 2026. Branch: `feat/product-upgrade` (base 3891021). Local commits only.
Judged against the concierge register in BOTH presets. Verdicts: **pass** (already at bar) or **fixed**.

## Cross-cutting theme layer (globals.css) — FIXED
- No `prefers-reduced-motion` support anywhere → added global reduce block (kills animation/transition durations, both presets).
- No visible keyboard focus on custom controls; choice cards use `sr-only` inputs so focus was invisible → added palette-driven `:focus-visible` outlines (2px, `--ring`) plus `.sr-only:focus-visible + label` / `label:has(.sr-only:focus-visible)` so radio/checkbox cards show focus. Concierge redefines `--ring` to gold, so focus follows the preset automatically.
- Concierge preset only remapped arbitrary hex classes; token-styled components (Button default, Alert, Card) still rendered brand teal inside concierge → concierge scope now retints the full shadcn token set (background, foreground, card, primary=gold-deep, ring=gold, border, muted...).
- Contrast: brand teal-500 `#14b8a6` is 2.49:1 on white — fails AA even for large text; it was the fill of every primary CTA in the quiz. All quiz-flow solid CTAs, links and the progress fill moved to deep teal `#0f766e` (5.47:1), hover `#115e59`. Concierge mappings added (`.bg-[#0f766e]` → gold-deep, `.hover:bg-[#115e59]` → gold-press `#7a5f33`, borders → gold).
- Concierge gold-deep `#8c6f3e` was 4.44:1 on the ivory ground (11px overlines) → deepened to `#856a3b` (4.8:1 ivory, 5.09:1 white; white-on-gold CTAs 5.1:1).

## Landing / welcome screen (`WelcomeScreen.tsx`) — FIXED
- Hero subtext `#6bb0a2/80` was 2.51:1 on white → `#2f7265` (5.65:1), teal register kept; concierge maps it to muted ink.
- Blood-test CTA label was teal-500 text on white (2.49:1) → deep teal; hover border matched and concierge-mapped.
- Guided-check primary CTA moved to AA deep teal; shadow tint follows.
- Trust highlight descriptions were 11px bold grey → 12px semibold (legibility).
- Keyboard access: card click bubbles from the real inner button — pass.

## Question steps: choice / multi-select / boolean / text / number / slider / textarea / select / date (`DynamicStep.tsx`) — FIXED
- Continue and Skip CTAs, Back link, required asterisk to AA deep teal; Back link given a real touch target.
- Redundant per-input `focus:ring-[#14b8a6]` classes removed — inputs now use the token ring (preset-aware, gold under concierge).
- Validation copy de-bureaucratised: "This field is required" → "Please share this before continuing"; "Please select an option" → "Please choose an option to continue"; boolean variant matched. Errors get `role="alert"` and AA red `#B42318` (destructive `#ef4444` is 3.76:1 — fails).
- Selected-card treatment (charcoal-teal `#08514e`, 9.1:1) — pass, untouched (tests assert it).
- Empty state ("No questions are required for this step...") — pass.
- Slider: aria-label present, gold retint via CSS vars — pass.
- Sticky footer, 56px targets, mobile stacking — pass.

## Progress indication (`DynamicWizard.tsx`) — FIXED
- Progress bar had no semantics → `role="progressbar"` with valuemin/max/now and human `aria-valuetext` ("Step 2 of 7"). Fill to AA deep teal (concierge: thin gold line unchanged).
- Concierge editorial step numbering ("02 — About you") — pass.

## Wizard chrome — FIXED
- Close (X) button unlabelled, 40px → `aria-label="Close the health check"`, 44px target, calm 300ms hover.
- Initial loading: "Loading Health Check..." with pulsing text → "Preparing your health check…" with `role="status"`, spinner marked decorative, deep-teal spinner (concierge-mapped). Test updated to match copy.
- Config-unavailable state was an amber admin box ("Intake Is Not Available") → register-consistent white card, invitational copy ("The health check is not available right now... Please try again in a few minutes.").

## Resume-draft prompt — PASS
Toast "Resumed where you left off / We restored your saved answers" — right register, no change.

## Blood-test field (`BloodTestField.tsx`) — FIXED
- Copy: "Login to upload" → "Log in to upload"; "Supported format: PNG, JPG, PDF" → "Supported formats: PNG, JPG and PDF"; "Date of Blood Test" → sentence case.
- Upload/order CTAs to AA deep teal; error box gets `role="alert"`; file icon decorative.
- Drop zone is a real button (keyboard + new global focus ring) — pass.

## Date picker (`ui/date-picker.tsx`) — FIXED
- No Escape handling, no popup semantics, label not associated → Escape closes and restores focus to trigger; `aria-haspopup="dialog"` + `aria-expanded`; label wired via `useId`; month nav buttons labelled ("Previous/Next month") and enlarged to 40px.
- Selected/today/hover states from teal-500 to AA deep teal; error text `text-red-500` (3.3:1) → `#B42318` with `role="alert"`.
- Removed pre-existing unused Button import.

## Review / skipped-answers step (`ReviewAndGenerateStep.tsx`) — FIXED
- Generate CTA was h-10 admin-sized → min-h-12, rounded-xl, AA deep teal.
- "Answer now" link and Back link: AA colour + expanded hit areas.
- Skipped-section amber treatment (amber-800 on amber-50, 6.8:1) — pass.

## AI generation / loading sequence (`SummaryLoading.tsx`) — FIXED
- Stage label now `aria-live="polite"` so screen readers hear pipeline stages; progressbar semantics already present — pass.
- Icon/fill retinted to deep teal; icon marked decorative. Concierge editorial treatment (thin gold line, small-caps stage) — pass, untouched.
- Backend stage labels (Analysing your health profile / Running safety checks...) — pass.

## Error and retry state (`SummaryError.tsx`) — FIXED (rebuilt)
- Was bare shadcn admin tokens: "Something went wrong" + destructive alert + "Try Again". Rebuilt in the product register: soft error mark, "We couldn't prepare your summary", reassurance card ("Your answers are safe"), full-width Try again (56px, AA), Save and continue later / Contact support (48px), British English throughout, `role="alert"` on the header. Concierge inherits via token retint.
- Error message from the wizard still rendered verbatim (test contract kept).

## Red-flag / urgent-care interstitial (`UrgentCareScreen.tsx`) — FIXED (minor)
- Copy, 999/111/Samaritans cards, hierarchy — pass (already excellent).
- Added `role="alert"` on the header, decorative icons hidden, return CTA to AA deep teal.

## Age-restriction screen (`AgeRestrictionScreen.tsx`) — FIXED (minor)
- Copy and structure — pass. Icons decorative; CTA to AA deep teal.

## Summary / Health Report on screen (`GeneratedHealthSummary.tsx`) — FIXED
- Reveal was `zoom-in` (springy) → calm fade/rise, 500→(concierge 350ms).
- Primary CTA h-10 → h-12; secondary actions h-9/h-10 → h-11 (44px touch); all to AA deep teal with concierge gold mapping.
- Blood-panel wedge CTA: AA colour, h-11 — otherwise pass.
- Concierge editorial report on screen — pass.

## Print output (`HealthReport.tsx` + print CSS) — FIXED (real bug)
- `data-hp-print="report"` was never applied anywhere, so the print stylesheet's serif headings, `break-inside` rules and running-footer padding never fired. Now set on the print-only report wrapper.
- Report gold overlines to `#856a3b` for AA. Cover, numbered sections, footer disclaimer — pass.

## Post-summary next steps (`RecommendedNextSteps.tsx`) — FIXED (copy only)
- "Personalized to Your Data" → "Personalised to your data". Rest out of quiz-flow scope.

## Mobile layouts — PASS
Sticky footer stacks (Back / Skip / Continue), `pb-40` scroll clearance, cards single-column at `sm`, concierge card padding responsive (2.75rem → 3.5rem at md). No change needed.

---

## Commits (on `feat/product-upgrade`, local only)
- `c208285` feat(theme): accessible focus rings, reduced-motion support, concierge token retint
- `f8b6c2e` feat(wizard): calm loading and unavailable states, AA contrast, a11y chrome
- `4fbc717` feat(summary): calmer motion, print report attributes, redesigned error state
- `66e8f18` fix(interstitials): alert semantics and AA CTA colour on red-flag and age screens
- `c0bffbd` feat(review): larger generate CTA, AA links, wider touch targets
- `554138c` fix(landing): WCAG AA hero subtext and CTA colours on the welcome screen
- `ecb0df8` feat(fields): blood-test field copy polish, date picker keyboard and dialog semantics
- `50a0ce7` fix(next-steps): British English badge copy
- `bab36ee` fix(theme): deepen concierge gold-deep for AA overlines on ivory
- `7cd1???` chore(date-picker): drop unused Button import

## Verification
- `npx tsc --noEmit` — clean.
- `npx vitest run` — 39 pass / 13 fail, failure set diffed against base 3891021: **identical** (all 13 pre-existing checkbox/infinite-loop suite failures; zero regressions). One test updated for the new loading copy.
- `npm run build` — succeeds.
- Contrast ratios computed programmatically (WCAG relative luminance) for every colour decision.

## Deviations / not done
- Brand teal-500 remains on non-quiz surfaces (dashboard, blood-analysis pages, login) — out of scope per brief; they fail AA the same way the quiz did.
- 13 pre-existing test failures on the branch base were left as-is (not introduced here).
- `--destructive` token left at `#ef4444` globally; quiz-flow error text uses explicit AA red instead, to avoid rippling through non-quiz surfaces.
