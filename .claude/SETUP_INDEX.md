# Windows Development Environment Setup - Index

**Created**: 2026-01-01 20:45
**Purpose**: Complete setup guide for new Windows laptop development environment
**Project**: Hodie Content Processing Pipeline

---

## 📚 Documentation Overview

This folder contains everything you need to set up your new Windows laptop for development work with the hodie project.

---

## 🗂️ Files in This Guide

### 1. **WINDOWS_SETUP_GUIDE.md** ⭐ START HERE
**The comprehensive guide covering:**
- WSL2 installation and configuration
- Windows Terminal setup
- Separate drive configuration for storage
- Git and GitHub setup with SSH keys
- Development tools installation
- VS Code integration
- Daily workflow examples
- Troubleshooting tips

**Who it's for**: Complete step-by-step walkthrough for setting up everything
**Read this**: If you want detailed explanations and context

---

### 2. **QUICK_REFERENCE.md** 📄 PRINT THIS
**Quick reference card with:**
- Common commands (git, bash, file operations)
- Keyboard shortcuts
- File system path conversions (Windows ↔ WSL)
- Troubleshooting quick fixes
- Hodie project specifics

**Who it's for**: Quick lookups while working
**Read this**: Print and keep by your desk for quick reference

---

### 3. **setup-windows.ps1** 🪟 RUN FIRST (on Windows)
**PowerShell script for Windows setup:**
- Installs WSL2
- Installs Windows Terminal
- Optionally installs Git, VS Code
- Sets up development directory on separate drive

**How to use**:
```powershell
# Right-click PowerShell → "Run as Administrator"
cd path\to\hodie\.claude
.\setup-windows.ps1
```

**When to use**: First time setting up Windows, before WSL setup

---

### 4. **setup-wsl.sh** 🐧 RUN SECOND (in WSL)
**Bash script for WSL/Ubuntu setup:**
- Updates system packages
- Installs development tools (git, node, build tools)
- Configures git with your identity
- Generates SSH keys for GitHub
- Sets up development directory structure
- Clones hodie repository

**How to use**:
```bash
# In WSL/Ubuntu terminal
cd ~
curl -O https://raw.githubusercontent.com/Eaprime1/hodie/main/.claude/setup-wsl.sh
bash setup-wsl.sh
```

**When to use**: After WSL is installed and running

---

## 🚀 Quick Start Path

### For Brand New Setup:

1. **On Windows** (PowerShell as Admin):
   ```powershell
   # If you don't have the repo yet, download the script:
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Eaprime1/hodie/main/.claude/setup-windows.ps1" -OutFile "setup-windows.ps1"
   .\setup-windows.ps1
   ```

2. **Restart Computer** (if WSL was just installed)

3. **In WSL/Ubuntu Terminal**:
   ```bash
   cd ~
   curl -O https://raw.githubusercontent.com/Eaprime1/hodie/main/.claude/setup-wsl.sh
   bash setup-wsl.sh
   ```

4. **Start Developing!**
   ```bash
   cd ~/dev/Projects/hodie
   code .
   ```

### If You Want to Read First:

1. Read `WINDOWS_SETUP_GUIDE.md` - Comprehensive guide
2. Print `QUICK_REFERENCE.md` - Keep handy
3. Run `setup-windows.ps1` when ready
4. Run `setup-wsl.sh` when WSL is ready

---

## 💡 Setup Options

### Option A: Automated (Recommended for Quick Start)
- Run `setup-windows.ps1` → Restart → Run `setup-wsl.sh`
- Everything configured automatically
- Interactive prompts for choices
- ~15-20 minutes total

### Option B: Manual (Recommended for Learning)
- Follow `WINDOWS_SETUP_GUIDE.md` step by step
- Understand each command and configuration
- Customize as you go
- ~30-45 minutes total

### Option C: Hybrid (Best of Both)
- Read `WINDOWS_SETUP_GUIDE.md` first to understand
- Run scripts for automation
- Refer to guide for any questions
- ~20-25 minutes total

---

## 🎯 What Gets Set Up

### On Windows:
- ✅ WSL2 (Windows Subsystem for Linux)
- ✅ Windows Terminal (modern terminal app)
- ✅ Git for Windows (optional)
- ✅ VS Code (optional)
- ✅ Development folder structure on separate drive

### In WSL/Ubuntu:
- ✅ Git with your identity configured
- ✅ SSH keys for GitHub authentication
- ✅ Essential development tools (curl, wget, build-essential)
- ✅ Node.js LTS (optional, for future tools)
- ✅ Development directory with custom aliases
- ✅ Hodie repository cloned and ready

---

## 📋 Prerequisites

### Hardware:
- Windows 10 (version 2004+) or Windows 11
- At least 8GB RAM (16GB recommended)
- Optional: Separate drive for development storage

### Software:
- Windows with latest updates
- Administrator access
- Internet connection

### Knowledge:
- Basic command line familiarity (helpful but not required)
- GitHub account (for cloning repository)

---

## 🆘 Troubleshooting

### Scripts Not Running?

**PowerShell script blocked**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Bash script permission denied**:
```bash
chmod +x setup-wsl.sh
./setup-wsl.sh
```

### WSL Issues?
- Check `WINDOWS_SETUP_GUIDE.md` troubleshooting section
- Ensure virtualization is enabled in BIOS
- Try: `wsl --update` in PowerShell

### Need More Help?
- See `QUICK_REFERENCE.md` troubleshooting section
- Check hodie project `README.md`
- Review git status and logs

---

## 🔗 Related Documentation

In the hodie repository root:
- `README.md` - Hodie project overview
- `QUICK_START.md` - Hodie usage guide
- `PLEXUS_SYSTEM.md` - Pipeline documentation
- `INVENTORY.md` - Current project status

---

## 📞 Support Resources

- **WSL Documentation**: https://learn.microsoft.com/en-us/windows/wsl/
- **Git Documentation**: https://git-scm.com/doc
- **Windows Terminal**: https://learn.microsoft.com/en-us/windows/terminal/
- **VS Code WSL**: https://code.visualstudio.com/docs/remote/wsl

---

## ✨ After Setup

Once everything is configured, your daily workflow will be:

1. Open Windows Terminal
2. Navigate to project: `cd ~/dev/Projects/hodie` (or use `devhome` alias)
3. Create branch: `git checkout -b claude/feature-xxxxx`
4. Make changes
5. Commit and push: `git add . && git commit -m "message" && git push -u origin branch-name`

---

## 🎊 Welcome to Your New Development Environment!

You're setting up a professional development environment that gives you:

- **Flexibility**: Work in Windows GUI or Linux terminal
- **Power**: Full Linux toolchain on Windows
- **Integration**: VS Code connects seamlessly to WSL
- **Organization**: Separate drive for clean storage management
- **Efficiency**: Custom aliases and automated workflows

Enjoy the journey! 🚀

---

**Last Updated**: 2026-01-01
**Version**: 1.0
