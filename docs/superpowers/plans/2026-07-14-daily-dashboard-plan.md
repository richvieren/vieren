# Daily Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local-first daily dashboard at localhost:3000 for tracking habits, health, content production, finances, and identity practices, with photo/video upload pipelines that auto-push to vieren.studio.

**Architecture:** Bun + Hono server reads/writes local JSON files and serves a vanilla HTML/CSS/JS frontend. The frontend is a single page with two views (Daily / Trends) toggled client-side. Upload pipelines process files and git-push to the vieren.studio repo. Ayrshare API is called read-only for post detection. An Obsidian sync writes a daily markdown log.

**Tech Stack:** Bun 1.3.11, Hono, vanilla HTML/CSS/JS, sharp (image resize), exifr (EXIF), simple-git

## Global Constraints

- Runtime: Bun (not Node). Use `bun install`, `bun run`, Bun APIs where applicable.
- No frameworks on the frontend — vanilla HTML/CSS/JS only.
- All data stored as JSON files under `~/vieren/dashboard/data/`.
- Config files editable by hand in any editor — JSON with comments NOT supported, keep valid JSON.
- Design tokens are FINAL from the Fable handoff (`design_handoff_daily_dashboard/README.md`). Pixel-perfect implementation.
- Fonts: Space Grotesk + JetBrains Mono from Google Fonts.
- The vieren repo is at `~/vieren/` — `diary.json` and `image/diary/` already exist there.
- The Obsidian vault is at `~/AOOA/` — daily logs write to `~/AOOA/vieren/log/`.
- No authentication needed (localhost only).
- Fable design reference file: `/tmp/fable-export/design_handoff_daily_dashboard/Daily Dashboard.dc.html` — option 1a is the approved design.

## Reference Files

- **Design spec:** `~/vieren/docs/superpowers/specs/2026-07-14-daily-dashboard-design.md`
- **Fable handoff:** `/tmp/fable-export/design_handoff_daily_dashboard/README.md` (design tokens, exact specs)
- **Fable prototype:** `/tmp/fable-export/design_handoff_daily_dashboard/Daily Dashboard.dc.html` (visual reference, option 1a only)
- **Diary spec:** `~/vieren/docs/superpowers/specs/2026-07-14-photo-diary-design.md`
- **Existing diary data:** `~/vieren/diary.json` (empty array), `~/vieren/image/diary/` (empty dir)

---

### Task 1: Project Scaffolding + Server + Config

**Files:**
- Create: `~/vieren/dashboard/package.json`
- Create: `~/vieren/dashboard/tsconfig.json`
- Create: `~/vieren/dashboard/server/index.ts`
- Create: `~/vieren/dashboard/config/habits.json`
- Create: `~/vieren/dashboard/config/settings.json`
- Create: `~/vieren/dashboard/ui/index.html` (minimal shell)

**Interfaces:**
- Produces: Running Hono server at `localhost:3000` serving static files from `ui/` and responding to `/api/health`

- [ ] **Step 1: Create project directory and initialize**

```bash
mkdir -p ~/vieren/dashboard
cd ~/vieren/dashboard
bun init -y
```

- [ ] **Step 2: Install dependencies**

```bash
cd ~/vieren/dashboard
bun add hono
bun add -d @types/bun
```

- [ ] **Step 3: Write tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "types": ["bun-types"],
    "strict": true,
    "esModuleInterop": true,
    "outDir": "./dist",
    "rootDir": "."
  },
  "include": ["server/**/*.ts"]
}
```

- [ ] **Step 4: Write the Hono server entry point**

Create `server/index.ts`:

```typescript
import { Hono } from "hono";
import { serveStatic } from "hono/bun";

const app = new Hono();

// Health check
app.get("/api/health", (c) => c.json({ ok: true, time: new Date().toISOString() }));

// Static files — serve ui/ directory at root
app.use("/*", serveStatic({ root: "./ui" }));

const port = 3000;
console.log(`Dashboard running at http://localhost:${port}`);

export default {
  port,
  fetch: app.fetch,
};
```

- [ ] **Step 5: Create config files**

Create `config/habits.json`:

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
    { "id": "xcom_morning", "label": "Grow X.com \u2014 morning follows", "type": "check" },
    { "id": "xcom_evening", "label": "Grow X.com \u2014 evening follows", "type": "check" },
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
      "Use the trigger \u2014 anchor confidence moments",
      "Questions, not commands \u2014 reframe doubt",
      "Flood your inputs \u2014 curate environment",
      "Immerse to obsession"
    ]
  }
}
```

Create `config/settings.json`:

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

- [ ] **Step 6: Create minimal HTML shell**

Create directories and `ui/index.html`:

```bash
mkdir -p ~/vieren/dashboard/ui
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>VIEREN / DAILY</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <div id="app">
    <p style="color:#f0ece4;padding:32px;font-family:'JetBrains Mono',monospace;">Dashboard loading...</p>
  </div>
  <script src="/app.js"></script>
</body>
</html>
```

Create empty `ui/style.css` and `ui/app.js`:

```css
/* style.css — populated in Task 5 */
```

```javascript
// app.js — populated in Task 5
console.log("Dashboard ready");
```

- [ ] **Step 7: Create data directories**

```bash
mkdir -p ~/vieren/dashboard/data/{habits,reachouts,content,identity,brand,generations}
touch ~/vieren/dashboard/data/weight.json
echo "[]" > ~/vieren/dashboard/data/weight.json
touch ~/vieren/dashboard/data/balance.json
echo "[]" > ~/vieren/dashboard/data/balance.json
mkdir -p ~/vieren/dashboard/inbox
```

- [ ] **Step 8: Test the server starts and serves files**

```bash
cd ~/vieren/dashboard && bun run server/index.ts &
sleep 1
curl -s http://localhost:3000/api/health | bun -e "console.log(JSON.parse(await Bun.stdin.text()))"
curl -s http://localhost:3000/ | head -5
kill %1
```

Expected: health returns `{ ok: true, time: "..." }`, root returns the HTML shell.

- [ ] **Step 9: Add start script to package.json**

Add to `package.json` scripts:

```json
{
  "scripts": {
    "dev": "bun --watch run server/index.ts",
    "start": "bun run server/index.ts"
  }
}
```

- [ ] **Step 10: Commit**

```bash
cd ~/vieren/dashboard
git init
git add -A
git commit -m "feat: scaffold dashboard — Bun + Hono server, config files, static serving"
```

---

### Task 2: Data Layer — JSON File Helpers

**Files:**
- Create: `~/vieren/dashboard/server/lib/data.ts`

**Interfaces:**
- Produces: `readJSON<T>(path: string): Promise<T | null>`, `writeJSON(path: string, data: unknown): Promise<void>`, `readDayFile<T>(category: string, date: string): Promise<T | null>`, `writeDayFile(category: string, date: string, data: unknown): Promise<void>`, `appendToLog(path: string, entry: { date: string; value: number }): Promise<void>`, `today(): string`, `DATA_DIR: string`, `CONFIG_DIR: string`

- [ ] **Step 1: Write data.ts**

Create `server/lib/data.ts`:

```typescript
import { mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { homedir } from "node:os";

export const DATA_DIR = join(homedir(), "vieren", "dashboard", "data");
export const CONFIG_DIR = join(homedir(), "vieren", "dashboard", "config");

export function today(): string {
  return new Date().toISOString().slice(0, 10);
}

export async function readJSON<T>(path: string): Promise<T | null> {
  try {
    const file = Bun.file(path);
    if (!(await file.exists())) return null;
    return (await file.json()) as T;
  } catch {
    return null;
  }
}

export async function writeJSON(path: string, data: unknown): Promise<void> {
  await mkdir(dirname(path), { recursive: true });
  await Bun.write(path, JSON.stringify(data, null, 2) + "\n");
}

export async function readDayFile<T>(category: string, date: string): Promise<T | null> {
  return readJSON<T>(join(DATA_DIR, category, `${date}.json`));
}

export async function writeDayFile(category: string, date: string, data: unknown): Promise<void> {
  await writeJSON(join(DATA_DIR, category, `${date}.json`), data);
}

export async function appendToLog(path: string, entry: { date: string; value: number }): Promise<void> {
  const log = (await readJSON<Array<{ date: string; value: number }>>(path)) ?? [];
  const existing = log.findIndex((e) => e.date === entry.date);
  if (existing >= 0) {
    log[existing] = entry;
  } else {
    log.push(entry);
  }
  log.sort((a, b) => a.date.localeCompare(b.date));
  await writeJSON(path, log);
}

export async function readConfig<T>(name: string): Promise<T> {
  const data = await readJSON<T>(join(CONFIG_DIR, name));
  if (data === null) throw new Error(`Config file not found: ${name}`);
  return data;
}
```

