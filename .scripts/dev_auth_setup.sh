#!/bin/bash
# =============================================================================
# dev_auth_setup.sh - Universal Developer Authentication & CLI Setup
# =============================================================================
# Sets up authentication for GitHub, AI tools, and common dev dependencies
#
# Usage:
#   ./dev_auth_setup.sh              # Interactive mode - guides through all setup
#   ./dev_auth_setup.sh --check      # Check what's already configured
#   ./dev_auth_setup.sh --github     # Only setup GitHub CLI
#   ./dev_auth_setup.sh --ai         # Only setup AI CLIs
#   ./dev_auth_setup.sh --all        # Non-interactive, setup everything
#
# Can be run from any repo - designed to be portable!
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)
            if grep -q Microsoft /proc/version 2>/dev/null; then
                echo "wsl"
            elif [ -f /data/data/com.termux/files/usr/bin/termux-info ] 2>/dev/null; then
                echo "termux"
            else
                echo "linux"
            fi
            ;;
        Darwin*)    echo "macos";;
        MINGW*|MSYS*|CYGWIN*) echo "windows";;
        *)          echo "unknown";;
    esac
}

OS=$(detect_os)

# Print with color
print_header() {
    echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_status() { echo -e "${GREEN}[✓]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }
print_info() { echo -e "${BLUE}[i]${NC} $1"; }

# Check if command exists
cmd_exists() {
    command -v "$1" &> /dev/null
}

# =============================================================================
# CHECK FUNCTIONS - What's already installed/configured?
# =============================================================================

check_github_cli() {
    print_header "GitHub CLI Status"

    if cmd_exists gh; then
        print_status "GitHub CLI (gh) is installed: $(gh --version | head -1)"

        if gh auth status &>/dev/null; then
            print_status "GitHub CLI is authenticated"
            gh auth status
            return 0
        else
            print_warning "GitHub CLI is installed but NOT authenticated"
            return 1
        fi
    else
        print_error "GitHub CLI (gh) is NOT installed"
        return 1
    fi
}

check_claude_cli() {
    print_header "Claude CLI Status"

    if cmd_exists claude; then
        print_status "Claude CLI is installed: $(claude --version 2>/dev/null || echo 'version unknown')"
        return 0
    else
        print_warning "Claude CLI is NOT installed"
        return 1
    fi
}

check_gemini_cli() {
    print_header "Gemini CLI Status"

    # Check for Google Cloud CLI with Gemini
    if cmd_exists gcloud; then
        print_status "Google Cloud CLI is installed"
        if [ -n "$GEMINI_API_KEY" ]; then
            print_status "GEMINI_API_KEY is set"
            return 0
        else
            print_warning "GEMINI_API_KEY is not set"
            return 1
        fi
    fi

    # Check for dedicated gemini CLI if exists
    if cmd_exists gemini; then
        print_status "Gemini CLI is installed"
        return 0
    fi

    print_warning "No Gemini CLI found"
    return 1
}

check_openai_cli() {
    print_header "OpenAI CLI Status"

    if cmd_exists openai; then
        print_status "OpenAI CLI is installed"
        if [ -n "$OPENAI_API_KEY" ]; then
            print_status "OPENAI_API_KEY is set"
            return 0
        else
            print_warning "OPENAI_API_KEY is not set"
            return 1
        fi
    else
        print_warning "OpenAI CLI is NOT installed"
        return 1
    fi
}

check_all() {
    print_header "Development Environment Status Check"
    echo -e "OS Detected: ${CYAN}$OS${NC}\n"

    local issues=0

    # Core tools
    echo -e "${BLUE}=== Core Development Tools ===${NC}"

    if cmd_exists git; then
        print_status "git: $(git --version)"
    else
        print_error "git: NOT installed"
        ((issues++))
    fi

    if cmd_exists python3; then
        print_status "python3: $(python3 --version)"
    else
        print_error "python3: NOT installed"
        ((issues++))
    fi

    if cmd_exists node; then
        print_status "node: $(node --version)"
    else
        print_warning "node: NOT installed (optional)"
    fi

    if cmd_exists npm; then
        print_status "npm: $(npm --version)"
    else
        print_warning "npm: NOT installed (optional)"
    fi

    # GitHub
    echo -e "\n${BLUE}=== GitHub CLI ===${NC}"
    check_github_cli || ((issues++))

    # AI CLIs
    echo -e "\n${BLUE}=== AI CLI Tools ===${NC}"
    check_claude_cli || true
    check_openai_cli || true
    check_gemini_cli || true

    # Environment variables
    echo -e "\n${BLUE}=== Environment Variables ===${NC}"
    [ -n "$ANTHROPIC_API_KEY" ] && print_status "ANTHROPIC_API_KEY: set" || print_warning "ANTHROPIC_API_KEY: not set"
    [ -n "$OPENAI_API_KEY" ] && print_status "OPENAI_API_KEY: set" || print_warning "OPENAI_API_KEY: not set"
    [ -n "$GEMINI_API_KEY" ] && print_status "GEMINI_API_KEY: set" || print_warning "GEMINI_API_KEY: not set"
    [ -n "$GITHUB_TOKEN" ] && print_status "GITHUB_TOKEN: set" || print_warning "GITHUB_TOKEN: not set"

    echo ""
    if [ $issues -eq 0 ]; then
        print_status "All core tools are configured!"
    else
        print_warning "$issues issue(s) found - run with --all to fix"
    fi
}

# =============================================================================
# INSTALL FUNCTIONS
# =============================================================================

install_github_cli() {
    print_header "Installing GitHub CLI"

    if cmd_exists gh; then
        print_status "GitHub CLI already installed"
    else
        print_info "Installing GitHub CLI..."

        case $OS in
            macos)
                if cmd_exists brew; then
                    brew install gh
                else
                    print_error "Homebrew not found. Install from: https://cli.github.com"
                    return 1
                fi
                ;;
            linux|wsl)
                # Official GitHub instructions
                (type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
                && sudo mkdir -p -m 755 /etc/apt/keyrings \
                && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
                && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
                && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
                && sudo apt update \
                && sudo apt install gh -y
                ;;
            termux)
                pkg install gh
                ;;
            *)
                print_error "Unsupported OS for automatic install. Visit: https://cli.github.com"
                return 1
                ;;
        esac
    fi

    print_status "GitHub CLI installed: $(gh --version | head -1)"
}

