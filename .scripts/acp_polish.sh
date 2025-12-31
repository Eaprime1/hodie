#!/bin/bash
# ACP - Polish: Clean up, format, improve existing content
# Usage: ./acp_polish.sh [target_directory]

TARGET="${1:-.}"

echo "🔧 ACP POLISH - Cleaning and formatting..."
echo "Target: $TARGET"
echo ""

# Remove trailing whitespace
echo "→ Removing trailing whitespace..."
find "$TARGET" -name "*.md" -type f -exec sed -i 's/[[:space:]]*$//' {} +

# Ensure files end with newline
echo "→ Ensuring files end with newline..."
find "$TARGET" -name "*.md" -type f -exec sh -c 'tail -c1 "$0" | read -r _ || echo "" >> "$0"' {} \;

# Check for TODO markers
echo "→ Scanning for TODO markers..."
grep -r "TODO\|FIXME\|XXX" "$TARGET" --include="*.md" | head -10

echo ""
echo "✓ Polish complete"
