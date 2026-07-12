# Dependency Security Remediation — Go-Live Branches
Date: 2026-07-12 · Conservative pass (npm audit fix, no --force; revert-if-not-green). For Felix handover. CONFIDENTIAL/local.

## Safely fixed + committed (lockfile-only, non-breaking, verified green)
| Repo | Before (C/H/M/L) | After | Commit |
|------|------------------|-------|--------|
| health-pilot-frontend (harden/frontend-golive) | 2/12/6/2 (22) | 2/1/2/0 (5) | c9e4457 |
| health-pilot-backend (harden/backend-golive) | 1/17/10/1 (29) | 0/3/0/0 (3) | e119019 |
| th-whitelabel frontend (feat/supplement-commerce) | 3/18/11/4 (36) | 0/1/4/0 (5) | ab4f786 |
| th-whitelabel server (feat/supplement-commerce) | 4/25/32/7 (68) | 2/17/20/3 (42) | dc5fc71 |

th-whitelabel server: bullmq 5.53.1->5.80.2 broke tsc (JobProgress not assignable to number). Fixed 4 assignment sites
(queue.service.ts:117,157; line-item-event-queue.service.ts:225; email-queue.service.ts:204) via
`typeof job.progress === 'number' ? job.progress : 0`, ran npm audit fix (no --force). 68->42 (crit 4->2, high 25->17),
tsc clean, jest 1419 pass/26 pre-existing. Remaining need --force/majors: @nestjs/cli->webpack chain, @google-cloud/storage
chain = FELIX.

## Remaining — NEEDS FELIX (major/breaking bumps, per-package decision)
### #1 GO-LIVE PRIORITY — health-pilot-frontend `next` 16.1.6 -> 16.2.10
Only production-facing, internet-exposed HIGH left. NON-major minor bump (safe; blocked only by the pinned `^16.1.6` range).
Clears ~19 advisories incl. HTTP request smuggling, Server-Actions CSRF bypass, SSRF, cache poisoning. **Bump first.**
### Others (Felix, per-package)
- hp-frontend: vitest + @vitest/ui on `4.x-beta` -> stable 4.x (CRIT but DEV-ONLY, no prod exposure).
- hp-backend: bcrypt 5.1.1 -> 6.0.0 (major, hash-compatible, drops old Node; verify login/hashing) — resolves bcrypt + @mapbox/node-pre-gyp + tar chain.
- th-frontend: onfido-sdk-ui major bump (picomatch HIGH + moderates) — it's the KYC/identity SDK; needs QA of the verification flow.
- th-server (if bullmq fix reverts): @nestjs/cli 11.0.24 + @nestjs/platform-express 11.1.28 majors (express/multer/path-to-regexp/glob/tmp/webpack) — Nest framework major, full regression needed.

## Method note
`npm audit fix` is all-or-nothing per package tree; where one bad bump was bundled with good ones, the whole set was reverted
to keep trees green (green tree mandatory). No `--force`, no hand-bumped majors, no app-code changes except the bullmq typing.
