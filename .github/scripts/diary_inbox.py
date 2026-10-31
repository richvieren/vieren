"""Photo diary inbox: files phone uploads into the diary.

The iPhone shortcut "Add to diary" uploads into inbox/:
  <stamp>-<n>__<YYYY-MM-DD>.jpg   one per photo (metadata already stripped on the phone,
                                  the date taken is carried in the name)
  <stamp>.json                    {"tags": "a,b", "eden": "yes"|"no", "caption": "..."}

For every <stamp>.json this script:
  1. resizes each photo to 2048px long edge, saves it to image/diary/<date>/<stamp>-<n>.jpg
     with no metadata, and writes the 400px-wide thumbnail to image/diary-thumbs/<date>/
  2. adds the photos to diary.json (same one-line-per-entry layout, newest first)
  3. deletes the inbox files
  4. if eden is on, appends a job to $EDEN_JOBS for eden_post.py

Same rules as vieren/sops/sop-photo-diary.md: tags only from the list, no tag is ever invented.
"""
import json
import os
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
INBOX = ROOT / "inbox"
DIARY_JSON = ROOT / "diary.json"
TAGS = {"bts", "wolf-children", "vieren", "off-the-grid", "portfolio"}
LONG_EDGE = 2048
THUMB_WIDTH = 400
PHOTO_RE = re.compile(r"^(?P<stamp>.+)-(?P<n>\d+)__(?P<date>\d{4}-\d{2}-\d{2})\.jpe?g$", re.I)


def write_diary(entries):
    entries.sort(key=lambda e: e["date"], reverse=True)
    lines = []
    for e in entries:
        body = json.dumps(e, ensure_ascii=False, separators=(", ", ": "))
        lines.append("  { " + body[1:-1] + " }")
    DIARY_JSON.write_text("[\n" + ",\n".join(lines) + "\n]\n")


def add_to_diary(entries, date, tags, files):
    entry = next((e for e in entries if e["date"] == date), None)
    if entry is None:
        entries.append({"date": date, "tags": tags, "photos": list(files)})
        return
    for f in files:
        # A day that already has other tags keeps them; the new photo carries its own
        entry["photos"].append(f if sorted(entry.get("tags", [])) == sorted(tags) else {"file": f, "tags": tags})


def save_photo(src, date, name):
    out = ROOT / "image" / "diary" / date / name
    thumb = ROOT / "image" / "diary-thumbs" / date / name
    out.parent.mkdir(parents=True, exist_ok=True)
    thumb.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((LONG_EDGE, LONG_EDGE), Image.LANCZOS)
        im.save(out, "JPEG", quality=85, optimize=True, progressive=True)  # no exif= → no metadata
        t = im.copy()
        t.thumbnail((THUMB_WIDTH, 100000), Image.LANCZOS)
        t.save(thumb, "JPEG", quality=80, optimize=True)


def main():
    jobs_path = os.environ.get("EDEN_JOBS")
    entries = json.loads(DIARY_JSON.read_text())
    done = 0
    for meta_path in sorted(INBOX.glob("*.json")):
        stamp = meta_path.stem
        meta = json.loads(meta_path.read_text())
        tags = [t.strip() for t in str(meta.get("tags", "")).replace("\n", ",").split(",") if t.strip()]
        bad = [t for t in tags if t not in TAGS]
        if bad or not tags:
            sys.exit(f"{meta_path.name}: tags must be from {sorted(TAGS)}, got {tags}")
        photos = []
        for p in INBOX.iterdir():
            m = PHOTO_RE.match(p.name)
            if m and m["stamp"] == stamp:
                photos.append((int(m["n"]), m["date"], p))
        if not photos:
            sys.exit(f"{meta_path.name}: no photos named {stamp}-<n>__<date>.jpg in inbox/")
        photos.sort()

        by_date, posted = {}, []
        for n, date, p in photos:
            name = f"{stamp}-{n}.jpg"
            save_photo(p, date, name)
            by_date.setdefault(date, []).append(name)
            posted.append(f"image/diary/{date}/{name}")
            p.unlink()
            print(f"{p.name} -> {posted[-1]}")
        for date, files in by_date.items():
            add_to_diary(entries, date, tags, files)
        meta_path.unlink()
        done += 1

        eden = str(meta.get("eden", "")).strip().lower() in {"yes", "true", "1"}
        caption = str(meta.get("caption", "")).strip()
        if eden and not caption:
            print(f"{stamp}: Eden asked but no caption given, so no Eden post")
        elif eden and jobs_path:
            with open(jobs_path, "a") as f:
                f.write(json.dumps({"key": f"diary-{stamp}", "caption": caption, "photos": posted}) + "\n")

    if done:
        write_diary(entries)
    print(f"processed {done} upload(s)")


if __name__ == "__main__":
    main()
