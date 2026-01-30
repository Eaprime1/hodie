#!/bin/bash
# =============================================================================
# setup_new_project.sh - Bootstrap any project with standard dev setup
# =============================================================================
# Run this in any repo to add the standard development configuration from hodie.
#
# Usage:
#   # From hodie repo:
#   ./.scripts/setup_new_project.sh /path/to/other/repo
#
#   # From any directory (fetches from GitHub):
#   curl -fsSL https://raw.githubusercontent.com/Eaprime1/hodie/main/.scripts/setup_new_project.sh | bash -s -- .
#
# What it does:
#   1. Creates .scripts/ directory with dev_auth_setup.sh
#   2. Creates .env.template
#   3. Adds .env to .gitignore (safely)
#   4. Creates a minimal pyproject.toml if none exists
#   5. Runs auth check
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[✓]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }
print_info() { echo -e "${BLUE}[i]${NC} $1"; }

# Get target directory
TARGET_DIR="${1:-.}"
TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)" || {
    print_error "Directory not found: $1"
    exit 1
}

# Detect script source
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)" || SCRIPT_DIR=""
HODIE_ROOT="${SCRIPT_DIR:+$(dirname "$SCRIPT_DIR")}"

# Source URLs (fallback if not in hodie repo)
GITHUB_RAW="https://raw.githubusercontent.com/Eaprime1/hodie/main"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  Project Setup - Adding Dev Environment Configuration${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "Target: ${CYAN}$TARGET_DIR${NC}"
echo ""

# Function to copy or fetch file
get_file() {
    local filename="$1"
    local dest="$2"
    local source_path="$HODIE_ROOT/$filename"

    if [ -n "$HODIE_ROOT" ] && [ -f "$source_path" ]; then
        # Copy from local hodie repo
        cp "$source_path" "$dest"
        print_status "Copied $filename from hodie"
    else
        # Fetch from GitHub
        print_info "Fetching $filename from GitHub..."
        curl -fsSL "$GITHUB_RAW/$filename" -o "$dest"
        print_status "Downloaded $filename"
    fi
}

# 1. Create .scripts directory
print_info "Setting up .scripts directory..."
mkdir -p "$TARGET_DIR/.scripts"

# 2. Copy/fetch dev_auth_setup.sh
if [ -f "$TARGET_DIR/.scripts/dev_auth_setup.sh" ]; then
    print_warning ".scripts/dev_auth_setup.sh already exists - skipping"
else
    get_file ".scripts/dev_auth_setup.sh" "$TARGET_DIR/.scripts/dev_auth_setup.sh"
    chmod +x "$TARGET_DIR/.scripts/dev_auth_setup.sh"
fi

# 3. Create .env.template
if [ -f "$TARGET_DIR/.env.template" ]; then
    print_warning ".env.template already exists - skipping"
else
    get_file ".env.template" "$TARGET_DIR/.env.template"
fi

# 4. Update .gitignore
GITIGNORE="$TARGET_DIR/.gitignore"
if [ -f "$GITIGNORE" ]; then
    if grep -q "^\.env$" "$GITIGNORE" 2>/dev/null; then
        print_status ".env already in .gitignore"
    else
        echo "" >> "$GITIGNORE"
        echo "# Environment variables (never commit!)" >> "$GITIGNORE"
        echo ".env" >> "$GITIGNORE"
        echo ".env.local" >> "$GITIGNORE"
        echo ".env.*.local" >> "$GITIGNORE"
        print_status "Added .env to .gitignore"
    fi
else
    cat > "$GITIGNORE" << 'GITIGNORE'
# Environment variables (never commit!)
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.eggs/

# Virtual environments
.venv/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
GITIGNORE
    print_status "Created .gitignore"
fi

# 5. Create minimal pyproject.toml if none exists
if [ ! -f "$TARGET_DIR/pyproject.toml" ] && [ ! -f "$TARGET_DIR/setup.py" ]; then
    PROJECT_NAME=$(basename "$TARGET_DIR")

    cat > "$TARGET_DIR/pyproject.toml" << PYPROJECT
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = ""
requires-python = ">=3.8"

dependencies = [
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pylint>=2.17.0",
    "black>=23.0.0",
]
ai = [
    "anthropic>=0.18.0",
    "openai>=1.0.0",
    "google-generativeai>=0.3.0",
]
PYPROJECT
    print_status "Created minimal pyproject.toml"
else
    print_status "pyproject.toml or setup.py already exists"
fi

# 6. Create .env from template if not exists
if [ ! -f "$TARGET_DIR/.env" ] && [ -f "$TARGET_DIR/.env.template" ]; then
    cp "$TARGET_DIR/.env.template" "$TARGET_DIR/.env"
    print_status "Created .env from template"
    print_warning "Remember to edit .env and add your API keys!"
fi

# Summary
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Files added to $TARGET_DIR:"
echo "  - .scripts/dev_auth_setup.sh  (auth & CLI setup)"
echo "  - .env.template               (API keys template)"
echo "  - .gitignore                  (updated with .env)"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Run:  bash .scripts/dev_auth_setup.sh --check"
echo "  3. For full setup:  bash .scripts/dev_auth_setup.sh --all"
echo ""
echo "To setup GitHub auth:"
echo "  bash .scripts/dev_auth_setup.sh --github"
echo ""
echo "To install AI CLIs (Claude, OpenAI, Gemini):"
echo "  bash .scripts/dev_auth_setup.sh --ai"