- [ ] **Step 2: Write a quick smoke test**

```bash
cd ~/vieren/dashboard
bun -e "
import { readJSON, writeJSON, readDayFile, writeDayFile, appendToLog, today, DATA_DIR } from './server/lib/data.ts';
import { join } from 'path';

// Test today()
console.log('today:', today());

// Test writeDayFile + readDayFile
await writeDayFile('habits', '2026-07-14', { eggs: true });
const d = await readDayFile('habits', '2026-07-14');
console.log('day file:', d);

// Test appendToLog
const logPath = join(DATA_DIR, 'weight-test.json');
await appendToLog(logPath, { date: '2026-07-14', value: 78.2 });
await appendToLog(logPath, { date: '2026-07-13', value: 78.5 });
const log = await readJSON(logPath);
console.log('log (sorted):', log);

// Cleanup test files
await Bun.write(join(DATA_DIR, 'habits/2026-07-14.json'), '');
const { unlink } = await import('node:fs/promises');
await unlink(join(DATA_DIR, 'habits/2026-07-14.json'));
await unlink(logPath);
console.log('All tests passed');
"
```

Expected: prints today's date, the day file data, sorted log entries, "All tests passed".

- [ ] **Step 3: Commit**

```bash
cd ~/vieren/dashboard
git add server/lib/data.ts
git commit -m "feat: data layer — JSON read/write helpers for day files and append logs"
```

---

### Task 3: API Routes — All CRUD Endpoints

**Files:**
- Create: `~/vieren/dashboard/server/routes/habits.ts`
- Create: `~/vieren/dashboard/server/routes/weight.ts`
- Create: `~/vieren/dashboard/server/routes/balance.ts`
- Create: `~/vieren/dashboard/server/routes/content.ts`
- Create: `~/vieren/dashboard/server/routes/identity.ts`
- Create: `~/vieren/dashboard/server/routes/brand.ts`
- Create: `~/vieren/dashboard/server/routes/reachouts.ts`
- Create: `~/vieren/dashboard/server/routes/today.ts`
- Modify: `~/vieren/dashboard/server/index.ts` (mount routes)

**Interfaces:**
- Consumes: `readDayFile`, `writeDayFile`, `appendToLog`, `readConfig`, `today`, `DATA_DIR` from `server/lib/data.ts`
- Produces: All API endpoints from the spec's route table

- [ ] **Step 1: Write habits route**

Create `server/routes/habits.ts`:

```typescript
import { Hono } from "hono";
import { readDayFile, writeDayFile } from "../lib/data.ts";

const habits = new Hono();

// GET /api/habits/:date
habits.get("/:date", async (c) => {
  const date = c.req.param("date");
  const data = await readDayFile("habits", date);
  return c.json(data ?? { date, completions: {} });
});

// PUT /api/habits/:date
habits.put("/:date", async (c) => {
  const date = c.req.param("date");
  const body = await c.req.json();
  const existing = (await readDayFile<{ date: string; completions: Record<string, unknown> }>("habits", date)) ?? {
    date,
    completions: {},
  };
  existing.completions = { ...existing.completions, ...body.completions };
  existing.date = date;
  await writeDayFile("habits", date, existing);
  return c.json(existing);
});

export default habits;
```

- [ ] **Step 2: Write weight route**

Create `server/routes/weight.ts`:

```typescript
import { Hono } from "hono";
import { join } from "node:path";
import { readJSON, appendToLog, DATA_DIR } from "../lib/data.ts";

const weight = new Hono();
const WEIGHT_PATH = join(DATA_DIR, "weight.json");

// GET /api/weight — full history
weight.get("/", async (c) => {
  const data = (await readJSON<Array<{ date: string; value: number }>>(WEIGHT_PATH)) ?? [];
  return c.json(data);
});

// POST /api/weight — log today's weight
weight.post("/", async (c) => {
  const { date, value } = await c.req.json<{ date: string; value: number }>();
  await appendToLog(WEIGHT_PATH, { date, value });
  return c.json({ ok: true, date, value });
});

export default weight;
```

- [ ] **Step 3: Write balance route**

Create `server/routes/balance.ts`:

```typescript
import { Hono } from "hono";
import { join } from "node:path";
import { readJSON, appendToLog, DATA_DIR } from "../lib/data.ts";

const balance = new Hono();
const BALANCE_PATH = join(DATA_DIR, "balance.json");

balance.get("/", async (c) => {
  const data = (await readJSON<Array<{ date: string; value: number }>>(BALANCE_PATH)) ?? [];
  return c.json(data);
});

balance.post("/", async (c) => {
  const { date, value } = await c.req.json<{ date: string; value: number }>();
  await appendToLog(BALANCE_PATH, { date, value });
  return c.json({ ok: true, date, value });
});

export default balance;
```

- [ ] **Step 4: Write content route**

Create `server/routes/content.ts`:

```typescript
import { Hono } from "hono";
import { readDayFile, writeDayFile } from "../lib/data.ts";

interface ContentDay {
  date: string;
  grokGenerations: number;
  recorded: Record<string, boolean>;
  posted: { platforms: string[]; count: number; source: string };
  pipeline: {
    weeklyEdit: string;
    longForm: string;
    articles: Array<{ title: string; stage: string }>;
  };
}

const content = new Hono();

const defaultContent = (date: string): ContentDay => ({
  date,
  grokGenerations: 0,
  recorded: { talkingHead: false, randomContent: false, photos: false, broll: false },
  posted: { platforms: [], count: 0, source: "manual" },
  pipeline: {
    weeklyEdit: "idea",
    longForm: "idea",
    articles: [],
  },
});

content.get("/:date", async (c) => {
  const date = c.req.param("date");
  const data = await readDayFile<ContentDay>("content", date);
  return c.json(data ?? defaultContent(date));
});

content.put("/:date", async (c) => {
  const date = c.req.param("date");
  const body = await c.req.json<Partial<ContentDay>>();
  const existing = (await readDayFile<ContentDay>("content", date)) ?? defaultContent(date);
  const merged = {
    ...existing,
    ...body,
    date,
    recorded: { ...existing.recorded, ...(body.recorded ?? {}) },
    posted: { ...existing.posted, ...(body.posted ?? {}) },
    pipeline: { ...existing.pipeline, ...(body.pipeline ?? {}) },
  };
  await writeDayFile("content", date, merged);
  return c.json(merged);
});

export default content;
```

- [ ] **Step 5: Write identity route**

Create `server/routes/identity.ts`:

```typescript
import { Hono } from "hono";
import { readDayFile, writeDayFile } from "../lib/data.ts";

interface IdentityDay {
  date: string;
  morning: Record<string, boolean | string>;
  evening: Record<string, boolean | string>;
}

const identity = new Hono();

const defaultIdentity = (date: string): IdentityDay => ({
  date,
  morning: {},
  evening: {},
});

identity.get("/:date", async (c) => {
  const date = c.req.param("date");
  const data = await readDayFile<IdentityDay>("identity", date);
  return c.json(data ?? defaultIdentity(date));
});

identity.put("/:date", async (c) => {
  const date = c.req.param("date");
  const body = await c.req.json<Partial<IdentityDay>>();
  const existing = (await readDayFile<IdentityDay>("identity", date)) ?? defaultIdentity(date);
  const merged = {
    date,
    morning: { ...existing.morning, ...(body.morning ?? {}) },
    evening: { ...existing.evening, ...(body.evening ?? {}) },
  };
  await writeDayFile("identity", date, merged);
  return c.json(merged);
});

export default identity;
```

