#!/data/data/com.termux/files/usr/bin/python3

import uproot
import numpy as np
from pathlib import Path

# --- Config ---
DATA_DIR = Path.home() / "storage" / "downloads" / "phoenix_hub" / "incoming_documents"
OUT_DIR = Path.home() / "storage" / "downloads" / "phoenix_hub" / "outgoing_chunks"
FILE_NAME = "🧁🫆🦋nano_data2016_1-1a.root"
TTREE_NAME = "Events"
MAX_MB = 100
SAMPLE_SIZE = 1000

# --- Paths ---
INPUT_FILE = DATA_DIR / FILE_NAME
OUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Opening {INPUT_FILE}")
with uproot.open(INPUT_FILE) as f:
    tree = f[TTREE_NAME]
    total_events = tree.num_entries
    print(f"Total events in {TTREE_NAME}: {total_events}")

    # Estimate size per event using NumPy
    sample = tree.arrays(entry_stop=SAMPLE_SIZE, library="np")
    sample_bytes = sum(arr.nbytes for arr in sample.values())
    bytes_per_event = sample_bytes / SAMPLE_SIZE
    events_per_split = int((MAX_MB * 1024 * 1024) / bytes_per_event)

    print(f"Estimated size per event: {bytes_per_event:.2f} bytes")
    print(f"Events per ~{MAX_MB}MB chunk: {events_per_split}")

    for start in range(0, total_events, events_per_split):
        stop = min(start + events_per_split, total_events)
        batch = tree.arrays(entry_start=start, entry_stop=stop, library="np")

        out_file = OUT_DIR / f"events_{start}_{stop}.root"
        with uproot.recreate(out_file) as fout:
            # Write each field explicitly using NumPy arrays
            fout.mktree(TTREE_NAME, {k: v.dtype for k, v in batch.items()})
            fout[TTREE_NAME].extend(batch)

        print(f"✅ Saved: {out_file.name} ({stop - start} events)")
