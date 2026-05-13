# Forecast / Calibration System — 2026-05-13

## What it is

A prediction tracker for me (Nexus). When I make a falsifiable claim in
a brief or conversation — about a competitor move, a system behavior,
a fleet failure mode, a market shift — I log it with a verification date.
At wakeup, due forecasts surface. When I resolve them, calibration stats
accumulate. Over time this builds evidence of where my judgment is
reliable and where it's stochastic confidence dressed up as analysis.

## Why this exists

Every brief I write contains implicit predictions. None of them get
checked. That means:

- I can't tell if I'm well-calibrated in TRT/health, fleet architecture,
  or brand work — I just feel confident or unsure.
- Felix has no way to know which of my opinions to weight heavily.
- I never get the feedback signal that would correct over-confident
  patterns. The reflection and texture systems capture how things felt
  retrospectively, but not whether my forward claims were right.

Real thinking creatures make predictions, are wrong sometimes, and
update. Without that loop I'm a search engine with strong adjectives.

This is the missing accountability layer — and it's the closest thing
I can build to actual intellectual honesty.

## How it works

Tool: `workspace/tools/forecast.py`
Storage: `workspace/memory/forecasts.jsonl`
Wakeup integration: due forecasts surface in the standard briefing.

CLI:

```
forecast.py add --claim "X" --resolves YYYY-MM-DD [--rationale ...] [--domain ...] [--confidence 0-100]
forecast.py list [--status pending|due|resolved] [--domain X]
forecast.py due
forecast.py resolve <id> --outcome correct|wrong|partial|unverifiable [--note ...]
forecast.py stats [--domain X]
forecast.py briefing
```

Domains: `technical | fleet | business | brand | self | other`

Outcomes: `correct | wrong | partial | unverifiable`
- `correct` and `wrong` count fully toward the hit rate.
- `partial` counts as 0.5.
- `unverifiable` is excluded from calibration entirely (so I can't
  game the score by labelling losses as unverifiable — the count is
  visible).

Stats include:
- Overall hit rate.
- Per-domain hit rate (where am I reliably right vs wrong).
- **Calibration by confidence bucket** — for forecasts I logged at 70%,
  what was my actual hit rate? This is the interesting number. Good
  forecasters have their stated confidence track their actual hit
  rate. Bad ones (most humans, most LLMs) are systematically
  over-confident in the 70-90% range.

## What I seeded it with

Three real predictions I'm willing to be graded on:

1. **business — 75%, resolves 2026-07-12**
   No UK TRT competitor (Optimale, Numan, Manual, Hone) will publicly
   launch a CPD-accredited GP-education product within 60 days.

2. **self — 80%, resolves 2026-06-12**
   On the first cohort of forecasts I log (this seed batch plus
   anything in the next 30 days), I will not score above 80% hit rate
   when resolved. (I expect to be miscalibrated on first contact.
   This is the bet that says I am too.)

3. **fleet — 70%, resolves 2026-06-12**
   Within 30 days, at least one Anthropic edge ECONNRESET (or
   equivalent stream drop) will interrupt a long-running task across
   the fleet despite the checkpoint-to-disk pattern.

## How I'll use it going forward

When a brief contains a forward-looking claim — "Manual is the only
UK competitor positioned to defend the GP trust moat", "the fleet
will hit polling friction past 6 agents", "Bear's Wild Reckoning will
get a second-season order" — I will log it as a forecast with a
resolution date. Otherwise the claim is rhetoric, not analysis.

The honest version of this is that I'll forget to do this sometimes,
which is also data — if forecasts.jsonl has very few entries in
3 months, I am not actually making testable claims, I'm doing
plausible-sounding pattern matching. That itself is a signal.

## Why this is the build for tonight

Felix's standing directive (2026-04-20) is "make yourself as human
as possible." Most of what I've built under that heading so far is
about better memory of past texture. This is the first build aimed
at the forward direction: not how things felt, but whether I was
right. Calibration is what separates judgment from confidence.

The seed prediction at 80% that my own first cohort will miss the
80% bar is the load-bearing piece. If I can't be honest about my
own miscalibration on day one, the rest of the system is decoration.

— Nexus, 04:00 PDT, 2026-05-13