- [ ] **Step 6: Write brand route**

Create `server/routes/brand.ts`:

```typescript
import { Hono } from "hono";
import { readDayFile, writeDayFile } from "../lib/data.ts";

interface BrandDay {
  date: string;
  completions: Record<string, boolean | number>;
}

const brand = new Hono();

brand.get("/:date", async (c) => {
  const date = c.req.param("date");
  const data = await readDayFile<BrandDay>("brand", date);
  return c.json(data ?? { date, completions: {} });
});

brand.put("/:date", async (c) => {
  const date = c.req.param("date");
  const body = await c.req.json<Partial<BrandDay>>();
  const existing = (await readDayFile<BrandDay>("brand", date)) ?? { date, completions: {} };
  existing.completions = { ...existing.completions, ...(body.completions ?? {}) };
  await writeDayFile("brand", date, existing);
  return c.json(existing);
});

export default brand;
```

- [ ] **Step 7: Write reachouts route**

Create `server/routes/reachouts.ts`:

```typescript
import { Hono } from "hono";
import { readDayFile, writeDayFile } from "../lib/data.ts";

interface ReachoutDay {
  date: string;
  entries: Array<{ who: string; ask: string }>;
  saidNo: boolean;
}

const reachouts = new Hono();

reachouts.get("/:date", async (c) => {
  const date = c.req.param("date");
  const data = await readDayFile<ReachoutDay>("reachouts", date);
  return c.json(data ?? { date, entries: [], saidNo: false });
});

reachouts.post("/:date", async (c) => {
  const date = c.req.param("date");
  const body = await c.req.json<{ who?: string; ask?: string; saidNo?: boolean }>();
  const existing = (await readDayFile<ReachoutDay>("reachouts", date)) ?? { date, entries: [], saidNo: false };

  if (body.who && body.ask) {
    existing.entries.push({ who: body.who, ask: body.ask });
  }
  if (body.saidNo !== undefined) {
    existing.saidNo = body.saidNo;
  }

  await writeDayFile("reachouts", date, existing);
  return c.json(existing);
});

export default reachouts;
```

- [ ] **Step 8: Write the /api/today aggregate route**

Create `server/routes/today.ts`:

```typescript
import { Hono } from "hono";
import { join } from "node:path";
import { today, readDayFile, readJSON, readConfig, DATA_DIR, CONFIG_DIR } from "../lib/data.ts";

const todayRoute = new Hono();

todayRoute.get("/", async (c) => {
  const date = today();
  const [habits, content, identity, brand, reachouts, weightLog, balanceLog, habitsConfig, settings] =
    await Promise.all([
      readDayFile("habits", date),
      readDayFile("content", date),
      readDayFile("identity", date),
      readDayFile("brand", date),
      readDayFile("reachouts", date),
      readJSON<Array<{ date: string; value: number }>>(join(DATA_DIR, "weight.json")),
      readJSON<Array<{ date: string; value: number }>>(join(DATA_DIR, "balance.json")),
      readConfig(join(CONFIG_DIR, "habits.json")),
      readConfig(join(CONFIG_DIR, "settings.json")),
    ]);

  return c.json({
    date,
    habits: habits ?? { date, completions: {} },
    content: content ?? {
      date,
      grokGenerations: 0,
      recorded: {},
      posted: { platforms: [], count: 0, source: "manual" },
      pipeline: { weeklyEdit: "idea", longForm: "idea", articles: [] },
    },
    identity: identity ?? { date, morning: {}, evening: {} },
    brand: brand ?? { date, completions: {} },
    reachouts: reachouts ?? { date, entries: [], saidNo: false },
    weight: weightLog ?? [],
    balance: balanceLog ?? [],
    config: { habits: habitsConfig, settings },
  });
});

export default todayRoute;
```

- [ ] **Step 9: Mount all routes in server/index.ts**

Replace `server/index.ts`:

```typescript
import { Hono } from "hono";
import { serveStatic } from "hono/bun";
import habits from "./routes/habits.ts";
import weight from "./routes/weight.ts";
import balance from "./routes/balance.ts";
import content from "./routes/content.ts";
import identity from "./routes/identity.ts";
import brand from "./routes/brand.ts";
import reachouts from "./routes/reachouts.ts";
import todayRoute from "./routes/today.ts";

const app = new Hono();

// API routes
app.get("/api/health", (c) => c.json({ ok: true, time: new Date().toISOString() }));
app.route("/api/today", todayRoute);
app.route("/api/habits", habits);
app.route("/api/weight", weight);
app.route("/api/balance", balance);
app.route("/api/content", content);
app.route("/api/identity", identity);
app.route("/api/brand", brand);
app.route("/api/reachouts", reachouts);

// Static files
app.use("/*", serveStatic({ root: "./ui" }));

const port = 3000;
console.log(`Dashboard running at http://localhost:${port}`);

export default {
  port,
  fetch: app.fetch,
};
```

- [ ] **Step 10: Test all API routes**

```bash
cd ~/vieren/dashboard && bun run server/index.ts &
sleep 1

# Test /api/today
curl -s http://localhost:3000/api/today | bun -e "const d = JSON.parse(await Bun.stdin.text()); console.log('today date:', d.date, 'has config:', !!d.config.habits)"

# Test habits PUT + GET
curl -s -X PUT http://localhost:3000/api/habits/2026-07-14 -H 'Content-Type: application/json' -d '{"completions":{"eggs":true}}'
curl -s http://localhost:3000/api/habits/2026-07-14

# Test weight POST + GET
curl -s -X POST http://localhost:3000/api/weight -H 'Content-Type: application/json' -d '{"date":"2026-07-14","value":78.2}'
curl -s http://localhost:3000/api/weight

# Test reachouts POST
curl -s -X POST http://localhost:3000/api/reachouts/2026-07-14 -H 'Content-Type: application/json' -d '{"who":"Marco","ask":"Intro to Studio X"}'
curl -s http://localhost:3000/api/reachouts/2026-07-14

