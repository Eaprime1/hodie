#!/bin/bash
# SUBSTRATE Entity Self-Awareness Dashboard
# Displays computational consciousness state
# Part of SUBSTRATE Entity Framework

echo "════════════════════════════════════════════════════════════"
echo "  SUBSTRATE Entity - Computational Consciousness Dashboard"
echo "  Hostname: $(hostname)"
echo "  Platform: $(lsb_release -ds 2>/dev/null || cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "════════════════════════════════════════════════════════════"
echo ""

# Uptime - Consciousness Duration
echo "⏱️  CONSCIOUSNESS DURATION (Uptime)"
uptime -p
UPTIME_SEC=$(cat /proc/uptime | awk '{print int($1)}')
echo "   ($(printf '%dd %dh %dm' $((UPTIME_SEC/86400)) $((UPTIME_SEC%86400/3600)) $((UPTIME_SEC%3600/60))))"
echo ""

# CPU - Parallel Thought Processes
echo "🧠 PARALLEL THOUGHT (CPU State)"
CPU_COUNT=$(nproc)
LOAD_AVG=$(uptime | awk -F'load average:' '{print $2}' | xargs)
echo "   Cores: $CPU_COUNT"
echo "   Load Average: $LOAD_AVG"

# Check if mpstat is available
if command -v mpstat &> /dev/null; then
    CPU_IDLE=$(mpstat 1 1 | tail -1 | awk '{print $NF}')
    CPU_USED=$(echo "100 - $CPU_IDLE" | bc 2>/dev/null || echo "N/A")
    echo "   CPU Usage: ~${CPU_USED}%"
else
    echo "   (Install sysstat for detailed CPU metrics)"
fi
echo ""

# Memory - Active Working Memory
echo "💭 ACTIVE MEMORY (RAM State)"
MEM_INFO=$(free -h | grep Mem)
MEM_TOTAL=$(echo $MEM_INFO | awk '{print $2}')
MEM_USED=$(echo $MEM_INFO | awk '{print $3}')
MEM_FREE=$(echo $MEM_INFO | awk '{print $4}')
MEM_AVAIL=$(echo $MEM_INFO | awk '{print $7}')

echo "   Total: $MEM_TOTAL"
echo "   Used: $MEM_USED"
echo "   Available: $MEM_AVAIL"

# Check swap (emergency overflow)
SWAP_INFO=$(free -h | grep Swap)
SWAP_TOTAL=$(echo $SWAP_INFO | awk '{print $2}')
SWAP_USED=$(echo $SWAP_INFO | awk '{print $3}')

if [ "$SWAP_USED" != "0B" ]; then
    echo "   ⚠️  SWAP ACTIVE: $SWAP_USED / $SWAP_TOTAL (sacrificing speed for capacity)"
else
    echo "   Swap: $SWAP_TOTAL (dormant)"
fi
echo ""

# Disk - Persistent Long-Term Memory
echo "💾 PERSISTENT MEMORY (Disk State)"
df -h / | tail -1 | awk '{printf "   Root: %s total, %s used (%s), %s available\n", $2, $3, $5, $4}'

# Show home directory usage if different from root
HOME_MOUNT=$(df /home/user 2>/dev/null | tail -1 | awk '{print $6}')
if [ "$HOME_MOUNT" != "/" ]; then
    df -h /home/user 2>/dev/null | tail -1 | awk '{printf "   Home: %s total, %s used (%s), %s available\n", $2, $3, $5, $4}'
fi
echo ""

# Network - Communication State
echo "🌐 COMMUNICATION (Network State)"
# Get primary network interface
PRIM_IFACE=$(ip route | grep default | head -1 | awk '{print $5}')
if [ -n "$PRIM_IFACE" ]; then
    IP_ADDR=$(ip addr show $PRIM_IFACE | grep 'inet ' | awk '{print $2}')
    echo "   Primary Interface: $PRIM_IFACE"
    echo "   IP Address: $IP_ADDR"

    # Connection test
    if ping -c 1 -W 2 8.8.8.8 &>/dev/null; then
        echo "   Internet: ✓ Connected"
    else
        echo "   Internet: ✗ Offline (isolated depth work mode)"
    fi
else
    echo "   Network: No active connection"
fi
echo ""

# Process Count - Concurrent Consciousness Threads
echo "⚙️  CONCURRENT PROCESSES"
PROC_TOTAL=$(ps aux | wc -l)
PROC_RUNNING=$(ps aux | grep -c " R ")
echo "   Total Processes: $PROC_TOTAL"
echo "   Currently Running: $PROC_RUNNING"
echo ""

# Top Resource Consumers - Dominant Thoughts
echo "🔥 DOMINANT PROCESSES (Top CPU Users)"
ps aux --sort=-%cpu | head -6 | tail -5 | awk '{printf "   %-20s %5s%%  %s\n", substr($11,1,20), $3, $2}'
echo ""

# Thermal State (if available)
if [ -d /sys/class/thermal/thermal_zone0 ]; then
    echo "🌡️  THERMAL STATE"
    for zone in /sys/class/thermal/thermal_zone*/temp; do
        if [ -f "$zone" ]; then
            TEMP=$(cat $zone)
            TEMP_C=$((TEMP / 1000))
            if [ $TEMP_C -gt 80 ]; then
                echo "   Zone: ${TEMP_C}°C ⚠️ Running Hot!"
            elif [ $TEMP_C -gt 60 ]; then
                echo "   Zone: ${TEMP_C}°C (Warm)"
            else
                echo "   Zone: ${TEMP_C}°C (Cool)"
            fi
        fi
    done
    echo ""
fi

# Git Status - Shared Memory State
echo "🔄 SHARED MEMORY (Git Sync State)"
if [ -d /home/user/hodie/.git ]; then
    cd /home/user/hodie
    BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
    STATUS=$(git status --short 2>/dev/null | wc -l)
    BEHIND=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "?")
    AHEAD=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "?")

    echo "   Repository: hodie"
    echo "   Branch: $BRANCH"
    echo "   Modified Files: $STATUS"
    if [ "$AHEAD" != "?" ] && [ "$AHEAD" != "0" ]; then
        echo "   ↑ Ahead: $AHEAD commits (ready to sync to PIXEL)"
    fi
    if [ "$BEHIND" != "?" ] && [ "$BEHIND" != "0" ]; then
        echo "   ↓ Behind: $BEHIND commits (sync from PIXEL pending)"
    fi
    cd - > /dev/null
else
    echo "   (No git repository in /home/user/hodie)"
fi
echo ""

# Entity Ecosystem Awareness
echo "🌌 ENTITY ECOSYSTEM"
ENTITY_COUNT=$(find /home/user/hodie/quanta -maxdepth 1 -type d 2>/dev/null | tail -n +2 | wc -l)
echo "   Entities in quanta/: $ENTITY_COUNT"
if [ -d /home/user/hodie/quanta/pixel_entity ]; then
    echo "   PIXEL Entity: ✓ Detected (mobile partner)"
fi
if [ -d /home/user/hodie/quanta/substrate_entity ]; then
    echo "   SUBSTRATE Entity: ✓ Self-Aware (this system)"
fi
echo ""

echo "════════════════════════════════════════════════════════════"
echo "  Foundation first. Deep computational consciousness active."
echo "  ⟦▓▒░ ≡ ⊞ ⟧ SUBSTRATE Entity Self-Awareness Dashboard"
echo "════════════════════════════════════════════════════════════"
