# Modern Savage — 3PL Selection Brief
**Date:** May 27, 2026 | **T-35 to July 1 Launch**

---

## SITUATION OVERVIEW

Commerce architecture is now locked:
- **Stack:** Next.js / Vercel / Supabase (custom build - Felix confirmed)
- **Payments:** Stripe under Modern Savage Inc
- **QuickBooks:** SOLVED - Stripe's official QBO connector (built by Stripe, used by thousands of DTC brands, a few clicks in QBO marketplace once Stripe is live)
- **Delaware entity:** Ice Miller finishing documents now

**The one unresolved operational blocker: no 3PL has been selected or onboarded.**

ShipBob standard onboarding = 2-4 weeks. You need to sign by **May 29** at the latest to have fulfilment live for July 1.

---

## WHY THIS NEEDS A DECISION THIS WEEK

| Timeline | Milestone |
|----------|-----------|
| May 29 | 3PL signed — onboarding begins |
| May 30 | Stripe account set up (entity is ready) |
| Jun 2 | Lightning Nutra ship date confirmed (samples arrived, density test done) |
| Jun 17-25 | Inventory arrives at 3PL warehouse |
| Jun 27 | Soft launch test orders |
| Jul 1 | Full launch |

If the 3PL isn't signed by May 30, the domino collapses. You'll still launch but with manual fulfilment, which is a nightmare at any scale above 50 orders.

---

## 3PL OPTIONS COMPARISON

### Option 1: ShipBob (RECOMMENDED)
**Best fit for Modern Savage**

| Factor | Detail |
|--------|--------|
| Markets | US + UK (warehouses in both, single account) |
| Supplement experience | Handles dietary supplements, FDA-compliant storage |
| DTC track record | Industry standard for sub-10K orders/month DTC brands |
| Custom integrations | Full REST API - Felix can connect the custom backend directly |
| QuickBooks | Works natively via Stripe connector |
| Pick & pack | ~$3-5 per order |
| Storage | ~$40/pallet/month |
| Onboarding | 2-3 weeks from contract to receiving inventory |
| Subscription support | Handles repeat orders and subscription batches |
| UK fulfilment | UK warehouse means no customs issues for UK orders |
| Contact | partner@shipbob.com or shipbob.com/get-started |

**Verdict:** Single contract covers both US and UK. Felix can wire it in. No Shopify required.

---

### Option 2: ShipMonk
**Strong US option, no UK**

| Factor | Detail |
|--------|--------|
| Markets | US only (Florida HQ + 9 US locations) |
| DTC experience | Very strong. Subscription-native platform. |
| Custom integrations | REST API available |
| Weakness | No UK warehouse. UK orders need a separate solution or international shipping |
| Best for | US-only launch strategy |

**Verdict:** Good if you want to delay UK fulfilment. Means UK customers wait 7-14 days for delivery.

---

### Option 3: Huboo
**UK specialist**

| Factor | Detail |
|--------|--------|
| Markets | UK + EU (Bristol warehouse) |
| Supplement experience | Handles health/beauty products |
| DTC experience | Strong for UK DTC brands |
| Custom integrations | API available |
| Weakness | No US warehouse. US orders not practical. |
| Best for | UK-first or UK-only fulfilment |

**Verdict:** If you want the best UK experience, pair Huboo (UK) with ShipBob (US). Two 3PL contracts is operationally messier but optimises both markets.

---

### Option 4: ShipsAlot (Susan U - referenced in April)
**Status unknown**

This was referenced as the US fulfilment contact in April planning. No confirmation of whether this conversation is still live or dead. If Susan has already been engaged and given a quote, compare against ShipBob on price. If not, ShipBob is the safer default.

---

### Option 5: Stord / Bezos
**Pass for now**

Stord and Bezos (Amazon's 3PL arm) are newer, less proven for DTC supplement brands, and have no UK presence. Not recommended for July 1.

---

## RECOMMENDATION

**Sign with ShipBob this week.** One contract for both US + UK, supplement-native, REST API for Felix's custom backend, strong DTC subscription track record.

If the ShipsAlot conversation is already active and priced, compare costs - but only switch if they can beat ShipBob on price AND confirm UK capability.

---

## WHAT TO SEND SHIPBOB

When you reach out, tell them:
- DTC supplement brand, July 1 launch
- Two SKUs: adult blend (~600g, monthly subscription) and kids blend (~280g, monthly subscription)
- Launch volume estimate: 500-1,000 orders in month 1
- Warehouses needed: US (primary) + UK
- Integration: custom REST API (not Shopify)
- Timeline: inventory arriving mid-to-late June

Ask for: pricing proposal, onboarding timeline, and API documentation for their developer.

---

## UPDATED BLOCKER STATUS (May 27)

| Item | Status |
|------|--------|
| Delaware entity (Modern Savage Inc) | NEAR DONE - Ice Miller finishing docs |
| QuickBooks integration | RESOLVED - Stripe QBO connector |
| Commerce stack | RESOLVED - Next.js/Vercel/Supabase confirmed |
| Stripe account | BLOCKED ON ENTITY - set up once Ice Miller delivers |
| 3PL selection | OPEN - needs decision by May 29 |
| modernsavage.com domain | OPEN - still parked on GiantPanda, expires Jun 24 |
| Lightning Nutra ship date | NEAR RESOLVED - samples in transit, density test today |
| Salty Packaging order | BLOCKED ON density test - bag sizing unconfirmed |
| Founding Tribe email list | ACTIVE - Bear sent first email May 26 |

---

## JESSE'S DECISIONS THIS WEEK

1. **3PL: Sign with ShipBob (or confirm ShipsAlot if already in conversation)** - by Friday May 29
2. **Stripe setup: Confirm with Raemy once entity docs arrive from Ice Miller** - by end of week
3. **modernsavage.com domain: Push CJ on MediaOptions status** - hard deadline Jun 17

That's it. Everything else is running.

---

*Built by Junior, May 27 2026 — T-35 to launch*
