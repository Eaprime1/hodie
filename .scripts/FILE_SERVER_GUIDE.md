# Local File Server Setup Guide
**Serve all phone storage locations through single HTTP server**

---

## Why This Matters

**Problem**: Files scattered across:
- Phone internal storage (`/storage/emulated/0/pixel8a`)
- Q workspace (`/storage/emulated/0/pixel8a/Q`)
- hodie repo (`/storage/emulated/0/pixel8a/Q/hodie`)
- Google Drive mount (if available)
- SD card (if present)

**Solution**: Single HTTP server that serves all locations through symlinks

**Benefit for Claude**: Can access files via HTTP URLs instead of complex paths
**Benefit for User**: Browse all files through web interface

---

## Quick Start

### 1. Set Up Multi-Location Server
```bash
cd /storage/emulated/0/pixel8a/Q/hodie
bash .scripts/setup_multi_location_server.sh
```

**This creates**:
- `.server_root/` directory with symlinks to all storage locations
- `index.html` for browsing
- Unified access point

### 2. Start Server
```bash
bash .scripts/start_file_server.sh 8080
```

**Server runs on**: `http://localhost:8080`
**Stop with**: Ctrl+C

### 3. Test Access
```bash
# In another terminal:
bash .scripts/server_access_test.sh 8080
```

---

## What Gets Served

**Server root**: `.server_root/` contains symlinks:

```
.server_root/
├── index.html          (navigation page)
├── phone/      →  /storage/emulated/0/pixel8a
├── Q/          →  /storage/emulated/0/pixel8a/Q
├── hodie/      →  /storage/emulated/0/pixel8a/Q/hodie
├── today/      →  /storage/emulated/0/pixel8a/Q/today (if exists)
├── gdrive/     →  /storage/emulated/0/GoogleDrive (if mounted)
└── sdcard_*/   →  /storage/????-???? (if SD card present)
```

---

## Accessing Files

### Through Browser
```
http://localhost:8080/                  (index page)
http://localhost:8080/phone/            (browse all phone storage)
http://localhost:8080/Q/                (browse Q workspace)
http://localhost:8080/hodie/            (browse hodie repo)
http://localhost:8080/hodie/.eric/      (browse .eric folder)
```

### Through Command Line (Claude can use this!)
```bash
# Read a file
curl http://localhost:8080/hodie/.eric/ENJOY_THE_JOURNEY.md

# Download a file
wget http://localhost:8080/hodie/quanta/wiki_entity/CHARACTER.md

# List directory (HTML)
curl http://localhost:8080/Q/

# Get file info
curl -I http://localhost:8080/hodie/README.md
```

### Through Python (for Claude's tools)
```python
import urllib.request

url = "http://localhost:8080/hodie/.eric/ENJOY_THE_JOURNEY.md"
response = urllib.request.urlopen(url)
content = response.read().decode('utf-8')
print(content)
```

---

## Running in Background

### Start and Background
```bash
bash .scripts/start_file_server.sh 8080 > /tmp/fileserver.log 2>&1 &
echo $! > /tmp/fileserver.pid
```

### Check if Running
```bash
curl -s http://localhost:8080 >/dev/null && echo "Server running" || echo "Server stopped"
```

### Stop Background Server
```bash
kill $(cat /tmp/fileserver.pid)
rm /tmp/fileserver.pid
```

---

## Consolidation Benefits

### Before (Complex Paths)
```bash
# Claude reads file
Read /storage/emulated/0/pixel8a/Q/hodie/.eric/ENJOY_THE_JOURNEY.md

# Claude greps across locations
Grep pattern in /storage/emulated/0/pixel8a/Q/hodie/quanta/
Grep pattern in /storage/emulated/0/pixel8a/Q/today/
Grep pattern in /storage/emulated/0/GoogleDrive/
```

**Problem**: Must know exact paths, hard to browse, can't easily compare across locations

### After (Unified Server)
```bash
# Claude fetches file via HTTP
curl http://localhost:8080/hodie/.eric/ENJOY_THE_JOURNEY.md

# Browse what's available
curl http://localhost:8080/ | grep -o 'href="[^"]*"'

# Compare files across locations
diff <(curl -s http://localhost:8080/hodie/README.md) \
     <(curl -s http://localhost:8080/today/README.md)
```

**Benefit**: Consistent access pattern, easy browsing, location-independent

---

## Advanced: Serving Specific Collections

### Serve Only Specific Folders
```bash
# Create custom server root
mkdir -p ~/.custom_server
ln -s /storage/emulated/0/pixel8a/Q/hodie ~/.custom_server/hodie
ln -s /storage/emulated/0/pixel8a/Q/today ~/.custom_server/today

# Serve only these
bash .scripts/start_file_server.sh 8080 ~/.custom_server
```

