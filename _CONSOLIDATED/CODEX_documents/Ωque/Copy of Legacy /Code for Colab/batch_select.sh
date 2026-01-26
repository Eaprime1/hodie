#!/data/data/com.termux/files/usr/bin/bash
# Phoenix Hub - Prime Batch Selector
# Selects a prime number of documents and stages them for processing
# Logs batch info for future reference

SRC=~/storage/downloads/phoenix_hub/incoming_documents
DST=~/storage/downloads/phoenix_hub/batch_staging
LOG=~/storage/downloads/phoenix_hub/logs/batch_select.log
PRIME_BATCH_SIZE=17  # Can be changed to 11, 13, 19, etc.

mkdir -p "$DST"
mkdir -p "$(dirname "$LOG")"

# Get list of files
files=($(ls "$SRC"/*.pdf 2>/dev/null | head -n "$PRIME_BATCH_SIZE"))
count=${#files[@]}
timestamp=$(date +%Y%m%d_%H%M%S)

if [ "$count" -eq 0 ]; then
  echo "🚫 No files to stage. [$timestamp]" | tee -a "$LOG"
  exit 1
fi

echo "📦 Staging $count files for processing [$timestamp]" | tee -a "$LOG"
for f in "${files[@]}"; do
  fname=$(basename "$f")
  cp "$f" "$DST/$fname"
  echo "→ Staged: $fname" | tee -a "$LOG"
done

echo "✅ Prime batch staging complete [$timestamp]" | tee -a "$LOG"