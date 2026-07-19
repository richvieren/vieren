#!/bin/bash
# Auto-generate diary.json from image/diary/ folder
# Run after dropping new photos, before pushing

cd "$(dirname "$0")"

photos=$(ls image/diary/*.{jpg,jpeg,png,webp} 2>/dev/null | sed 's|image/diary/||' | sort)

if [ -z "$photos" ]; then
  echo "[]" > diary.json
  echo "No photos found. diary.json cleared."
  exit 0
fi

# Build JSON array
echo "[" > diary.json
echo "  { \"date\": \"$(date +%Y-%m-%d)\", \"photos\": [" >> diary.json

first=true
while IFS= read -r photo; do
  if [ "$first" = true ]; then
    first=false
  else
    echo "," >> diary.json
  fi
  printf "    \"%s\"" "$photo" >> diary.json
done <<< "$photos"

echo "" >> diary.json
echo "  ] }" >> diary.json
echo "]" >> diary.json

count=$(echo "$photos" | wc -l | tr -d ' ')
echo "diary.json updated with $count photos."
