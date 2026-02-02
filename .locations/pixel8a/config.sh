#!/bin/bash
# Pixel 8a — Mobile Field Station Configuration

export LOCATION_NAME="pixel8a"
export LOCATION_ROLE="field"
export LOCATION_DEVICE="mobile"

# Paths
export Q_ROOT="/storage/emulated/0/pixel8a"
export Q_PATH="/storage/emulated/0/pixel8a/Q"
export HODIE_PATH="/storage/emulated/0/pixel8a/Q/hodie"

# Mobile constraints
export HQ_MULTI_STREAM=false
export HQ_MAX_CONCURRENT=3
export HQ_FILE_SERVER_PORT=8080

# Streams active on this location
export STREAMS="prime"

# Git review hooks (lighter on mobile)
export GIT_REVIEW_HOOKS=false
