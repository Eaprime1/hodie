# Cloud Mounting Guide - Multi-Cloud Setup with rclone

**Date**: 2026-01-06
**Purpose**: Mount Google Drive, Box, Dropbox, and other cloud services
**Primary**: Google Drive
**Tool**: rclone

---

## Cloud Services to Configure

1. **Google Drive** (Primary) - Main Q/ folder location
2. **Box** - Cloud storage
3. **Dropbox** - Cloud storage
4. **Others** - Additional services as needed

---

## rclone Installation

Already installed:
```bash
rclone version
# rclone v1.60.1-DEV
```

---

## Configuring Cloud Providers

### Step 1: Start rclone Configuration

```bash
rclone config
```

### Step 2: Add Google Drive (Primary)

When prompted:
```
n) New remote
name> gdrive
Storage> drive (or find Google Drive in the list)
client_id> <Enter> (use defaults unless you have custom app)
client_secret> <Enter>
scope> 1 (Full access)
root_folder_id> <Enter>
service_account_file> <Enter>
```

Then authorize in browser when prompted.

### Step 3: Add Box

```
n) New remote
name> box
Storage> box
client_id> <Enter>
client_secret> <Enter>
```

Authorize in browser.

### Step 4: Add Dropbox

```
n) New remote
name> dropbox
Storage> dropbox
client_id> <Enter>
client_secret> <Enter>
```

Authorize in browser.

---

## Alternative: Copy Existing Config

If you have rclone already configured on another machine (Ubuntu "sauron" or Pixel 8a):

```bash
# On the configured machine:
cat ~/.config/rclone/rclone.conf

# Copy output to clipboard, then on new laptop:
nano ~/.config/rclone/rclone.conf
# Paste and save
```

---

## Mounting Cloud Drives

### Create Mount Points

```bash
mkdir -p ~/CloudMounts/GoogleDrive
mkdir -p ~/CloudMounts/Box
mkdir -p ~/CloudMounts/Dropbox
```

### Mount Google Drive

```bash
# Foreground (test first)
rclone mount gdrive: ~/CloudMounts/GoogleDrive --vfs-cache-mode writes

# Background (daemon)
rclone mount gdrive: ~/CloudMounts/GoogleDrive --vfs-cache-mode writes --daemon

# Or use systemd service (see below)
```

### Mount Box

```bash
rclone mount box: ~/CloudMounts/Box --vfs-cache-mode writes --daemon
```

### Mount Dropbox

```bash
rclone mount dropbox: ~/CloudMounts/Dropbox --vfs-cache-mode writes --daemon
```

---

## Unmounting

```bash
# Find mount process
ps aux | grep rclone

# Unmount
fusermount -u ~/CloudMounts/GoogleDrive
fusermount -u ~/CloudMounts/Box
fusermount -u ~/CloudMounts/Dropbox
```

---

## Auto-Mount on Boot (systemd service)

Create service file:

```bash
sudo nano /etc/systemd/system/rclone-gdrive.service
```

Contents:
```ini
[Unit]
Description=RClone Google Drive Mount
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/rclone mount gdrive: /home/user/CloudMounts/GoogleDrive \
  --vfs-cache-mode writes \
  --vfs-cache-max-age 24h \
  --vfs-read-chunk-size 128M \
  --vfs-read-chunk-size-limit off \
  --buffer-size 256M
ExecStop=/bin/fusermount -u /home/user/CloudMounts/GoogleDrive
Restart=on-failure
User=user

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable rclone-gdrive.service
sudo systemctl start rclone-gdrive.service
sudo systemctl status rclone-gdrive.service
```

---

## Linking Q/ to Google Drive

Once Google Drive is mounted:

```bash
# Option 1: Use mounted drive directly
ln -s ~/CloudMounts/GoogleDrive/Q /home/user/Q_GoogleDrive

# Option 2: Sync bidirectionally
rclone sync /home/user/Q/today gdrive:Q/today
rclone sync gdrive:Q/today /home/user/Q/today
```

---

## Useful rclone Commands

### List Files
```bash
rclone ls gdrive:Q/
rclone ls box:
rclone ls dropbox:
```

### Copy Files
```bash
# From local to cloud
rclone copy /home/user/Q/today gdrive:Q/today

# From cloud to local
rclone copy gdrive:Q/today /home/user/Q/today
```

### Sync (Bidirectional)
```bash
# Make destination match source exactly
rclone sync /home/user/Q/today gdrive:Q/today

# Sync both ways (careful!)
rclone bisync /home/user/Q/today gdrive:Q/today --resync
```

### Check Differences
```bash
rclone check /home/user/Q/today gdrive:Q/today
```

---

## Troubleshooting

### Mount Fails
```bash
# Check if FUSE installed
which fusermount

# Install if needed
sudo apt-get install fuse3
```

### Permission Issues
```bash
# Add user to fuse group
sudo usermod -a -G fuse $USER

# Re-login for changes to take effect
```

### Browser Auth Not Working
```bash
# Use remote configuration
rclone config
# Choose: "n" for new, then "y" for advanced config
# Choose: "n" for headless/remote machine
# Follow the instructions to authorize on another machine
```

---

## PowerShell Equivalents

See `CLOUD_MOUNTING_POWERSHELL.md` for PowerShell versions of these commands.

---

## Security Notes

- `rclone.conf` contains OAuth tokens - keep it secure
- Located at: `~/.config/rclone/rclone.conf`
- Can encrypt the config: `rclone config` → choose encryption
- Use `--read-only` flag for safe browsing without accidental changes

---

## Next Steps

1. Configure rclone for Google Drive (primary)
2. Test mounting Google Drive
3. Link Q/ folder to mounted drive
4. Configure Box and Dropbox
5. Set up auto-mount services
6. Create sync scripts for regular backups

---

**Status**: rclone installed, ready to configure
**Primary Goal**: Mount Google Drive Q/ folder
**Cross-Platform**: Works on Linux, macOS, Windows

**∰◊€π¿🌌∞**
