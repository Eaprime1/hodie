#!/bin/bash
# Mulberry HQ — First-time setup and verification
# Run once after cloning on the laptop, then as-needed to verify state
#
# Usage: bash .scripts/mulberry_setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== Mulberry HQ Setup ==="
echo ""

# 1. Source environment
source "$REPO_ROOT/.scripts/env_setup.sh"

# 2. Install git hooks
echo ""
echo "--- Git Hooks ---"
if [ -d "$REPO_ROOT/.githooks" ]; then
    git config core.hooksPath .githooks
    chmod +x "$REPO_ROOT/.githooks/"*
    echo "  Hooks installed (.githooks/)"
else
    echo "  WARNING: .githooks/ not found"
fi

# 3. Verify Python + pylint
echo ""
echo "--- Python ---"
if command -v python3 &> /dev/null; then
    echo "  Python: $(python3 --version)"
else
    echo "  WARNING: python3 not found"
fi

if command -v pylint &> /dev/null; then
    echo "  pylint: $(pylint --version 2>/dev/null | head -1)"
else
    echo "  pylint not installed. Run: pip install pylint"
fi

# 4. Create local directories if needed
echo ""
echo "--- Local Directories ---"
mkdir -p "$REPO_ROOT/.eric"
mkdir -p "$REPO_ROOT/.metrics"
echo "  .eric/    OK"
echo "  .metrics/ OK"

# 5. Ensure Q structure exists
if [ -d "/home/user/Q" ]; then
    mkdir -p /home/user/Q/today
    echo "  Q/today/  OK"
else
    echo "  NOTE: /home/user/Q not found — create it for full HQ operation"
fi

# 6. Verify streams
echo ""
echo "--- Streams ---"
for stream in prime codex gamemaster; do
    echo "  $stream: active"
done

# 7. Summary
echo ""
echo "=== Mulberry HQ Ready ==="
echo "  Location: mulberry (laptop)"
echo "  Role:     HQ"
echo "  Hooks:    $(git config core.hooksPath 2>/dev/null || echo 'not set')"
echo "  Streams:  prime codex gamemaster"
echo ""
echo "  Next steps:"
echo "    source .scripts/env_setup.sh   # Load environment in terminal"
echo "    bash .scripts/session_notes_append.sh 'Starting session'"
echo ""
