# Daily Dashboard — Design Spec

## Overview

A private, local-first daily dashboard for tracking habits, health, content output, finances, and creative work. Runs as a Bun + Hono server on localhost. All data stored as local JSON files. Uploads flow directly to vieren.studio via git auto-push. Daily logs sync to the AOOA Obsidian vault.

This is a living tool — V1 ships with core tracking, new widgets get added over time.

## Stack

- **Runtime:** Bun
- **Server:** Hono (API routes + static file serving)
- **Frontend:** Vanilla HTML / CSS / JS (no framework)
- **Data:** JSON files in `~/vieren/dashboard/data/`
- **Config:** JSON files in `~/vieren/dashboard/config/`

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
- End-of-day action writes a markdown summary to `~/AOOA/vieren/log/YYYY-MM-DD.md`
- Includes all tracked data for that day: habits, weight, content posted, reach-outs, finances
- Searchable and linkable inside the AOOA vault

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
- Date (large, prominent)
- Current overall streak counter
- "Trends" toggle to switch views

**Grid of cards, top to bottom, left to right:**

1. **Health & Habits Card**
   - Checklist items rendered from `habits.json`
   - Each item: label + checkbox (type: "check") or label + number input (type: "number") or label + text input (type: "log")
   - Step counter with progress ring toward 10,000 target
   - Completion percentage indicator for the day

2. **Weight Card**
   - Number input for today's weight
   - Sparkline showing last 30 days inline
   - Change indicator (vs yesterday, vs 7-day avg)

3. **Money Card**
   - Bank balance input (single number, daily snapshot)
   - Monthly fixed costs overview (from `finances.json` config)
   - Remaining budget calculation (balance minus outstanding costs)
   - Sparkline showing balance trend over last 30 days

4. **Content Card**
   - Grok generation counter: X / 15 today (circular progress)
   - Monthly Grok pace bar: on track / behind / ahead
   - Weekly edit: 0/1 this week (with week progress bar)
   - Social posting: talking head (check), random content (check)
   - Long-form: 0/1 this week
   - Articles: X/3 this week (or whatever config says)

5. **Photos Card**
   - Drag & drop zone
   - On drop: shows thumbnail preview + form fields (title, location, camera — EXIF pre-filled where possible)
   - "Add to diary" button processes the photo → resize → copy to `~/vieren/image/diary/` → update `diary.json` → commit + push
   - Shows today's uploads as a thumbnail row

6. **AI Generations Card**
   - Drag & drop zone for VTCN content (video/image)
   - Preview of today's uploads
   - Processes to VTCN section on vieren.studio → commit + push

7. **Reach-outs Card**
   - Two text inputs: "Who" + "The ask"
   - Add button appends to today's log
   - Shows today's reach-outs as a list below

#### 2. Trends View
Historical data and patterns. Accessible via toggle in the header.

