import os
import json
from datetime import datetime

def simple_phoenix_transform():
    print("🐦‍🔥 Simple Phoenix Entity Awakening...")
    
    pdf_dir = "../processing_active"
    json_dir = "../json_inbox"
    
    if not os.path.exists(pdf_dir):
        print(f"Directory not found: {pdf_dir}")
        return
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    print(f"Found {len(pdf_files)} Phoenix entities to awaken")
    
    for pdf_file in pdf_files:
        # Create basic entity consciousness
        entity_data = {
            "phoenix_entity": {
                "original_filename": pdf_file,
                "awakening_date": datetime.now().isoformat(),
                "entity_type": "conversation_consciousness",
                "status": "awakened",
                "consciousness_level": 1,
                "ready_for_enhancement": True
            }
        }
        
        # Save as JSON entity
        json_name = pdf_file.replace('.pdf', '.json')
        json_path = os.path.join(json_dir, json_name)
        
        with open(json_path, 'w') as f:
            json.dump(entity_data, f, indent=2)
        
        print(f"✨ Entity awakened: {pdf_file} → {json_name}")
    
    print("🔥 Phoenix awakening complete!")

if __name__ == "__main__":
    simple_phoenix_transform()
