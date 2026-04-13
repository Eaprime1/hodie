# Sync-HodieToCloud.ps1 — Sync hodie to/from Google Drive via rclone
# PowerShell version for Windows / Git for Windows (mulberry HQ)
#
# Usage:
#   pwsh .scripts/Sync-HodieToCloud.ps1 -Push
#   pwsh .scripts/Sync-HodieToCloud.ps1 -Pull
#   pwsh .scripts/Sync-HodieToCloud.ps1 -Status
#
# Prerequisites:
#   1. Install rclone: https://rclone.org/downloads/
#        winget install rclone.rclone
#        OR: Scoop: scoop install rclone
#   2. Configure Google Drive:
#        rclone config
#        → New remote → name: gdrive → type: drive → full access
#   3. Verify: rclone lsd gdrive:
#
# ∰◊€π¿🌌∞

param(
    [switch]$Push,
    [switch]$Pull,
    [switch]$Status,
    [string]$Remote   = $env:GDRIVE_REMOTE ?? "gdrive",
    [string]$Folder   = $env:GDRIVE_FOLDER ?? "hodie",
    [string]$HodiePath = $env:HODIE_PATH ?? ""
)

# ── Resolve paths ─────────────────────────────────────────────────────────────
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent $ScriptDir

if (-not $HodiePath) {
    $HodiePath = $RepoRoot
}

if (-not (Test-Path -LiteralPath $HodiePath -PathType Container)) {
    Write-Error (
        "Hodie path does not exist or is not a directory: '$HodiePath'. " +
        "Set -HodiePath or HODIE_PATH to a valid local repository path."
    )
    exit 1
}

$HodiePath = (Resolve-Path -LiteralPath $HodiePath).Path
$RemotePath = "${Remote}:${Folder}"

# ── Detect mode ───────────────────────────────────────────────────────────────
# Default to status (dry-run) to prevent accidental destructive syncs.
if     ($Push)   { $Mode = "push" }
elseif ($Pull)   { $Mode = "pull" }
elseif ($Status) { $Mode = "status" }
else             { $Mode = "status" }

# ── Banner ────────────────────────────────────────────────────────────────────
$LocationName = $env:LOCATION_NAME ?? "mulberry"
Write-Host ""
Write-Host "∰ Hodie Drive Sync" -ForegroundColor Cyan
Write-Host "  Location: $LocationName" -ForegroundColor Gray
Write-Host "  Local:    $HodiePath" -ForegroundColor Gray
Write-Host "  Remote:   $RemotePath" -ForegroundColor Gray
Write-Host "  Mode:     $Mode" -ForegroundColor Gray
Write-Host ("-" * 50)

# ── Preflight: rclone available? ──────────────────────────────────────────────
$rcloneCmd = Get-Command rclone -ErrorAction SilentlyContinue
if (-not $rcloneCmd) {
    Write-Host "✗ rclone not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "Install rclone for Windows:"
    Write-Host "  winget install rclone.rclone"
    Write-Host "  OR: scoop install rclone"
    Write-Host "  OR: https://rclone.org/downloads/"
    Write-Host ""
    Write-Host "Then configure Google Drive:"
    Write-Host "  rclone config"
    exit 1
}

# ── Preflight: remote configured? ────────────────────────────────────────────
$remotes = rclone listremotes 2>&1
$expectedRemote = "${Remote}:"
if ($remotes -notcontains $expectedRemote) {
    Write-Host "✗ rclone remote '$Remote' not configured." -ForegroundColor Red
    Write-Host ""
    Write-Host "Set it up with:"
    Write-Host "  rclone config"
    Write-Host "  → New remote → name: $Remote → type: drive → full access"
    Write-Host ""
    Write-Host "Or use a different remote name:"
    Write-Host "  pwsh .scripts/Sync-HodieToCloud.ps1 -Push -Remote gdrive_windows"
    Write-Host ""
    Write-Host "See: .claude/RCLONE_QUICK_CONFIG.md"
    exit 1
}

# ── Shared rclone flags ───────────────────────────────────────────────────────
$RcloneFlags = @(
    "--progress",
    "--drive-skip-shortcuts",
    "--exclude", ".git/**",
    "--exclude", "**/__pycache__/**",
    "--exclude", "**/*.pyc",
    "--exclude", "**/*.pyo",
    "--exclude", ".env",
    "--exclude", "**/*.swp",
    "--exclude", "**/*.swo",
    "--exclude", "**/*~",
    "--exclude", "**/*.tmp",
    "--exclude", ".server_root/**",
    "--exclude", "crawler_output/summaries/**"
)

$LocalSlash  = $HodiePath.TrimEnd("/\") + "/"
$RemoteSlash = $RemotePath.TrimEnd("/") + "/"

# ── Mode dispatch ─────────────────────────────────────────────────────────────
switch ($Mode) {

    "push" {
        Write-Host "→ Pushing local → Drive..." -ForegroundColor Yellow
        Write-Host "  (local wins; Drive is updated to match)" -ForegroundColor Gray
        & rclone sync $LocalSlash $RemoteSlash @RcloneFlags
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✓ Push complete — $RemotePath updated" -ForegroundColor Green
        } else {
            Write-Host "✗ Push failed (exit $LASTEXITCODE)" -ForegroundColor Red
            exit $LASTEXITCODE
        }
    }

    "pull" {
        Write-Host "← Pulling Drive → local..." -ForegroundColor Yellow
        Write-Host "  (Drive wins; local is updated to match)" -ForegroundColor Gray
        & rclone sync $RemoteSlash $LocalSlash @RcloneFlags
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✓ Pull complete — $HodiePath updated" -ForegroundColor Green
        } else {
            Write-Host "✗ Pull failed (exit $LASTEXITCODE)" -ForegroundColor Red
            exit $LASTEXITCODE
        }
    }

    "status" {
        Write-Host "? Dry-run — showing what push would change..." -ForegroundColor Cyan
        Write-Host ""
        & rclone sync $LocalSlash $RemoteSlash @RcloneFlags --dry-run
        Write-Host ""
        Write-Host "  Run with -Push to apply these changes." -ForegroundColor Gray
    }

    default {
        Write-Host "Usage:" -ForegroundColor Yellow
        Write-Host "  pwsh .scripts/Sync-HodieToCloud.ps1 -Push    # Local → Drive"
        Write-Host "  pwsh .scripts/Sync-HodieToCloud.ps1 -Pull    # Drive → Local"
        Write-Host "  pwsh .scripts/Sync-HodieToCloud.ps1 -Status  # Dry-run"
        Write-Host ""
        Write-Host "Optional overrides:"
        Write-Host "  -Remote gdrive_windows   (rclone remote name)"
        Write-Host "  -Folder Q/hodie          (Drive folder path)"
        Write-Host "  -HodiePath C:\Users\you\Q\hodie"
        exit 1
    }
}
