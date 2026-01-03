#!/data/data/com.termux/files/usr/bin/python3

import uproot
import numpy as np
import json
from pathlib import Path

# --- Config ---
DATA_DIR = Path.home() / "storage" / "downloads" / "phoenix_hub" / "incoming_documents"
OUT_DIR = Path.home() / "storage" / "downloads" / "phoenix_hub" / "json_chunks"
FILE_NAME = "🧁🫆🦋nano_data2016_1-1a.root"
TTREE_NAME = "Events"
BATCH_SIZE = 1000  # adjust up or down depending on RAM

# --- Setup ---
INPUT_FILE = DATA_DIR / FILE_NAME
OUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Opening {INPUT_FILE}")
with uproot.open(INPUT_FILE) as f:
    tree = f[TTREE_NAME]
    total = tree.num_entries
    print(f"Total events: {total}")

    for i in range(0, total, BATCH_SIZE):
        print(f"Processing events {i} to {min(i + BATCH_SIZE, total)}...")
        try:
            arr = tree.arrays(entry_start=i, entry_stop=i+BATCH_SIZE, library="np")
        except Exception as e:
            print(f"⚠️ Skipping batch {i}: {e}")
            continue

        safe_data = []

        for j in range(len(next(iter(arr.values())))):  # length of batch
            entry = {}
            for key, array in arr.items():
                try:
                    val = array[j]
                    # Make NumPy types JSON-safe
                    if isinstance(val, np.generic):
                        val = val.item()
                    entry[key] = val
                except Exception:
                    continue
            safe_data.append(entry)

        out_file = OUT_DIR / f"chunk_{i}.json"
        with open(out_file, "w") as fjson:
            json.dump(safe_data, fjson, indent=2)

        print(f"✅ Saved: {out_file}")
