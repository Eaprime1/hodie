#!/data/data/com.termux/files/usr/bin/bash
# Phoenix Hub - Clean Batch Staging
# Clears all files in the batch staging area

STAGING=~/storage/downloads/phoenix_hub/batch_staging
LOG=~/storage/downloads/phoenix_hub/logs/clean_staging.log
timestamp=$(date +%Y%m%d_%H%M%S)

mkdir -p "$STAGING"
mkdir -p "$(dirname "$LOG")"

echo "🧹 Cleaning staging folder [$timestamp]" | tee -a "$LOG"

rm "$STAGING"/*.pdf 2>/dev/null
echo "✅ Staging cleared [$timestamp]" | tee -a "$LOG"