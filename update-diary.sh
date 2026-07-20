#!/usr/bin/env bash
# Photo diary pipeline
# 1. Sort unsorted photos by EXIF date
# 2. Detect and remove duplicates (by content hash)
# 3. Generate thumbnails for homepage strip
# 4. Build diary.json
#
# Drop photos into image/diary/unsorted/ or date folders
# Run this script, then push.

cd "$(dirname "$0")"

THUMB_WIDTH=400
THUMB_QUALITY=80

# ── Step 1: Sort unsorted photos by EXIF date ──
if [ -d "image/diary/unsorted" ]; then
  moved=0
  for f in image/diary/unsorted/*.jpg image/diary/unsorted/*.jpeg image/diary/unsorted/*.png image/diary/unsorted/*.webp; do
    [ -f "$f" ] || continue
    date=$(mdls -name kMDItemContentCreationDate "$f" 2>/dev/null | awk '{print $3}')
    if [ -z "$date" ] || [ "$date" = "(null)" ]; then
      date=$(date +%Y-%m-%d)
      echo "  No EXIF date for $(basename "$f"), using today: $date"
    fi
    mkdir -p "image/diary/$date"
    mv "$f" "image/diary/$date/"
    echo "  $(basename "$f") → $date/"
    moved=$((moved + 1))
  done
  rmdir "image/diary/unsorted" 2>/dev/null
  if [ $moved -gt 0 ]; then
    echo "Sorted $moved photos."
  fi
fi

# ── Step 2: Duplicate detection (by content hash) ──
echo ""
echo "Checking for duplicates..."
hashfile=$(mktemp)
dupes=0
for dir in image/diary/*/; do
  [ -d "$dir" ] || continue
  for f in "$dir"*.jpg "$dir"*.jpeg "$dir"*.png "$dir"*.webp; do
    [ -f "$f" ] || continue
    hash=$(md5 -q "$f")
    if grep -q "^$hash " "$hashfile" 2>/dev/null; then
      original=$(grep "^$hash " "$hashfile" | head -1 | cut -d' ' -f2-)
      echo "  DUPE: $f is identical to $original — removing"
      rm "$f"
      dupes=$((dupes + 1))
    else
      echo "$hash $f" >> "$hashfile"
    fi
  done
done
rm -f "$hashfile"
if [ $dupes -gt 0 ]; then
  echo "Removed $dupes duplicates."
else
  echo "No duplicates found."
fi

# ── Step 3: Generate thumbnails ──
echo ""
echo "Generating thumbnails..."
thumbs=0
for dir in image/diary/*/; do
  [ -d "$dir" ] || continue
  date=$(basename "$dir")
  mkdir -p "image/diary-thumbs/$date"
  for f in "$dir"*.jpg "$dir"*.jpeg "$dir"*.png "$dir"*.webp; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    thumb="image/diary-thumbs/$date/$fname"
    if [ -f "$thumb" ]; then
      continue
    fi
    sips --resampleWidth $THUMB_WIDTH "$f" --out "$thumb" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      thumbs=$((thumbs + 1))
    else
      echo "  WARN: failed to thumbnail $fname"
    fi
  done
done
if [ $thumbs -gt 0 ]; then
  echo "Generated $thumbs new thumbnails."
else
  echo "All thumbnails up to date."
fi

# ── Step 4: Check file sizes ──
echo ""
echo "Size check:"
for dir in image/diary/*/; do
  [ -d "$dir" ] || continue
  for f in "$dir"*.jpg "$dir"*.jpeg "$dir"*.png "$dir"*.webp; do
    [ -f "$f" ] || continue
    size=$(stat -f%z "$f")
    kb=$((size / 1024))
    if [ $kb -gt 500 ]; then
      echo "  LARGE: $(basename "$f") — ${kb}KB (consider compressing)"
    fi
  done
done

# ── Step 5: Build diary.json (uses thumbnails for strip) ──
entries=()
total=0

for dir in $(ls -d image/diary/*/ 2>/dev/null | sort -r); do
  date=$(basename "$dir")
  # Skip thumbs dir
  [ "$date" = "diary-thumbs" ] && continue
  photos=$(ls "$dir"*.jpg "$dir"*.jpeg "$dir"*.png "$dir"*.webp 2>/dev/null | sed "s|$dir||")

  if [ -z "$photos" ]; then
    continue
  fi

  photo_json=""
  first=true
  while IFS= read -r photo; do
    if [ "$first" = true ]; then
      first=false
    else
      photo_json="$photo_json, "
    fi
    photo_json="$photo_json\"$photo\""
    total=$((total + 1))
  done <<< "$photos"

  entries+=("  { \"date\": \"$date\", \"photos\": [$photo_json] }")
done

if [ ${#entries[@]} -eq 0 ]; then
  echo "[]" > diary.json
  echo "No photos found. diary.json cleared."
  exit 0
fi

echo "[" > diary.json
for i in "${!entries[@]}"; do
  if [ $i -lt $((${#entries[@]} - 1)) ]; then
    echo "${entries[$i]}," >> diary.json
  else
    echo "${entries[$i]}" >> diary.json
  fi
done
echo "]" >> diary.json

echo ""
echo "diary.json updated: ${#entries[@]} dates, $total photos."
