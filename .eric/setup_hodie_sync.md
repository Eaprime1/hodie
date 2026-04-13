# Creation Request: Hodie Sync Setup

**Date**: 2025-12-24
**Updated**: 2026-04-13
**Priority**: High
**Type**: Configuration

---

## Task: Setup Dual Sync for Hodie

### Requirements
1. **Git sync** to GitHub (code, structure)
2. **Drive sync** to Google Drive (content, files)

### Git Setup (Already Done ✓)
```bash
cd /storage/emulated/0/pixel8a/Q/hodie
git remote -v
# Already connected to github.com/Eaprime1/hodie
```

### Drive Sync Setup (Scripts Created ✓ — rclone config needed per device)

**Drive folder**: https://drive.google.com/drive/folders/1qSUXHL4fXb8R1n3wBG4A8bwUOWE6SNOf

**Bash sync script (Linux / WSL / Termux)**:
```bash
# Push local → Drive
bash .scripts/sync_hodie_to_drive.sh push

# Pull Drive → local
bash .scripts/sync_hodie_to_drive.sh pull

# Dry-run: see what would change
bash .scripts/sync_hodie_to_drive.sh status
```

**PowerShell sync script (Windows / Git for Windows)**:
```powershell
# Push local → Drive
pwsh .scripts/Sync-HodieToCloud.ps1 -Push

# Pull Drive → local
pwsh .scripts/Sync-HodieToCloud.ps1 -Pull

# Dry-run
pwsh .scripts/Sync-HodieToCloud.ps1 -Status
```

**Custom remote name** (if rclone config uses different name):
```bash
GDRIVE_REMOTE=gdrive_terminal bash .scripts/sync_hodie_to_drive.sh push
# or PowerShell:
pwsh .scripts/Sync-HodieToCloud.ps1 -Push -Remote gdrive_terminal
```

---

## What Gets Synced

### Excluded from Drive sync (handled by Git or not needed):
- `.git/` — git history stays local + GitHub
- `**/__pycache__/`, `*.pyc` — generated Python cache
- `.env` — secrets, never synced
- `crawler_output/summaries/` — large generated JSONs (regeneratable)
- `.server_root/` — runtime symlinks

### Everything else syncs to Drive:
- `_SORTING/`, `_CONSOLIDATED/` — conversation content
- `quanta/`, `redundancy_entity/` — entity and analysis files
- `crawler_pixel8/`, `tests/` — code (also on GitHub)
- `crawler_output/` master summary and maps — preserved
- All documentation (.eric/, .claude/, .scripts/, etc.)

---

## Bidirectional strategy

| What | Where | Tool |
|------|-------|------|
| Code, structure, docs | Git → GitHub | `git push` |
| Conversation content, entities | Local → Drive | `sync push` |
| New files from phone to laptop | Drive → Local | `sync pull` |
| Everything backup | All → Drive | `sync push` |

---

## Per-Device Setup Checklist

### Pixel 8a (Termux)
- [x] Git connected to GitHub
- [ ] Install rclone: `pkg install rclone`
- [ ] Configure: `rclone config` (name: `gdrive`)
- [ ] Test: `rclone lsd gdrive:`
- [ ] First push: `bash .scripts/sync_hodie_to_drive.sh push`

### Mulberry Laptop (Git for Windows / WSL)
- [x] Git connected to GitHub
- [x] rclone installed (per MULTI_CLOUD_SETUP.md)
- [ ] Configure: `rclone config` (name: `gdrive`)
- [ ] Test: `rclone lsd gdrive:`
- [ ] First push (bash): `bash .scripts/sync_hodie_to_drive.sh push`
- [ ] OR PowerShell: `pwsh .scripts/Sync-HodieToCloud.ps1 -Push`

### Codespaces (cloud, ephemeral)
- [x] Git connected to GitHub
- [ ] rclone optional (install if needed: `sudo apt install rclone`)
- [ ] Configure if needed (use headless option with phone as auth device)

---

## rclone Configuration Quick Reference

```bash
# Interactive setup (has browser)
rclone config
# → New → name: gdrive → type: drive → scope: 1 (full) → authorize

# Headless (no browser — authorize on phone)
rclone config
# → when asked "Use auto config?" → choose No
# → open URL on phone, paste token back

# Copy config from Pixel 8a to laptop
# On phone: cat ~/.config/rclone/rclone.conf
# On laptop: paste into ~/.config/rclone/rclone.conf
```

See also: `.claude/RCLONE_QUICK_CONFIG.md`

---

## Checklist

- [x] Test current git remote
- [x] Create Drive sync script (bash)
- [x] Create Drive sync script (PowerShell)
- [x] Document sync workflow
- [x] Define excluded patterns
- [ ] Configure rclone on Pixel 8a
- [ ] Configure rclone on mulberry
- [ ] Test first push from each device
- [ ] Test pull (Drive → device)
- [ ] Set up automation for regular sync (cron or Task Scheduler)

---

## Automation (next step after manual sync works)

**Termux cron**:
```bash
# Edit crontab
crontab -e
# Add: sync every hour
0 * * * * bash /storage/emulated/0/pixel8a/Q/hodie/.scripts/sync_hodie_to_drive.sh push >> /tmp/hodie_sync.log 2>&1
```

**Windows Task Scheduler**:
```powershell
# Create scheduled task (run as admin)
$action  = New-ScheduledTaskAction -Execute "pwsh" -Argument "-File C:\Users\user\Q\hodie\.scripts\Sync-HodieToCloud.ps1 -Push"
$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 1) -Once -At (Get-Date)
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "HodieDriveSync" -RunLevel Highest
```

---

**Status**: Scripts ready — configure rclone per device to activate

**∰◊€π¿🌌∞**
