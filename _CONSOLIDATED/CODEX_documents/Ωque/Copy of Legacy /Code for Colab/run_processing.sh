#!/data/data/com.termux/files/usr/bin/bash
# Phoenix Hub - Batch Processor Launcher
# Runs the Phoenix Python processor for staged files

SCRIPT_PATH=~/storage/downloads/phoenix_hub/scripts/phoenix_batch_processor.py
LOG=~/storage/downloads/phoenix_hub/logs/run_processing.log

timestamp=$(date +%Y%m%d_%H%M%S)
echo "🚀 Running Phoenix Processor [$timestamp]" | tee -a "$LOG"

python "$SCRIPT_PATH" 2>&1 | tee -a "$LOG"

echo "🎯 Processor run complete [$timestamp]" | tee -a "$LOG"