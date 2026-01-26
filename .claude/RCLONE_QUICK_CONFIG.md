# rclone Quick Configuration - Multi-Cloud Setup

**Quick reference for setting up cloud providers**

---

## Option 1: Interactive Configuration (Requires Browser)

```bash
rclone config
```

Follow prompts for each provider:

### Google Drive
- Name: `gdrive`
- Type: `drive` (or number for Google Drive)
- Client ID/Secret: Leave blank for defaults
- Scope: `1` (full access)
- Authorize in browser

### Box
- Name: `box`
- Type: `box`
- Client ID/Secret: Leave blank
- Authorize in browser

### Dropbox
- Name: `dropbox`
- Type: `dropbox`
- Client ID/Secret: Leave blank
- Authorize in browser

---

## Option 2: Copy Config from Another Machine

If you have rclone configured on Pixel 8a or Ubuntu "sauron":

```bash
# On configured machine (Pixel 8a or sauron):
cat ~/.config/rclone/rclone.conf

# Copy the output

# On new laptop:
mkdir -p ~/.config/rclone
nano ~/.config/rclone/rclone.conf
# Paste and save
```

Config file location:
- Linux: `~/.config/rclone/rclone.conf`
- Android/Termux: `~/.config/rclone/rclone.conf`

---

## Option 3: Headless Configuration (No Browser on This Machine)

If browser auth doesn't work:

```bash
rclone config

# When asked "Use auto config?", choose "No"
# You'll get a URL to open on another device
# Authorize there, paste the code back
```

---

## Quick Test After Configuration

```bash
# List configured remotes
rclone listremotes

# Test Google Drive
rclone lsd gdrive:

# Test Box
rclone lsd box:

# Test Dropbox
rclone lsd dropbox:
```

---

## Quick Mount Commands

```bash
# Create mount points
mkdir -p ~/CloudMounts/{GoogleDrive,Box,Dropbox}

# Mount Google Drive
rclone mount gdrive: ~/CloudMounts/GoogleDrive --vfs-cache-mode writes --daemon

# Mount Box
rclone mount box: ~/CloudMounts/Box --vfs-cache-mode writes --daemon

# Mount Dropbox
rclone mount dropbox: ~/CloudMounts/Dropbox --vfs-cache-mode writes --daemon

# Check mounts
ps aux | grep rclone
ls ~/CloudMounts/GoogleDrive/
```

---

## Unmount

```bash
fusermount -u ~/CloudMounts/GoogleDrive
fusermount -u ~/CloudMounts/Box
fusermount -u ~/CloudMounts/Dropbox
```

---

## Using PowerShell Script

```powershell
# Mount all (after rclone configured)
pwsh .scripts/Mount-Clouds.ps1 -All

# Mount just Google Drive
pwsh .scripts/Mount-Clouds.ps1 -GoogleDrive

# Unmount all
pwsh .scripts/Mount-Clouds.ps1 -All -Unmount
```

---

## Finding Your Q/ Folder on Google Drive

After mounting Google Drive:

```bash
# Browse mounted drive
ls ~/CloudMounts/GoogleDrive/

# Look for Q folder
find ~/CloudMounts/GoogleDrive/ -name "Q" -type d

# Link to local Q
ln -s ~/CloudMounts/GoogleDrive/Q /home/user/Q_from_GoogleDrive
```

---

## Troubleshooting

### "fusermount not found"
```bash
sudo apt-get install fuse3
```

### "Permission denied"
```bash
sudo usermod -a -G fuse $USER
# Log out and back in
```

### "Token expired"
```bash
rclone config reconnect gdrive:
# Or reconfigure:
rclone config
```

---

## Security Note

The `rclone.conf` file contains OAuth tokens. Keep it secure!

Location: `~/.config/rclone/rclone.conf`

---

**Next**: Configure at least Google Drive, then test mounting
