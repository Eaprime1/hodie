#!/usr/bin/env python3
import os
import json
from datetime import datetime

print("🐦‍🔥 Simple Phoenix Test")
print("Current directory:", os.getcwd())
print("Python working:", "YES")

# Check directories
base_dir = "../"
print("\nDirectories found:")
for item in os.listdir(base_dir):
    print(f"  - {item}")

# Look for PDFs
pdf_active = "../processing_active"
if os.path.exists(pdf_active):
    pdfs = [f for f in os.listdir(pdf_active) if f.endswith('.pdf')]
    print(f"\nPDFs in processing_active: {len(pdfs)}")
    for pdf in pdfs[:3]:  # Show first 3
        print(f"  - {pdf}")
else:
    print("processing_active directory not found")

print("\n✅ Python test complete!")
