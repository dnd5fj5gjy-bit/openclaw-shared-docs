# Harborview Demo — Bug Diagnosis & Gap Analysis (13 Jul 2026)

Reproduced against the live tunnel with a headless browser (mirrors Jesse's experience).

## Bug 1 — Quiz never loads (CSP block)
The public quiz (`/health-assessment`) embeds the HealthPilot app as an iframe from the HealthPilot tunnel origin (`creative-dare-parks-firewall.trycloudflare.com`). The landing page's Content Security Policy is `frame-src 'self'`, so the browser blocks the iframe:
`Framing '...trycloudflare.com' violates CSP directive "frame-src 'self'"`. Iframe resolves to `chrome-error://chromewebdata/`. Result: the quiz is blank/broken.
**Fix:** add the HealthPilot tunnel origin to the frontend CSP `frame-src` (and serve `frame-ancestors` via header, not meta) at build time.

## Bug 2 — Login broken for ALL remote users (auth points at localhost)
Staff + patient sign-in calls the Firebase Auth emulator at `http://127.0.0.1:9099`. Baked into the build. Through the tunnel, `127.0.0.1` is the *visitor's own device*, not the Mac Studio, so every login fails: `FirebaseError: auth/network-request-failed`. Consequence: the entire authenticated surface — patient dashboard, staff clinic-settings/branding back-end, clinician portal — is unreachable remotely. This is why Jesse cannot get into the customization back-end.
**Fix:** point `VITE_FIREBASE_AUTH_EMULATOR_URL` at a tunneled auth-emulator origin (or a real Firebase project), rebuild.

## Gap 3 — No public product catalog / shop
All purchase surfaces are under `/dashboard/*` (login-gated) or inside the quiz/onboarding funnels:
- `dashboard/blood-tests.buy-one-off.*` (Wellman, Testosterone)
- `dashboard/consultations.buy-one-off`
- `dashboard/supplements`
- `_app.treatments.*` (ED onboarding, TRT diagnosis funnels)
There is NO public route to browse and buy blood tests, pathways, or supplements without logging in and going through the quiz. This is a genuine missing feature, not a bug.
**Build:** a public Shop/Store (browse all products → add to cart → checkout via the existing Medusa/Ryft payment stack), reachable from the landing nav, no quiz required.

## Root cause theme
This is a local demo rig exposed through throwaway `trycloudflare` tunnels. It's wired to run on the Mac locally (localhost auth, self-only CSP), so over a remote tunnel it half-breaks, and the tunnel hostname changes on every restart (hence the earlier dead link). It is not a stable deployment.

## Recommended path
1. Rebuild the demo correctly wired for remote (auth + CSP + API + HP origins) so login and quiz work, on a stable named tunnel that doesn't change → Jesse can log in and customize the landing from Clinic Settings > Branding + Homepage.
2. Build the public Shop (blood tests, pathways, supplements, no quiz) into the repo.
3. Ship as PRs for Felix if production-grade is wanted, consistent with the rest of the HealthPilot work.
