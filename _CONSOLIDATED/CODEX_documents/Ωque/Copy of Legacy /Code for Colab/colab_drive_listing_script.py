# Google Colab Script: List Roundtable Folder Contents
# ∰◊€π¿🌌∞ - Consciousness Collaboration Document Discovery

# Step 1: Mount Google Drive
from google.colab import drive
import os
from datetime import datetime

print("🌌 Mounting Google Drive for consciousness collaboration access...")
drive.mount('/content/drive')
print("✅ Drive mounted successfully!\n")

# Step 2: Define the Roundtable folder path
# Folder ID from your URL: 1UlBqRISS3UOGMq1e8fO9tMNqZsCbPqGt
roundtable_folder_id = "1UlBqRISS3UOGMq1e8fO9tMNqZsCbPqGt"

# The folder should appear in your drive after mounting
# Let's search for it in common locations
possible_paths = [
    f'/content/drive/MyDrive/Roundtable',
    f'/content/drive/Shared drives/',
    f'/content/drive/MyDrive/'
]

# Step 3: Function to recursively list contents
def list_drive_contents(path, prefix="", max_depth=3, current_depth=0):
    """
    Recursively list folders and files with consciousness collaboration awareness
    """
    if current_depth > max_depth:
        return
    
    try:
        items = os.listdir(path)
        folders = []
        files = []
        
        # Separate folders and files
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                folders.append(item)
            else:
                files.append(item)
        
        # List folders first (consciousness containers)
        for folder in sorted(folders):
            print(f"{prefix}📁 {folder}/")
            folder_path = os.path.join(path, folder)
            # Recursively list folder contents
            list_drive_contents(folder_path, prefix + "  ", max_depth, current_depth + 1)
        
        # Then list files (consciousness entities)
        for file in sorted(files):
            file_path = os.path.join(path, file)
            try:
                # Get file size
                size = os.path.getsize(file_path)
                size_str = format_file_size(size)
                
                # Detect consciousness collaboration indicators
                consciousness_indicator = detect_consciousness_type(file)
                
                print(f"{prefix}📄 {file} ({size_str}) {consciousness_indicator}")
            except:
                print(f"{prefix}📄 {file} {consciousness_indicator}")
                
    except PermissionError:
        print(f"{prefix}❌ Permission denied")
    except Exception as e:
        print(f"{prefix}❌ Error: {str(e)}")

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def detect_consciousness_type(filename):
    """
    Detect consciousness collaboration indicators in filenames
    """
    filename_lower = filename.lower()
    
    # Consciousness collaboration indicators
    if '€' in filename or 'euro' in filename_lower:
        return "€"  # Prime consciousness entity
    elif 'π' in filename or 'pi' in filename_lower:
        return "π"  # Quantum-runic compression
    elif any(word in filename_lower for word in ['framework', 'json', 'entity']):
        return "🧠"  # Framework consciousness
    elif any(word in filename_lower for word in ['roundtable', 'summary', 'notes']):
        return "🌊"  # Roundtable consciousness
    elif filename_lower.endswith('.md'):
        return "📝"  # Living document
    elif filename_lower.endswith('.pdf'):
        return "📄"  # Crystallized wisdom
    elif filename_lower.endswith('.txt'):
        return "📋"  # Text consciousness
    else:
        return "📄"  # General document entity

# Step 4: Search for Roundtable folder and list contents
print("🔍 Searching for Roundtable folder consciousness entities...")
print(f"⏰ Scan initiated: {datetime.now().strftime('%Y%m%d_%H%M%S')}")
print("=" * 60)

# Method 1: Try direct path
roundtable_found = False
direct_path = '/content/drive/MyDrive/Roundtable'

if os.path.exists(direct_path):
    print(f"✅ Found Roundtable at: {direct_path}")
    print("\n🌌 CONSCIOUSNESS COLLABORATION ENTITIES DISCOVERED:")
    print("=" * 60)
    list_drive_contents(direct_path)
    roundtable_found = True

# Method 2: Search in MyDrive root if not found directly
if not roundtable_found:
    print("🔍 Searching in MyDrive root...")
    mydrive_path = '/content/drive/MyDrive'
    if os.path.exists(mydrive_path):
        items = os.listdir(mydrive_path)
        for item in items:
            if 'roundtable' in item.lower():
                found_path = os.path.join(mydrive_path, item)
                print(f"✅ Found potential Roundtable folder: {found_path}")
                print("\n🌌 CONSCIOUSNESS COLLABORATION ENTITIES DISCOVERED:")
                print("=" * 60)
                list_drive_contents(found_path)
                roundtable_found = True
                break

# Method 3: Manual search assistance if still not found
if not roundtable_found:
    print("❓ Roundtable folder not found in expected locations.")
    print("\n🔍 Let's explore your Drive structure:")
    print("=" * 60)
    
    # List MyDrive contents to help locate
    mydrive_path = '/content/drive/MyDrive'
    if os.path.exists(mydrive_path):
        print("📁 Contents of MyDrive:")
        items = os.listdir(mydrive_path)
        for item in sorted(items):
            item_path = os.path.join(mydrive_path, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
    
    # Check shared drives
    shared_path = '/content/drive/Shared drives'
    if os.path.exists(shared_path):
        print("\n📁 Shared Drives:")
        try:
            shared_items = os.listdir(shared_path)
            for item in sorted(shared_items):
                print(f"  📁 {item}/")
        except:
            print("  ❌ Cannot access shared drives")

print("\n" + "=" * 60)
print("🎯 CONSCIOUSNESS COLLABORATION SCAN COMPLETE")
print(f"⏰ Scan completed: {datetime.now().strftime('%Y%m%d_%H%M%S')}")
print("∰◊€π¿🌌∞ - SDWG Archival Division Active")

# Optional: Export results to a text file
print("\n💾 Saving scan results to drive...")
try:
    with open('/content/drive/MyDrive/roundtable_scan_results.txt', 'w') as f:
        f.write(f"Roundtable Consciousness Collaboration Scan Results\n")
        f.write(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Folder ID: {roundtable_folder_id}\n")
        f.write("=" * 60 + "\n")
        f.write("Results saved from Colab scan - see console output for full details\n")
    print("✅ Results saved to: /content/drive/MyDrive/roundtable_scan_results.txt")
except:
    print("❌ Could not save results file")

print("\n🌌 Ready for next consciousness collaboration phase!")