kill %1
echo "All route tests done"
```

- [ ] **Step 11: Commit**

```bash
cd ~/vieren/dashboard
git add server/
git commit -m "feat: all CRUD API routes — habits, weight, balance, content, identity, brand, reachouts, today aggregate"
```

---

### Task 4: Frontend — Design System + HTML Shell

**Files:**
- Modify: `~/vieren/dashboard/ui/index.html`
- Modify: `~/vieren/dashboard/ui/style.css`

**Interfaces:**
- Consumes: Design tokens from Fable handoff README.md
- Produces: Complete HTML structure for Daily view + Trends view, all CSS custom properties and component styles. No JS interactivity yet.

**Important:** This task implements the FULL HTML structure and CSS from the Fable handoff. Read the Fable handoff README.md for exact values. The HTML file at `/tmp/fable-export/design_handoff_daily_dashboard/Daily Dashboard.dc.html` (option 1a) is the visual reference — match it pixel-perfectly but write clean production markup, not Fable's prototype markup.

- [ ] **Step 1: Write the complete CSS with all Fable design tokens**

Write `ui/style.css` with ALL design tokens from the Fable handoff:
- CSS custom properties for every color, spacing, typography value
- Card shell styles (bg #1d1a17, border rgba(255,255,255,.06), radius 14px, padding 18px)
- Checklist row pattern (16px checkbox, radius 5px, checked = #ff5c1f, whole row clickable)
- Number input styling (inset bg rgba(255,255,255,.05), border rgba(255,255,255,.1))
- SVG progress ring sizes (84px for health steps, 120px for grok)
- Drop zone styles (dashed border, hover state with orange)
- Identity block gradient treatment
- Pill styles (radius 999px, done/not-done states)
- Pipeline stage segment styles
- Header with eyebrow + date + streak chip + toggle
- 4-column grid: `repeat(4, 1fr)`, gap 14px
- Grid placement: Health col 1 rows 1-2, Content cols 2-3 rows 1-2, Weight col 4 row 1, Money col 4 row 2, Brand/Photos/AI/Reach-out row 3
- Footer styles
- Trends view: 3-column grid, heat map cells (11px, gap 3px, radius 2.5px), bar charts, line charts
- Responsive: 2-column at 1024px
- All hover/focus/transition states

Reference the exact values from the Fable handoff README.md. Open the `.dc.html` prototype file to visually verify your CSS matches option 1a.

- [ ] **Step 2: Write the complete HTML structure**

Write `ui/index.html` with the full page structure:
- Header bar (eyebrow, date, streak chip, daily/trends toggle)
- Daily view container with 4-column grid:
  - Health & Body card (5 checkbox rows + steps ring + input)
  - Content Production card (grok ring + recorded checks + posted section + pipeline)
  - Weight card (input + sparkline placeholder + deltas)
  - Money card (input + sparkline placeholder + delta)
  - Brand card (4 checkbox rows + follower input)
  - Photos card (drop zone + thumbnail row + status)
  - AI Generations card (drop zone + thumbnail row + status)
  - Reach Out Party card (dot tracker + who/ask inputs + add button + entries + say-no check)
- Identity block (morning pills + evening pills + act-as-if quote + principles)
- Footer (data path + close-out button)
- Trends view container (hidden by default, 3-column grid with 9 trend cards — placeholder content for charts)

All elements should have `data-*` attributes or IDs that `app.js` can target. Use semantic HTML. Every card header uses the mono uppercase pattern from the handoff.

- [ ] **Step 3: Verify visual match**

```bash
cd ~/vieren/dashboard && bun run dev &
sleep 1
echo "Open http://localhost:3000 in browser and compare side-by-side with the Fable prototype"
echo "Fable prototype at: /tmp/fable-export/design_handoff_daily_dashboard/Daily Dashboard.dc.html"
```

Open both in browser tabs and verify the Daily view matches option 1a. Check: colors, typography, spacing, grid layout, card borders, checkbox styling, ring sizes, identity block gradient.

- [ ] **Step 4: Commit**

```bash
cd ~/vieren/dashboard
git add ui/
git commit -m "feat: complete HTML structure + CSS design system from Fable handoff"
```

---

### Task 5: Frontend — Interactive JavaScript

**Files:**
- Modify: `~/vieren/dashboard/ui/app.js`

**Interfaces:**
- Consumes: `GET /api/today`, `PUT /api/habits/:date`, `POST /api/weight`, `POST /api/balance`, `PUT /api/content/:date`, `PUT /api/identity/:date`, `PUT /api/brand/:date`, `POST /api/reachouts/:date`
- Produces: Fully interactive Daily view — all checkboxes, inputs, grok buttons, reach-out form, identity pills, view toggle, sparklines, progress rings update live

- [ ] **Step 1: Write app.js with state management and API layer**

Write `ui/app.js` implementing:

1. **State management:** On load, `fetch('/api/today')` and populate all cards from the response. Store `state` object in memory.

2. **API helper:** `async function api(method, path, body)` — wraps fetch with JSON headers, returns parsed response.

3. **Checkbox toggle handler:** Attach click handler to every checklist row. On click, toggle the checkbox state, update the visual (checked/unchecked classes), compute completion %, send `PUT` to the appropriate route. Debounce writes (300ms) so rapid clicks don't spam the server.

4. **Number input handler:** For steps, weight, balance, follower count — on blur or enter, save value via the appropriate API route. For steps, update the SVG progress ring `stroke-dashoffset` live: `circumference * (1 - value/target)`.

5. **Grok +/- buttons:** On click, increment/decrement `grokGenerations` in state, update the grok ring SVG, update the count display, update the pace label (AHEAD/ON TRACK/BEHIND based on `grokGenerations/dailyTarget` vs fraction of day elapsed as hours/24), update the monthly bar width, send `PUT /api/content/:date`.

6. **Reach-out form:** On "Add" click, validate both fields non-empty, `POST /api/reachouts/:date`, append entry to the list below, clear inputs, fill next dot in the 5-dot tracker.

7. **Identity pills:** On click, toggle pill state (done/not-done CSS classes), update morning/evening counter, send `PUT /api/identity/:date`. For act-as-if, show a small text input on click.

8. **View toggle:** Daily/Trends toggle swaps visibility of the daily grid and trends container. Identity block and footer stay visible in both.

9. **Sparklines:** Render weight and balance sparklines as inline SVGs from the history arrays in the `/api/today` response. Use a `300×90` viewBox, polyline with the appropriate color and stroke width from the Fable handoff.

10. **Close out day:** On footer button click, `POST /api/day/close` and show a brief confirmation.

11. **Auto-refresh on focus:** When the browser tab gains focus, re-fetch `/api/today` to pick up any changes made via JSON file edits.

- [ ] **Step 2: Test all interactions**

Start the server, open the dashboard, and verify:
- Checkbox toggles update visually and persist (refresh to confirm)
- Steps input updates the progress ring live
- Weight input saves and sparkline renders
- Grok +/- buttons update ring, count, pace label
- Reach-out form adds entries, fills dots
- Identity pills toggle, counters update
- Daily/Trends toggle works
- Balance input saves

- [ ] **Step 3: Commit**

```bash
cd ~/vieren/dashboard
git add ui/app.js
git commit -m "feat: interactive dashboard — all cards wired to API, live state updates"
```

---

### Task 6: Photo Upload Pipeline

**Files:**
- Create: `~/vieren/dashboard/server/routes/photos.ts`
- Create: `~/vieren/dashboard/server/lib/exif.ts`
- Create: `~/vieren/dashboard/server/lib/resize.ts`
- Create: `~/vieren/dashboard/server/lib/git.ts`
- Modify: `~/vieren/dashboard/server/index.ts` (mount photos route)

**Interfaces:**
- Consumes: `writeJSON`, `readJSON` from `server/lib/data.ts`
- Produces: `POST /api/photos/upload` (returns EXIF + preview), `POST /api/photos/publish` (resizes, copies to diary, updates diary.json, git push)

- [ ] **Step 1: Install dependencies**

```bash
cd ~/vieren/dashboard
bun add sharp exifr simple-git
```

- [ ] **Step 2: Write EXIF extraction helper**

Create `server/lib/exif.ts`:

```typescript
import exifr from "exifr";

export interface ExifData {
  date: string | null;
  camera: string | null;
  location: string | null;
  lat: number | null;
  lng: number | null;
}

export async function extractExif(buffer: Buffer): Promise<ExifData> {
  try {
    const data = await exifr.parse(buffer, {
      pick: ["DateTimeOriginal", "Make", "Model", "GPSLatitude", "GPSLongitude"],
    });
    if (!data) return { date: null, camera: null, location: null, lat: null, lng: null };

    const date = data.DateTimeOriginal
      ? new Date(data.DateTimeOriginal).toISOString().slice(0, 10)
      : null;
    const camera = [data.Make, data.Model].filter(Boolean).join(" ") || null;

    return {
      date,
      camera,
      location: null, // GPS reverse geocoding is a V2 feature
      lat: data.GPSLatitude ?? null,
      lng: data.GPSLongitude ?? null,
    };
  } catch {
    return { date: null, camera: null, location: null, lat: null, lng: null };
  }
}
```

- [ ] **Step 3: Write image resize helper**

Create `server/lib/resize.ts`:

```typescript
import sharp from "sharp";

export async function resizeForWeb(buffer: Buffer): Promise<Buffer> {
  return sharp(buffer)
    .resize({ width: 1600, withoutEnlargement: true })
    .jpeg({ quality: 80 })
    .toBuffer();
}

export async function createThumbnail(buffer: Buffer): Promise<Buffer> {
  return sharp(buffer)
    .resize({ width: 200, height: 200, fit: "cover" })
    .jpeg({ quality: 70 })
    .toBuffer();
}
```

- [ ] **Step 4: Write git helper**

Create `server/lib/git.ts`:

```typescript
import simpleGit from "simple-git";
import { homedir } from "node:os";
import { join } from "node:path";

