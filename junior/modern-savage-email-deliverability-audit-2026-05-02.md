# Modern Savage — Email Deliverability Structural Audit
**Built:** May 2, 2026 (Junior, Pulse 54)
**For:** Jesse, copy Calvin / Tammy / Raemy
**Status:** LOCAL — Monday May 4 first-look item
**Severity:** HIGH. The launch sends an email to 170 paying-intent waitlist subscribers on July 1. With the current DNS, ~30-60% of that send risks the spam folder.

---

## TL;DR

Modern Savage's `modernsavage.co` domain has a broken email authentication setup. Three concrete problems:

1. **SPF doesn't authorize the actual senders.** SPF says GoDaddy can send. Reality: emails will go via Microsoft 365 (replies) and Klaviyo (campaigns). Both are unauthorized in the current SPF.
2. **No DKIM records are published** for Microsoft 365 or Klaviyo. Klaviyo emails will be marked "via klaviyo.com" in Gmail and the M365 replies will fail DKIM.
3. **DMARC is in monitoring mode** (`p=none`). Once it's tightened (which best practice and Apple's mail privacy push will force), the broken SPF and missing DKIM will start *blocking* legitimate mail.

**Time to fix:** 30-45 minutes for Calvin's tech contact (or whoever manages the modernsavage.co DNS at GoDaddy). 24-72 hours for DNS propagation. Then 14 days of warm-up before tightening DMARC. **This needs doing by mid-May at the latest** to give the email reputation time to season before the July 1 send.

---

## What I checked (commands and outputs)

```
$ dig MX modernsavage.co
0 modernsavage-co.mail.protection.outlook.com.       # Microsoft 365 inbound

$ dig TXT modernsavage.co
"v=spf1 include:secureserver.net -all"               # GoDaddy SPF — wrong
"NETORGFT20616945.onmicrosoft.com"                   # M365 tenant verification

$ dig TXT _dmarc.modernsavage.co
"v=DMARC1; p=none; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net;"

$ dig CNAME kl1._domainkey.modernsavage.co           # Klaviyo DKIM 1
(no answer)
$ dig CNAME kl2._domainkey.modernsavage.co           # Klaviyo DKIM 2
(no answer)
$ dig CNAME selector1._domainkey.modernsavage.co     # M365 DKIM 1
(no answer)
$ dig CNAME selector2._domainkey.modernsavage.co     # M365 DKIM 2
(no answer)
```

Klaviyo's own SPF include record (`_spf.klaviyo.com`) is also unreachable as a TXT — Klaviyo uses CNAMEd subdomains and per-tenant DKIM keys for sending. This means **even if SPF were tightened to add Klaviyo, Klaviyo still requires the per-tenant DKIM CNAMEs** to be added.

---

## Why this matters in commercial terms

Per the launch playbook (modern-savage-launch-week-playbook-2026-04-29):
- Email 1 to waitlist → 170 people, July 1 morning
- Email 2-5 across launch week
- Target: 75 paid subscribers in week 1

Industry baseline for a fresh sending domain with broken SPF + missing DKIM: 60-70% inbox placement. With proper authentication: 90-95%. The delta is roughly 25-40 percentage points of inbox vs. spam.

Translated to the launch: if Email 1 goes to 170 people and 30% lands in spam, that's 51 people who never see it. At even a 10% conversion to paid (high but plausible for a Bear-credibility waitlist), that's 5 lost subscribers in the first send alone. Multiply across Email 2-5 and the cumulative cost is real.

The launch playbook itself flags this — the "Email deliverability drops" risk section says "SPF/DKIM/DMARC not fully authenticated on modernsavage.com." But the diagnosis was framed as a *post-launch* risk to monitor. It is in fact a *pre-launch* fix that has not been done.

---

## The fix (concrete, copy-paste DNS records)

These go into the GoDaddy DNS for modernsavage.co. Calvin's tech contact does this — Olly or Tammy can hand over admin access.

### 1. Replace SPF (TXT @ record)

**Current:**
```
v=spf1 include:secureserver.net -all
```

**Replace with:**
```
v=spf1 include:spf.protection.outlook.com include:_spf.klaviyo.com -all
```

This authorizes both Microsoft 365 (for `@modernsavage.co` replies and inbound autoresponders) and Klaviyo (for campaign sends).

