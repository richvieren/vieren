#!/bin/bash
# Auto-generate diary.json from image/diary/ date subfolders
# Structure: image/diary/2026-07-19/photo.jpg
# Run after dropping new photos, before pushing

cd "$(dirname "$0")"

entries=()
total=0

for dir in $(ls -d image/diary/*/  2>/dev/null | sort -r); do
  date=$(basename "$dir")
  photos=$(ls "$dir"*.{jpg,jpeg,png,webp} 2>/dev/null | sed "s|$dir||")

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

# Write JSON
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
