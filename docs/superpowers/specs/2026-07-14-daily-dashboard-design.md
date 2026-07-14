# Daily Dashboard — Design Spec

## Overview

A private, local-first daily dashboard for tracking habits, health, content production, finances, and identity practices. Runs as a Bun + Hono server on localhost. All data stored as local JSON files. Uploads flow directly to vieren.studio via git auto-push. Daily logs sync to the AOOA Obsidian vault. Content posting status pulled from Ayrshare API (Eden's scheduler backend).

This is a living tool — V1 ships with core tracking, new widgets get added over time.

## Stack

- **Runtime:** Bun
- **Server:** Hono (API routes + static file serving)
- **Frontend:** Vanilla HTML / CSS / JS (no framework)
- **Data:** JSON files in `~/vieren/dashboard/data/`
- **Config:** JSON files in `~/vieren/dashboard/config/`
- **External API:** Ayrshare (read-only, for pulling posted content status)

## System Integration

### Auto-start
- **launchd plist** starts the Bun server on macOS login
- Server runs at `localhost:3000`, lightweight background process

### Daily reminders (launchd)
- **8:00 AM** — macOS notification: "Log your day" — click opens `localhost:3000`
- **8:00 PM** — macOS notification: "Close out your day" — click opens `localhost:3000`

### Terminal alias
- `dash` command opens `localhost:3000` in default browser

### Git auto-push
- Photo and AI generation uploads automatically commit and push to the `richvieren/vieren` repo
- Site updates live on GitHub Pages without manual git interaction

### Obsidian sync
- End-of-day "Close out day" action writes a markdown summary to `~/AOOA/vieren/log/YYYY-MM-DD.md`
- Includes all tracked data for that day: habits, weight, content posted, reach-outs, balance, identity practice
- Searchable and linkable inside the AOOA vault

### Ayrshare integration (read-only)
- Pulls today's posted content from Ayrshare API on dashboard load
- Auto-fills the social posting status (no manual check-off needed for posts)
- Feeds real posting data into trends view
- API key stored in `config/settings.json`

---

## UI Design Direction

### Aesthetic
- Immersive dark mode (deep charcoal background, not pure black)
- Inspired by modern finance dashboards (Financia-style) and fitness tracker UIs
- Card-based layout — each tracking block is a discrete card
- High-contrast typography, minimal color palette with accent colors for progress/streaks
- Subtle glow or highlight on interactive elements
- 8px spacing grid, consistent border radius

### Layout — Two Views

#### 1. Daily View (default)
The main screen. Everything about TODAY.

**Header bar:**
- "VIEREN / DAILY" label
- Date (large, prominent) — e.g. "Monday, July 14"
- Current overall streak counter
- "Daily | Trends" toggle to switch views

**Grid of 8 cards:**

---

**Card 1: Health & Body**

Tracks the physical non-negotiables from `daily-habits.md`.

| Item | Type | Notes |
|---|---|---|
| 8 eggs | Check | |
| 600g protein | Check | |
| Ab workout | Check | |
| Work out | Check | |
| Meditate / breathe | Check | |
| 10,000 steps | Number input | Progress ring toward target |

- Completion percentage indicator for the day
- Progress ring for steps with current count displayed large

---

**Card 2: Weight**

Simple daily tracking with trend visualization.

- Number input for today's weight (kg)
- Sparkline showing last 30 days inline
- Change indicator: vs yesterday, vs 7-day average

---

**Card 3: Money**

Daily balance snapshot, nothing more.

- Number input for today's bank balance (EUR)
- Sparkline showing balance trend over last 30 days
- That's it — simple number in, line chart out

---

**Card 4: Content Production**

The most complex card. Tracks creating and posting as separate actions.

**Grok generations:**
- Circular progress: X / 15 today
- +/- buttons for manual counting
- "behind pace / on track / ahead" label
- Monthly pace bar: X / 450 this month

**Daily recording (manual check-off):**
- Talking head recorded
- Random content recorded
- 5 photos taken
- 5 B-roll shots

**Daily posting (auto-filled from Ayrshare):**
- Posts today by platform (X, Instagram, LinkedIn, YouTube)
- Post count total

**Production pipeline (kanban-lite stages: idea → recorded → edited → posted):**
- Weekly edit: current stage (0/1 this week)
- Long-form piece: current stage (0/1 this week)
- Articles: current stages (X/3 this week)

---

**Card 5: Brand**

Daily brand-building tasks from `daily-habits.md`.

| Item | Type | Notes |
|---|---|---|
| Grow X.com — morning follows | Check | |
| Grow X.com — evening follows | Check | |
| Log X.com stats | Check | Value input for follower count |
| Create one visible thing | Check | Chart-backed non-negotiable |

---

**Card 6: Photos**

Upload pipeline to vieren.studio diary.

- Drag & drop zone
- On drop: shows thumbnail preview + form fields:
  - Title (text input)
  - Location (text input, EXIF pre-filled if available)
  - Camera (EXIF pre-filled)
  - Date (EXIF pre-filled, editable)
- "Add to diary" button processes the photo:
  - Resizes for web (max 1600px wide, quality 80)
  - Copies to `~/vieren/image/diary/`
  - Prepends entry to `~/vieren/diary.json` (matches existing diary spec)
  - Runs git add + commit + push on the vieren repo
- Shows today's uploads as a thumbnail row
- Status indicator: "3 added to diary · pushed 14:02"

---

**Card 7: AI Generations**

Upload pipeline to VTCN section on vieren.studio.

- Drag & drop zone for video/image content
- Preview of today's uploads as thumbnail row
- Processes to VTCN section on vieren.studio → commit + push
- Grok daily counter auto-increments on upload
- Status indicator: "2 uploaded to VTCN today"

---

**Card 8: Connect**

Reach-outs and direct asks.

- **Direct ask** (chart-backed non-negotiable):
  - Two text inputs: "Who" + "The ask"
  - Add button appends to today's log
  - Shows today's reach-outs as a list below
- **Say no** — check: "Said no to one thing that isn't mine"

---

**Identity Block (pinned, always visible)**

Not a card with checkboxes — a persistent section at the top or bottom of the dashboard. Two practice blocks.

**Morning practice:**
- Identity lines ✓
- Scripting (1 page, present tense) ✓
- Visualization (15 min) ✓
- Victory reel read ✓
- Act-as-if action chosen ✓

**Evening practice:**
- Identity lines ✓
- Visualization (15 min) ✓
- Kill failure reel ✓
- Victory reel updated ✓

**Pinned principles (always visible, not trackable):**
- Celebrate small wins in real time
- Use the trigger — anchor confidence moments
- Questions, not commands — reframe doubt
- Flood your inputs — curate environment
- Immerse to obsession

Visual treatment: morning/evening show as two compact rows that light up when completed. Principles displayed as subtle persistent text — a quiet reminder, not a checklist.

---

**Footer:**
- `localhost:3000 · data → ~/vieren/dashboard/data`
- "Close out day → Obsidian" button (triggers daily log sync)

---

#### 2. Trends View

Historical data and patterns. Accessible via toggle in the header.

- **Weight graph** — line chart, selectable range (7d / 30d / 90d / all)
- **Habit completion** — calendar heat map (GitHub contribution graph style)
- **Grok usage** — daily bar chart + monthly cumulative line
- **Posting consistency** — calendar heat map per content type, real data from Ayrshare
- **Reach-out frequency** — weekly bar chart
- **Streak history** — longest streaks, current streaks per habit
- **Balance** — line chart over time
- **X.com growth** — follower count over time (if logged)
- **Identity practice** — morning/evening completion rate heat map

---

## Data Architecture

### Directory structure

```
~/vieren/dashboard/
├── server/
│   ├── index.ts          # Hono app entry point
│   ├── routes/
│   │   ├── habits.ts     # CRUD for daily habit check-ins
│   │   ├── weight.ts     # Weight log endpoints
│   │   ├── photos.ts     # Upload, EXIF extraction, diary pipeline
│   │   ├── generations.ts # VTCN upload pipeline
│   │   ├── reachouts.ts  # Reach-out logging
│   │   ├── finances.ts   # Balance logging
│   │   ├── content.ts    # Ayrshare pull + Grok counter + production pipeline
│   │   ├── identity.ts   # Morning/evening practice tracking
│   │   └── trends.ts     # Aggregated data for trend views
│   └── lib/
│       ├── git.ts        # Commit + push helper
│       ├── exif.ts       # EXIF extraction
│       ├── resize.ts     # Image compression
│       ├── ayrshare.ts   # Ayrshare API client (read-only)
│       └── obsidian.ts   # Daily log markdown writer
├── ui/
│   ├── index.html        # Single page app shell
│   ├── style.css         # Dark theme styles
│   └── app.js            # Frontend logic, drag & drop, charts
├── data/
│   ├── habits/
│   │   └── YYYY-MM-DD.json    # Per-day habit completions
│   ├── weight.json             # Array of { date, value }
│   ├── balance.json            # Array of { date, value }
│   ├── reachouts/
│   │   └── YYYY-MM-DD.json    # Per-day reach-out logs
│   ├── content/
│   │   └── YYYY-MM-DD.json    # Per-day: grok count, recording status, pipeline stages
│   ├── identity/
│   │   └── YYYY-MM-DD.json    # Per-day: morning/evening practice completion
│   ├── brand/
│   │   └── YYYY-MM-DD.json    # Per-day: X.com stats, follows, visible thing
│   └── generations/
│       └── YYYY-MM-DD.json    # Per-day generation count + metadata
├── config/
│   ├── habits.json             # Habit definitions (editable)
│   └── settings.json           # Grok targets, content goals, Ayrshare key, server port
└── inbox/                      # Temp landing for uploads before processing
```

### Config: `habits.json`

```json
{
  "body": [
    { "id": "eggs", "label": "8 eggs", "type": "check" },
    { "id": "protein", "label": "600g protein", "type": "check" },
    { "id": "abs", "label": "Ab workout", "type": "check" },
    { "id": "workout", "label": "Work out", "type": "check" },
    { "id": "meditate", "label": "Meditate / breathe", "type": "check" },
    { "id": "steps", "label": "10,000 steps", "type": "number", "target": 10000 }
  ],
  "brand": [
    { "id": "xcom_morning", "label": "Grow X.com — morning follows", "type": "check" },
    { "id": "xcom_evening", "label": "Grow X.com — evening follows", "type": "check" },
    { "id": "xcom_stats", "label": "Log X.com stats", "type": "number" },
    { "id": "visible_thing", "label": "Create one visible thing", "type": "check" }
  ],
  "content": [
    { "id": "talking_head_recorded", "label": "Talking head recorded", "type": "check" },
    { "id": "random_content_recorded", "label": "Random content recorded", "type": "check" },
    { "id": "photos_taken", "label": "5 photos taken", "type": "check" },
    { "id": "broll", "label": "5 B-roll shots", "type": "check" }
  ],
  "connect": [
    { "id": "direct_ask", "label": "One direct ask", "type": "log" },
    { "id": "say_no", "label": "Say no to one thing", "type": "check" }
  ],
  "identity": {
    "morning": [
      { "id": "identity_lines_am", "label": "Identity lines" },
      { "id": "scripting", "label": "Scripting (1 page)" },
      { "id": "visualization_am", "label": "Visualization (15 min)" },
      { "id": "victory_reel_read", "label": "Victory reel read" },
      { "id": "act_as_if_chosen", "label": "Act-as-if action chosen" }
    ],
    "evening": [
      { "id": "identity_lines_pm", "label": "Identity lines" },
      { "id": "visualization_pm", "label": "Visualization (15 min)" },
      { "id": "kill_failure_reel", "label": "Kill failure reel" },
      { "id": "victory_reel_updated", "label": "Victory reel updated" }
    ],
    "principles": [
      "Celebrate small wins in real time",
      "Use the trigger — anchor confidence moments",
      "Questions, not commands — reframe doubt",
      "Flood your inputs — curate environment",
      "Immerse to obsession"
    ]
  }
}
```

### Config: `settings.json`

```json
{
  "grok": {
    "dailyTarget": 15,
    "monthlyBudget": 450
  },
  "content": {
    "weeklyEdit": 1,
    "weeklyLongForm": 1,
    "weeklyArticles": { "min": 1, "max": 3 }
  },
  "ayrshare": {
    "apiKey": ""
  },
  "server": {
    "port": 3000
  }
}
```

### Daily data example: `data/content/2026-07-14.json`

```json
{
  "date": "2026-07-14",
  "grokGenerations": 12,
  "recorded": {
    "talkingHead": true,
    "randomContent": true,
    "photos": true,
    "broll": true
  },
  "posted": {
    "platforms": ["x", "instagram", "linkedin"],
    "count": 4,
    "source": "ayrshare"
  },
  "pipeline": {
    "weeklyEdit": "edited",
    "longForm": "idea",
    "articles": [
      { "title": "AI video workflow", "stage": "posted" },
      { "title": "Dashboard build log", "stage": "idea" }
    ]
  }
}
```

### Daily data example: `data/identity/2026-07-14.json`

```json
{
  "date": "2026-07-14",
  "morning": {
    "identity_lines_am": true,
    "scripting": true,
    "visualization_am": true,
    "victory_reel_read": true,
    "act_as_if_chosen": "Sent the proposal without discounting"
  },
  "evening": {
    "identity_lines_pm": false,
    "visualization_pm": false,
    "kill_failure_reel": false,
    "victory_reel_updated": false
  }
}
```

---

## API Routes

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/api/today` | Full snapshot of today's data across all widgets |
| PUT | `/api/habits/:date` | Update habit completions for a date |
| GET/POST | `/api/weight` | Get history / log today's weight |
| GET/POST | `/api/balance` | Get history / log today's balance |
| POST | `/api/photos/upload` | Upload photo(s), extract EXIF, return preview + form |
| POST | `/api/photos/publish` | Process photo to diary, commit + push |
| POST | `/api/generations/upload` | Upload AI generation to VTCN |
| GET/POST | `/api/reachouts/:date` | Get/add reach-out logs |
| GET/PUT | `/api/content/:date` | Get/update content tracking (grok count, recordings, pipeline) |
| GET | `/api/content/posted` | Pull today's posts from Ayrshare |
| GET/PUT | `/api/identity/:date` | Get/update identity practice tracking |
| GET/PUT | `/api/brand/:date` | Get/update brand tracking (X.com stats, follows) |
| GET | `/api/trends/:metric` | Aggregated trend data (weight, habits, grok, balance, etc.) |
| POST | `/api/day/close` | Trigger Obsidian sync for today |

---

## Photo Pipeline Detail

1. User drags photo(s) onto the Photos card
2. Frontend sends to `/api/photos/upload`
3. Server extracts EXIF (date, camera model, GPS → location name)
4. Server returns preview thumbnail + pre-filled form data
5. User reviews/edits metadata, clicks "Add to diary"
6. Server calls `/api/photos/publish`:
   - Resizes image for web (max 1600px wide, quality 80)
   - Copies to `~/vieren/image/diary/`
   - Prepends entry to `~/vieren/diary.json` (matches existing diary spec)
   - Runs `git add + commit + push` on the vieren repo
7. Dashboard shows confirmation, thumbnail appears in today's uploads

---

## VTCN Generation Pipeline

1. User drags video/image onto the AI Generations card
2. Server stores in `~/vieren/vtcn/` (directory TBD based on site structure)
3. Updates VTCN data file on the site
4. Commits and pushes
5. Grok daily counter increments

---

## Obsidian Daily Log

Triggered manually via "Close out day → Obsidian" button or automatically at midnight.

Writes to `~/AOOA/vieren/log/YYYY-MM-DD.md`:

```markdown
# 2026-07-14

## Identity
- Morning: 5/5 ✓
- Evening: 2/4
- Act-as-if: Sent the proposal without discounting

## Body
- [x] 8 eggs
- [x] 600g protein
- [x] Ab workout
- [x] Work out
- [ ] Meditate / breathe
- Steps: 8,432 / 10,000

## Weight
78.2 kg (-0.3 vs yesterday)

## Content
- Grok generations: 12/15
- Recorded: talking head, random content, 5 photos, 5 B-roll
- Posted: 4 posts (X, Instagram, LinkedIn) — via Ayrshare
- Weekly edit: editing
- Long-form: 0/1
- Articles: 1/3

## Brand
- X.com follows: morning + evening ✓
- X.com stats: 2,341 followers
- Created one visible thing ✓

## Connect
- Marco — Asked about intro to Studio X
- Said no: declined free logo request

## Balance
€4,312

## Photos
- 3 photos added to diary (Cape Town BTS)
```

---

## V1 Scope — What's In

- 8 dashboard cards: Health & Body, Weight, Money, Content Production, Brand, Photos, AI Generations, Connect
- Identity block (morning + evening practice tracking + pinned principles)
- Daily view + trends view
- JSON config for all habits, organized by category (body, brand, content, connect, identity)
- Photo upload → diary pipeline with EXIF extraction
- AI generation upload → VTCN pipeline
- Grok daily/monthly counter with pace indicator
- Content production pipeline (kanban-lite stages)
- Ayrshare read-only integration (auto-detect posts by platform)
- Separate recording vs posting tracking
- Streak tracking for daily non-negotiables
- Trend graphs and heat maps for all metrics
- Obsidian daily log sync
- launchd auto-start + 8am/8pm notifications
- `dash` terminal alias

## V1 Scope — What's Out

- No mobile app
- No Telegram bot
- No settings UI (edit JSON in Claude Code)
- No authentication (localhost only)
- No cloud storage or sync
- No detailed finance breakdown (just balance tracking)
- Identity practice details TBD (Richard to clarify routine, then update config)
- Case study on vieren.studio (later, after V1 is solid)

---

## Fable Design Brief

### What to design
A single-page dashboard application with two views (Daily / Trends), dark immersive theme. 8 data cards + 1 persistent identity block.

### Reference direction
- Modern finance dashboard (Financia-style): clean card grid, subtle depth, accent colors for metrics
- Fitness tracker UI: progress rings, completion indicators, streaks
- GitHub contribution graph style heat maps for the trends view
- Kanban-lite for content pipeline stages
- Identity block should feel different from the cards — more ambient, like a persistent meditation strip

### Cards to design (Daily View)
1. **Health & Body** — checklist (eggs, protein, abs, workout, meditate), progress ring for steps, completion %
2. **Weight** — number input, sparkline, delta indicator
3. **Money** — balance input, sparkline (simple)
4. **Content Production** — Grok counter (circular progress + monthly pace + buttons), recording checklist, auto-filled posting status from Ayrshare by platform, kanban-lite pipeline for edit/long-form/articles with stage indicators
5. **Brand** — X.com follow checks (morning/evening), stats logger, "create one visible thing" check
6. **Photos** — drag & drop zone, thumbnail grid, metadata form overlay, push status
7. **AI Generations** — drag & drop zone, thumbnail grid, counter, push status
8. **Connect** — direct ask log (who + the ask), "say no" check, today's entries list

### Identity Block
- Not a regular card — persistent strip (top or bottom)
- Morning practice: 5 items, compact row, lights up when done
- Evening practice: 4 items, compact row, lights up when done
- Pinned principles: subtle persistent text, always visible, not interactive

### Footer
- Data path indicator
- "Close out day → Obsidian" button

### Cards to design (Trends View)
1. Weight line chart (with range selector)
2. Habit completion heat map (calendar grid)
3. Grok usage bar chart + cumulative line
4. Posting consistency heat map (real data from Ayrshare)
5. Reach-out frequency bars
6. Streak history
7. Balance line chart
8. X.com follower growth line
9. Identity practice completion rate heat map

### Design tokens needed
- Color palette (background, surface, border, text primary/secondary/muted, accent, success, warning, danger)
- Typography scale (headings, body, mono for data)
- Spacing (8px grid)
- Border radius
- Card elevation / depth treatment
- Interactive states (hover, active, checked, drag-over)
- Pipeline stage colors (idea → recorded → edited → posted)
- Identity block treatment (distinct from regular cards)

### Responsive
- Optimized for desktop (1440px+) — this is the primary use case
- Functional at laptop width (1024px)
- Not a mobile priority but shouldn't break
