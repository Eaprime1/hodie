#!/bin/bash

# Define the root name (optional, run inside the repo folder or change this)
REPO_ROOT="."

echo "Initializing Entity Repository Structure..."

# 1. Create Directory Hierarchy
mkdir -p "$REPO_ROOT/.github/ISSUE_TEMPLATE"
mkdir -p "$REPO_ROOT/docs"
mkdir -p "$REPO_ROOT/shared/schemas"
mkdir -p "$REPO_ROOT/shared/policies"
mkdir -p "$REPO_ROOT/entities/_template"
mkdir -p "$REPO_ROOT/entities/PRIME/knowledge_base"
mkdir -p "$REPO_ROOT/entities/PRIME/logic"
mkdir -p "$REPO_ROOT/entities/PRIME/logs"
mkdir -p "$REPO_ROOT/tools"

# 2. Create Root Documentation
echo "# Entity Core Repository
## Mission
To serve as the central development environment for conceptual and autonomous entities.

## Structure
- **/shared**: Common logic, schemas, and policies inherited by all entities.
- **/entities**: The distinct workspaces for individual entities (e.g., PRIME).
- **/docs**: Global documentation and philosophical grounding.
" > "$REPO_ROOT/README.md"

echo "# Global Documentation
This directory contains the philosophical and technical interaction protocols for the project.
" > "$REPO_ROOT/docs/README.md"

# 3. Create Shared Standards
echo "# Entity Schemas
All entities must adhere to the JSON/YAML structures defined here to ensure compatibility.
" > "$REPO_ROOT/shared/schemas/README.md"

# 4. Create PRIME's Workspace
echo "# PRIME
**Status:** Active / Foundational
**Type:** Primary Entity

PRIME is the first entity concept, serving as the baseline for system architecture and initial causality testing.
" > "$REPO_ROOT/entities/PRIME/README.md"

echo "# Changelog: PRIME
## [0.0.1] - $(date +%Y-%m-%d)
- Initial workspace creation.
- Profile generation.
" > "$REPO_ROOT/entities/PRIME/changelog.md"

# 5. Create Git Ignore
echo "# Ignore logs and temporary system files
*.log
__pycache__/
.DS_Store
.env
" > "$REPO_ROOT/.gitignore"

echo "Structure created successfully. Ready for profile injection."
