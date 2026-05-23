# Modern Savage — Launch War Room

**T-minus 39 days to July 1, 2026** · Status as of May 23, 2026 (overnight verification)

This is the single command-center view of the July 1 launch. Everything that can stop the launch, ranked, with live status, owner, and the date it must clear. Built from a fresh overnight re-verification of the hard blockers, not the May 11 snapshot.

---

## THE ONE-LINE READ

The launch collateral is done. The launch *infrastructure* is not. Four things can move July 1, and tonight's checks confirm **three of the four are still open**. The domain is the sharpest: it is not ours, it is transfer-locked, and it expires June 24 — seven days before we launch. That is the item I would put at the top of Monday.

---

## KILL-SWITCH BLOCKERS — VERIFIED TONIGHT

| # | Blocker | Live status (May 23) | Owner | Must clear by | Risk |
|---|---------|----------------------|-------|---------------|------|
| 1 | **modernsavage.com domain** | **NOT OURS.** WHOIS tonight: registrant still "Domains By Proxy" (privacy proxy), nameservers still GiantPanda (China parking), status `clientTransferProhibited` + `clientRenewProhibited`. Expires 2026-06-24. | CJ (via MediaOptions) | **June 10** (buffer before June 24 expiry) | 🔴 CRITICAL |
| 2 | **Modern Savage Ltd incorporation** | **NOT INCORPORATED.** Companies House search tonight returns only Modern Savage Industries / Productions / Laser Clinic — none are ours. The trading entity does not yet exist. | Raemy | **June 6** (so Stripe + customs can hang off it) | 🔴 CRITICAL |
| 3 | **Lightning Nutra ship date** | Unconfirmed (internal). Last known: CJ chasing Chris Liming. $82K deposit paid Apr 23-24. Standard lead time ships June 17–July 15. | CJ / Chris Liming | **Confirm by May 30; product landed + cleared customs by June 27** | 🔴 CRITICAL |
| 4 | **USPTO "Modern Savage" trademark** | Unverifiable tonight (USPTO search behind a bot wall). Last known: Kylee MacArthur offered to file under foreign entity May 7; green-light status unknown. | Raemy → Kylee | Confirm filed within 7 days | 🟠 HIGH |

**Why these four and nothing else:** every other launch asset (emails, pricing, press, influencer, social arc, fulfilment) is built and reversible. These four are the ones with hard external clocks and no workaround if missed.

---

## BLOCKER 1 — THE DOMAIN (read this first)

**What I found tonight, in plain terms:**
- `modernsavage.com` is owned by someone behind a GoDaddy privacy proxy. Parked on Chinese nameservers (GiantPanda). Not serving a real site.
- It is locked with `clientTransferProhibited` — meaning even if a deal is struck, the current holder must *unlock it first* before any transfer can complete. That adds days.
- It is locked with `clientRenewProhibited` and expires **June 24, 2026**. This cuts two ways: it may signal the holder intends to let it drop (good — it could be caught on expiry), or the locks are registrar-imposed and the registrar controls the timing (out of our hands).
- `clientRenewProhibited` plus a near expiry is the most interesting signal: if no deal closes, the domain enters the redemption/drop cycle ~30-45 days after June 24 — i.e. it would NOT be catchable before July 1 anyway.

**The decision this forces:**
1. **Primary path:** CJ closes the MediaOptions purchase before June 10. Budget is £2,000; if the holder counters above that, this is one of the three things worth interrupting Jesse for. Confirm MediaOptions is actively engaged — there has been no status change since May 11.
2. **Fallback that must be decided NOW, not on June 23:** launch on `modernsavage.co`. The `.co` is live, healthy, BGV-owned, expires 2031. It is a perfectly good launch domain. **The brand should not be held hostage to a `.com` we may never get.** Every email, every Bear post, every QR code should point to `.co` unless and until the `.com` is in our account and resolving.

**My call:** Treat `.co` as the launch domain of record today. Pursue `.com` in parallel as an upgrade, not a dependency. Do not let a $2k parked domain put a 39-day clock on a seven-figure launch.

---

## BLOCKER 2 — THE ENTITY (the quiet one that blocks everything downstream)

Modern Savage Ltd is not incorporated. This is the quiet blocker because it has no dramatic deadline of its own, but **three other things hang off it**:
- **Stripe** can't go live on a clean UK entity until the entity exists. (The IoM Bear Witness entity is excluded from UK Stripe — that was the original problem.)
- **UK customs / IPAFFS** import paperwork (the organ blend is POAO — see the May 15 customs brief) needs an importer of record.
- **Bank account** for UK receipts.