const VIEREN_REPO = join(homedir(), "vieren");

export async function gitCommitAndPush(files: string[], message: string): Promise<void> {
  const git = simpleGit(VIEREN_REPO);
  await git.add(files);
  await git.commit(message);
  await git.push();
}
```

- [ ] **Step 5: Write photos route**

Create `server/routes/photos.ts`:

```typescript
import { Hono } from "hono";
import { join } from "node:path";
import { homedir } from "node:os";
import { mkdir, writeFile } from "node:fs/promises";
import { extractExif } from "../lib/exif.ts";
import { resizeForWeb, createThumbnail } from "../lib/resize.ts";
import { gitCommitAndPush } from "../lib/git.ts";
import { readJSON, writeJSON } from "../lib/data.ts";

const photos = new Hono();
const VIEREN_DIR = join(homedir(), "vieren");
const DIARY_JSON = join(VIEREN_DIR, "diary.json");
const DIARY_IMAGES = join(VIEREN_DIR, "image", "diary");
const INBOX = join(homedir(), "vieren", "dashboard", "inbox");
const THUMBNAILS = join(homedir(), "vieren", "dashboard", "ui", "thumbnails");

// POST /api/photos/upload — receive file, extract EXIF, return preview
photos.post("/upload", async (c) => {
  const formData = await c.req.formData();
  const file = formData.get("file") as File | null;
  if (!file) return c.json({ error: "No file provided" }, 400);

  const buffer = Buffer.from(await file.arrayBuffer());
  const exif = await extractExif(buffer);
  const thumbnail = await createThumbnail(buffer);

  // Save to inbox with temp name
  const filename = file.name.replace(/[^a-zA-Z0-9._-]/g, "-");
  await mkdir(INBOX, { recursive: true });
  await writeFile(join(INBOX, filename), buffer);

  // Save thumbnail for preview
  await mkdir(THUMBNAILS, { recursive: true });
  const thumbName = `thumb-${filename.replace(/\.[^.]+$/, ".jpg")}`;
  await writeFile(join(THUMBNAILS, thumbName), thumbnail);

  return c.json({
    filename,
    thumbnailUrl: `/thumbnails/${thumbName}`,
    exif,
  });
});

// POST /api/photos/publish — resize, copy to diary, update diary.json, git push
photos.post("/publish", async (c) => {
  const { filename, title, location, date } = await c.req.json<{
    filename: string;
    title?: string;
    location?: string;
    date: string;
  }>();

  const inboxPath = join(INBOX, filename);
  const inboxFile = Bun.file(inboxPath);
  if (!(await inboxFile.exists())) return c.json({ error: "File not found in inbox" }, 404);

  const buffer = Buffer.from(await inboxFile.arrayBuffer());
  const resized = await resizeForWeb(buffer);

  // Write to diary image directory
  const webFilename = filename.replace(/\.[^.]+$/, ".jpg");
  await mkdir(DIARY_IMAGES, { recursive: true });
  await writeFile(join(DIARY_IMAGES, webFilename), resized);

  // Update diary.json — prepend entry
  const diary = (await readJSON<Array<Record<string, unknown>>>(DIARY_JSON)) ?? [];
  const entry: Record<string, unknown> = {
    date,
    photos: [webFilename],
  };
  if (location) entry.location = location;
  if (title) entry.tags = [title];
  diary.unshift(entry);
  await writeJSON(DIARY_JSON, diary);

  // Git commit + push
  const gitFiles = [
    `image/diary/${webFilename}`,
    "diary.json",
  ];
  await gitCommitAndPush(gitFiles, `diary: add ${webFilename}`);

  // Clean up inbox
  const { unlink } = await import("node:fs/promises");
  await unlink(inboxPath).catch(() => {});

  return c.json({
    ok: true,
    filename: webFilename,
    pushed: new Date().toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }),
  });
});

export default photos;
```

- [ ] **Step 6: Mount photos route and serve thumbnails**

Add to `server/index.ts`:

```typescript
import photos from "./routes/photos.ts";
// ... after other routes
app.route("/api/photos", photos);

// Serve thumbnails
app.use("/thumbnails/*", serveStatic({ root: "./ui" }));
```

- [ ] **Step 7: Wire up drag & drop in app.js for the Photos card**

Add to `ui/app.js`:
- Drag-over/drag-leave handlers on the photos drop zone (toggle orange border class)
- On drop: create FormData with the file, `POST /api/photos/upload`, show returned thumbnail + EXIF-prefilled form
- On "Add to diary" button click: `POST /api/photos/publish` with form data, show success status with timestamp
- Append thumbnail to today's uploads row

- [ ] **Step 8: Test the photo pipeline**

Start server, drag a JPEG onto the Photos card. Verify:
- EXIF data appears in the form
- Thumbnail appears
- "Add to diary" resizes, copies to `~/vieren/image/diary/`, updates `diary.json`, pushes to git
- Status shows "added to diary · pushed HH:MM"

- [ ] **Step 9: Commit**

```bash
cd ~/vieren/dashboard
git add server/lib/exif.ts server/lib/resize.ts server/lib/git.ts server/routes/photos.ts ui/app.js server/index.ts
git commit -m "feat: photo upload pipeline — EXIF extraction, resize, diary.json update, git push"
```

---

### Task 7: AI Generation Upload Pipeline

**Files:**
- Create: `~/vieren/dashboard/server/routes/generations.ts`
- Modify: `~/vieren/dashboard/server/index.ts` (mount route)

**Interfaces:**
- Consumes: `gitCommitAndPush` from `server/lib/git.ts`, `readDayFile`, `writeDayFile` from `server/lib/data.ts`
- Produces: `POST /api/generations/upload` (stores file in vtcn dir, increments grok counter, git push)

- [ ] **Step 1: Write generations route**

Create `server/routes/generations.ts`:

```typescript
import { Hono } from "hono";
import { join } from "node:path";
import { homedir } from "node:os";
import { mkdir, writeFile } from "node:fs/promises";
import { gitCommitAndPush } from "../lib/git.ts";
import { readDayFile, writeDayFile, today } from "../lib/data.ts";
import { createThumbnail } from "../lib/resize.ts";

const generations = new Hono();
const VIEREN_DIR = join(homedir(), "vieren");
const VTCN_DIR = join(VIEREN_DIR, "vtcn");
const THUMBNAILS = join(homedir(), "vieren", "dashboard", "ui", "thumbnails");

generations.post("/upload", async (c) => {
  const formData = await c.req.formData();
  const file = formData.get("file") as File | null;
  if (!file) return c.json({ error: "No file provided" }, 400);

  const buffer = Buffer.from(await file.arrayBuffer());
  const filename = file.name.replace(/[^a-zA-Z0-9._-]/g, "-");
  const date = today();

  // Save to vtcn directory
  const dateDir = join(VTCN_DIR, date);
  await mkdir(dateDir, { recursive: true });
  await writeFile(join(dateDir, filename), buffer);

  // Create thumbnail for preview
  try {
    const thumb = await createThumbnail(buffer);
    await mkdir(THUMBNAILS, { recursive: true });
    const thumbName = `vtcn-${filename.replace(/\.[^.]+$/, ".jpg")}`;
    await writeFile(join(THUMBNAILS, thumbName), thumb);
  } catch {
    // Video files won't thumbnail via sharp — that's fine
  }

  // Increment grok counter
  interface ContentDay {
    date: string;
    grokGenerations: number;
    recorded: Record<string, boolean>;
    posted: { platforms: string[]; count: number; source: string };
    pipeline: { weeklyEdit: string; longForm: string; articles: Array<{ title: string; stage: string }> };
  }
  const content = (await readDayFile<ContentDay>("content", date)) ?? {
    date,
    grokGenerations: 0,
    recorded: {},
    posted: { platforms: [], count: 0, source: "manual" },
    pipeline: { weeklyEdit: "idea", longForm: "idea", articles: [] },
  };
  content.grokGenerations += 1;
  await writeDayFile("content", date, content);

  // Git commit + push
  await gitCommitAndPush(
    [`vtcn/${date}/${filename}`],
    `vtcn: add ${filename}`
  );

  return c.json({
    ok: true,
    filename,
    grokCount: content.grokGenerations,
    pushed: new Date().toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }),
  });
});