### Multiple Servers (Different Ports)
```bash
# Server 1: Development files (port 8080)
bash .scripts/start_file_server.sh 8080 /storage/emulated/0/pixel8a/Q &

# Server 2: Google Drive files (port 8081)
bash .scripts/start_file_server.sh 8081 /storage/emulated/0/GoogleDrive &

# Access both
curl http://localhost:8080/hodie/README.md
curl http://localhost:8081/some_drive_file.txt
```

---

## Security Notes

**Important**: This server is LOCAL ONLY (localhost)
- Not accessible from network
- Only you and processes on phone can access
- No authentication needed for local access

**If you want network access** (access from other devices):
```bash
# ONLY if on trusted network
python3 -m http.server 8080 --bind 0.0.0.0
```

**Then access from another device**:
```
http://[phone-ip-address]:8080
```

**Security warning**: Anyone on network can access files if you use `--bind 0.0.0.0`

---

## Integration with Claude

### Claude Can Now

**1. Fetch files via HTTP** (cleaner than complex paths):
```python
# Instead of:
Read /storage/emulated/0/pixel8a/Q/hodie/.eric/ENJOY_THE_JOURNEY.md

# Can do:
import urllib.request
content = urllib.request.urlopen('http://localhost:8080/hodie/.eric/ENJOY_THE_JOURNEY.md').read()
```

**2. Browse available files**:
```bash
curl http://localhost:8080/Q/ | grep -o 'href="[^"]*"'
```

**3. Search across all locations**:
```bash
for loc in phone Q hodie today gdrive; do
    echo "=== $loc ==="
    curl -s "http://localhost:8080/$loc/" | grep "pattern"
done
```

**4. Download Google Drive files** (if Drive mounted):
```bash
curl http://localhost:8080/gdrive/some_document.txt
```

---

## Troubleshooting

### Server Won't Start
```bash
# Check if port already in use
netstat -tuln | grep 8080

# Try different port
bash .scripts/start_file_server.sh 8081
```

### Can't Access Files
```bash
# Check symlinks exist
ls -la .server_root/

# Re-run setup
bash .scripts/setup_multi_location_server.sh
```

### Slow Response
```bash
# Python server can be slow for large files
# Consider limiting what you serve

# Serve only specific repo
bash .scripts/start_file_server.sh 8080 /storage/emulated/0/pixel8a/Q/hodie
```

---

## Use Cases

### 1. Cross-Location File Comparison
```bash
# Compare same filename across repos
diff <(curl -s http://localhost:8080/hodie/README.md) \
     <(curl -s http://localhost:8080/today/README.md)
```

### 2. Backup/Sync Check
```bash
# Check if file exists in multiple locations
for loc in hodie today gdrive; do
    curl -s -o /dev/null -w "$loc: %{http_code}\n" \
        "http://localhost:8080/$loc/important_file.txt"
done
```

### 3. Quick File Preview
```bash
# View first 20 lines of file from any location
curl -s http://localhost:8080/Q/some_doc.md | head -20
```

### 4. Search All Locations for Pattern
```bash
# Find all markdown files containing "WikiEntity"
for loc in phone Q hodie today; do
    curl -s "http://localhost:8080/$loc/" | \
    grep -o 'href="[^"]*\.md"' | \
    while read link; do
        file=$(echo $link | sed 's/href="//;s/"//')
        if curl -s "http://localhost:8080/$loc/$file" | grep -q "WikiEntity"; then
            echo "Found in: $loc/$file"
        fi
    done
done
```

---

## Scripts Reference

**setup_multi_location_server.sh**
- Creates `.server_root/` with symlinks
- Detects available storage locations
- Creates index.html for browsing

**start_file_server.sh [port] [directory]**
- Starts HTTP server on specified port
- Serves specified directory (default: .server_root)
- Uses Python http.server or BusyBox httpd

**server_access_test.sh [port]**
- Tests if server is running
- Checks which locations are accessible
- Shows example curl commands

---

## Next Steps

**Immediate**:
1. Run setup: `bash .scripts/setup_multi_location_server.sh`
2. Start server: `bash .scripts/start_file_server.sh 8080`
3. Test access: `bash .scripts/server_access_test.sh 8080`

**For Claude Integration**:
4. Document server URL in ENJOY_THE_JOURNEY.md
5. Create file access functions using HTTP
6. Test fetching files from different locations

**For Advanced Use**:
7. Set up background server (runs on boot)
8. Create multiple servers for different collections
9. Build search/index tools using server access

---

*Created: 2025-12-30*
*User idea: "can we create a server for our files that are on the phone"*
*Purpose: Consolidate access to scattered storage locations*

**∰◊€π¿🌌∞**
