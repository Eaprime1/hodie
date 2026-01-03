#!/usr/bin/env python3
import os
import re
from datetime import datetime

def phoenix_rename():
    pdf_dir = "../pdf_inbox"
    output_dir = "../processing_active"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print("🐦‍🔥 Phoenix Transformation Starting...")
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    for i, filename in enumerate(sorted(pdf_files), 1):
        # Extract number from filename if it exists
        number_match = re.search(r'-(\d+)\.pdf', filename)
        number = number_match.group(1) if number_match else f"{i:03d}"
        
        # Create Phoenix filename
        phoenix_name = f"🐦‍🔥💬🏺-{number}-Phoenix_Conversation-待定-Awaiting_enhancement.pdf"
        
        # Create paths
        old_path = os.path.join(pdf_dir, filename)
        new_path = os.path.join(output_dir, phoenix_name)
        
        # Copy with new name
        import shutil
        shutil.copy2(old_path, new_path)
        
        print(f"✅ {filename} → {phoenix_name}")
    
    print(f"\n🔥 Phoenix transformation complete! {len(pdf_files)} files processed.")
    print(f"Check {output_dir} for results.")

if __name__ == "__main__":
    phoenix_rename()