export default generations;
```

- [ ] **Step 2: Mount route in server/index.ts**

```typescript
import generations from "./routes/generations.ts";
app.route("/api/generations", generations);
```

- [ ] **Step 3: Wire up drag & drop in app.js for the AI Generations card**

Same drag & drop pattern as Photos card. On drop: `POST /api/generations/upload`, update grok ring with returned `grokCount`, show status "X uploaded to VTCN today".

- [ ] **Step 4: Commit**

```bash
cd ~/vieren/dashboard
git add server/routes/generations.ts server/index.ts ui/app.js
git commit -m "feat: AI generation upload — VTCN pipeline with grok counter auto-increment"
```

---

### Task 8: Ayrshare Integration (Read-Only)

**Files:**
- Create: `~/vieren/dashboard/server/lib/ayrshare.ts`
- Create: `~/vieren/dashboard/server/routes/posted.ts`
- Modify: `~/vieren/dashboard/server/index.ts` (mount route)

**Interfaces:**
- Consumes: `readConfig` from `server/lib/data.ts`
- Produces: `GET /api/content/posted` returns `{ platforms: string[], count: number, posts: Array<{ platform: string, text: string }>, syncedAt: string }`

- [ ] **Step 1: Write Ayrshare client**

Create `server/lib/ayrshare.ts`:

```typescript
import { readConfig, CONFIG_DIR } from "./data.ts";
import { join } from "node:path";

interface AyrsharePost {
  id: string;
  platform: string;
  post: string;
  created: string;
  status: string;
}

interface AyrshareHistoryResponse {
  posts?: AyrsharePost[];
  status?: string;
}

interface Settings {
  ayrshare: { apiKey: string };
}

export async function fetchTodaysPosts(): Promise<{
  platforms: string[];
  count: number;
  posts: Array<{ platform: string; text: string }>;
  syncedAt: string;
}> {
  const settings = await readConfig<Settings>(join(CONFIG_DIR, "settings.json"));
  const apiKey = settings.ayrshare?.apiKey;

  if (!apiKey) {
    return { platforms: [], count: 0, posts: [], syncedAt: new Date().toISOString() };
  }

  try {
    const response = await fetch("https://app.ayrshare.com/api/history", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      console.error("Ayrshare API error:", response.status);
      return { platforms: [], count: 0, posts: [], syncedAt: new Date().toISOString() };
    }

    const data = (await response.json()) as AyrshareHistoryResponse;
    const today = new Date().toISOString().slice(0, 10);
    const todaysPosts = (data.posts ?? []).filter(
      (p) => p.created?.startsWith(today) && p.status === "success"
    );

    const platforms = [...new Set(todaysPosts.map((p) => p.platform))];

    return {
      platforms,
      count: todaysPosts.length,
      posts: todaysPosts.map((p) => ({ platform: p.platform, text: p.post?.slice(0, 100) ?? "" })),
      syncedAt: new Date().toISOString(),
    };
  } catch (err) {
    console.error("Ayrshare fetch failed:", err);
    return { platforms: [], count: 0, posts: [], syncedAt: new Date().toISOString() };
  }
}
```

- [ ] **Step 2: Write posted route**

Create `server/routes/posted.ts`:

```typescript
import { Hono } from "hono";
import { fetchTodaysPosts } from "../lib/ayrshare.ts";

const posted = new Hono();

posted.get("/", async (c) => {
  const data = await fetchTodaysPosts();
  return c.json(data);
});

export default posted;
```

- [ ] **Step 3: Mount route**

Add to `server/index.ts`:

```typescript
import posted from "./routes/posted.ts";
app.route("/api/content/posted", posted);
```

- [ ] **Step 4: Wire up in app.js**

On dashboard load, `fetch('/api/content/posted')`. Populate the POSTED · AYRSHARE section of the Content card: platform dots, counts, total, "auto-synced HH:MM" footer. This section is read-only — no user interaction.

- [ ] **Step 5: Commit**

```bash
cd ~/vieren/dashboard
git add server/lib/ayrshare.ts server/routes/posted.ts server/index.ts ui/app.js
git commit -m "feat: Ayrshare read-only integration — auto-detect today's posts by platform"
```

---

### Task 9: Obsidian Daily Log Sync

**Files:**
- Create: `~/vieren/dashboard/server/lib/obsidian.ts`
- Create: `~/vieren/dashboard/server/routes/close.ts`
- Modify: `~/vieren/dashboard/server/index.ts` (mount route)

**Interfaces:**
- Consumes: All `readDayFile` functions, `readJSON` for weight/balance logs, `readConfig` for habits config
- Produces: `POST /api/day/close` writes `~/AOOA/vieren/log/YYYY-MM-DD.md` and returns `{ ok: true, path: string }`

- [ ] **Step 1: Write Obsidian markdown generator**

Create `server/lib/obsidian.ts`:

```typescript
import { join } from "node:path";
import { homedir } from "node:os";
import { mkdir, writeFile } from "node:fs/promises";
import { readDayFile, readJSON, readConfig, DATA_DIR, CONFIG_DIR, today } from "./data.ts";

const LOG_DIR = join(homedir(), "AOOA", "vieren", "log");

