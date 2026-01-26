# Windows Development Quick Reference Card

**Date**: 2026-01-01
**Project**: Hodie

---

## 🚀 Getting Started (First Time)

### 1. Install WSL2
**PowerShell (as Administrator)**:
```powershell
wsl --install
```
Then restart computer.

### 2. Run Setup Script
**In WSL Ubuntu terminal**:
```bash
cd ~
curl -O https://raw.githubusercontent.com/Eaprime1/hodie/main/.claude/setup-wsl.sh
bash setup-wsl.sh
```

---

## 📁 File System Navigation

| Location | Windows Path | WSL Path |
|----------|-------------|----------|
| C: Drive | `C:\` | `/mnt/c/` |
| D: Drive | `D:\` | `/mnt/d/` |
| WSL Home | `\\wsl$\Ubuntu\home\username\` | `~` or `/home/username/` |
| Development | `D:\Development\` | `/mnt/d/Development/` or `~/dev/` |

---

## 💻 Common Commands

### Navigation
```bash
cd ~              # Go home
cd ~/dev          # Go to development folder
devhome           # Custom alias to projects
pwd               # Show current directory
ls -la            # List all files (detailed)
```

### Git Workflow
```bash
# Check status
git status

# Create new branch (use claude/ prefix)
git checkout -b claude/feature-name-xxxxx

# Stage changes
git add .                    # All files
git add filename.txt         # Specific file

# Commit
git commit -m "Your message"

# Push to GitHub
git push -u origin branch-name

# Pull latest changes
git fetch origin
git pull origin main
```

### File Operations
```bash
# Copy
cp source.txt destination.txt
cp -r folder/ new-folder/

# Move/Rename
mv oldname.txt newname.txt

# Delete
rm file.txt          # Delete file
rm -r folder/        # Delete folder

# Create
mkdir foldername     # Create directory
touch filename.txt   # Create empty file
```

---

## 🔧 Useful Shortcuts

### Windows Terminal
| Shortcut | Action |
|----------|--------|
| `Ctrl + Shift + T` | New tab |
| `Ctrl + Shift + W` | Close tab |
| `Ctrl + Tab` | Next tab |
| `Ctrl + Shift + P` | Command palette |
| `Ctrl + ,` | Settings |
| `Alt + Click` | Split pane |

### Bash
| Shortcut | Action |
|----------|--------|
| `Ctrl + C` | Cancel current command |
| `Ctrl + L` | Clear screen |
| `Ctrl + R` | Search command history |
| `Ctrl + A` | Go to start of line |
| `Ctrl + E` | Go to end of line |
| `Tab` | Auto-complete |
| `↑/↓` | Previous/Next command |

---

## 🌟 VS Code Integration

### Open from WSL
```bash
# Navigate to project
cd ~/dev/Projects/hodie

# Open in VS Code
code .
```

### Essential Extensions
- Remote - WSL
- GitLens
- Markdown All in One

---

## 🆘 Troubleshooting

### WSL not starting
```powershell
# In PowerShell (Admin)
wsl --shutdown
wsl
```

### SSH Key Issues
```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# Test GitHub
ssh -T git@github.com
```

### Git Authentication
```bash
# Check config
git config --list

# Reset if needed
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Permission Denied
```bash
# Fix file permissions
chmod +x filename.sh

# Fix directory permissions
chmod -R 755 directory/
```

---

## 📚 Hodie Project Specifics

### Repository
- **GitHub**: https://github.com/Eaprime1/hodie
- **Drive**: https://drive.google.com/drive/folders/1qSUXHL4fXb8R1n3wBG4A8bwUOWE6SNOf

### Important Files
- `README.md` - Project overview
- `QUICK_START.md` - Getting started guide
- `PLEXUS_SYSTEM.md` - Pipeline documentation
- `INVENTORY.md` - Current status

### Structure
```
hodie/
├── plexus/          # Processing stages
├── quanta/          # Entity concepts
├── .claude/         # Setup scripts & guides
└── _SORTING/        # Files to be organized
```

### Custom Aliases (after setup)
```bash
devhome    # cd to projects directory
devgo      # cd to development root
```

---

## 🎯 Daily Workflow

1. **Open Windows Terminal**
2. **Navigate to project**: `cd ~/dev/Projects/hodie`
3. **Check status**: `git status`
4. **Create branch**: `git checkout -b claude/task-name-xxxxx`
5. **Make changes**
6. **Commit**: `git add . && git commit -m "Description"`
7. **Push**: `git push -u origin branch-name`

---

## 🔗 Helpful Links

- [WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [Bash Cheat Sheet](https://devhints.io/bash)
- [Windows Terminal Docs](https://learn.microsoft.com/en-us/windows/terminal/)

---

**Print this page and keep it handy!** 📄
