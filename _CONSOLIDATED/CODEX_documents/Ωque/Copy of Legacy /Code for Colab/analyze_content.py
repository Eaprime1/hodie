#!/usr/bin/env python3
import os
import re

def analyze_phoenix_files():
    active_dir = "../processing_active"
    
    print("🔍 Analyzing Phoenix conversations for content enhancement...")
    
    pdf_files = [f for f in os.listdir(active_dir) if f.endswith('.pdf')]
    
    for filename in sorted(pdf_files):
        # Extract number from Phoenix filename
        number_match = re.search(r'🐦‍🔥💬🏺-(\d+)-', filename)
        number = number_match.group(1) if number_match else "unknown"
        
        file_path = os.path.join(active_dir, filename)
        file_size = os.path.getsize(file_path)
        
        print(f"📄 File {number}: {file_size:,} bytes")
        print(f"   Current: {filename}")
        print(f"   Needs: Title analysis + Chinese symbol assignment")
        print()
    
    print("🎯 Next steps:")
    print("1. Extract text content from PDFs")
    print("2. Analyze conversation themes") 
    print("3. Generate meaningful titles")
    print("4. Assign appropriate Chinese wisdom symbols")
    print("5. Create final Phoenix names")

if __name__ == "__main__":
    analyze_phoenix_files()
