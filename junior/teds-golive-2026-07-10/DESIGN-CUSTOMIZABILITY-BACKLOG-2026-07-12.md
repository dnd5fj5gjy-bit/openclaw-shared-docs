# White-Label Look & Feel + Customizability Backlog
Date: 2026-07-12 · Branch `feat/supplement-commerce` · Read-only audit (agent a048678b)
Feeds the continuous improvement loop (stage 4 backlog burn-down). Motion/smoothness = standing acceptance criterion.

## Bottom line
Color/logo/landing customization is already premium-grade (ClinicHomepage fully token-driven, real live preview).
The demo-visible credibility gaps: (a) fonts silently don't work, (b) charts stuck in Ted's blue, (c) editor
won't let admins preview or set what premium buyers ask for first (fonts, presets, their whole site).

## Top 10 (ranked)
| # | Title | Lens | Location | Effort | Fix type |
|---|-------|------|----------|--------|----------|
| 1 | Custom font never applies to the app (token set, never consumed) | custom | `clinic-brand.tsx:439` sets `--font-family`; `styles.css:266` hardcodes body font, no `var(--font-family)` | S | FIXABLE NOW |
| 2 | No font control in branding editor | custom | `clinic-settings.branding.tsx` (no typography section) | M | design-decision then fix |
| 3 | Charts ignore clinic brand | look+custom | `analytics.health-quiz.tsx:67` `CHART_BLUE='#2563EB'` (fill :290); `--chart-1..5` Ted's teal `styles.css:132` | S | FIXABLE NOW |
| 4 | Branding preview shows only Login + Dashboard | custom | `BrandingPreview.tsx:18-21` | M | fixable now (add landing/storefront tabs) |
| 5 | No per-clinic corner radius token | look+custom | `--radius:0.75rem` `styles.css:155`; no Clinic radius field | M | design-decision (schema) |
| 6 | No theme presets / starter templates | custom | none exist | M | design-decision |
| 7 | Supplement storefront has no product imagery | look | `supplements.tsx:194-265` text-only; `SupplementProduct` `lib/api/supplements.ts:13` no imageUrl | M | design-decision + fix render |
| 8 | Dark mode defined but dormant, not a WL option | look+custom | `.dark` theme `styles.css:169`; cookie default dark `cookies.const.ts:4`; no toggler; editor locks bg `#ffffff` `branding.tsx:121,278` | M | design-decision |
| 9 | Patient support hardcoded to Ted's | custom | `_app.tsx:107` `support@tedshealth.com`; `supportEmail` editable but unused on patient footer | S | design-decision (policy/compliance) |
| 10 | Loading states plain text, not skeletons | look | `analytics.supplements.tsx`/`supplements.tsx`/`ClinicHomepage` use "Loading..." | S | FIXABLE NOW |

## Customizability gap map (surface -> brand-inherited?)
- Public landing ClinicHomepage: YES (excellent)
- Homepage editor: YES (real live preview, best surface)
- Patient dashboard: YES
- Login/signup: PARTIAL (`bg-gray-50` hardcoded `_app._auth.signup.tsx:50`)
- Supplement storefront: PARTIAL (no product imagery)
- Analytics health-quiz: HARDCODED (CHART_BLUE)
- Analytics supplements: PARTIAL (CSS-bar placeholder, brand-aware)
- Charts globally (--chart-1..5): NO (default teal, brand never overrides)
- Typography/fonts: HARDCODED/BROKEN (--font-family never consumed; no editor control; only quiz embed maps fontKey)
- Corner radius: NO
- Page background light/dark: LOCKED (editor forces #ffffff)
- Quiz embed: YES send-side (buildEmbedTheme); receiver confirm pending Felix
- Emails: PARTIAL (header img/footer/support editable; templates central)
- Legal pages: NO ("Managed by Ted's Health" controller `clinic-settings.legal.tsx:33`)
- Patient support contact: HARDCODED
- Favicon/logo/logoScale: YES (upload + crop, safe-URL gated)
- Custom CSS: YES (sanitized `@layer clinic-overrides`)

## Quick wins (safe, mechanical — batch into a cleanup/design pass)
- Wire `--font-family` into body/heading stacks in styles.css (#1) [pair with #2 for full value]
- Drive chart fills from brand `var(--primary)`/`--chart-*` instead of CHART_BLUE + brand-set the chart tokens (#3)
- Skeleton components instead of "Loading..." on storefront/analytics/homepage (#10)
- Signup `bg-gray-50` -> brand background (#2 map row)
- Consolidate duplicated `lighten/darken` + card-color logic shared by `clinic-brand.tsx:355-395` and
  `usePreviewStyles.ts:24-40` into one shared module (kills preview/live drift) — pure refactor

## Needs design/product decision first
- Font picker UX + curated premium list (#2)
- Radius schema field + control (#5)
- Preset theme gallery: which presets, storage (#6)
- Product imagery: add imageUrl to SupplementProduct + upload flow (#7)
- Dark mode: per-clinic option vs remove dead `.dark` theme (#8)
- Patient-facing support/legal clinic identity vs central Ted's (#9) — compliance-governed

## Premium opportunities (worth a premium price)
Preset theme gallery; real typography system; radius/shape dial; per-clinic dark mode; unified live preview across
landing+dashboard+storefront+quiz; storefront imagery + richer cards; brand-kit export; secondary/tertiary color +
gradient controls.

## Motion note
Landing has restrained tasteful transitions (compliant with "smooth movements" bar). Elsewhere minimal — do NOT
over-animate a medical product; apply smooth easing to state/page/quiz-step transitions, honor prefers-reduced-motion.
House rule: no drawn cartoon human figures — currently COMPLIANT.