setup_github_auth() {
    print_header "GitHub Authentication Setup"

    if ! cmd_exists gh; then
        print_warning "GitHub CLI not installed. Installing first..."
        install_github_cli || return 1
    fi

    if gh auth status &>/dev/null; then
        print_status "Already authenticated with GitHub"
        gh auth status

        read -p "Re-authenticate? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 0
        fi
    fi

    print_info "Starting GitHub authentication..."
    print_info "This will open a browser for authentication."
    echo ""

    # Interactive login with recommended scopes
    gh auth login --web --git-protocol https --scopes "repo,read:org,workflow,gist"

    print_status "GitHub authentication complete!"
    gh auth status
}

install_claude_cli() {
    print_header "Installing Claude CLI (Claude Code)"

    if cmd_exists claude; then
        print_status "Claude CLI already installed"
        return 0
    fi

    print_info "Installing Claude Code CLI via npm..."

    if ! cmd_exists npm; then
        print_error "npm is required for Claude CLI. Install Node.js first."
        return 1
    fi

    npm install -g @anthropic-ai/claude-code

    if cmd_exists claude; then
        print_status "Claude CLI installed successfully"
        print_info "Run 'claude' to start, or 'claude --help' for options"
    else
        print_error "Claude CLI installation may have failed"
        return 1
    fi
}

install_openai_cli() {
    print_header "Installing OpenAI CLI"

    if cmd_exists openai; then
        print_status "OpenAI CLI already installed"
        return 0
    fi

    print_info "Installing OpenAI CLI via pip..."

    pip install --upgrade openai

    print_status "OpenAI CLI installed"
    print_info "Set OPENAI_API_KEY in your environment"
}

install_google_cloud_cli() {
    print_header "Installing Google Cloud CLI (for Gemini)"

    if cmd_exists gcloud; then
        print_status "Google Cloud CLI already installed"
        return 0
    fi

    print_info "Installing Google Cloud CLI..."

    case $OS in
        macos)
            if cmd_exists brew; then
                brew install --cask google-cloud-sdk
            else
                curl https://sdk.cloud.google.com | bash
            fi
            ;;
        linux|wsl)
            curl https://sdk.cloud.google.com | bash
            ;;
        termux)
            print_warning "Google Cloud CLI not available on Termux"
            print_info "Use the Gemini API directly with GEMINI_API_KEY"
            return 0
            ;;
        *)
            print_error "Unsupported OS. Visit: https://cloud.google.com/sdk/docs/install"
            return 1
            ;;
    esac

    print_status "Google Cloud CLI installed"
    print_info "Run 'gcloud init' to configure"
}

install_all_ai_clis() {
    print_header "Installing All AI CLI Tools"

    install_claude_cli || true
    install_openai_cli || true
    install_google_cloud_cli || true

    print_status "AI CLI installation complete"
}

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

