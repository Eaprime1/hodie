# Windows Development Environment Setup Guide

**Date**: 2026-01-01
**For**: New Windows Laptop Setup
**Project**: Hodie Content Processing Pipeline

---

## 🎯 Overview

This guide will help you set up your new Windows laptop for development work with the hodie project, enabling you to work both locally and via web-based terminals.

---

## 🚀 Recommended Setup: WSL2 + Windows Terminal

### Why This Approach?

- **Best of both worlds**: Windows GUI + Linux command line
- **Native tools**: Git, shell scripts, and Linux tools work perfectly
- **Seamless integration**: VS Code can connect directly to WSL
- **Flexibility**: Access files from both Windows and Linux

---

## 📝 Step-by-Step Setup

### 1. Install WSL2 (Windows Subsystem for Linux)

**Open PowerShell as Administrator** and run:

```powershell
wsl --install
```

This will:
- Enable WSL2
- Install Ubuntu (default distribution)
- Set up virtualization

**Restart your computer** when prompted.

After restart, Ubuntu will complete installation:
- Set your username (e.g., your Windows username)
- Set your password (save this!)

### 2. Install Windows Terminal

**Option A - Microsoft Store** (Recommended):
- Open Microsoft Store
- Search for "Windows Terminal"
- Click Install

**Option B - Command Line**:
```powershell
winget install Microsoft.WindowsTerminal
```

### 3. Set Up Separate Drive for Projects

**If you have a second drive (D:, E:, etc.):**

1. In Windows, create a folder structure:
   ```
   D:\Development\
   D:\Development\Projects\
   D:\Development\Storage\
   ```

2. In WSL, mount and create a symbolic link:
   ```bash
   # WSL automatically mounts Windows drives at /mnt/
   # Create a shortcut in your home directory
   ln -s /mnt/d/Development ~/dev

   # Now you can access with: cd ~/dev
   ```

3. Add to your `~/.bashrc` for easier access:
   ```bash
   echo 'export DEV_HOME="/mnt/d/Development"' >> ~/.bashrc
   echo 'alias devhome="cd $DEV_HOME"' >> ~/.bashrc
   source ~/.bashrc
   ```

### 4. Install Development Tools in WSL

Open Windows Terminal → Ubuntu tab:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y \
  git \
  curl \
  wget \
  build-essential \
  nano \
  vim

# Install Node.js (if needed for future tools)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installations
git --version
node --version
npm --version
```

### 5. Configure Git

```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Improve git output
git config --global color.ui auto
git config --global core.editor "nano"
```

### 6. Set Up SSH Keys for GitHub

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Press Enter to accept default location
# Enter a passphrase (optional but recommended)

# Start SSH agent
eval "$(ssh-agent -s)"

# Add your SSH key
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub
```

**Add to GitHub**:
1. Go to GitHub.com → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste your public key
4. Click "Add SSH key"

**Test connection**:
```bash
ssh -T git@github.com
# Should see: "Hi username! You've successfully authenticated..."
```

### 7. Clone the Hodie Project

```bash
# Navigate to your projects directory
cd ~/dev/Projects  # or wherever you set up your dev folder

# Clone the repository
git clone git@github.com:Eaprime1/hodie.git

# Enter the project
cd hodie

# Check status
git status
```

---

## 🛠️ Additional Tools (Optional but Recommended)

### VS Code with WSL Extension

1. **Install VS Code** (Windows version):
   - Download from https://code.visualstudio.com/

2. **Install Remote-WSL extension**:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search "Remote - WSL"
   - Install

3. **Open project from WSL**:
   ```bash
   cd ~/dev/Projects/hodie
   code .
   ```
   This opens VS Code on Windows connected to WSL!

### Windows Terminal Customization

**Set Ubuntu as default**:
1. Open Windows Terminal
2. Settings (Ctrl+,)
3. Startup → Default profile → Ubuntu

**Customize appearance**:
- Settings → Ubuntu profile → Appearance
- Choose color scheme, font, transparency

---

## 📂 File Access Between Windows and WSL

**From Windows Explorer**:
- Type in address bar: `\\wsl$\Ubuntu\home\yourusername\`
- This shows your WSL home directory
- You can navigate to your D: drive projects too!

**From WSL**:
- Access Windows C: drive: `cd /mnt/c/`
- Access D: drive: `cd /mnt/d/`

---

## 🔄 Working with the Hodie Project

### Daily Workflow

```bash
# Open Windows Terminal
# Navigate to project
cd ~/dev/Projects/hodie

# Create/switch to feature branch
git checkout -b claude/feature-name-xxxxx

# Make changes, then commit
git add .
git commit -m "Description of changes"

# Push to GitHub
git push -u origin claude/feature-name-xxxxx
```

### Syncing with Remote

```bash
# Fetch latest changes
git fetch origin

# Pull updates
git pull origin main
```

---

## 💾 Backup Strategy with Separate Drive

Since you have a separate drive, consider:

1. **Projects on D: drive** - Main working directory
2. **Automated backups** - Windows File History to external drive
3. **Git as primary backup** - Push to GitHub regularly
4. **Google Drive sync** (already set up): https://drive.google.com/drive/folders/1qSUXHL4fXb8R1n3wBG4A8bwUOWE6SNOf

---

## 🎓 Learning Resources

### Windows Terminal
- Docs: https://learn.microsoft.com/en-us/windows/terminal/

### WSL2
- Docs: https://learn.microsoft.com/en-us/windows/wsl/

### Git
- Pro Git Book: https://git-scm.com/book/en/v2

---

## 🆘 Troubleshooting

### WSL won't install
- Ensure Windows is updated
- Enable virtualization in BIOS
- Run: `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`

### Can't access files between Windows/WSL
- Use `\\wsl$\` in Windows Explorer
- Use `/mnt/c/` or `/mnt/d/` in WSL

### Git SSH authentication fails
- Ensure SSH agent is running: `eval "$(ssh-agent -s)"`
- Add key: `ssh-add ~/.ssh/id_ed25519`
- Verify key on GitHub

---

## ✅ Quick Setup Checklist

- [ ] Install WSL2
- [ ] Install Windows Terminal
- [ ] Set up separate drive structure
- [ ] Install development tools (git, node, etc.)
- [ ] Configure git identity
- [ ] Generate and add SSH key to GitHub
- [ ] Clone hodie project
- [ ] Install VS Code with Remote-WSL extension
- [ ] Test workflow: create branch, commit, push

---

## 🌟 Next Steps

Once your environment is set up:

1. Read `QUICK_START.md` in the hodie project
2. Review `PLEXUS_SYSTEM.md` to understand the pipeline
3. Check `INVENTORY.md` for current project status
4. Start working on your first task!

---

**Ready to enjoy the journey!** 🚀
