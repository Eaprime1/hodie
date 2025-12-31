#!/bin/bash
# Consolidate Unsorted Files - Move loose files to sorting folder
# Usage: ./consolidate_unsorted.sh [source_dir]

SOURCE_DIR="${1:-.}"
SORTING_DIR="$SOURCE_DIR/_SORTING"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "📦 Consolidating unsorted files..."
echo "Source: $SOURCE_DIR"
echo "Target: $SORTING_DIR"
echo ""

# Create sorting folder with timestamp subdirectory
mkdir -p "$SORTING_DIR/batch_$TIMESTAMP"

# Find loose files (not in organized folders, exclude system files)
echo "Finding loose files..."

# Files in root of source dir (not in subdirectories)
find "$SOURCE_DIR" -maxdepth 1 -type f \
    ! -name "README.md" \
    ! -name "QUICK_START.md" \
    ! -name ".gitignore" \
    ! -name "*.md" \
    -print | while read file; do
    filename=$(basename "$file")
    echo "  → $filename"
    mv "$file" "$SORTING_DIR/batch_$TIMESTAMP/"
done

# Count what we moved
MOVED_COUNT=$(ls -1 "$SORTING_DIR/batch_$TIMESTAMP/" 2>/dev/null | wc -l)

echo ""
if [ "$MOVED_COUNT" -gt 0 ]; then
    echo "✓ Moved $MOVED_COUNT files to sorting folder"
    echo "Location: $SORTING_DIR/batch_$TIMESTAMP/"
else
    echo "✓ No loose files found - already organized!"
    rmdir "$SORTING_DIR/batch_$TIMESTAMP" 2>/dev/null
fi