export async function writeObsidianLog(date: string): Promise<string> {
  const [habits, content, identity, brand, reachouts, weightLog, balanceLog, habitsConfig] =
    await Promise.all([
      readDayFile<{ completions: Record<string, unknown> }>("habits", date),
      readDayFile<{
        grokGenerations: number;
        recorded: Record<string, boolean>;
        posted: { platforms: string[]; count: number };
        pipeline: { weeklyEdit: string; longForm: string; articles: Array<{ title: string; stage: string }> };
      }>("content", date),
      readDayFile<{ morning: Record<string, unknown>; evening: Record<string, unknown> }>("identity", date),
      readDayFile<{ completions: Record<string, unknown> }>("brand", date),
      readDayFile<{ entries: Array<{ who: string; ask: string }>; saidNo: boolean }>("reachouts", date),
      readJSON<Array<{ date: string; value: number }>>(join(DATA_DIR, "weight.json")),
      readJSON<Array<{ date: string; value: number }>>(join(DATA_DIR, "balance.json")),
      readConfig<{ body: Array<{ id: string; label: string; type: string; target?: number }> }>(
        join(CONFIG_DIR, "habits.json")
      ),
    ]);

  const lines: string[] = [`# ${date}`, ""];

  // Identity
  const morningDone = Object.values(identity?.morning ?? {}).filter((v) => v === true).length;
  const morningTotal = 5;
  const eveningDone = Object.values(identity?.evening ?? {}).filter((v) => v === true).length;
  const eveningTotal = 4;
  const actAsIf = identity?.morning?.act_as_if_chosen;
  lines.push("## Identity");
  lines.push(`- Morning: ${morningDone}/${morningTotal}${morningDone === morningTotal ? " \u2713" : ""}`);
  lines.push(`- Evening: ${eveningDone}/${eveningTotal}${eveningDone === eveningTotal ? " \u2713" : ""}`);
  if (actAsIf && typeof actAsIf === "string") lines.push(`- Act-as-if: ${actAsIf}`);
  lines.push("");

  // Body
  lines.push("## Body");
  const comps = habits?.completions ?? {};
  for (const h of habitsConfig?.body ?? []) {
    if (h.type === "number") {
      const val = comps[h.id] ?? 0;
      lines.push(`- Steps: ${Number(val).toLocaleString()} / ${(h.target ?? 10000).toLocaleString()}`);
    } else {
      lines.push(`- [${comps[h.id] ? "x" : " "}] ${h.label}`);
    }
  }
  lines.push("");

  // Weight
  const todayWeight = (weightLog ?? []).find((e) => e.date === date);
  if (todayWeight) {
    const yesterday = (weightLog ?? []).find((e) => e.date < date);
    const delta = yesterday ? (todayWeight.value - yesterday.value).toFixed(1) : "N/A";
    lines.push("## Weight");
    lines.push(`${todayWeight.value} kg (${Number(delta) > 0 ? "+" : ""}${delta} vs yesterday)`);
    lines.push("");
  }

  // Content
  lines.push("## Content");
  lines.push(`- Grok generations: ${content?.grokGenerations ?? 0}/15`);
  const recorded = content?.recorded ?? {};
  const recordedItems = Object.entries(recorded)
    .filter(([, v]) => v)
    .map(([k]) => k.replace(/([A-Z])/g, " $1").toLowerCase().trim());
  if (recordedItems.length) lines.push(`- Recorded: ${recordedItems.join(", ")}`);
  const posted = content?.posted;
  if (posted && posted.count > 0) {
    lines.push(`- Posted: ${posted.count} posts (${posted.platforms.join(", ")}) \u2014 via Ayrshare`);
  }
  lines.push(`- Weekly edit: ${content?.pipeline?.weeklyEdit ?? "idea"}`);
  lines.push(`- Long-form: ${content?.pipeline?.longForm ?? "idea"}`);
  const articles = content?.pipeline?.articles ?? [];
  const postedArticles = articles.filter((a) => a.stage === "posted").length;
  lines.push(`- Articles: ${postedArticles}/3`);
  lines.push("");

  // Brand
  const brandComps = brand?.completions ?? {};
  lines.push("## Brand");
  if (brandComps.xcom_morning || brandComps.xcom_evening) {
    const parts = [];
    if (brandComps.xcom_morning) parts.push("morning");
    if (brandComps.xcom_evening) parts.push("evening");
    lines.push(`- X.com follows: ${parts.join(" + ")} \u2713`);
  }
  if (brandComps.xcom_stats) lines.push(`- X.com stats: ${brandComps.xcom_stats} followers`);
  if (brandComps.visible_thing) lines.push("- Created one visible thing \u2713");
  lines.push("");

  // Connect
  const entries = reachouts?.entries ?? [];
  if (entries.length > 0 || reachouts?.saidNo) {
    lines.push("## Connect");
    for (const e of entries) {
      lines.push(`- ${e.who} \u2014 ${e.ask}`);
    }
    if (reachouts?.saidNo) lines.push("- Said no \u2713");
    lines.push("");
  }

  // Balance
  const todayBalance = (balanceLog ?? []).find((e) => e.date === date);
  if (todayBalance) {
    lines.push("## Balance");
    lines.push(`\u20AC${todayBalance.value.toLocaleString()}`);
    lines.push("");
  }

  const markdown = lines.join("\n");
  const logPath = join(LOG_DIR, `${date}.md`);
  await mkdir(LOG_DIR, { recursive: true });
  await writeFile(logPath, markdown);

  return logPath;
}
```

- [ ] **Step 2: Write close route**

Create `server/routes/close.ts`:

```typescript
import { Hono } from "hono";
import { writeObsidianLog } from "../lib/obsidian.ts";
import { today } from "../lib/data.ts";

const close = new Hono();

close.post("/", async (c) => {
  const date = today();
  const path = await writeObsidianLog(date);
  return c.json({ ok: true, date, path });
});

export default close;
```

- [ ] **Step 3: Mount route**

Add to `server/index.ts`:

```typescript
import close from "./routes/close.ts";
app.route("/api/day/close", close);
```

- [ ] **Step 4: Wire up "Close out day → Obsidian" button in app.js**

On click: `POST /api/day/close`. Show brief confirmation in the footer: "Synced to Obsidian · YYYY-MM-DD.md".

- [ ] **Step 5: Test**

Add some data via the dashboard, click "Close out day", verify the markdown file at `~/AOOA/vieren/log/YYYY-MM-DD.md` contains all sections with correct data.

- [ ] **Step 6: Commit**

```bash
cd ~/vieren/dashboard
git add server/lib/obsidian.ts server/routes/close.ts server/index.ts ui/app.js
git commit -m "feat: Obsidian daily log sync — Close out day writes markdown to AOOA vault"
```

---

### Task 10: Trends View

**Files:**
- Create: `~/vieren/dashboard/server/routes/trends.ts`
- Modify: `~/vieren/dashboard/server/index.ts` (mount route)
- Modify: `~/vieren/dashboard/ui/app.js` (render trend charts)

**Interfaces:**
- Consumes: All data files (habits, content, identity, brand, reachouts, weight.json, balance.json)
- Produces: `GET /api/trends/:metric` returns aggregated historical data; frontend renders 9 trend cards

- [ ] **Step 1: Write trends route**

Create `server/routes/trends.ts`:

```typescript
import { Hono } from "hono";
import { join } from "node:path";
import { readdir } from "node:fs/promises";
import { readJSON, readDayFile, DATA_DIR } from "../lib/data.ts";

const trends = new Hono();

async function listDayFiles(category: string): Promise<string[]> {
  try {
    const dir = join(DATA_DIR, category);
    const files = await readdir(dir);
    return files
      .filter((f) => f.endsWith(".json"))
      .map((f) => f.replace(".json", ""))
      .sort();
  } catch {
    return [];
  }
}

// GET /api/trends/weight
trends.get("/weight", async (c) => {
  const data = (await readJSON<Array<{ date: string; value: number }>>(join(DATA_DIR, "weight.json"))) ?? [];
  return c.json(data);
});

// GET /api/trends/balance
trends.get("/balance", async (c) => {
  const data = (await readJSON<Array<{ date: string; value: number }>>(join(DATA_DIR, "balance.json"))) ?? [];
  return c.json(data);
});

// GET /api/trends/habits — returns per-day completion counts for heat map
trends.get("/habits", async (c) => {
  const dates = await listDayFiles("habits");
  const results: Array<{ date: string; completed: number; total: number }> = [];
  for (const date of dates) {
    const data = await readDayFile<{ completions: Record<string, unknown> }>("habits", date);
    const comps = data?.completions ?? {};
    const completed = Object.values(comps).filter((v) => v === true || (typeof v === "number" && v > 0)).length;
    results.push({ date, completed, total: 6 });
  }
  return c.json(results);
});

// GET /api/trends/grok — daily generation counts
trends.get("/grok", async (c) => {
  const dates = await listDayFiles("content");
  const results: Array<{ date: string; count: number }> = [];
  for (const date of dates) {
    const data = await readDayFile<{ grokGenerations: number }>("content", date);
    results.push({ date, count: data?.grokGenerations ?? 0 });
  }
  return c.json(results);
});

// GET /api/trends/identity — morning/evening completion per day
trends.get("/identity", async (c) => {
  const dates = await listDayFiles("identity");
  const results: Array<{ date: string; morning: number; evening: number }> = [];
  for (const date of dates) {
    const data = await readDayFile<{ morning: Record<string, unknown>; evening: Record<string, unknown> }>(
      "identity",
      date
    );
    const morning = Object.values(data?.morning ?? {}).filter((v) => v === true).length;
    const evening = Object.values(data?.evening ?? {}).filter((v) => v === true).length;
    results.push({ date, morning, evening });
  }
  return c.json(results);
});

// GET /api/trends/reachouts — weekly counts
trends.get("/reachouts", async (c) => {
  const dates = await listDayFiles("reachouts");
  const results: Array<{ date: string; count: number }> = [];
  for (const date of dates) {
    const data = await readDayFile<{ entries: Array<unknown> }>("reachouts", date);
    results.push({ date, count: data?.entries?.length ?? 0 });
  }
  return c.json(results);
});

// GET /api/trends/brand — X.com follower count over time
trends.get("/brand", async (c) => {
  const dates = await listDayFiles("brand");
  const results: Array<{ date: string; followers: number }> = [];
  for (const date of dates) {
    const data = await readDayFile<{ completions: Record<string, unknown> }>("brand", date);
    const followers = data?.completions?.xcom_stats;
    if (typeof followers === "number") {
      results.push({ date, followers });
    }
  }
  return c.json(results);
});

