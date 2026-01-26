#!/bin/bash
# Environment Setup - Cross-platform path configuration
# Usage: source .scripts/env_setup.sh

# Detect environment
if [ -d "/storage/emulated/0/pixel8a" ]; then
    # Android/Termux environment
    export Q_ROOT="/storage/emulated/0/pixel8a"
    export ENV_NAME="pixel8a"
elif [ -d "/home/user/Q" ]; then
    # New laptop environment
    export Q_ROOT="/home/user"
    export ENV_NAME="laptop"
else
    # Default fallback
    export Q_ROOT="$HOME"
    export ENV_NAME="unknown"
fi

# Set derived paths
export Q_PATH="$Q_ROOT/Q"
export HODIE_PATH="$Q_PATH/hodie"
export TODAY_PATH="$Q_PATH/today"
export ERIC_PATH="$HODIE_PATH/.eric"
export SCRIPTS_PATH="$HODIE_PATH/.scripts"

# Display configuration
echo "🌍 Environment: $ENV_NAME"
echo "📁 Q Root: $Q_ROOT"
echo "📂 Q Path: $Q_PATH"
echo "📘 Hodie: $HODIE_PATH"
echo "📅 Today: $TODAY_PATH"
echo ""
echo "✓ Environment configured. Scripts will use these paths."
