# Photo Diary — Design Spec

## Overview

An infinite photo diary for vieren.studio. A personal visual log updated a few times per week. Latest entries appear on the homepage as a film strip carousel; the full diary lives on its own page as a vertical scroll.

## Data Layer

### `diary.json` (repo root)

```json
[
  {
    "date": "2026-07-13",
    "photos": ["cape-town-bts-01.jpg", "cape-town-bts-02.jpg"],
    "location": "Cape Town",
    "tags": ["behind the scenes", "travel"]
  }
]
```

- Array of entries, newest first
- `date` — required, `YYYY-MM-DD`
- `photos` — required, array of filenames (1 or more), stored in `image/diary/`
- `location` — optional string
- `tags` — optional array of strings

### `image/diary/`

All diary photos live here. Compressed to reasonable web size before committing.

### `~/diary-drop/`

Staging folder on Richard's Mac. Drop photos here, tell Claude the metadata, Claude handles the rest.

## Workflow

1. Richard drops photo(s) in `~/diary-drop/`
2. Richard tells Claude: "diary entry. 20260713 - cape town - behind the scenes, travel"
3. Claude moves photos to `image/diary/`, compresses if needed, prepends entry to `diary.json`, commits, pushes
4. Live on GitHub Pages

## Homepage Section — Film Strip Carousel

### Position
Above the "creative retainer" / deck CTA section, near the bottom of the homepage.

### Layout
- Section title top left (e.g. "PHOTO DIARY")
- PREV / NEXT controls top right
- Full-width film strip below

### Film Strip (CSS, no images)
- Dark (#1a1a1a) border top and bottom
- Sprocket holes: repeating rounded rectangles along top and bottom edges (CSS pseudo-elements or repeating-linear-gradient)
- Photos sit inside the strip with small gaps between them
- Frame counter text along the bottom: `VIEREN STUDIO — 01`, `— 02`, etc. (monospace, small, muted)

### Behavior
- Shows the latest ~10 diary entries (one photo per entry — first photo if multi-photo)
- Auto-slides left: smooth slide to next photo, pause ~3s, repeat
- PREV / NEXT buttons override auto-play, resume after idle
- Touch swipe support on mobile
- Clicking anywhere on the strip navigates to `diary.html`

### Responsive
- Strip height scales proportionally
- On mobile: fewer visible photos (2-3 instead of 5-6)
- PREV/NEXT still accessible

## Diary Page — `diary.html`

### Layout
- Same nav/footer as homepage
- Vertical scroll, newest first
- Each entry is a discrete block

### Per Entry
- Film strip border treatment (same sprocket holes + dark border as homepage)
- Date displayed prominently — monospace, fits the site's technical/viewfinder aesthetic
- Location below date (if present), smaller text
- Tags below location (if present), smallest text, comma-separated

### Photo Display Within Entry
- **Single photo**: framed in the film strip border, static
- **Multiple photos**: horizontal swipe/slide within the film border frame. Same slide-pause-slide mechanic. Dots or frame counter indicate position. Touch swipe on mobile.

### Infinite Scroll
- Initially loads the latest ~20 entries
- Loads more as user scrolls (or loads all if total count is small enough — under 100 entries)

## Tech Stack

- Vanilla HTML + CSS + JS (no dependencies, matches rest of site)
- `fetch('diary.json')` on page load
- CSS-only sprocket holes and film borders
- `IntersectionObserver` for lazy loading images and infinite scroll trigger
- Touch events for mobile swipe
- `requestAnimationFrame` or CSS animation for auto-slide

## File Structure

```
vieren/
├── diary.json                    # entry data
├── diary.html                    # full diary page
├── image/diary/                  # all diary photos
├── index.html                    # homepage (film strip section added)
└── ~/diary-drop/                 # staging folder (outside repo)
```
