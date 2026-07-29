# Mount-Clouds.ps1
# PowerShell script to mount cloud services using rclone
# Usage: pwsh Mount-Clouds.ps1

param(
    [switch]$GoogleDrive,
    [switch]$Box,
    [switch]$Dropbox,
    [switch]$All,
    [switch]$Unmount
)

$MountBase = "$HOME/CloudMounts"

# Ensure mount directories exist
function Initialize-MountPoints {
    @("GoogleDrive", "Box", "Dropbox") | ForEach-Object {
        $path = Join-Path $MountBase $_
        if (-not (Test-Path $path)) {
            New-Item -ItemType Directory -Path $path -Force | Out-Null
            Write-Host "✓ Created mount point: $path" -ForegroundColor Green
        }
    }
}

# Mount a cloud service
function Mount-CloudService {
    param(
        [string]$ServiceName,
        [string]$RemoteName,
        [string]$MountPath
    )

    Write-Host "📂 Mounting $ServiceName..." -ForegroundColor Cyan

    # Check if MountPath is already a mount point via the `mount` command.
    # This works reliably on Linux/PowerShell Core where Get-Process does not
    # expose a CommandLine property. The standard Linux mount output format is:
    # "device on /mount/path type fstype (options)"
    $isMounted = & mount 2>$null | Where-Object { $_ -match (" on " + [regex]::Escape($MountPath) + '\b') }

    if ($isMounted) {
        Write-Host "⚠ $ServiceName already mounted at $MountPath" -ForegroundColor Yellow
        return
    }

    try {
        & rclone mount "${RemoteName}:" $MountPath --vfs-cache-mode writes --daemon
        if ($LASTEXITCODE -ne 0) {
            throw "rclone mount exited with code $LASTEXITCODE"
        }
        Write-Host "✓ $ServiceName mounted successfully at $MountPath" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to mount $ServiceName : $_" -ForegroundColor Red
    }
}

# Unmount a cloud service
function Unmount-CloudService {
    param(
        [string]$ServiceName,
        [string]$MountPath
    )

    Write-Host "📤 Unmounting $ServiceName..." -ForegroundColor Cyan

    try {
        & fusermount -u $MountPath
        Write-Host "✓ $ServiceName unmounted from $MountPath" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to unmount $ServiceName : $_" -ForegroundColor Red
    }
}

# Main execution
Initialize-MountPoints

if ($Unmount) {
    Write-Host "`n=== Unmounting Cloud Services ===" -ForegroundColor Magenta

    if ($GoogleDrive -or $All) {
        Unmount-CloudService "Google Drive" "$MountBase/GoogleDrive"
    }
    if ($Box -or $All) {
        Unmount-CloudService "Box" "$MountBase/Box"
    }
    if ($Dropbox -or $All) {
        Unmount-CloudService "Dropbox" "$MountBase/Dropbox"
    }
} else {
    Write-Host "`n=== Mounting Cloud Services ===" -ForegroundColor Magenta

    if ($GoogleDrive -or $All) {
        Mount-CloudService "Google Drive" "gdrive" "$MountBase/GoogleDrive"
    }
    if ($Box -or $All) {
        Mount-CloudService "Box" "box" "$MountBase/Box"
    }
    if ($Dropbox -or $All) {
        Mount-CloudService "Dropbox" "dropbox" "$MountBase/Dropbox"
    }
}

Write-Host "`n=== Mount Status ===" -ForegroundColor Magenta
# rclone mounts appear as type 'fuse.rclone' in mount output on Linux
$activeMounts = & mount 2>$null | Where-Object { $_ -match "fuse\.rclone" }
if ($activeMounts) {
    $activeMounts | ForEach-Object { Write-Host "  $_" -ForegroundColor Green }
} else {
    Write-Host "  No rclone mounts active" -ForegroundColor Gray
}

Write-Host "`nTip: Access your clouds at:" -ForegroundColor Cyan
Write-Host "  Google Drive: $MountBase/GoogleDrive"
Write-Host "  Box:          $MountBase/Box"
Write-Host "  Dropbox:      $MountBase/Dropbox"
