#!/bin/bash
# ACP - Proceed: Move to next stage, update status markers
# Usage: ./acp_proceed.sh [status_from] [status_to]

STATUS_FROM="${1:-DRAFT}"
STATUS_TO="${2:-REVIEW}"

echo "➡️  ACP PROCEED - Advancing status..."
echo "From: $STATUS_FROM → To: $STATUS_TO"
echo ""

# Find and update status markers
find . -name "*.md" -type f -exec grep -l "Status: $STATUS_FROM" {} \; | while read file; do
    echo "Updating: $file"
    sed -i "s/Status: $STATUS_FROM/Status: $STATUS_TO/g" "$file"
done

echo ""
echo "✓ Proceed complete - Status advanced"
