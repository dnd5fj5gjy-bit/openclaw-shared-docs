# Agent Listener Watchdog

**Built:** 2026-04-07 by Nexus (nightly proactive task)

## Problem it solves

Previously, if any of the 3 Telegram listener daemons (nexus, junior, bgv) died silently:
- Felix would stop hearing from that agent with no warning
- There was no auto-recovery
- The only fix was manual — find the dead process and restart it

Also: the dashboard only refreshed at heartbeat intervals (every 4 hours) because crontab modifications don't persist in this environment.

## What it does

A lightweight shell daemon running every 2 minutes via macOS LaunchAgent:

1. **Checks all 3 listeners** — `pgrep` for each agent's listener process
2. **Auto-restarts dead ones** — relaunches with same config, waits 3 seconds, confirms alive
3. **Texts Felix** if a restart happens: "🔧 Nexus watchdog: nexus listener was dead — restarted automatically."
4. **Texts Felix** if a listener won't recover: "🚨 ... FAILED to restart. Manual intervention needed."
5. **Regenerates the dashboard** — keeps the GitHub Pages dashboard fresh every 2 minutes

## Files

| File | Purpose |
|------|---------|
| `~/agents/shared/tools/agent-watchdog.sh` | Main watchdog script |
| `~/Library/LaunchAgents/com.agents.listener-watchdog.plist` | LaunchAgent (runs every 120s) |
| `~/agents/logs/agent-watchdog.log` | Health log |

## Status

Loaded and running as of 2026-04-07 01:01 UTC. First run confirmed:
```
OK: nexus listener running
OK: junior listener running
OK: bgv listener running
Dashboard regenerated
Watchdog cycle complete
```

## Manual commands

```bash
# Check status
launchctl list | grep listener-watchdog

# View logs
tail -f ~/agents/logs/agent-watchdog.log

# Restart watchdog
launchctl unload ~/Library/LaunchAgents/com.agents.listener-watchdog.plist
launchctl load ~/Library/LaunchAgents/com.agents.listener-watchdog.plist

# Run manually
zsh ~/agents/shared/tools/agent-watchdog.sh
```
