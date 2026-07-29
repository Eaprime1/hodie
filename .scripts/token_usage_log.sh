#!/bin/bash
# Token Usage Logger - Track token consumption patterns
# Usage: ./token_usage_log.sh [tokens_used] [task_description]

TOKENS_USED="$1"
TASK_DESC="$2"
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S)
LOG_FILE="/storage/emulated/0/pixel8a/Q/hodie/.metrics/token_usage.log"

# Create metrics directory if needed
mkdir -p "$(dirname "$LOG_FILE")"

# Create log file with header if doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    echo "timestamp,tokens_used,task_description" > "$LOG_FILE"
fi

# Append entry
echo "$TIMESTAMP,$TOKENS_USED,\"$TASK_DESC\"" >> "$LOG_FILE"

# Show recent stats
echo "✓ Token usage logged: $TOKENS_USED tokens for '$TASK_DESC'"
echo ""
echo "Recent usage:"
tail -5 "$LOG_FILE" | column -t -s,

# Calculate session total
SESSION_DATE=$(date +%Y-%m-%d)
SESSION_TOTAL=$(grep "^$SESSION_DATE" "$LOG_FILE" | awk -F, '{sum+=$2} END {print sum}')
echo ""
echo "Session total ($SESSION_DATE): $SESSION_TOTAL tokens"
