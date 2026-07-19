#!/usr/bin/env bash
# Auto-generate diary.json from image/diary/ date subfolders
# Structure: image/diary/2026-07-19/photo.jpg
#
# Drop photos into image/diary/unsorted/ and this script
# will auto-sort them into date folders using EXIF data.
#
# Run after dropping new photos, before pushing.

cd "$(dirname "$0")"

# Step 1: Sort any unsorted photos by EXIF date
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
  # Remove unsorted if empty
  rmdir "image/diary/unsorted" 2>/dev/null
  if [ $moved -gt 0 ]; then
    echo "Sorted $moved photos."
  fi
fi

# Step 2: Build diary.json from date subfolders
entries=()
total=0

for dir in $(ls -d image/diary/*/  2>/dev/null | sort -r); do
  date=$(basename "$dir")
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

echo "diary.json updated: ${#entries[@]} dates, $total photos."
