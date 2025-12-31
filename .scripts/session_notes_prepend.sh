#!/bin/bash
# Session Notes Prepend - Add note to beginning of document
# Usage: ./session_notes_prepend.sh [file_path] "Your note here"

FILE_PATH="$1"
NOTE="$2"
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S)

if [ ! -f "$FILE_PATH" ]; then
    echo "✗ File not found: $FILE_PATH"
    exit 1
fi

# Create temp file with prepended note
TEMP_FILE=$(mktemp)
cat > "$TEMP_FILE" <<EOF
<!-- Prepended: [$TIMESTAMP] $NOTE -->

EOF
cat "$FILE_PATH" >> "$TEMP_FILE"

# Replace original with temp
mv "$TEMP_FILE" "$FILE_PATH"

echo "✓ Note prepended to $FILE_PATH"
