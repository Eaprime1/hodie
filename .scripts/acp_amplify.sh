#!/bin/bash
# ACP - Amplify: Expand, elaborate, add detail
# Usage: ./acp_amplify.sh [target_file]

TARGET="$1"

if [ -z "$TARGET" ]; then
    echo "Usage: ./acp_amplify.sh [target_file]"
    exit 1
fi

echo "📢 ACP AMPLIFY - Expanding content..."
echo "Target: $TARGET"
echo ""

# Find short sections (< 3 lines between headers)
echo "→ Short sections that could be expanded:"
awk '/^##/ {if (NR>1 && lines<3) print prev_header " (" lines " lines)"; prev_header=$0; lines=0; next} {lines++}' "$TARGET"

# Find stub markers
echo ""
echo "→ Stub markers found:"
grep -n "TODO\|TBD\|...\|\[expand\]" "$TARGET"

echo ""
echo "✓ Amplify analysis complete"