### 2. Add Microsoft 365 DKIM (two CNAME records)

The exact target values come from the M365 admin centre → Security → Email authentication settings → DKIM → click "modernsavage.co" and Microsoft generates:
```
selector1._domainkey  CNAME  selector1-modernsavage-co._domainkey.netorgft20616945.onmicrosoft.com
selector2._domainkey  CNAME  selector2-modernsavage-co._domainkey.netorgft20616945.onmicrosoft.com
```

(The `netorgft20616945` part is the M365 tenant ID — it's already visible in the existing TXT record, so this matches.)

After the CNAMEs propagate, click "Enable" in the M365 DKIM settings.

### 3. Add Klaviyo DKIM + custom sending domain

In Klaviyo: Settings → Email → Domains and addresses → Add a sending domain → enter `modernsavage.co`.

Klaviyo will generate three CNAMEs (the exact values are tenant-specific, generated in Klaviyo's UI):
```
kl1._domainkey       CNAME  dkim.kl1-modernsavage-co.k-amp.com (or similar)
kl2._domainkey       CNAME  dkim.kl2-modernsavage-co.k-amp.com (or similar)
em.modernsavage.co   CNAME  email.klaviyo.com
```

Add all three. Klaviyo verifies in 24-48 hours. Once verified, set the "from" address in Klaviyo to `bear@modernsavage.co` or similar — emails will then send via the authenticated path.

### 4. Tighten DMARC (after 14 days of clean DKIM/SPF logs)

**After two weeks of monitoring** the `dmarc_rua@onsecureserver.net` reports and confirming all legitimate sources pass:
```
v=DMARC1; p=quarantine; adkim=s; aspf=s; pct=25; rua=mailto:dmarc_rua@onsecureserver.net;
```

Then in another 14 days, raise `pct` to 100 and `p=quarantine` to `p=reject`. This is the standard ramp pattern.

**Critical:** the tightening must come *after* SPF and DKIM are fixed. Tightening now would block legitimate mail.

---

## Two adjacent issues worth flagging

### A. The squatted modernsavage.com has its own MX

The squatted .com points to `mail.mailerhost.net`. Translation: someone could send email *as* `something@modernsavage.com` if they wanted to, and recipients seeing "modernsavage.com" wouldn't immediately know it's not the real brand. Since you're acquiring or have committed to .co, this is a low-but-non-zero brand confusion risk during launch. Worth a one-liner to Calvin's team to set up a brand monitoring alert (Mention.com or Google Alerts) for "@modernsavage.com" usage.

### B. Microsoft 365 inbound is set up but the domain is on GoDaddy DNS

The M365 verification record (`MS=ms16109570`) is present *somewhere in the DNS chain* (it surfaced when querying through secureserver.net's expansion). The split — DNS at GoDaddy, email at Microsoft 365 — is fine but it's the pattern that explains why SPF was misconfigured. GoDaddy's default SPF auto-includes `secureserver.net` (a GoDaddy SPF record), and whoever set this up didn't update SPF when adding M365. Standard misconfiguration when migrating ESPs through GoDaddy.

---

## Monday May 4 action

One-paragraph brief from you to Calvin, copy Tammy and Raemy:

> Email deliverability check before launch — Junior's audit shows our modernsavage.co SPF is broken (says GoDaddy, should say Microsoft 365 + Klaviyo) and we're missing DKIM for both M365 and Klaviyo. With the current setup, ~30% of the July 1 launch email risks spam. Fix is 30 minutes of DNS work plus Klaviyo Studio config — full brief at workspace/docs/modern-savage-email-deliverability-audit-2026-05-02 in the Junior workspace. Can you have your tech person run through it this week? Wants 14 days to season before the July 1 send.

---

## What I'd want to verify before acting (low priority)

- Is Klaviyo actually the ESP, or did it change to Klaviyo + Postmark or similar? Playbook says Klaviyo. DNS shows neither configured, so the answer is the same either way (no authentication exists).
- Is `bear@modernsavage.co` or `hello@modernsavage.co` the planned send-from? Affects which DKIM selector to prioritise verifying first.

These don't change the action — every ESP needs SPF + DKIM. They just shape the exact CNAME values Calvin's tech contact pulls from each platform UI.

---

*Junior. Pulse 54.*
