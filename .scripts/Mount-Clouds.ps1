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

    $processCheck = Get-Process rclone -ErrorAction SilentlyContinue |
                    Where-Object { $_.CommandLine -like "*$MountPath*" }

    if ($processCheck) {
        Write-Host "⚠ $ServiceName already mounted at $MountPath" -ForegroundColor Yellow
        return
    }

    $cmd = "rclone mount ${RemoteName}: $MountPath --vfs-cache-mode writes --daemon"

    try {
        Invoke-Expression $cmd
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
Get-Process rclone -ErrorAction SilentlyContinue |
    Select-Object Id, ProcessName, @{Name="Runtime";Expression={(Get-Date) - $_.StartTime}} |
    Format-Table -AutoSize

Write-Host "`nTip: Access your clouds at:" -ForegroundColor Cyan
Write-Host "  Google Drive: $MountBase/GoogleDrive"
Write-Host "  Box:          $MountBase/Box"
Write-Host "  Dropbox:      $MountBase/Dropbox"
