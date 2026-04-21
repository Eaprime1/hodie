# Windows Initial Setup Script
# For: Hodie Project Development Environment
# Date: 2026-01-01
# Run this in PowerShell as Administrator

Write-Host "🚀 Windows Development Environment Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Error: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Running as Administrator" -ForegroundColor Green
Write-Host ""

# Install WSL
Write-Host "📦 Installing WSL2..." -ForegroundColor Cyan

if (Get-Command wsl -ErrorAction SilentlyContinue) {
    Write-Host "✓ WSL is already installed" -ForegroundColor Green
} else {
    Write-Host "Installing WSL2 and Ubuntu..." -ForegroundColor Yellow
    wsl --install

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ WSL2 installation initiated" -ForegroundColor Green
        Write-Host "⚠ You will need to RESTART your computer" -ForegroundColor Yellow
    } else {
        Write-Host "❌ WSL installation failed" -ForegroundColor Red
    }
}

Write-Host ""

# Install Windows Terminal
Write-Host "📦 Installing Windows Terminal..." -ForegroundColor Cyan

if (Get-Command wt -ErrorAction SilentlyContinue) {
    Write-Host "✓ Windows Terminal is already installed" -ForegroundColor Green
} else {
    Write-Host "Installing Windows Terminal..." -ForegroundColor Yellow

    # Try winget first
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install Microsoft.WindowsTerminal
        Write-Host "✓ Windows Terminal installed" -ForegroundColor Green
    } else {
        Write-Host "⚠ Please install Windows Terminal from Microsoft Store" -ForegroundColor Yellow
        Write-Host "  Opening Microsoft Store..." -ForegroundColor Yellow
        Start-Process "ms-windows-store://pdp/?ProductId=9n0dx20hk701"
    }
}

Write-Host ""

# Install Git for Windows (optional, mainly for Windows-side operations)
Write-Host "📦 Git for Windows..." -ForegroundColor Cyan

$installGit = Read-Host "Install Git for Windows? (y/n) [You'll also have git in WSL]"
if ($installGit -eq 'y' -or $installGit -eq 'Y') {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        Write-Host "✓ Git is already installed" -ForegroundColor Green
    } else {
        if (Get-Command winget -ErrorAction SilentlyContinue) {
            winget install Git.Git
            Write-Host "✓ Git for Windows installed" -ForegroundColor Green
        } else {
            Write-Host "⚠ Please download Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
            Start-Process "https://git-scm.com/download/win"
        }
    }
}

Write-Host ""

# Install VS Code
Write-Host "📦 Visual Studio Code..." -ForegroundColor Cyan

$installVSCode = Read-Host "Install VS Code? (y/n)"
if ($installVSCode -eq 'y' -or $installVSCode -eq 'Y') {
    if (Get-Command code -ErrorAction SilentlyContinue) {
        Write-Host "✓ VS Code is already installed" -ForegroundColor Green
    } else {
        if (Get-Command winget -ErrorAction SilentlyContinue) {
            winget install Microsoft.VisualStudioCode
            Write-Host "✓ VS Code installed" -ForegroundColor Green
        } else {
            Write-Host "⚠ Please download VS Code from: https://code.visualstudio.com/" -ForegroundColor Yellow
            Start-Process "https://code.visualstudio.com/"
        }
    }
}

Write-Host ""

# Check for additional drives
Write-Host "💾 Available Drives:" -ForegroundColor Cyan
Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -ne $null } | Format-Table -Property Name, @{Label="Size (GB)"; Expression={[math]::Round($_.Used/1GB + $_.Free/1GB, 2)}}, @{Label="Free (GB)"; Expression={[math]::Round($_.Free/1GB, 2)}}

Write-Host ""
$setupDrive = Read-Host "Set up development folder on separate drive? (y/n)"
if ($setupDrive -eq 'y' -or $setupDrive -eq 'Y') {
    $driveLetter = Read-Host "Enter drive letter (e.g., D, E)"
    $devPath = "${driveLetter}:\Development"

    if (-not (Test-Path $devPath)) {
        New-Item -ItemType Directory -Path $devPath -Force | Out-Null
        New-Item -ItemType Directory -Path "$devPath\Projects" -Force | Out-Null
        New-Item -ItemType Directory -Path "$devPath\Storage" -Force | Out-Null
        Write-Host "✓ Created development directories at $devPath" -ForegroundColor Green

        # Create a README
        $readmeContent = @"
# Development Directory

Created: $(Get-Date -Format "yyyy-MM-dd")

## Structure

- Projects/ - Active development projects
- Storage/ - Additional storage for large files, backups, etc.

## Access from WSL

In WSL/Ubuntu, access this directory with:

```bash
cd /mnt/$($driveLetter.ToLower())/Development
```

Add to ~/.bashrc for quick access:

```bash
export DEV_HOME="/mnt/$($driveLetter.ToLower())/Development"
alias devhome="cd `$DEV_HOME/Projects"
```

"@
        Set-Content -Path "$devPath\README.txt" -Value $readmeContent
        Write-Host "✓ Created README in development directory" -ForegroundColor Green
    } else {
        Write-Host "✓ Directory already exists: $devPath" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "Development folder setup at: $devPath" -ForegroundColor Cyan
    Write-Host "WSL path will be: /mnt/$($driveLetter.ToLower())/Development" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✨ Windows Setup Complete!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. RESTART your computer if WSL was just installed" -ForegroundColor White
Write-Host "  2. Open Windows Terminal" -ForegroundColor White
Write-Host "  3. Ubuntu will complete its setup (username & password)" -ForegroundColor White
Write-Host "  4. Run the WSL setup script:" -ForegroundColor White
Write-Host ""
Write-Host "     cd ~" -ForegroundColor Cyan
Write-Host "     curl -fsSLo setup-wsl.sh https://raw.githubusercontent.com/Eaprime1/hodie/main/.claude/setup-wsl.sh" -ForegroundColor Cyan
Write-Host "     less setup-wsl.sh   # review before running" -ForegroundColor Cyan
Write-Host "     bash setup-wsl.sh" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 Documentation:" -ForegroundColor Yellow
Write-Host "  Once hodie is cloned, check .claude/ folder for:" -ForegroundColor White
Write-Host "  - WINDOWS_SETUP_GUIDE.md (detailed guide)" -ForegroundColor White
Write-Host "  - QUICK_REFERENCE.md (command reference)" -ForegroundColor White
Write-Host ""

$needsRestart = -not (Get-Command wsl -ErrorAction SilentlyContinue)
if ($needsRestart) {
    Write-Host "⚠ RESTART REQUIRED" -ForegroundColor Red
    $restart = Read-Host "Restart now? (y/n)"
    if ($restart -eq 'y' -or $restart -eq 'Y') {
        Restart-Computer -Confirm
    }
} else {
    Write-Host "You can continue with WSL setup now!" -ForegroundColor Green
}

Write-Host ""
Read-Host "Press Enter to exit"
