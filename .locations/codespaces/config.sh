#!/bin/bash
# GitHub Codespaces — Cloud Ephemeral Configuration

export LOCATION_NAME="codespaces"
export LOCATION_ROLE="cloud"
export LOCATION_DEVICE="codespaces"

# Paths (codespaces default workspace)
export Q_ROOT="/workspaces"
export Q_PATH="/workspaces/hodie"
export HODIE_PATH="/workspaces/hodie"

# Cloud capabilities
export HQ_MULTI_STREAM=true
export HQ_MAX_CONCURRENT=4
export HQ_FILE_SERVER_PORT=8080

export STREAMS="prime codex"
export GIT_REVIEW_HOOKS=true
