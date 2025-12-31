#!/bin/bash
# Session Notes Append - Add note to end of current session
# Usage: ./session_notes_append.sh "Your note here"

SESSION_DATE=$(date +%Y-%m-%d)
NOTES_FILE="/storage/emulated/0/pixel8a/Q/hodie/.eric/session_notes_${SESSION_DATE}.md"

# Create file if doesn't exist
if [ ! -f "$NOTES_FILE" ]; then
    cat > "$NOTES_FILE" <<EOF
# Session Notes - $SESSION_DATE

---

EOF
fi

# Append note with timestamp
TIMESTAMP=$(date +%H:%M:%S)
echo "" >> "$NOTES_FILE"
echo "## [$TIMESTAMP] $1" >> "$NOTES_FILE"
echo "" >> "$NOTES_FILE"

echo "✓ Note appended to $NOTES_FILE"