setup_env_file() {
    print_header "Environment File Setup"

    local env_template="${SCRIPT_DIR}/../.env.template"
    local env_file="${SCRIPT_DIR}/../.env"

    if [ ! -f "$env_template" ]; then
        print_warning ".env.template not found, creating..."
        create_env_template
    fi

    if [ -f "$env_file" ]; then
        print_status ".env file exists"
        print_info "Edit .env to add your API keys"
    else
        print_info "Creating .env from template..."
        cp "$env_template" "$env_file"
        print_status ".env file created"
        print_warning "IMPORTANT: Edit .env and add your API keys!"
    fi
}

create_env_template() {
    local template_path="${SCRIPT_DIR}/../.env.template"

    cat > "$template_path" << 'ENVTEMPLATE'
# =============================================================================
# Environment Variables Template
# =============================================================================
# Copy this file to .env and fill in your values
# NEVER commit .env to git!
# =============================================================================

# GitHub
GITHUB_TOKEN=

# Anthropic (Claude)
ANTHROPIC_API_KEY=

# OpenAI
OPENAI_API_KEY=

# Google (Gemini)
GEMINI_API_KEY=
GOOGLE_APPLICATION_CREDENTIALS=

# Optional: Other AI providers
COHERE_API_KEY=
MISTRAL_API_KEY=
REPLICATE_API_TOKEN=

# Local development
DEBUG=false
LOG_LEVEL=INFO
ENVTEMPLATE

    print_status "Created .env.template"
}

# =============================================================================
# PORTABLE SETUP FOR OTHER REPOS
# =============================================================================

create_portable_setup() {
    print_header "Creating Portable Setup Script"

    local output_file="${1:-dev_setup_portable.sh}"

    cat > "$output_file" << 'PORTABLE'
#!/bin/bash
# Portable dev setup - run this in any repo to configure auth & tools
# Generated by hodie/dev_auth_setup.sh

curl -fsSL https://raw.githubusercontent.com/Eaprime1/hodie/main/.scripts/dev_auth_setup.sh | bash -s -- --check

echo ""
echo "To run full setup:"
echo "  curl -fsSL https://raw.githubusercontent.com/Eaprime1/hodie/main/.scripts/dev_auth_setup.sh | bash -s -- --all"
PORTABLE

    chmod +x "$output_file"
    print_status "Created portable setup: $output_file"
}

# =============================================================================
# INTERACTIVE MENU
# =============================================================================

show_menu() {
    print_header "Developer Environment Setup"
    echo -e "OS: ${CYAN}$OS${NC}\n"

    echo "What would you like to set up?"
    echo ""
    echo "  1) Check current status"
    echo "  2) GitHub CLI (gh auth login)"
    echo "  3) Claude CLI"
    echo "  4) OpenAI CLI"
    echo "  5) Google Cloud CLI (Gemini)"
    echo "  6) All AI CLIs"
    echo "  7) Environment file (.env)"
    echo "  8) Everything (full setup)"
    echo "  9) Create portable setup script"
    echo "  0) Exit"
    echo ""
    read -p "Choose an option [0-9]: " -n 1 -r
    echo ""

    case $REPLY in
        1) check_all ;;
        2) setup_github_auth ;;
        3) install_claude_cli ;;
        4) install_openai_cli ;;
        5) install_google_cloud_cli ;;
        6) install_all_ai_clis ;;
        7) setup_env_file ;;
        8)
            setup_github_auth
            install_all_ai_clis
            setup_env_file
            check_all
            ;;
        9) create_portable_setup ;;
        0) exit 0 ;;
        *) print_error "Invalid option" ;;
    esac

    echo ""
    read -p "Continue? (Y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        show_menu
    fi
}

# =============================================================================
# MAIN
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "${1:-}" in
    --check|-c)
        check_all
        ;;
    --github|-g)
        setup_github_auth
        ;;
    --ai|-a)
        install_all_ai_clis
        ;;
    --claude)
        install_claude_cli
        ;;
    --openai)
        install_openai_cli
        ;;
    --gemini|--gcloud)
        install_google_cloud_cli
        ;;
    --env)
        setup_env_file
        ;;
    --all)
        setup_github_auth
        install_all_ai_clis
        setup_env_file
        check_all
        ;;
    --portable)
        create_portable_setup "${2:-dev_setup_portable.sh}"
        ;;
    --help|-h)
        echo "Usage: $0 [OPTION]"
        echo ""
        echo "Options:"
        echo "  --check, -c     Check what's installed/configured"
        echo "  --github, -g    Setup GitHub CLI authentication"
        echo "  --ai, -a        Install all AI CLI tools"
        echo "  --claude        Install Claude CLI only"
        echo "  --openai        Install OpenAI CLI only"
        echo "  --gemini        Install Google Cloud CLI only"
        echo "  --env           Setup .env file from template"
        echo "  --all           Setup everything (non-interactive)"
        echo "  --portable      Generate portable setup script"
        echo "  --help, -h      Show this help"
        echo ""
        echo "Without options: Interactive menu"
        ;;
    "")
        show_menu
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
