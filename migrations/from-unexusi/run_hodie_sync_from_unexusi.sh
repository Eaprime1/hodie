#!/bin/bash
# run_hodie_sync.sh — Server/cron wrapper for syncing the hodie folder from Google Drive
#
# Usage:
#   bash scripts/run_hodie_sync.sh                          # uses .secrets/gdrive-key.json
#   bash scripts/run_hodie_sync.sh /path/to/key.json        # explicit credentials path
#
# Cron example (noon UTC daily):
#   0 12 * * * /path/to/UNEXUSI/scripts/run_hodie_sync.sh >> /var/log/hodie-sync.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
CREDS="${1:-$REPO_ROOT/.secrets/gdrive-key.json}"

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Starting hodie sync..."

cd "$REPO_ROOT"

python3 scripts/sync_hodie.py --credentials "$CREDS"

git add hodie/
if git diff --cached --quiet; then
    echo "No new files — nothing to commit."
else
    git config user.name "Hodie Sync"
    git config user.email "hodie-sync@localhost"
    git commit -m "hodie: sync $(date -u '+%Y-%m-%d')"
    git pull --rebase || { git rebase --abort; exit 1; }
    git push
    echo "Committed and pushed synced files."
fi

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Done."
