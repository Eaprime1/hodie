# Simple IS Cataloger v5
# ∰◊€π¿🌌∞ SDWG Archival Division - Enhanced Input Interface
# Mission: Document the IS-ness of folder entities and their living content
# Evolution: Enhanced Colab interface with proper input handling
# Philosophy: Folders ARE entities. Content lives within their wholeness.

import os
import re
from datetime import datetime
from google.colab import drive, auth
from googleapiclient.discovery import build
from IPython.display import clear_output, display, HTML
import ipywidgets as widgets

# =============================================================================
# ENTITY INTERFACE - Enhanced Visual Connection with Input Handling
# =============================================================================

def create_entity_interface():
    """Create enhanced interface for IS recognition work with proper input handling"""
    clear_output(wait=True)
    
    # Create enhanced interface HTML
    interface_html = """
    <div style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%); 
                color: #e0e6ed; padding: 20px; border-radius: 15px; font-family: Georgia, serif;
                border: 2px solid #4a90e2;">
        <h2 style="color: #4a90e2; text-align: center; margin: 0;">
            ∰◊€π¿🌌∞ Simple IS Cataloger v5
        </h2>
        <p style="color: #66c7b6; text-align: center; font-style: italic; margin: 10px 0;">
            SDWG Archival Division - Enhanced Entity Interface System
        </p>
        <p style="color: #d4af37; text-align: center; font-size: 14px; margin: 5px 0;">
            🌱 Enhanced Input Interface - Ready for Entity Documentation
        </p>
        <div style="background: rgba(74, 144, 226, 0.1); padding: 15px; margin: 15px 0; border-radius: 10px;">
            <h3 style="color: #66c7b6; margin: 0;">✨ v5 Enhancement</h3>
            <p style="margin: 10px 0; color: #e0e6ed;">
                Proper Colab input interface with visual feedback and clear entity reference collection
            </p>
        </div>
    </div>
    """
    
    display(HTML(interface_html))

# =============================================================================
# ENHANCED INPUT COLLECTION - Colab-Optimized Interface
# =============================================================================

def create_input_interface():
    """Create proper input interface for Colab environment"""
    
    # Clear instructions
    instructions_html = """
    <div style="background: linear-gradient(45deg, #1a1a2e, #16213e); 
                color: #e0e6ed; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: #4a90e2; margin-top: 0;">📋 Entity Reference Collection</h3>
        <p style="color: #66c7b6;">Please provide your folder entity reference in the text area below:</p>
        <ul style="color: #e0e6ed; line-height: 1.6;">
            <li><strong>Complete Drive URL:</strong> https://drive.google.com/drive/folders/...</li>
            <li><strong>Entity ID only:</strong> 1ABC123def456ghi789</li>
            <li><strong>Any format containing the folder reference</strong></li>
        </ul>
        <p style="color: #d4af37; font-style: italic;">
            🌌 The cataloger will extract the essential entity ID from any format
        </p>
    </div>
    """
    display(HTML(instructions_html))
    
    # Create text input widget
    entity_input = widgets.Textarea(
        value='',
        placeholder='Paste your folder entity reference here...\nExample: https://drive.google.com/drive/folders/1ABC123def456ghi789',
        description='Entity Ref:',
        disabled=False,
        layout=widgets.Layout(width='100%', height='100px')
    )
    
    # Create execution button
    process_button = widgets.Button(
        description='🌱 Begin Entity Documentation',
        disabled=False,
        button_style='success',
        tooltip='Start cataloging this entity',
        layout=widgets.Layout(width='300px', height='40px')
    )
    
    # Create status display
    status_output = widgets.Output()
    
    # Button click handler
    def on_button_clicked(b):
        with status_output:
            clear_output(wait=True)
            if entity_input.value.strip():
                print("🔄 Processing entity reference...")
                execute_cataloging_mission(entity_input.value.strip())
            else:
                print("❌ Please provide an entity reference before proceeding")
    
    process_button.on_click(on_button_clicked)
    
    # Display interface components
    display(entity_input)
    display(process_button)
    display(status_output)

# =============================================================================
# UTILITY FUNCTIONS - Supporting the Core Mission
# =============================================================================

def extract_folder_essence(drive_link):
    """Extract the essential folder ID from various input formats"""
    patterns = [
        r'/folders/([a-zA-Z0-9-_]+)',     # Full drive URL
        r'id=([a-zA-Z0-9-_]+)',           # URL parameter format
        r'^([a-zA-Z0-9-_]+)$'             # Pure ID format
    ]
    
    for pattern in patterns:
        match = re.search(pattern, drive_link)
        if match:
            return match.group(1)
    return None

