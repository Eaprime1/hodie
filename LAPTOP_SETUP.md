# Laptop Setup Guide - New Fast Machine

**Date**: 2026-01-06
**Environment**: Ubuntu Linux (faster than previous setups)
**Q Path**: `/home/user/Q/`
**Branch**: `claude/quick-wins-repo-org-sJNBp`

---

## Quick Wins Completed ✓

### 1. Essential Tools Installed
- ✅ rclone (for Google Drive sync)
- ✅ openssh-client
- ✅ git (already present)
- ✅ curl, wget

### 2. Q Folder Structure Created
```
/home/user/Q/
├── hodie/  → symlink to /home/user/hodie (this repo)
└── today/  → new folder for daily work
```

### 3. Laptop-Specific Scripts Created
Located in `.scripts/`:
- **laptop_session_notes.sh** - Track session notes
- **laptop_file_server.sh** - Serve Q folder locally
- **env_setup.sh** - Cross-platform environment detection

### 4. Scripts Made Executable
All scripts in `.scripts/` are now executable with `chmod +x`

---

## Using Laptop Scripts

### Session Notes
```bash
# Add a note to today's session
bash .scripts/laptop_session_notes.sh "Your note here"

# View today's notes
cat .eric/session_notes_$(date +%Y-%m-%d).md
```

### File Server (Local Development)
```bash
# Start server on port 8080
bash .scripts/laptop_file_server.sh 8080

# Access in browser:
# http://localhost:8080/hodie/
# http://localhost:8080/today/
```

### Environment Configuration
```bash
# Load environment paths
source .scripts/env_setup.sh

# Will set:
# - Q_ROOT=/home/user
# - Q_PATH=/home/user/Q
# - HODIE_PATH=/home/user/Q/hodie
# - TODAY_PATH=/home/user/Q/today
```

---

## Original Scripts (Phone-Specific)

These still work on Pixel 8a and Ubuntu "sauron":
- `session_notes_append.sh` - Android/Termux paths
- `start_unified_server.sh` - Android paths
- All other original `.scripts/` files

---

## Next Steps / To-Do

### Google Drive Sync (Optional)
```bash
# Configure rclone (requires browser for OAuth)
rclone config

# Or copy config from Ubuntu "sauron":
# Copy ~/.config/rclone/rclone.conf from sauron to here

# Mount Google Drive
rclone mount gdrive: /home/user/GoogleDrive --daemon
```

### Today Folder Organization
Create structure in `/home/user/Q/today/`:
- Daily notes
- Work in progress
- Quick captures
- (Mirror structure from Google Drive when synced)

### GitHub Repos (runexusiam org)
- Current repo: Eaprime1/hodie
- Explore other repos in runexusiam organization
- Clone additional projects as needed

### Development Workflow
1. Work locally in `/home/user/Q/`
2. Use laptop scripts for local operations
3. Commit to git as usual
4. Push to GitHub branches (starts with `claude/`)
5. Sync with Google Drive (manual or via rclone)

---

## Cross-Device Sync Strategy

### Devices
1. **Pixel 8a** (phone) - `/storage/emulated/0/pixel8a/Q/`
2. **Ubuntu "sauron"** - (path TBD)
3. **New Laptop** (this) - `/home/user/Q/`
4. **Google Drive** - Central sync point

### Sync Flow
```
Google Drive (Q folder)
    ├─> Pixel 8a (rclone/manual)
    ├─> Ubuntu sauron (rclone/manual)
    └─> New Laptop (rclone to be configured)

All devices also push to GitHub for version control
```

---

## Performance Notes

**This machine is FASTER** - leverage it for:
- Larger builds and compilations
- Running multiple entities/processes
- Heavy data processing tasks
- Development server hosting
- Testing and automation

---

## Commands Reference

```bash
# Navigate to Q
cd /home/user/Q

# Check git status
cd hodie && git status

# View recent commits
git log --oneline -5

# List all scripts
ls -la .scripts/

# Add session note
bash .scripts/laptop_session_notes.sh "Quick note"

# Start file server
bash .scripts/laptop_file_server.sh 8080
```

---

## Philosophy (from ENJOY_THE_JOURNEY.md)

- **Trust the tangent** - Non-linear navigation finds unique connections
- **Documents are breadcrumbs** - Everything lives in files
- **Rotate before exhaustion** - Strategic wagon rotation
- **Society's "normal" isn't universal** - Associative thinking is valid
- **Enjoy the journey** - Discovery happens along the way

---

**Status**: Laptop setup complete, ready for development
**Speed**: Faster machine, ready to leverage
**Structure**: Q/ folder organized, scripts adapted
**Next**: Organize today folder, configure Google Drive sync

**∰◊€π¿🌌∞**