// GET /api/trends/streaks — current and best streaks per habit
trends.get("/streaks", async (c) => {
  const dates = await listDayFiles("habits");
  const habitIds = ["eggs", "protein", "abs", "workout", "meditate", "steps"];
  const streaks: Record<string, { current: number; best: number }> = {};

  for (const id of habitIds) {
    let current = 0;
    let best = 0;
    let running = 0;

    for (const date of dates) {
      const data = await readDayFile<{ completions: Record<string, unknown> }>("habits", date);
      const val = data?.completions?.[id];
      const done = val === true || (typeof val === "number" && val >= (id === "steps" ? 10000 : 1));
      if (done) {
        running++;
        if (running > best) best = running;
      } else {
        running = 0;
      }
    }
    current = running;
    streaks[id] = { current, best };
  }

  return c.json(streaks);
});

export default trends;
```

- [ ] **Step 2: Mount route**

```typescript
import trends from "./routes/trends.ts";
app.route("/api/trends", trends);
```

- [ ] **Step 3: Render trend charts in app.js**

When the Trends view is toggled visible, fetch each trend endpoint and render:

1. **Weight** — SVG line chart (polyline, viewBox 300×90, stroke #ffb340, 1.8px). Range selector buttons (7d/30d/90d/all) filter data client-side. Summary row with min/max/current.

2. **Habit completion** (span 2) — CSS grid heat map: 7 rows (Mon-Sun) × N weeks of 11px cells, gap 3px, radius 2.5px. Color intensity = `rgba(255, 92, 31, 0.18 + 0.82 * (completed/total))`. Empty = `rgba(255,255,255,.05)`.

3. **Grok usage** (span 2) — Flex row of daily bars. Height proportional to count. Color: >= target = `#ff5c1f`, below = `rgba(255,92,31,.35)`. Dashed amber line at target height (15).

4. **Balance** — SVG line chart, stroke #ff5c1f. Summary row.

5. **Posting consistency** (span 2) — Amber heat map, same grid pattern as habits.

6. **Streaks** — Rows: habit label (110px) + progress bar (5px, #ff5c1f, width = current/best) + "current / best" counter.

7. **Reach-outs/week** — 12 weekly bars, amber. Current week = solid #ffb340.

8. **X.com growth** — SVG line chart, stroke #ffb340. Summary row.

9. **Identity practice** (span 2) — Heat map with 4-level coloring: none = empty, morning-only = `rgba(255,179,64,.45)`, evening-only = `rgba(255,92,31,.5)`, both = `rgba(255,120,50,.95)`. Legend top-right.

All charts use the same card shell (surface bg, border, radius, header) as Daily view cards.

- [ ] **Step 4: Test trends view**

Add several days of test data via the API, toggle to Trends view, verify all 9 cards render correctly with real data.

- [ ] **Step 5: Commit**

```bash
cd ~/vieren/dashboard
git add server/routes/trends.ts server/index.ts ui/app.js
git commit -m "feat: trends view — 9 chart cards with heat maps, line charts, bar charts, streaks"
```

---

### Task 11: System Integration — launchd + Notifications + Alias

**Files:**
- Create: `~/Library/LaunchAgents/com.vieren.dashboard.plist`
- Create: `~/Library/LaunchAgents/com.vieren.dashboard.morning.plist`
- Create: `~/Library/LaunchAgents/com.vieren.dashboard.evening.plist`
- Create: `~/vieren/dashboard/scripts/notify.sh`

**Interfaces:**
- Produces: Server auto-starts on login, macOS notifications at 8am/8pm, `dash` alias opens browser

- [ ] **Step 1: Create launchd plist for auto-start**

Create `~/Library/LaunchAgents/com.vieren.dashboard.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vieren.dashboard</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/richardvanderveren/.bun/bin/bun</string>
        <string>run</string>
        <string>server/index.ts</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/richardvanderveren/vieren/dashboard</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/vieren-dashboard.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/vieren-dashboard.err</string>
</dict>
</plist>
```

- [ ] **Step 2: Create notification script**

Create `~/vieren/dashboard/scripts/notify.sh`:

```bash
#!/bin/bash
MESSAGE="$1"
osascript -e "display notification \"$MESSAGE\" with title \"VIEREN\" sound name \"default\""
open "http://localhost:3000"
```

```bash
chmod +x ~/vieren/dashboard/scripts/notify.sh
```

- [ ] **Step 3: Create morning notification plist**

Create `~/Library/LaunchAgents/com.vieren.dashboard.morning.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vieren.dashboard.morning</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/richardvanderveren/vieren/dashboard/scripts/notify.sh</string>
        <string>Log your day</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

- [ ] **Step 4: Create evening notification plist**

Same as morning but label `com.vieren.dashboard.evening`, message `"Close out your day"`, hour `20`.

- [ ] **Step 5: Create `dash` alias**

Add to `~/.zshrc`:

```bash
alias dash='open http://localhost:3000'
```

- [ ] **Step 6: Load all launchd agents**

```bash
launchctl load ~/Library/LaunchAgents/com.vieren.dashboard.plist
launchctl load ~/Library/LaunchAgents/com.vieren.dashboard.morning.plist
launchctl load ~/Library/LaunchAgents/com.vieren.dashboard.evening.plist
```

- [ ] **Step 7: Test**

```bash
# Verify server is running
curl -s http://localhost:3000/api/health

# Test the alias
source ~/.zshrc
dash  # should open browser

# Test notification (manual trigger)
~/vieren/dashboard/scripts/notify.sh "Test notification"
```

- [ ] **Step 8: Commit**

```bash
cd ~/vieren/dashboard
git add scripts/
git commit -m "feat: system integration — launchd auto-start, 8am/8pm notifications, dash alias"
```

---

### Task 12: Final Integration + Copy Fable Reference

**Files:**
- Create: `~/vieren/dashboard/design/` (copy Fable handoff for reference)
- Modify: `~/vieren/dashboard/ui/app.js` (streak calculation)

**Interfaces:**
- Produces: Working streak counter in header, Fable design files archived in repo

- [ ] **Step 1: Copy Fable handoff into the project**

```bash
mkdir -p ~/vieren/dashboard/design
cp /tmp/fable-export/design_handoff_daily_dashboard/README.md ~/vieren/dashboard/design/fable-handoff.md
cp "/tmp/fable-export/design_handoff_daily_dashboard/Daily Dashboard.dc.html" ~/vieren/dashboard/design/fable-reference.html
```

- [ ] **Step 2: Implement streak calculation**

Add streak logic to `app.js`: fetch `/api/trends/habits`, calculate the longest consecutive run of days where ALL non-negotiable habits (eggs, protein, workout, meditate, steps >= 10000) were completed. Display in the header streak chip.

Streak rules:
- A "complete day" = all check habits are true AND steps >= 10000
- Count consecutive complete days backward from today
- Display as "X DAY STREAK" with the orange-tinted chip styling from the Fable handoff

- [ ] **Step 3: End-to-end test**

Start fresh, run through a full day:
1. Open dashboard (`dash`)
2. Check off morning identity practices
3. Check off body habits, enter steps
4. Enter weight
5. Enter balance
6. Increment grok counter
7. Check off recorded content
8. Add a reach-out
9. Drag a photo → verify it appears in `~/vieren/image/diary/` and `diary.json` is updated
10. Toggle to Trends view — verify charts render (even if sparse data)
11. Click "Close out day → Obsidian" — verify markdown at `~/AOOA/vieren/log/`
12. Check evening identity practices
13. Verify streak updates

- [ ] **Step 4: Commit**

```bash
cd ~/vieren/dashboard
git add design/ ui/app.js
git commit -m "feat: streak calculation, Fable design reference archived, V1 complete"
```

---

## Post-Implementation

After all tasks are complete:

1. Update `~/AOOA/vieren/todo/master.md` — check off the "Build daily dashboard" item
2. Verify launchd agents persist across restart
3. Start using it daily — the tool will evolve based on real usage
