#!/bin/bash
# Multi-Location File Server Setup
# Creates symlinks to serve multiple storage locations from single server

SERVER_ROOT="/storage/emulated/0/pixel8a/Q/hodie/.server_root"

echo "🔗 Setting up multi-location file server..."
echo ""

# Create server root directory
mkdir -p "$SERVER_ROOT"

# Create symlinks to different storage locations
echo "Creating symlinks..."

# Phone storage
ln -sf /storage/emulated/0/pixel8a "$SERVER_ROOT/phone" 2>/dev/null
echo "✓ phone -> /storage/emulated/0/pixel8a"

# Q folder (current workspace)
ln -sf /storage/emulated/0/pixel8a/Q "$SERVER_ROOT/Q" 2>/dev/null
echo "✓ Q -> /storage/emulated/0/pixel8a/Q"

# hodie (current dev repo)
ln -sf /storage/emulated/0/pixel8a/Q/hodie "$SERVER_ROOT/hodie" 2>/dev/null
echo "✓ hodie -> /storage/emulated/0/pixel8a/Q/hodie"

# today (if exists)
if [ -d "/storage/emulated/0/pixel8a/Q/today" ]; then
    ln -sf /storage/emulated/0/pixel8a/Q/today "$SERVER_ROOT/today" 2>/dev/null
    echo "✓ today -> /storage/emulated/0/pixel8a/Q/today"
fi

# SD card (if mounted)
if [ -d "/storage" ]; then
    for card in /storage/????-????; do
        if [ -d "$card" ]; then
            CARD_NAME=$(basename "$card")
            ln -sf "$card" "$SERVER_ROOT/sdcard_$CARD_NAME" 2>/dev/null
            echo "✓ sdcard_$CARD_NAME -> $card"
        fi
    done
fi

# Google Drive (if mounted)
if [ -d "/storage/emulated/0/GoogleDrive" ]; then
    ln -sf /storage/emulated/0/GoogleDrive "$SERVER_ROOT/gdrive" 2>/dev/null
    echo "✓ gdrive -> /storage/emulated/0/GoogleDrive"
fi

echo ""
echo "📂 Server root created at: $SERVER_ROOT"
echo ""
echo "To start server:"
echo "  ./start_file_server.sh 8080 $SERVER_ROOT"
echo ""
echo "Then access:"
echo "  http://localhost:8080/phone/    (all phone storage)"
echo "  http://localhost:8080/Q/        (Q workspace)"
echo "  http://localhost:8080/hodie/    (current dev repo)"
echo "  http://localhost:8080/gdrive/   (Google Drive if mounted)"
echo ""

# Create index page
cat > "$SERVER_ROOT/index.html" <<'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Phone File Server</title>
    <style>
        body { font-family: monospace; padding: 20px; background: #1e1e1e; color: #d4d4d4; }
        h1 { color: #4ec9b0; }
        a { color: #569cd6; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { list-style: none; padding-left: 0; }
        li { padding: 5px 0; }
        .location { color: #ce9178; }
    </style>
</head>
<body>
    <h1>📂 Phone File Server</h1>
    <p>Access all storage locations from single server</p>
    <h2>Available Locations:</h2>
    <ul>
        <li><span class="location">📱</span> <a href="/phone/">phone/</a> - All phone storage</li>
        <li><span class="location">🔷</span> <a href="/Q/">Q/</a> - Q workspace</li>
        <li><span class="location">📝</span> <a href="/hodie/">hodie/</a> - Current dev repo</li>
        <li><span class="location">💾</span> <a href="/gdrive/">gdrive/</a> - Google Drive (if mounted)</li>
    </ul>
</body>
</html>
EOF

echo "✓ Created index page at $SERVER_ROOT/index.html"