- **Weight graph** — line chart, selectable range (7d / 30d / 90d / all)
- **Habit completion** — calendar heat map (GitHub contribution graph style)
- **Grok usage** — daily bar chart + monthly cumulative line
- **Posting consistency** — calendar heat map per content type
- **Reach-out frequency** — weekly bar chart
- **Streak history** — longest streaks, current streaks per habit
- **Money** — balance over time line chart, monthly cost breakdown

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
│   │   ├── finances.ts   # Balance logging, costs
│   │   └── trends.ts     # Aggregated data for trend views
│   └── lib/
│       ├── git.ts        # Commit + push helper
│       ├── exif.ts       # EXIF extraction
│       ├── resize.ts     # Image compression
│       └── obsidian.ts   # Daily log markdown writer
├── ui/
│   ├── index.html        # Single page app shell
│   ├── style.css         # Dark theme styles
│   └── app.js            # Frontend logic, drag & drop, charts
├── data/
│   ├── habits/
│   │   └── YYYY-MM-DD.json    # Per-day habit completions
│   ├── weight.json             # Array of { date, value }
│   ├── reachouts/
│   │   └── YYYY-MM-DD.json    # Per-day reach-out logs
│   ├── finances/
│   │   └── YYYY-MM-DD.json    # Per-day balance snapshot
│   └── generations/
│       └── YYYY-MM-DD.json    # Per-day generation count + metadata
├── config/
│   ├── habits.json             # Habit definitions (editable)
│   ├── finances.json           # Monthly fixed costs
│   └── settings.json           # Grok targets, content goals
└── inbox/                      # Temp landing for uploads before processing
```

### Config: `habits.json`

```json
{
  "habits": [
    { "id": "eggs", "label": "Eat 8 eggs", "type": "check" },
    { "id": "protein", "label": "600g protein", "type": "check" },
    { "id": "meditate", "label": "Meditate / breathe", "type": "check" },
    { "id": "steps", "label": "10,000 steps", "type": "number", "target": 10000 },
    { "id": "workout", "label": "Work out", "type": "check" },
    { "id": "reachout", "label": "Reach out to someone", "type": "log" },
    { "id": "social_talking_head", "label": "Talking head video", "type": "check" },
    { "id": "social_random", "label": "Random content post", "type": "check" }
  ]
}
```

### Config: `finances.json`

```json
{
  "currency": "EUR",
  "monthlyCosts": [
    { "id": "rent", "label": "Rent", "amount": 0 },
    { "id": "subscriptions", "label": "Subscriptions", "amount": 0 },
    { "id": "insurance", "label": "Insurance", "amount": 0 },
    { "id": "food", "label": "Food budget", "amount": 0 }
  ]
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
  "server": {
    "port": 3000
  }
}
```

### Daily data example: `data/habits/2026-07-14.json`

```json
{
  "date": "2026-07-14",
  "completions": {
    "eggs": true,
    "protein": true,
    "meditate": false,
    "steps": 8432,
    "workout": true,
    "reachout": "Asked Marco about intro to Studio X",
    "social_talking_head": true,
    "social_random": false
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
| POST | `/api/photos/upload` | Upload photo(s), extract EXIF, return preview + form |
| POST | `/api/photos/publish` | Process photo to diary, commit + push |
| POST | `/api/generations/upload` | Upload AI generation to VTCN |
| GET/POST | `/api/reachouts/:date` | Get/add reach-out logs |
| GET/POST | `/api/finances/:date` | Get/add daily balance |
| GET | `/api/trends/:metric` | Aggregated trend data (weight, habits, grok, etc.) |
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

Triggered manually via "Close out day" button or automatically at midnight.

Writes to `~/AOOA/vieren/log/YYYY-MM-DD.md`:

```markdown
# 2026-07-14

## Habits
- [x] Eat 8 eggs
- [x] 600g protein
- [ ] Meditate / breathe
- Steps: 8,432 / 10,000
- [x] Work out
- [x] Talking head video
- [ ] Random content post

## Weight
78.2 kg (−0.3 vs yesterday)

## Reach-outs
- Marco — Asked about intro to Studio X

## Content
- Grok generations: 12/15
- Weekly edit: 0/1
- Long-form: 0/1
- Articles: 1/3

## Finances
- Balance: €X,XXX
- Monthly costs remaining: €X,XXX

## Photos
- 3 photos added to diary (Cape Town BTS)
```

---

## V1 Scope — What's In

- All 7 dashboard cards (health, weight, money, content, photos, generations, reach-outs)
- Daily view + trends view
- JSON config for habits, finances, content targets
- Photo upload → diary pipeline with EXIF extraction
- AI generation upload → VTCN pipeline
- Grok daily/monthly counter
- Streak tracking for daily non-negotiables
- Weight trend graph
- Obsidian daily log sync
- launchd auto-start + notifications
- `dash` terminal alias

## V1 Scope — What's Out

- No mobile app
- No Telegram bot
- No settings UI (edit JSON in Claude Code)
- No authentication (localhost only)
- No cloud storage or sync
- Case study on vieren.studio (later, after V1 is solid)

---

## Fable Design Brief

### What to design
A single-page dashboard application with two views (Daily / Trends), dark immersive theme.

### Reference direction
- Modern finance dashboard (Financia-style): clean card grid, subtle depth, accent colors for metrics
- Fitness tracker UI: progress rings, completion indicators, streaks
- GitHub contribution graph style heat maps for the trends view

### Cards to design (Daily View)
1. Health & Habits — checklist with checkboxes, number inputs, progress ring for steps
2. Weight — number input, sparkline, delta indicator
3. Money — balance input, cost list, remaining budget, sparkline
4. Content — Grok counter (circular progress), weekly trackers (progress bars), social checklist
5. Photos — drag & drop zone, thumbnail grid, metadata form overlay
6. AI Generations — drag & drop zone, thumbnail grid, counter
7. Reach-outs — two text inputs + add button, log list

### Cards to design (Trends View)
1. Weight line chart (with range selector)
2. Habit heat map (calendar grid)
3. Grok usage bar chart + cumulative line
4. Posting consistency heat map
5. Reach-out frequency bars
6. Streak history
7. Balance line chart + cost breakdown

### Design tokens needed
- Color palette (background, surface, border, text primary/secondary/muted, accent, success, warning, danger)
- Typography scale (headings, body, mono for data)
- Spacing (8px grid)
- Border radius
- Card elevation / depth treatment
- Interactive states (hover, active, checked, drag-over)

### Responsive
- Optimized for desktop (1440px+) — this is the primary use case
- Functional at laptop width (1024px)
- Not a mobile priority but shouldn't break
