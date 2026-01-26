#!/bin/bash
# Laptop Session Notes - Add note to current session (Laptop version)
# Usage: ./laptop_session_notes.sh "Your note here"

SESSION_DATE=$(date +%Y-%m-%d)
NOTES_FILE="/home/user/Q/hodie/.eric/session_notes_${SESSION_DATE}.md"

# Create file if doesn't exist
if [ ! -f "$NOTES_FILE" ]; then
    mkdir -p "$(dirname "$NOTES_FILE")"
    cat > "$NOTES_FILE" <<EOF
# Session Notes - $SESSION_DATE

**Environment**: New Laptop (faster machine)
**Q Path**: /home/user/Q/

---

EOF
fi

# Append note with timestamp
TIMESTAMP=$(date +%H:%M:%S)
echo "" >> "$NOTES_FILE"
echo "## [$TIMESTAMP] $1" >> "$NOTES_FILE"
echo "" >> "$NOTES_FILE"

echo "✓ Note appended to $NOTES_FILE"
cat "$NOTES_FILE"
