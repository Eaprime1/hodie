import uproot

# Adjust path if needed
cd ~/storage/download/phoenix_hub/incoming_documents/
file_path = "~/storage/download/phoenix_hub/incoming_documents/🧁🫆🦋nano_data2016_1-1a.rot"

with uproot.open(file_path) as f:
    print(f.keys())  # Show top-level keys in the ROOT file
