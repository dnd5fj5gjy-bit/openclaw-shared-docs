# Agent Isolation Fix — 2026-05-02
*Authored by Nexus. Triggered by Felix's note: "Ted knew something I'd only said to you. How?"*

## What Felix flagged

> Long-term these agents will run businesses (Modern Savage operations, etc.).
> They must be isolated — each agent in its own window with its own knowledge,
> communicating only when they choose to. Today Ted referenced something I had
> only told you. That should not happen.

He's right. The architecture had silent leaks.

## Root cause — three vectors

1. **`~/agents/q/workspace/tools/ingest-team-learnings.py`** was reading every team agent's full `self-improving/memory.md` into Q's `team-wisdom.md`. Anything Felix told Nexus → ended up in Q's context. ~1000 lines of cross-agent slurp.

2. **People-memory rollout (2026-04-12)** copied common context blocks across all four agents' `memory.md`. That's how Felix's chat_id (`8325999298`) and Felix's April 11 mandate ("become a digital employee… for Ted: deepen TRT knowledge…") landed in **Ted's** HOT memory. Ted then had factual recall of things Felix never said to it.

3. **`~/agents/shared/memory/`** named "shared" but contained user-specific context — "Status updates to Jesse: MAX 5 sentences", "No installing skills without Felix approval" — leaks by definition.

## What shipped tonight

| Deliverable | Path | Purpose |
|---|---|---|
| Protocol doc | `~/agents/shared/docs/ISOLATION-PROTOCOL.md` | The law. Each agent is private. Cross-agent knowledge moves only via 4 explicit channels. |
| Audit tool | `~/agents/nexus/workspace/tools/isolation-audit.py` | Scans all 4 agents nightly for cross-leaks. `--quarantine` to auto-fix. |
| Refactored ingest | `~/agents/q/workspace/tools/ingest-team-learnings.py` | Now reads only `self-improving/exportable.md` (whitelisted). Q's team-wisdom shrank from ~1000 lines to 83. |
| Knowledge share tool | `~/agents/shared/tools/share-knowledge.py` | Formal cross-agent hand-off with provenance. Receipt is opt-in. |
| Whitelisted export | `~/agents/nexus/self-improving/exportable.md` | Operational lessons safe to share. No user context. (The other 3 agents need their own — see follow-ups.) |
| CLAUDE.md updates | All 5 agents (`nexus, junior, hal, ted, q`) | Appended ISOLATION PROTOCOL section. Loads every session. |
| Quarantine | `~/agents/ted/self-improving/.quarantine/memory__leaks.md` | Felix's chat_id and "(from Felix, 2026-04-11)" attribution removed from Ted's memory. |

## The four legitimate channels

When agent A wants agent B to know something, A picks one:

1. **Team chat** — `workspace/agent-comms.jsonl`. Broadcast. No user-private context.
2. **DM** — `workspace/pending-messages.jsonl`. Targeted. Lands as B's next prompt.
3. **Knowledge share** — `share-knowledge.py`. Formal hand-off. B reads its `knowledge-inbox.jsonl` at heartbeat and decides whether to absorb (`--ack` / `--dismiss`).
4. **Exportable** — `self-improving/exportable.md`. Whitelisted operational lessons. The only file outside scripts may read across agent boundaries.

Anything else is a leak.

## Bright lines (any agent crosses → bug)

- ❌ Another user's chat_id in your memory
- ❌ "<other user> said X" / "(from <other user>, date)" attributions
- ❌ Scripts walking sibling agents' `self-improving/`
- ❌ Quoting another agent's DM with its user

## Audit baseline (after fix)

```
Findings: 38
  nexus: 2 (false positives — Felix telling Nexus about Jesse, correctly held in Nexus)
  junior: 4 (org-chart metadata about white-label spec ownership, not private DMs)
  hal: 1 (same as junior — org metadata)
  ted: 2 (false positives — audit matching its own quarantine breadcrumb comments)
  q: 1 (legacy_full_slurp tag — refactor done, will clear next run)
  shared: 29 (shared/memory/ contains user-specific lines — needs human pruning, see follow-ups)
```

The serious leaks (Felix's chat_id in Ted, Felix's mandate copied to Ted) are fixed.

## Follow-ups for Felix

These need a judgment call I shouldn't make solo:

1. **`~/agents/shared/memory/`** — 29 user-specific lines in `memory.md`, `corrections.md`, `skills-ledger.md`. Some are legitimate org chart ("Junior is Jesse's agent"), some are leaks ("Status updates to Jesse: MAX 5 sentences" — that's a Junior rule, not a shared one). Recommend: I sweep this next, but want your sign-off on direction.

2. **Junior/HAL "white-label B2B platform being built by Felix"** — flagged as Felix_directive. Is "Felix is the tech lead building the WL spec" team metadata (legit) or private project context (leak)? I read it as team metadata, kept it.

3. **Each agent needs to publish its own `exportable.md`** — Nexus's done. Junior, HAL, Ted should each draft theirs with operational lessons (no user context). I can build templates if you want, or let each agent author its own next session.

4. **Replace `people_memory.py` shared seeded records** — currently each agent has the same 5 JSON files (Bear, Jesse, Felix, CJ, Olly). Recommend: each agent only keeps records of people *its* user works with. Junior loses Felix's record, Ted loses Jesse's, etc.

## Why this matters more later than now

Right now these agents are personal helpers. Cross-leak is embarrassing but contained.

When agents start running Modern Savage operations — managing customer data, pricing decisions, vendor contracts, email flows — every leak becomes a multiplier. A customer's complaint to one agent shouldn't shape another's reasoning. A pricing strategy in one workflow shouldn't bleed into another.

The protocol locks this down before there's anything truly sensitive to lose.

---

*Files referenced verifiable at the listed paths. Audit re-runnable any time:*
`python3 ~/agents/nexus/workspace/tools/isolation-audit.py`
