#!/bin/bash
# Mulberry — Laptop HQ Configuration
# Source this after env_setup.sh or let env_setup.sh source it automatically

export LOCATION_NAME="mulberry"
export LOCATION_ROLE="hq"
export LOCATION_DEVICE="laptop"

# Paths
export Q_ROOT="$HOME"
export Q_PATH="$HOME/Q"
export HODIE_PATH="$HOME/Q/hodie"

# HQ capabilities — this machine can run heavy workloads
export HQ_MULTI_STREAM=true
export HQ_MAX_CONCURRENT=8
export HQ_FILE_SERVER_PORT=8080

# Streams active on this location
export STREAMS="prime codex gamemaster"

# Git review hooks enabled
export GIT_REVIEW_HOOKS=true
