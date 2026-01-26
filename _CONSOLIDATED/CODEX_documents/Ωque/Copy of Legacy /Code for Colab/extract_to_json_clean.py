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
BATCH_SIZE = 1000

# --- Setup ---
INPUT_FILE = DATA_DIR / FILE_NAME
OUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Opening {INPUT_FILE}")
with uproot.open(str(INPUT_FILE)) as f:
    tree = f[TTREE_NAME]
    total = tree.num_entries
    print(f"Total entries in '{TTREE_NAME}': {total}")

    for start in range(0, total, BATCH_SIZE):
        stop = min(start + BATCH_SIZE, total)
        try:
            arr = tree.arrays(entry_start=start, entry_stop=stop, library="np")
        except Exception as e:
            print(f"⚠️ Skipping batch {start}-{stop}: {e}")
            continue

        events = []
        n_events = len(next(iter(arr.values())))
        for i in range(n_events):
            event = {}
            for key, array in arr.items():
                try:
                    val = array[i]
                    if isinstance(val, np.generic):
                        val = val.item()
                    if isinstance(val, (int, float)):
                        event[key] = val
                except Exception:
                    continue
            events.append(event)

        out_file = OUT_DIR / f"chunk_{start}.json"
        with open(out_file, "w") as fjson:
            json.dump(events, fjson, indent=2)

        print(f"✅ Saved: {out_file.name}")

