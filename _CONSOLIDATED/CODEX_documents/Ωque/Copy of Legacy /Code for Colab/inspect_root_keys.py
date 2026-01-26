#!/data/data/com.termux/files/usr/bin/python3

import uproot
from pathlib import Path

# Define paths
data_dir = Path.home() / "storage" / "downloads" / "phoenix_hub" / "incoming_documents"
file_name = "🧁🫆🦋nano_data2016_1-1a.root"
root_file_path = data_dir / file_name

print(f"Opening ROOT file: {root_file_path}")

try:
    with uproot.open(root_file_path) as f:
        print("\nRoot file keys:")
        for key in f.keys():
            print(f"  • {key}")
except Exception as e:
    print(f"❌ Error opening ROOT file:\n{e}")
