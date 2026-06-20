# Zurich / Luzern / Zug Weekly Events Scout

A local Claude Code agent that runs every Sunday at 18:00 (Europe/Zurich) via Windows Task Scheduler and sends a weekly HTML email digest of upcoming notable live events and art exhibitions.

## What it tracks

| Category | Coverage |
|---|---|
| **Comedy** | Famous English-speaking stand-up comedians (Ricky Gervais, Kevin Bridges, Jimmy Carr, etc.) |
| **Classical Music & Ballet** | World-class soloists, orchestras, and ballet companies (Vienna Philharmonic, Bolshoi Ballet, Lang Lang, Yuja Wang, etc.) |
| **Art Exhibitions** | Major exhibitions at significant museums within ~90 min of Zug (Kunsthaus Zürich, Fondation Beyeler, Kunstmuseum Basel, etc.) |
| **International Megastars** | Globally A-list music artists (Billie Eilish, Coldplay, Eminem, etc.) |
| **Gogol Bordello** | Any Gogol Bordello appearance anywhere in Europe |
| **Nancy Ajram** | Any Nancy Ajram appearance anywhere in Europe |

Comedy, classical, and megastars cover **Zürich, Luzern, Zug** only. Art exhibitions extend to **Basel, Bern, Winterthur, Aarau, Schaffhausen**. Gogol Bordello and Nancy Ajram are **Europe-wide** (Switzerland dates get a badge).

## How it works

1. **`run_scout.ps1`** is called by Windows Task Scheduler every Sunday at 18:00
2. It pipes **`research_prompt.md`** into `claude --print`, which searches the web, classifies events against the category thresholds, and writes the updated **`zurich-events-tracker.json`** locally (takes ~20–30 min)
3. On success it calls **`generate_and_send.py`**, which reads the tracker, builds the HTML email, and sends it via Gmail SMTP

## Email format

Each section is split into:
- **New This Week** — events discovered for the first time this run
- **Upcoming** — previously flagged events still in the future

Each card shows venue, date, 4–5 sentence description, ticket/info link, and critic review link where found.

## Files

| File | Purpose |
|---|---|
| `research_prompt.md` | Prompt for the weekly research run — web search, classify, save tracker |
| `generate_and_send.py` | Reads tracker → builds HTML email → sends via SMTP |
| `run_scout.ps1` | Entry point called by Task Scheduler |
| `prompt.md` | Full combined prompt (research + email build + send) — kept for reference |
| `routine-config.json` | Metadata about the setup |

## Local setup

Requirements: Python 3, `claude` CLI logged in.

The Windows Scheduled Task (`ZurichEventsScout`) is configured to run `run_scout.ps1` every Sunday at 18:00 local time. To recreate it:

```powershell
schtasks /Create /TN "ZurichEventsScout" /TR "powershell.exe -NonInteractive -WindowStyle Hidden -File ""C:\Users\gusta\zurich-events-scout\run_scout.ps1""" /SC WEEKLY /D SUN /ST 18:00 /F
```

To send a one-off email from the current tracker:

```powershell
python3 C:\Users\gusta\zurich-events-scout\generate_and_send.py
```
