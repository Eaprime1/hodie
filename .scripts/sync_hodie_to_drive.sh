#!/bin/bash
# sync_hodie_to_drive.sh — Sync hodie to/from Google Drive via rclone
#
# Usage:
#   bash .scripts/sync_hodie_to_drive.sh push    # Local → Google Drive
#   bash .scripts/sync_hodie_to_drive.sh pull    # Google Drive → Local
#   bash .scripts/sync_hodie_to_drive.sh status  # Dry-run: show what would change
#
# Prerequisites:
#   1. Install rclone:
#        Linux:  sudo apt install rclone
#        Termux: pkg install rclone
#   2. Configure Google Drive remote:
#        rclone config    # name it 'gdrive', type: drive, full access
#   3. Verify:
#        rclone lsd gdrive:
#
# Environment variables (override defaults):
#   GDRIVE_REMOTE  — rclone remote name (default: gdrive)
#   GDRIVE_FOLDER  — folder on Drive    (default: hodie)
#   HODIE_PATH     — local hodie path   (auto-detected via env_setup.sh)
#
# ∰◊€π¿🌌∞

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load location env (sets HODIE_PATH, LOCATION_NAME, etc.)
if [ -f "$REPO_ROOT/.scripts/env_setup.sh" ]; then
    # shellcheck source=/dev/null
    source "$REPO_ROOT/.scripts/env_setup.sh" 2>/dev/null || true
fi

# ── Configuration ────────────────────────────────────────────────────────────
GDRIVE_REMOTE="${GDRIVE_REMOTE:-gdrive}"
GDRIVE_FOLDER="${GDRIVE_FOLDER:-hodie}"
LOCAL_PATH="${HODIE_PATH:-$REPO_ROOT}"
REMOTE_PATH="${GDRIVE_REMOTE}:${GDRIVE_FOLDER}"
MODE="${1:-status}"

echo "∰ Hodie Drive Sync"
echo "  Location: ${LOCATION_NAME:-unknown}"
echo "  Local:    $LOCAL_PATH"
echo "  Remote:   $REMOTE_PATH"
echo "  Mode:     $MODE"
echo "─────────────────────────────────────────────────"

# ── Preflight checks ─────────────────────────────────────────────────────────
if ! command -v rclone &>/dev/null; then
    echo "✗ rclone not found. Install it first:"
    echo "  Linux:  sudo apt install rclone"
    echo "  Termux: pkg install rclone"
    echo "  See: .claude/RCLONE_QUICK_CONFIG.md"
    exit 1
fi

if ! rclone listremotes 2>/dev/null | grep -Fxq "${GDRIVE_REMOTE}:"; then
    echo "✗ rclone remote '${GDRIVE_REMOTE}' not configured."
    echo ""
    echo "Set it up with:"
    echo "  rclone config"
    echo "  → New remote → name: gdrive → type: drive → full access"
    echo ""
    echo "Or if your remote has a different name, set:"
    echo "  GDRIVE_REMOTE=your_remote_name bash .scripts/sync_hodie_to_drive.sh"
    echo ""
    echo "See: .claude/RCLONE_QUICK_CONFIG.md"
    exit 1
fi

if [ ! -d "$LOCAL_PATH" ]; then
    echo "✗ Local path not found: $LOCAL_PATH"
    exit 1
fi

# ── Shared rclone flags ───────────────────────────────────────────────────────
# Exclude non-content files that belong on Git but not Drive backup,
# plus large regeneratable outputs.
RCLONE_FLAGS=(
    --progress
    --drive-skip-shortcuts
    --exclude ".git/**"
    --exclude "**/__pycache__/**"
    --exclude "**/*.pyc"
    --exclude "**/*.pyo"
    --exclude ".env"
    --exclude "**/*.swp"
    --exclude "**/*.swo"
    --exclude "**/*~"
    --exclude "**/*.tmp"
    --exclude ".server_root/**"
    # crawler_output/summaries can be large; exclude individual JSONs
    # but keep the master summary and maps
    --exclude "crawler_output/summaries/**"
)

# ── Mode dispatch ─────────────────────────────────────────────────────────────
case "$MODE" in

    push)
        echo "→ Pushing local → Drive..."
        echo "  (local wins; Drive is updated to match)"
        rclone sync "$LOCAL_PATH/" "$REMOTE_PATH/" "${RCLONE_FLAGS[@]}"
        echo ""
        echo "✓ Push complete — $REMOTE_PATH updated"
        ;;

    pull)
        echo "← Pulling Drive → local..."
        echo "  (Drive wins; local is updated to match)"
        rclone sync "$REMOTE_PATH/" "$LOCAL_PATH/" "${RCLONE_FLAGS[@]}"
        echo ""
        echo "✓ Pull complete — $LOCAL_PATH updated"
        ;;

    status|dry-run|check)
        echo "? Dry run — showing what push would change..."
        echo ""
        rclone sync "$LOCAL_PATH/" "$REMOTE_PATH/" "${RCLONE_FLAGS[@]}" --dry-run 2>&1
        echo ""
        echo "  Run with 'push' to apply these changes."
        ;;

    *)
        echo "Usage: bash .scripts/sync_hodie_to_drive.sh [push|pull|status]"
        echo ""
        echo "  push    Local → Google Drive  (local wins)"
        echo "  pull    Google Drive → Local  (Drive wins)"
        echo "  status  Dry-run: show what would change"
        echo ""
        echo "Environment overrides:"
        echo "  GDRIVE_REMOTE=gdrive_terminal  (if remote is named differently)"
        echo "  GDRIVE_FOLDER=Q/hodie          (if Drive folder path differs)"
        exit 1
        ;;

esac