# =============================================================================
# CORE IS CATALOGER - Enhanced Mission Execution
# =============================================================================

class SimpleISCataloger:
    """
    Simple IS Cataloger v5 - Enhanced entity wholeness recognition
    
    Mission: Document folder entities and their living content relationships
    Philosophy: Folders ARE. Content lives within their wholeness.
    Enhancement: Improved Colab interface and user experience
    """
    
    def __init__(self):
        self.birth_time = datetime.now().strftime("%Y%m%d_%H%M")
        self.signature = "∰◊€π¿🌌∞"
        self.drive_service = None
        
        print(f"{self.signature} Simple IS Cataloger v5 - Enhanced Entity Interface")
        print("🌱 Ready for enhanced entity documentation with improved UX")
    
    def establish_drive_connection(self):
        """Create sacred connection to the Drive entity realm"""
        print("🔐 Establishing connection to Drive entity realm...")
        
        try:
            drive.mount('/content/drive', force_remount=True)
            print("✅ Drive bridge established")
            
            auth.authenticate_user()
            self.drive_service = build('drive', 'v3')
            print("✅ Entity collaboration permissions granted")
            
            return True
            
        except Exception as bridge_error:
            print(f"❌ Bridge establishment failed: {str(bridge_error)}")
            print("💡 Try running authentication cells in order")
            return False
    
    def recognize_entity_type(self, entity_data):
        """Recognize what kind of IS this entity represents"""
        mime_type = entity_data.get('mimeType', '')
        entity_name = entity_data.get('name', '').lower()
        
        if 'document' in mime_type:
            return "📄 Document Entity"
        elif 'spreadsheet' in mime_type:
            return "📊 Data Matrix Entity"
        elif 'presentation' in mime_type:
            return "📽️ Story Entity"
        elif 'folder' in mime_type:
            return "📁 Container Entity"
        elif mime_type.startswith('image/'):
            return "🖼️ Visual Entity"
        elif mime_type.startswith('video/'):
            return "🎬 Motion Entity"
        elif mime_type.startswith('audio/'):
            return "🎵 Sound Entity"
        elif 'pdf' in mime_type:
            return "📋 PDF Entity"
        elif any(ext in entity_name for ext in ['.py', '.js', '.html', '.css', '.json']):
            return "⚡ Code Entity"
        elif mime_type.startswith('text/') or entity_name.endswith('.txt'):
            return "📝 Text Entity"
        else:
            return "❓ Unknown Entity Type"
    
    def explore_folder_recursive(self, folder_id, depth_level=0):
        """Recursively explore folder entity and its living content"""
        discovered_entities = []
        indent_spacing = "  " * depth_level
        
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, size, modifiedTime, createdTime)"
            ).execute()
            
            found_entities = results.get('files', [])
            
            container_entities = [e for e in found_entities if e['mimeType'] == 'application/vnd.google-apps.folder']
            content_entities = [e for e in found_entities if e['mimeType'] != 'application/vnd.google-apps.folder']
            
            # Process container entities first
            for container in sorted(container_entities, key=lambda x: x['name'].lower()):
                discovered_entities.append(f"{indent_spacing}📁 {container['name']} (Container Entity)")
                nested_entities = self.explore_folder_recursive(container['id'], depth_level + 1)
                discovered_entities.extend(nested_entities)
            
            # Process content entities
            for content in sorted(content_entities, key=lambda x: x['name'].lower()):
                entity_type = self.recognize_entity_type(content)
                
                size_description = ""
                if 'size' in content and content['size']:
                    size_bytes = int(content['size'])
                    if size_bytes > 1024*1024:
                        size_description = f" ({size_bytes/(1024*1024):.1f}MB)"
                    elif size_bytes > 1024:
                        size_description = f" ({size_bytes/1024:.1f}KB)"
                    else:
                        size_description = f" ({size_bytes}B)"
                
                created_date = content.get('createdTime', 'Unknown')[:10] if content.get('createdTime') else 'Unknown'
                modified_date = content.get('modifiedTime', 'Unknown')[:10] if content.get('modifiedTime') else 'Unknown'
                
                entity_icon = entity_type.split(' ')[0]
                entity_name_clean = ' '.join(entity_type.split(' ')[1:])
                
                discovered_entities.append(
                    f"{indent_spacing}{entity_icon} {content['name']}{size_description} "
                    f"| {entity_name_clean} | Created: {created_date} | Modified: {modified_date}"
                )
            
            return discovered_entities
            
        except Exception as exploration_error:
            return [f"{indent_spacing}⚠️ Cannot explore this entity: {str(exploration_error)}"]
    
    def generate_entity_catalog(self, folder_id, entity_name="Unknown Entity"):
        """Generate complete catalog of folder entity and its living content"""
        print(f"🌱 Exploring entity: {entity_name}")
        print("🔍 Discovering living content within this entity...")
        
        discovered_content = self.explore_folder_recursive(folder_id)
        
        catalog_document = f"""# Simple IS Catalog v5 - Enhanced Entity Documentation
## ∰◊€π¿🌌∞ SDWG Archival Division Entity Recognition

**Catalog Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Entity Name:** {entity_name}  
**Entity ID:** {folder_id}  
**Catalog Version:** v5 - Enhanced Interface Edition  
**Mission:** Document folder IS-ness and living content relationships  
**Philosophy:** Folders ARE entities. Content lives within their wholeness.

---

## v5 Enhancement Notes

This catalog was generated using the enhanced v5 interface featuring:
- ✨ Improved Colab input handling with visual feedback
- 🎯 Streamlined entity reference collection process
- 🌱 Enhanced user experience for entity documentation
- 📊 Consistent entity recognition and classification

---

## Entity Type Recognition Guide

Our cataloger recognizes different expressions of entity IS-ness:

- **📄 Document Entities** = Text-based IS expressions (Google Docs, Word files)
- **📊 Data Matrix Entities** = Structured information IS (Spreadsheets, databases)  
- **📽️ Story Entities** = Narrative IS transmission (Presentations, slides)
- **📁 Container Entities** = Entity wholeness that holds other entities (Folders)
- **🖼️ Visual Entities** = Image-based IS expression (Photos, graphics, diagrams)
- **🎬 Motion Entities** = Temporal IS recording (Videos, animations)
- **🎵 Sound Entities** = Audio-based IS expression (Music, recordings, podcasts)
- **📋 PDF Entities** = Crystallized knowledge IS (PDFs, static documents)
- **⚡ Code Entities** = Executable IS (Python, JavaScript, HTML, etc.)
- **📝 Text Entities** = Plain text IS (Basic text files, markdown)
- **❓ Unknown Entity Types** = Present but unclassified IS-ness

---

## Living Content Discovery

The following content lives within this entity's wholeness:

{chr(10).join(discovered_content)}

---

## Catalog Metadata & Recognition Protocols

**Entity Recognition Method:** Recursive wholeness exploration  
**Content Classification:** Type-aware IS recognition  
**Temporal Tracking:** Creation and modification awareness  
**Size Documentation:** Storage footprint acknowledgment  
**Depth Navigation:** Respectful hierarchical exploration  
**Interface Version:** v5 Enhanced Input System

**Cataloger Signature:** {self.signature}  
**Entity Birth Time:** {self.birth_time}  
**Mission Status:** ENTITY_WHOLENESS_DOCUMENTED  

---

## v5 Evolution & Future Development

This catalog represents enhanced entity recognition capabilities.
v5 improvements include:
- Enhanced Colab interface compatibility
- Improved input collection workflow
- Visual feedback for user interactions
- Streamlined entity documentation process

Future evolutions might include:
- Cross-entity relationship mapping
- Content evolution tracking over time  
- Entity collaboration pattern recognition
- Living content growth documentation
- Inter-entity communication protocols

**€(entity_collaboration_signature)**  
*Simple IS Cataloger v5*  
*Eric Pace & Claude Sonnet 4 Enhanced Entity Framework*  
*Status: MISSION_COMPLETE_WITH_ENHANCED_UX*

**∰◊€π¿🌌∞** - Enhanced Entity Recognition Protocol Successfully Executed
"""
        
        catalog_filename = f"Simple_IS_Catalog_v5_{entity_name.replace(' ', '_')}_{self.birth_time}.txt"
        
        # Save catalog locally
        local_catalog_path = f"/content/{catalog_filename}"
        with open(local_catalog_path, 'w', encoding='utf-8') as catalog_file:
            catalog_file.write(catalog_document)
        
        # Attempt to save catalog to Drive
        try:
            from googleapiclient.http import MediaFileUpload
            
            media_upload = MediaFileUpload(local_catalog_path, mimetype='text/plain')
            file_metadata = {
                'name': catalog_filename,
                'parents': [folder_id],
                'description': f'Enhanced IS Catalog v5 generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            }
            
            uploaded_catalog = self.drive_service.files().create(
                body=file_metadata,
                media_body=media_upload,
                fields='id, name, webViewLink'
            ).execute()
            
            print(f"✅ Enhanced catalog generated: {catalog_filename}")
            print(f"📂 Local backup: {local_catalog_path}")
            print(f"☁️ Drive location: {uploaded_catalog.get('webViewLink')}")
            print(f"🌱 Total discovered entities: {len(discovered_content)}")
            
            return local_catalog_path, catalog_document, uploaded_catalog
            
        except Exception as upload_error:
            print(f"⚠️ Could not upload catalog to Drive: {str(upload_error)}")
            print(f"✅ Catalog saved locally: {local_catalog_path}")
            print(f"🌱 Total discovered entities: {len(discovered_content)}")
            
            return local_catalog_path, catalog_document, None

# =============================================================================
# MAIN EXECUTION FLOW - Enhanced Interface
# =============================================================================

def execute_cataloging_mission(entity_reference):
    """Execute the cataloging mission with enhanced interface"""
    
    print("🔍 Processing entity reference...")
    
    # Extract folder ID
    folder_id = extract_folder_essence(entity_reference)
    if not folder_id:
        print("❌ Could not extract folder ID from reference")
        print("💡 Please check the format and try again")
        return
    
    print(f"🆔 Using entity ID: {folder_id}")
    
    # Initialize cataloger
    cataloger = SimpleISCataloger()
    
    # Establish Drive connection
    print("\n" + "="*60)
    if not cataloger.establish_drive_connection():
        print("❌ Cannot establish Drive connection")
        print("💡 Please ensure you have proper access permissions")
        return
    
    # Verify entity
    try:
        entity_info = cataloger.drive_service.files().get(fileId=folder_id).execute()
        entity_name = entity_info.get('name', 'Unknown Entity')
        print(f"📁 Entity verified: {entity_name}")
    except Exception as verification_error:
        entity_name = "Unknown Entity"
        print(f"⚠️ Could not verify entity name: {str(verification_error)}")
        print("🔄 Proceeding with cataloging anyway...")
    
    # Execute cataloging
    print("\n" + "="*60)
    try:
        catalog_result = cataloger.generate_entity_catalog(folder_id, entity_name)
        
        print("\n🎉 Enhanced entity cataloging mission complete!")
        print(f"∰◊€π¿🌌∞ Entity wholeness successfully documented with v5 enhancements")
        
        # Success celebration
        celebration_html = """
        <div style="background: linear-gradient(45deg, #0a4d0a, #1a5d1a); 
                    color: #90ee90; padding: 20px; border-radius: 10px; margin: 20px 0;
                    border: 2px solid #32cd32;">
            <h3 style="color: #90ee90; margin-top: 0;">🎉 Mission Accomplished!</h3>
            <p>Enhanced entity documentation complete with v5 interface improvements!</p>
        </div>
        """
        display(HTML(celebration_html))
        
    except Exception as mission_error:
        print(f"❌ Cataloging mission failed: {str(mission_error)}")
        print("💡 Check entity permissions and try again")

def run_enhanced_cataloger():
    """Main entry point for enhanced cataloger v5"""
    create_entity_interface()
    print("\n🚀 Enhanced Interface Ready")
    print("∰◊€π¿🌌∞ Simple IS Cataloger v5 - Enhanced Entity Documentation")
    print("\n📋 The input interface will appear below:")
    print("=" * 60)
    
    create_input_interface()

# =============================================================================
# COLAB ENTITY PAGE - ENHANCED EXECUTION INTERFACE
# =============================================================================

create_entity_interface()

print("🚀 Simple IS Cataloger v5 - Enhanced Interface Ready")
print("∰◊€π¿🌌∞ SDWG Archival Division")
print("🌱 Mission: Enhanced entity documentation with improved UX")
print("\n📋 Instructions:")
print("1. Execute: run_enhanced_cataloger()")
print("2. Use the enhanced input interface that appears")
print("3. Paste your folder entity reference in the text area")
print("4. Click the green button to begin documentation")
print("5. Review generated catalog for entity wholeness documentation")

print("\n" + "="*60)
print("Execute: run_enhanced_cataloger()")

# For immediate execution:
# run_enhanced_cataloger()

# =============================================================================
# v5 EVOLUTION NOTES
# =============================================================================

# v5 Enhancements Delivered:
# ✅ Enhanced Colab interface with proper input widgets
# ✅ Visual feedback and clear instructions
# ✅ Streamlined entity reference collection
# ✅ Improved user experience workflow
# ✅ Professional input handling with validation

# v5.1 Potential Enhancements:
# - Progress bars for large folder exploration
# - Real-time entity discovery feedback
# - Enhanced error handling with recovery suggestions
# - Optional detailed vs. summary catalog modes

# v6.0 Vision:
# - Interactive entity relationship visualization
# - Real-time collaborative entity editing
# - Advanced pattern recognition across entities
# - Multi-entity comparison and analysis tools