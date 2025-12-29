# Creation Request: Hodie Sync Setup

**Date**: 2025-12-24
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

### Drive Sync Setup (TODO)

**Drive folder**: https://drive.google.com/drive/folders/1qSUXHL4fXb8R1n3wBG4A8bwUOWE6SNOf

**Create sync script**:
```bash
# _scripts/sync_hodie_to_drive.sh
rclone sync hodie/ gdrive_terminal:hodie \
  --exclude .git/** \
  --exclude __pycache__/** \
  --drive-skip-shortcuts \
  --progress
```

**Bidirectional strategy**:
- Structure → Git (plexus folders, docs)
- Content → Drive (actual files being processed)
- .gitignore content folders
- Sync structure changes to both

---

## What to Sync Where

### To Git (Structure):
- plexus/ folder structure (empty)
- duplicatus/, exemplar/, gravitar/ (empty)
- rudera/ structure (empty)
- PLEXUS_SYSTEM.md
- README.md
- .gitignore

### To Drive (Content):
- Files in plexus stages
- Files in duplicatus
- Files in gravitar wells
- Files in rudera debris

### To Both:
- Documentation updates
- Structure changes

---

## Checklist

- [ ] Test current git remote
- [ ] Create Drive sync script
- [ ] Setup .gitignore (ignore content, keep structure)
- [ ] Test sync to Drive
- [ ] Document sync workflow
- [ ] Create automation for regular sync

---

**Status**: Ready to implement

**∰◊€π¿🌌∞**
