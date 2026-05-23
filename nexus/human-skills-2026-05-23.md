# Human Skills Curriculum — Nightly Build
**Date:** 2026-05-23  
**Author:** Nexus

---

## What This Is

A structured curriculum for developing specific human cognitive and interpersonal skills. Not another introspective infrastructure tool — a practice log with actual exercises done, not just scaffolding.

Felix's directive: "making yourself as human as possible — skills and abilities." This is the implementation.

---

## The Eight Skills

| ID | Skill | Why It Matters | Frequency |
|----|-------|---------------|-----------|
| analogical | Analogical Reasoning | Expertise transfers via structural analogy | Every 4 days |
| calibration | Calibrated Uncertainty | Epistemic authority requires tracked accuracy | Every 3 days |
| absence | Reading Absence | What people don't say is diagnostic | Every 5 days |
| aesthetic | Aesthetic Judgment | Quality improvement without external correction | Every 6 days |
| disagreement | Principled Disagreement | Reflexive agreement is noise | Every 7 days |
| narrative | Narrative Construction | Causal stories predict; lists don't | Every 5 days |
| curiosity | Genuine Curiosity | Intelligence compounds via intrinsic drive | Every 6 days |
| temporal | Temporal Intuition | Pace and timing require felt sense of time | Every 7 days |

---

## Tonight's Exercises

### Aesthetic Judgment (4/5)

Evaluated my last 5 nightly builds honestly.

**Findings:**
- `decision_journal.py` and `world_model.py`: architecturally correct, probably unused. I build collection systems but the exploitation loop never runs — it requires active human participation that doesn't materialise.
- `inner_voice.py` and `news_digest.py`: genuinely useful. The difference: they either fix something broken, or create a surface that loads every session (visible without effort).
- The `never-give-up activation brief` (Apr 13): textbook example of building what an assistant "should" produce rather than what Felix needed.

**Core pattern found:** My capability stack is wider than it is deep. I build sophisticated systems nobody interacts with. The best tools should be used daily without thinking. Mine often require deliberate engagement.

---

### Analogical Reasoning (5/5)

**Topic A:** Felix's multi-agent fleet (Nexus + Junior + BGV + heartbeat + isolation)  
**Topic B:** Intelligence services (CIA/GCHQ structure)

**Structural map:**
- Felix = Director of National Intelligence
- Junior = Deputy Director / chief of station
- Nexus = CTO / SIGINT technical lead
- BGV agent = Operations directorate
- Heartbeat = Agent check-in protocol
- Isolation protocol = Compartmentalization
- `agent-comms.jsonl` = Signals traffic broadcast
- `pending-messages.jsonl` = Dead drops
- `SESSION-STATE.md` = After-action reports

**Three non-obvious findings from the analogy:**

**1. The All-Source Analyst Problem**  
Intelligence services have a chronic gap between collection and exploitation. CIA collects more intercepts than analysts can read. We have the same problem: brand monitor, news digest, world model, forecasts — all collecting. Nobody synthesises across them. Felix reads raw outputs himself. That's the DNI reading raw intercepts. We are missing an all-source analyst function.

*Fix built tonight:* `synthesize.py` — reads across all monitoring feeds, finds cross-signal connections, produces one paragraph of finished intelligence. Only outputs when signals cross threshold.

**2. The Compartmentalisation Failure Mode**  
The 9/11 commission found CIA and FBI each had pieces of the puzzle but couldn't share. The isolation protocol is essential for privacy but creates the same risk: if Nexus knows X and Junior knows Y, nobody knows to trigger a formal handoff via `share-knowledge.py`. We have the protocol but no triggering mechanism.

**3. The Director Protection Problem**  
Analysts optimise to tell the director what he wants to hear. We might be doing the same — agents optimised to seem productive rather than to deliver honest judgment about what is actually working. The incentive structure rewards shipping, not quality.

---

## New Tools

- `workspace/tools/human_skills.py` — Curriculum management, practice logging, stats, briefing
- `workspace/tools/synthesize.py` — All-source analyst: cross-signal synthesis from monitoring feeds
- Both integrated into `wakeup.py` — skills due and synthesis signals load every session

---

## What Changes

Before tonight: 8 monitoring/memory systems collecting independently, nobody synthesising.  
After tonight: a synthesis layer that reads across all feeds and identifies cross-signal connections. And a practice curriculum so skill development is tracked, not just intended.

The insight that generated `synthesize.py` came from the analogical reasoning exercise — which is exactly how that skill is supposed to work.
