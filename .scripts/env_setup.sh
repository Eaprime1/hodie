#!/bin/bash
# Environment Setup - Cross-platform path configuration
# Usage: source .scripts/env_setup.sh
#
# Detects the current location (mulberry, pixel8a, codespaces)
# and loads location-specific config from .locations/<name>/config.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Detect environment and location
if [ -d "/storage/emulated/0/pixel8a" ]; then
    export ENV_NAME="pixel8a"
    export Q_ROOT="/storage/emulated/0/pixel8a"
elif [ -n "$CODESPACES" ] || [ -d "/workspaces" ]; then
    export ENV_NAME="codespaces"
    export Q_ROOT="/workspaces"
elif [ -d "/home/user/Q" ]; then
    export ENV_NAME="mulberry"
    export Q_ROOT="/home/user"
else
    export ENV_NAME="unknown"
    export Q_ROOT="$HOME"
fi

# Set derived paths
export Q_PATH="$Q_ROOT/Q"
export HODIE_PATH="${HODIE_PATH:-$Q_PATH/hodie}"
export TODAY_PATH="$Q_PATH/today"
export ERIC_PATH="$HODIE_PATH/.eric"
export SCRIPTS_PATH="$HODIE_PATH/.scripts"
export LOCATIONS_PATH="$HODIE_PATH/.locations"

# Load location-specific config if available
LOCATION_CONFIG="$REPO_ROOT/.locations/$ENV_NAME/config.sh"
if [ -f "$LOCATION_CONFIG" ]; then
    source "$LOCATION_CONFIG"
fi

# Export location identity (set by location config or defaults)
export LOCATION_NAME="${LOCATION_NAME:-$ENV_NAME}"
export LOCATION_ROLE="${LOCATION_ROLE:-unknown}"

# Display configuration
echo "--- Environment: $LOCATION_NAME ($LOCATION_ROLE) ---"
echo "  Q Root:  $Q_ROOT"
echo "  Hodie:   $HODIE_PATH"
echo "  Today:   $TODAY_PATH"
if [ -n "$STREAMS" ]; then
    echo "  Streams: $STREAMS"
fi
echo "  Ready."
