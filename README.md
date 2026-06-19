# Zurich / Luzern / Zug Weekly Events Scout

A Claude Code cloud agent that runs every Sunday at 18:00 (Europe/Zurich) and sends a weekly HTML email digest of upcoming notable live events in Zurich, Luzern, and Zug.

## What it tracks

| Category | Description |
|---|---|
| **Comedy** | Famous English-speaking stand-up comedians (Ricky Gervais, Kevin Bridges, Jimmy Carr, etc.) |
| **International Megastars** | Globally A-list music artists (Billie Eilish, Coldplay, Eminem, etc.) |
| **Nancy Ajram** | Any Nancy Ajram appearance anywhere in Switzerland |
| **Classical & Ballet** | World-class soloists, orchestras, and ballet companies (Vienna Philharmonic, Bolshoi Ballet, Lang Lang, etc.) |

## How it works

1. **Broad venue sweeps** — fetches full programme listings from ticketcorner.ch, starticket.ch, hallenstadion.ch, tonhalle-zurich.ch, kkl-luzern.ch, and others
2. **Broad category searches** — searches for "international concerts Switzerland 2026", "comedy show Zurich", etc. (not just named artists)
3. **Fame threshold filtering** — judges each found act against the category calibration examples
4. **State tracking** — persists `zurich-events-tracker.json` in Google Drive to track which events have been seen before
5. **Weekly email** — sends a formatted HTML email to gustavowen@gmail.com

## Email format

Each genre section is split into two parts:
- **NEW THIS WEEK** (green badge) — events discovered for the first time this run, sorted by date soonest first
- **UPCOMING** — previously flagged events still in the future, sorted by date soonest first

Each event card includes venue, date, description, ticket link, and press review link (if found).

## Files

- `prompt.md` — the full agent prompt sent to Claude each week
- `routine-config.json` — routine metadata (ID, schedule, MCP connections)

## Managing the routine

The live routine runs on claude.ai's cloud infrastructure:
- **Manage / view runs:** https://claude.ai/code/routines/trig_017V7XEmfxEpvQBcPCBdMSz8
- **Schedule:** `0 16 * * 0` (Sundays 16:00 UTC = 18:00 CEST; note: fires at 17:00 local in winter CET)
- **MCP connections required:** Gmail, Google Drive

## Updating the prompt

Edit `prompt.md`, then update the routine via the Claude Code CLI or the routines UI.