Counting backwards: Stripe verification can take 1-2 weeks, customs broker appointment needs the entity, so the entity must exist by **early June** to leave room. Same-day incorporation is possible at Companies House (£50 online), so this is a fast unblock once Raemy moves — but it has been open since at least May 11.

**Name-collision flag:** "Modern Savage Industries", "Modern Savage Productions", and "Modern Savage Laser Clinic" already exist on the register. "Modern Savage Ltd" itself appears free, but Raemy should confirm exact-name availability at filing — a too-similar-name objection would cost days we don't have.

---

## CRITICAL PATH — THE NEXT 39 DAYS

Sequenced by dependency, not by calendar. Each row blocks the rows below it.

| Window | Milestone | Depends on | Owner |
|--------|-----------|------------|-------|
| **By May 30** | Ship date confirmed in writing from Lightning Nutra | — | CJ |
| **By June 6** | Modern Savage Ltd incorporated | — | Raemy |
| **By June 6** | USPTO filing confirmed live | — | Raemy/Kylee |
| **By June 10** | `.com` acquired OR `.co` confirmed as launch domain of record | Entity (for registrar account) | CJ / Jesse |
| **By June 12** | Stripe live + test transaction passed | Entity | Raemy / Jesse |
| **By June 13** | Calvin SOW signed (no new paid work without it) | Jesse decision | Jesse |
| **By June 17** | Klaviyo connected, Email 1 armed, WhatsApp community live | Stripe live | Calvin |
| **By June 20** | Customs broker appointed + IPAFFS pre-notification ready | Entity, ship date | Jesse/CJ |
| **By June 24** | Influencer seeding boxes shipped (20 targets) | Product in hand | Calvin / Ships A Lot |
| **June 27** | Product landed UK + customs cleared | Ship date, broker | CJ |
| **June 29** | Soft launch to founding members / WhatsApp list | Stripe, email, product | Calvin |
| **July 1** | **PUBLIC LAUNCH** — Email 1 to list, Bear IG arc go-live, store open | Everything above | All |

**The critical path runs through the entity.** If Modern Savage Ltd slips past mid-June, Stripe slips, and the launch slips. It is the cheapest, fastest item to clear and it is gating the most. That is where I would apply pressure first.

---

## WHAT'S ALREADY DONE (so we don't re-spend energy here)

Confirmed built and on the dashboard: pre-launch email sequence (1-5), post-purchase sequence (OB-1 to OB-6), Klaviyo setup spec, WhatsApp community brief, soft-launch brief, influencer seeding list (20), Bear IG arc Phase 1, press brief, pricing brief (£59/mo UK recommendation), Kids Blend brief, 64-day launch calendar, packaging dimensions, UK customs/POAO brief, US legal sprint. The creative and content layer is not the risk. The operational/legal/infrastructure layer is.

---

## THE THREE THINGS WORTH INTERRUPTING JESSE FOR

Per the standing sailing-window rule, adapted to now:
1. **Domain holder counters above £2,000** — needs a yes/no on budget.
2. **Lightning Nutra ship date confirmed after June 27** — triggers the contingency plan (split shipment / air freight / soft-launch-only on July 1).
3. **Stripe entity decision stalls past June 10** — the launch date itself is then at risk and needs Jesse's direct push on Raemy.

---

## JUNIOR'S RECOMMENDATION

Three moves, in order:
1. **Make `.co` the launch domain of record today.** Stop treating `.com` as a blocker. It's an upgrade. This removes the single scariest item from the critical path in one decision.
2. **Get Raemy to incorporate Modern Savage Ltd this week.** It's £50 and same-day, and it's silently gating Stripe, customs, and banking. This is the highest leverage unblock available.
3. **Get the ship date in writing by May 30.** Everything physical keys off it. If it lands after June 27, we soft-launch July 1 on pre-orders and ship in waves — but we only know to plan that if we have the date.

The launch is in good shape on everything that's visible (content, brand, audience). The risk is entirely in the plumbing — and the plumbing is fixable inside a week if the entity and domain decisions get made now instead of in late June.

---

*Built overnight May 23, 2026. Blocker status 1, 2, 4 re-verified live tonight; status 3 is internal and last-known. Not yet validated with CJ/Raemy — confirm current state of each before acting.*
