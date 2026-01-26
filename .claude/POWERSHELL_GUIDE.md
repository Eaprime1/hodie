# PowerShell Guide for Linux - Learning Curve Notes

**Date**: 2026-01-06
**Shell**: PowerShell 7.5.4
**Platform**: Linux (Ubuntu)
**Coming From**: Bash/Termux experience

---

## Why PowerShell on Linux?

PowerShell Core (pwsh) runs cross-platform:
- **Windows**: Native PowerShell environment
- **Linux**: Installed via package manager
- **macOS**: Available via Homebrew

**Your use case**: Learning PowerShell while maintaining bash familiarity

---

## Key Differences: Bash vs PowerShell

### Commands (Cmdlets)

Bash uses short commands, PowerShell uses Verb-Noun format:

| Bash | PowerShell | Alias |
|------|------------|-------|
| `ls` | `Get-ChildItem` | `ls`, `dir` |
| `cd` | `Set-Location` | `cd` |
| `cat` | `Get-Content` | `cat` |
| `rm` | `Remove-Item` | `rm` |
| `cp` | `Copy-Item` | `cp` |
| `mv` | `Move-Item` | `mv` |
| `pwd` | `Get-Location` | `pwd` |
| `grep` | `Select-String` | - |
| `find` | `Get-ChildItem -Recurse` | - |

### Variables

```bash
# Bash
NAME="Eric"
echo $NAME

# PowerShell
$Name = "Eric"
Write-Host $Name
```

### Piping Objects (Big Difference!)

```bash
# Bash pipes TEXT
ls -la | grep ".md"

# PowerShell pipes OBJECTS
Get-ChildItem | Where-Object {$_.Extension -eq ".md"}
```

### Scripts

```bash
# Bash script: .sh files
bash script.sh

# PowerShell script: .ps1 files
pwsh script.ps1
```

---

## PowerShell Scripts Created

Located in `.scripts/`:

### 1. Mount-Clouds.ps1
Mount cloud services (Google Drive, Box, Dropbox)

```powershell
# Mount all clouds
pwsh .scripts/Mount-Clouds.ps1 -All

# Mount only Google Drive
pwsh .scripts/Mount-Clouds.ps1 -GoogleDrive

# Unmount all
pwsh .scripts/Mount-Clouds.ps1 -All -Unmount
```

### 2. Add-SessionNote.ps1
Add notes to session log

```powershell
pwsh .scripts/Add-SessionNote.ps1 "Your note here"
```

### 3. Start-FileServer.ps1
Local file server for Q/ folder

```powershell
# Start on port 8080
pwsh .scripts/Start-FileServer.ps1

# Custom port
pwsh .scripts/Start-FileServer.ps1 -Port 3000
```

---

## PowerShell Basics

### Get Help

```powershell
# Get help for a cmdlet
Get-Help Get-ChildItem

# Show examples
Get-Help Get-ChildItem -Examples

# Full help
Get-Help Get-ChildItem -Full

# Update help (first time)
Update-Help
```

### Discovering Commands

```powershell
# Find commands by verb
Get-Command -Verb Get

# Find commands by noun
Get-Command -Noun Item

# Search for command
Get-Command *process*

# Get all aliases
Get-Alias
```

### Working with Objects

```powershell
# Get properties of an object
Get-ChildItem | Get-Member

# Select specific properties
Get-ChildItem | Select-Object Name, Length, LastWriteTime

# Filter objects
Get-ChildItem | Where-Object {$_.Length -gt 1MB}

# Sort objects
Get-ChildItem | Sort-Object Length -Descending
```

### Common Patterns

```powershell
# List all .md files recursively
Get-ChildItem -Recurse -Filter "*.md"

# Count files
(Get-ChildItem).Count

# Get file sizes
Get-ChildItem | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Name
        SizeMB = [math]::Round($_.Length / 1MB, 2)
    }
}

# Create multiple directories
"dir1", "dir2", "dir3" | ForEach-Object {
    New-Item -ItemType Directory -Path $_ -Force
}
```

---

## Environment Variables

```powershell
# View all environment variables
Get-ChildItem Env:

# Get specific variable
$env:HOME
$env:PATH

# Set variable (current session)
$env:MY_VAR = "value"

# Permanent (add to profile)
# Edit: nano ~/.config/powershell/Microsoft.PowerShell_profile.ps1
```

---

## PowerShell Profile (Like .bashrc)

