#!/bin/bash
# WSL Development Environment Setup Script
# For: Hodie Project
# Date: 2026-01-01

set -e  # Exit on error

echo "🚀 Starting WSL Development Environment Setup..."
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y
print_success "System updated"
echo ""

# Install essential tools
print_status "Installing essential development tools..."
sudo apt install -y \
    git \
    curl \
    wget \
    build-essential \
    nano \
    vim \
    htop \
    tree \
    jq \
    unzip
print_success "Essential tools installed"
echo ""

# Check if Node.js is needed
read -p "Install Node.js LTS? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Installing Node.js LTS..."
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt install -y nodejs
    print_success "Node.js installed: $(node --version)"
    print_success "npm installed: $(npm --version)"
    echo ""
fi

# Configure Git
print_status "Configuring Git..."
echo ""
read -p "Enter your Git name (e.g., John Doe): " git_name
read -p "Enter your Git email: " git_email

git config --global user.name "$git_name"
git config --global user.email "$git_email"
git config --global init.defaultBranch main
git config --global color.ui auto
git config --global core.editor "nano"
git config --global pull.rebase false

print_success "Git configured"
echo "  Name: $git_name"
echo "  Email: $git_email"
echo ""

# SSH Key setup
print_status "Setting up SSH key for GitHub..."
echo ""

if [ -f ~/.ssh/id_ed25519 ]; then
    print_warning "SSH key already exists at ~/.ssh/id_ed25519"
    read -p "Generate new key? This will backup the old one. (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mv ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.backup
        mv ~/.ssh/id_ed25519.pub ~/.ssh/id_ed25519.pub.backup
        print_success "Old keys backed up"
    else
        print_warning "Skipping SSH key generation"
        echo ""
        print_status "Your existing public key:"
        cat ~/.ssh/id_ed25519.pub
        echo ""
        print_warning "Add this key to GitHub: https://github.com/settings/keys"
        echo ""
    fi
fi

if [ ! -f ~/.ssh/id_ed25519 ]; then
    ssh-keygen -t ed25519 -C "$git_email" -f ~/.ssh/id_ed25519 -N ""
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519

    print_success "SSH key generated!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Your PUBLIC SSH key (copy this to GitHub):"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    cat ~/.ssh/id_ed25519.pub
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Add this key to GitHub:"
    echo "  1. Go to: https://github.com/settings/keys"
    echo "  2. Click 'New SSH key'"
    echo "  3. Paste the key above"
    echo "  4. Click 'Add SSH key'"
    echo ""
    read -p "Press Enter after you've added the key to GitHub..."
    echo ""
fi

# Test GitHub connection
print_status "Testing GitHub connection..."
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    print_success "GitHub SSH connection successful!"
else
    print_warning "GitHub SSH connection failed. Please check your key setup."
fi
echo ""

# Set up development directory
print_status "Setting up development directory structure..."
echo ""
read -p "Enter path for development folder (e.g., /mnt/d/Development or ~/Development): " dev_path

if [ ! -d "$dev_path" ]; then
    mkdir -p "$dev_path"
    mkdir -p "$dev_path/Projects"
    mkdir -p "$dev_path/Storage"
    print_success "Created development directories at $dev_path"
else
    print_warning "Directory already exists: $dev_path"
fi

# Add to bashrc
if ! grep -q "DEV_HOME" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Development environment" >> ~/.bashrc
    echo "export DEV_HOME=\"$dev_path\"" >> ~/.bashrc
    echo "alias devhome='cd \$DEV_HOME/Projects'" >> ~/.bashrc
    echo "alias devgo='cd \$DEV_HOME'" >> ~/.bashrc
    print_success "Added DEV_HOME to ~/.bashrc"
else
    print_warning "DEV_HOME already exists in ~/.bashrc"
fi
echo ""

# Clone hodie project
print_status "Clone hodie project?"
echo ""
read -p "Clone hodie repository now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$dev_path/Projects"
    if [ ! -d "hodie" ]; then
        git clone git@github.com:Eaprime1/hodie.git
        print_success "Hodie repository cloned!"
        cd hodie
        print_status "Repository location: $(pwd)"
    else
        print_warning "hodie directory already exists"
        cd hodie
        git pull origin main 2>/dev/null || print_warning "Could not pull latest changes"
    fi
fi
echo ""

# Final summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
print_success "Development tools installed"
print_success "Git configured: $git_name <$git_email>"
print_success "Development home: $dev_path"
echo ""
echo "Quick commands:"
echo "  devhome  - Go to projects directory"
echo "  devgo    - Go to development root"
echo ""
echo "Next steps:"
echo "  1. Reload your shell: source ~/.bashrc"
echo "  2. Go to hodie: cd $dev_path/Projects/hodie"
echo "  3. Read QUICK_START.md"
echo ""
echo "Enjoy the journey! 🚀"
echo ""