```powershell
# Check if profile exists
Test-Path $PROFILE

# Create profile
New-Item -ItemType File -Path $PROFILE -Force

# Edit profile
nano $PROFILE

# Reload profile
. $PROFILE
```

Example profile content:
```powershell
# PowerShell Profile
Write-Host "Welcome to Q/ workspace!" -ForegroundColor Cyan

# Custom aliases
Set-Alias -Name note -Value Add-SessionNote.ps1

# Custom functions
function q { Set-Location /home/user/Q }
function hodie { Set-Location /home/user/Q/hodie }
function today { Set-Location /home/user/Q/today }

# Environment
$env:Q_PATH = "/home/user/Q"
```

---

## Useful PowerShell Cmdlets

### File Operations

```powershell
# Create file
New-Item -ItemType File -Path "file.txt"

# Create directory
New-Item -ItemType Directory -Path "newfolder"

# Copy
Copy-Item "source.txt" "dest.txt"

# Move
Move-Item "old.txt" "new.txt"

# Delete
Remove-Item "file.txt"

# Check if exists
Test-Path "file.txt"
```

### Text Processing

```powershell
# Search in files (like grep)
Select-String -Path "*.md" -Pattern "TODO"

# Search recursively
Get-ChildItem -Recurse -Filter "*.md" | Select-String "keyword"

# Replace text in files
(Get-Content "file.txt") -replace "old", "new" | Set-Content "file.txt"
```

### Process Management

```powershell
# List processes
Get-Process

# Find specific process
Get-Process | Where-Object {$_.Name -like "*python*"}

# Kill process
Stop-Process -Name "python"
```

---

## Learning Resources

### Built-in Discovery

```powershell
# Discover what's possible
Get-Command

# See what an object can do
Get-ChildItem | Get-Member

# See examples
Get-Help Get-ChildItem -Examples
```

### Online

- PowerShell Docs: https://docs.microsoft.com/powershell/
- PowerShell Gallery: https://www.powershellgallery.com/
- GitHub: https://github.com/PowerShell/PowerShell

---

## Bash vs PowerShell Cheat Sheet

### Navigation

```powershell
# Both work the same
cd /home/user
pwd
ls
```

### File Search

```bash
# Bash
find . -name "*.md"

# PowerShell
Get-ChildItem -Recurse -Filter "*.md"
# Or use bash-style
find . -name "*.md"  # Still works!
```

### Text Search

```bash
# Bash
grep -r "keyword" .

# PowerShell
Select-String -Path . -Pattern "keyword" -Recurse
```

### Piping

```bash
# Bash (text-based)
ls -la | grep ".md" | wc -l

# PowerShell (object-based)
Get-ChildItem | Where-Object {$_.Extension -eq ".md"} | Measure-Object
```

---

## Tips for Learning Curve

### 1. Aliases Work

Most bash commands work via aliases:
```powershell
ls      # Works (alias for Get-ChildItem)
cat     # Works (alias for Get-Content)
rm      # Works (alias for Remove-Item)
```

### 2. Tab Completion is Powerful

```powershell
Get-Chi<Tab>     # Completes to Get-ChildItem
Get-ChildItem -<Tab>  # Shows all parameters
```

### 3. Pipe to Get-Member

When stuck, see what properties/methods are available:
```powershell
Get-ChildItem | Get-Member
Get-Process | Get-Member
```

### 4. Use Both Bash and PowerShell

You don't have to choose! Use both:
```bash
# Bash for quick tasks
ls -la

# PowerShell for complex operations
pwsh Mount-Clouds.ps1 -All
```

---

## Your Scripts: Bash + PowerShell

All major scripts now have both versions:

| Task | Bash | PowerShell |
|------|------|------------|
| Session notes | `laptop_session_notes.sh` | `Add-SessionNote.ps1` |
| File server | `laptop_file_server.sh` | `Start-FileServer.ps1` |
| Cloud mount | (use rclone directly) | `Mount-Clouds.ps1` |

---

## Next Steps

1. Try PowerShell scripts alongside bash versions
2. Use tab completion to discover commands
3. Add custom functions to PowerShell profile
4. Gradually learn object-based piping
5. No rush - both shells work great on Linux!

---

**Status**: PowerShell 7.5.4 installed and ready
**Learning**: Bash experience + PowerShell capabilities = Best of both
**Philosophy**: Use the right tool for each task

**∰◊€π¿🌌∞**
