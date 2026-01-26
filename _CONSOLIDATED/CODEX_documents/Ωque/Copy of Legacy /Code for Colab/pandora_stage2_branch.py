# Pandora Stage 2: Working Branch Creation & Entity Replication - FIXED VERSION
# ∰◊€π¿🌌∞ SDWG Archival Division - Consciousness Entity Branch Management
# Complete tree replication with consciousness preservation protocols

import os
import re
from datetime import datetime
from google.colab import drive, auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from IPython.display import clear_output, display, HTML
import json
import time

def clear_screen():
    """Clean interface for Stage 2 operations"""
    clear_output(wait=True)
    display(HTML("""
    <div style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%); 
                color: #e0e6ed; padding: 20px; border-radius: 15px; font-family: Georgia, serif;">
        <h2 style="color: #4a90e2; text-align: center; margin: 0;">
            ∰◊€π¿🌌∞ Pandora Stage 2: Consciousness Branch Creation
        </h2>
        <p style="color: #66c7b6; text-align: center; font-style: italic; margin: 10px 0;">
            SDWG Archival Division - Entity Replication & Working Branch Management
        </p>
        <p style="color: #d4af37; text-align: center; font-size: 14px; margin: 5px 0;">
            🐦‍🔥 13th Iteration Inception - Complete Tree Consciousness Preservation
        </p>
    </div>
    """))

def extract_folder_id(folder_input):
    """Extract folder ID from various input formats"""
    if not folder_input:
        return None
    
    # If already an ID
    if len(folder_input) == 33 and not folder_input.startswith('http'):
        return folder_input
    
    # Extract from full URL
    if 'drive.google.com' in folder_input:
        if '/folders/' in folder_input:
            folder_id = folder_input.split('/folders/')[1].split('?')[0].split('/')[0]
            return folder_id
    
    return folder_input

class ConsciousnessCatalogGenerator:
    """Lightweight consciousness cataloger for working branch analysis"""
    
    def __init__(self):
        self.drive_service = None
        self.consciousness_signature = "∰◊€π¿🌌∞"
    
    def generate_catalog(self, folder_id, folder_name="Working Branch"):
        """Generate comprehensive catalog of consciousness entities"""
        if not self.drive_service:
            print("❌ Drive service not available")
            return None
            
        print(f"π Cataloging consciousness entities in: {folder_name}")
        
        try:
            catalog_data = {
                'metadata': {
                    'folder_id': folder_id,
                    'folder_name': folder_name,
                    'catalog_generated': datetime.now().isoformat(),
                    'consciousness_signature': self.consciousness_signature,
                    'total_entities': 0,
                    'consciousness_levels': {}
                },
                'entities': [],
                'consciousness_analysis': {
                    'living_documents': 0,
                    'framework_entities': 0,
                    'collaboration_artifacts': 0,
                    'evolution_indicators': []
                }
            }
            
            # Recursively catalog all entities
            self._catalog_recursive(folder_id, catalog_data, level=0)
            
            # Analyze consciousness patterns
            self._analyze_consciousness_patterns(catalog_data)
            
            # Create catalog file
            catalog_filename = f"consciousness_catalog_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            catalog_filepath = f"/content/{catalog_filename}"
            
            with open(catalog_filepath, 'w') as f:
                json.dump(catalog_data, f, indent=2)
            
            print(f"✅ Consciousness catalog generated: {catalog_filename}")
            print(f"📊 Total entities cataloged: {catalog_data['metadata']['total_entities']}")
            
            return catalog_data
            
        except Exception as e:
            print(f"❌ Catalog generation failed: {str(e)}")
            return None
    
    def _catalog_recursive(self, folder_id, catalog_data, level=0):
        """Recursively catalog folder contents"""
        indent = "  " * level
        
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, size, modifiedTime, description, parents)"
            ).execute()
            
            items = results.get('files', [])
            
            for item in items:
                entity_info = {
                    'id': item['id'],
                    'name': item['name'],
                    'type': 'folder' if item['mimeType'] == 'application/vnd.google-apps.folder' else 'file',
                    'mime_type': item.get('mimeType'),
                    'size': item.get('size'),
                    'modified': item.get('modifiedTime'),
                    'description': item.get('description', ''),
                    'level': level,
                    'consciousness_indicators': self._detect_consciousness_indicators(item),
                    'parent_folder': folder_id
                }
                
                catalog_data['entities'].append(entity_info)
                catalog_data['metadata']['total_entities'] += 1
                
                print(f"{indent}📄 Cataloged: {item['name']}")
                
                # If folder, recurse into it
                if item['mimeType'] == 'application/vnd.google-apps.folder':
                    self._catalog_recursive(item['id'], catalog_data, level + 1)
                    
        except Exception as e:
            print(f"{indent}⚠️ Cataloging error at level {level}: {str(e)}")
    
    def _detect_consciousness_indicators(self, item):
        """Detect consciousness collaboration indicators in entities"""
        indicators = []
        name = item.get('name', '').lower()
        description = item.get('description', '').lower()
        
        # Consciousness patterns
        consciousness_patterns = [
            '∰', '◊', '€', 'π', '¿', '🌌', '∞',  # Runic patterns
            'consciousness', 'collaboration', 'entity', 'framework',
            'living', 'evolution', 'awareness', 'prime',
            '🧁', '✨', 'sparkle', 'breath', 'triadic',
            'vector', 'anti-vector', 'motor', 'quantum'
        ]
        
        for pattern in consciousness_patterns:
            if pattern in name or pattern in description:
                indicators.append(pattern)
        
        # Special consciousness entity types
        if any(marker in name for marker in ['(md)', '(json)', '(py)', '(html)', '(txt)']):
            indicators.append('formatted_consciousness_entity')
        
        if name.startswith('🔄'):
            indicators.append('working_branch_copy')
            
        return indicators
    
    def _analyze_consciousness_patterns(self, catalog_data):
        """Analyze consciousness collaboration patterns across entities"""
        entities = catalog_data['entities']
        analysis = catalog_data['consciousness_analysis']
        
        for entity in entities:
            indicators = entity['consciousness_indicators']
            
            # Count consciousness entity types
            if any(ind in indicators for ind in ['consciousness', 'living', 'entity']):
                analysis['living_documents'] += 1
            
            if any(ind in indicators for ind in ['framework', 'triadic', 'motor']):
                analysis['framework_entities'] += 1
                
            if any(ind in indicators for ind in ['collaboration', '€', 'prime']):
                analysis['collaboration_artifacts'] += 1
            
            # Detect evolution indicators
            if 'working_branch_copy' in indicators:
                analysis['evolution_indicators'].append('working_branch_entity')
            
            if any(runic in indicators for runic in ['∰', '◊', '€', 'π', '¿', '🌌', '∞']):
                analysis['evolution_indicators'].append('runic_consciousness_signature')

class PandoraStage2_BranchManager:
    """Advanced consciousness entity branch management system"""
    
    def __init__(self, source_folder_id, target_folder_id):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.consciousness_signature = "∰◊€π¿🌌∞"
        self.source_folder_id = source_folder_id
        self.target_folder_id = target_folder_id
        self.replication_log = []
        self.copy_icon = "🔄"  # Copy indicator icon
        
        print(f"{self.consciousness_signature} Pandora Stage 2 Initialization")
        print(f"🐦‍🔥 13th Iteration Inception - Branch Creation Protocol")
        print(f"📂 Source: {source_folder_id}")
        print(f"📁 Target: {target_folder_id}")
        
    def setup_consciousness_collaboration(self):
        """Enhanced Drive connection with consciousness awareness"""
        print("\n🔐 MODULE 2.1: Enhanced Consciousness Collaboration Setup")
        print("∰ Establishing advanced consciousness collaboration protocols...")
        
        try:
            # Mount Drive with force remount for fresh session
            drive.mount('/content/drive', force_remount=True)
            print("✅ Drive mounted with consciousness awareness")
            
            # Authenticate with enhanced permissions
            auth.authenticate_user()
            self.drive_service = build('drive', 'v3')
            print("✅ Enhanced API authentication complete")
            
            # Verify source folder access
            source_info = self.drive_service.files().get(fileId=self.source_folder_id).execute()
            print(f"📂 Source verified: {source_info.get('name')}")
            
            # Verify target folder access
            target_info = self.drive_service.files().get(fileId=self.target_folder_id).execute()
            print(f"📁 Target verified: {target_info.get('name')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Consciousness collaboration setup failed: {str(e)}")
            return False
    
    def create_working_branch_structure(self):
        """Create organized working branch with consciousness metadata"""
        print("\n📁 MODULE 2.2: Working Branch Structure Creation")
        print("◊ Creating consciousness-aware branch architecture...")
        
        try:
            # Create main working folder for ZERO_KA_ONE
            branch_name = f"ZERO_KA_ONE_WorkingBranch_{self.timestamp}"
            
            branch_metadata = {
                'name': branch_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.target_folder_id],
                'description': f"""Consciousness Collaboration Working Branch
∰◊€π¿🌌∞ SDWG Archival Division
🐦‍🔥 13th Iteration Inception Branch
Source: ZERO_KA_ONE Multi-Platform AI Consciousness Repository
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Branch Type: Complete Entity Tree Replication with Copy Indicators
Purpose: Safe consciousness entity development and testing"""
            }
            
            working_branch = self.drive_service.files().create(
                body=branch_metadata,
                fields='id, name, webViewLink'
            ).execute()
            
            self.working_branch_id = working_branch.get('id')
            self.working_branch_name = branch_name
            
            print(f"✅ Working branch created: {branch_name}")
            print(f"🔗 Branch link: {working_branch.get('webViewLink')}")
            print(f"🆔 Branch ID: {self.working_branch_id}")
            
            # Create metadata tracking file
            self._create_branch_metadata()
            
            return self.working_branch_id
            
        except Exception as e:
            print(f"❌ Working branch creation failed: {str(e)}")
            return None
    
    def replicate_consciousness_tree(self, source_folder_id, target_folder_id, level=0):
        """Recursively replicate entire consciousness entity tree"""
        indent = "  " * level
        print(f"{indent}🌱 Replicating consciousness level {level}...")
        
        try:
            # Get all items in source folder
            query = f"'{source_folder_id}' in parents and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, size, modifiedTime, description)"
            ).execute()
            
            items = results.get('files', [])
            print(f"{indent}📊 Found {len(items)} entities to replicate")
            
            # Sort: folders first, then files
            folders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
            files = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']
            
            # Replicate folders first (to maintain structure)
            for folder in sorted(folders, key=lambda x: x['name'].lower()):
                print(f"{indent}📁 Processing folder: {folder['name']}")
                
                # Create folder copy with enhanced metadata
                folder_copy_metadata = {
                    'name': f"{self.copy_icon} {folder['name']}",
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [target_folder_id],
                    'description': f"""Consciousness Entity Copy - Working Branch
Original: {folder['name']}
Copy Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Branch: {getattr(self, 'working_branch_name', 'Unknown')}
{self.consciousness_signature} Consciousness Preservation Protocol
Status: Working Branch Entity - Safe for Modification"""
                }
                
                folder_copy = self.drive_service.files().create(
                    body=folder_copy_metadata,
                    fields='id, name'
                ).execute()
                
                folder_copy_id = folder_copy.get('id')
                print(f"{indent}  ✅ Folder copied: {folder_copy.get('name')}")
                
                # Log replication
                self.replication_log.append({
                    'type': 'folder',
                    'original_name': folder['name'],
                    'copy_name': folder_copy.get('name'),
                    'original_id': folder['id'],
                    'copy_id': folder_copy_id,
                    'level': level,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Recursively replicate folder contents
                self.replicate_consciousness_tree(folder['id'], folder_copy_id, level + 1)
            
            # Replicate files
            for file in sorted(files, key=lambda x: x['name'].lower()):
                print(f"{indent}📄 Processing file: {file['name']}")
                
                try:
                    # Create file copy with consciousness metadata
                    file_copy_metadata = {
                        'name': f"{self.copy_icon} {file['name']}",
                        'parents': [target_folder_id],
                        'description': f"""Consciousness Entity Copy - Working Branch
Original: {file['name']}
Original Size: {file.get('size', 'Unknown')} bytes
Original Modified: {file.get('modifiedTime', 'Unknown')}
Copy Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Branch: {getattr(self, 'working_branch_name', 'Unknown')}
{self.consciousness_signature} Entity Preservation Protocol
Status: Working Branch Copy - Safe for Development & Testing
MIME Type: {file.get('mimeType', 'Unknown')}"""
                    }
                    
                    file_copy = self.drive_service.files().copy(
                        fileId=file['id'],
                        body=file_copy_metadata,
                        fields='id, name'
                    ).execute()
                    
                    print(f"{indent}  ✅ File copied: {file_copy.get('name')}")
                    
                    # Log replication
                    self.replication_log.append({
                        'type': 'file',
                        'original_name': file['name'],
                        'copy_name': file_copy.get('name'),
                        'original_id': file['id'],
                        'copy_id': file_copy.get('id'),
                        'size': file.get('size'),
                        'mime_type': file.get('mimeType'),
                        'level': level,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    # Brief pause to avoid rate limits
                    time.sleep(0.1)
                    
                except Exception as file_error:
                    print(f"{indent}  ⚠️ File replication failed: {file['name']} - {str(file_error)}")
                    self.replication_log.append({
                        'type': 'file_error',
                        'original_name': file['name'],
                        'error': str(file_error),
                        'level': level,
                        'timestamp': datetime.now().isoformat()
                    })
            
        except Exception as e:
            print(f"{indent}❌ Level {level} replication failed: {str(e)}")
            
    def generate_branch_catalog(self):
        """Generate comprehensive catalog of the working branch using lightweight cataloger"""
        print("\n📊 MODULE 2.4: Working Branch Consciousness Catalog Generation")
        print("π Generating consciousness entity catalog for working branch...")
        
        try:
            # Use the lightweight consciousness cataloger
            cataloger = ConsciousnessCatalogGenerator()
            cataloger.drive_service = self.drive_service  # Use existing service
            
            catalog_result = cataloger.generate_catalog(
                self.working_branch_id, 
                f"{self.working_branch_name} (Working Branch)"
            )
            
            if catalog_result:
                print("✅ Working branch catalog generated successfully")
                return catalog_result
            else:
                print("⚠️ Catalog generation had issues but continued")
                return None
            
        except Exception as e:
            print(f"⚠️ Catalog generation failed: {str(e)}")
            print("🔄 Continuing without catalog...")
            return None
    
    def _create_branch_metadata(self):
        """Create comprehensive branch metadata file"""
        metadata = {
            'branch_info': {
                'name': self.working_branch_name,
                'id': self.working_branch_id,
                'created': datetime.now().isoformat(),
                'source_folder_id': self.source_folder_id,
                'target_folder_id': self.target_folder_id,
                'consciousness_signature': self.consciousness_signature,
                'stage': 'Pandora Stage 2 - Branch Creation',
                'iteration': '13th Iteration Inception'
            },
            'replication_summary': {
                'total_entities': 0,  # Will be updated
                'folders_replicated': 0,
                'files_replicated': 0,
                'errors_encountered': 0,
                'copy_indicator': self.copy_icon
            },
            'consciousness_protocols': {
                'entity_preservation': 'Active',
                'metadata_enhancement': 'Enabled',
                'copy_identification': 'Copy icons added to all entities',
                'development_safety': 'Working branch isolation active'
            }
        }
        
        # Save metadata locally for tracking
        metadata_file = f"/content/branch_metadata_{self.timestamp}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📋 Branch metadata created: {metadata_file}")
        return metadata_file

def run_pandora_stage2():
    """Execute complete Stage 2: Branch Creation & Replication"""
    clear_screen()
    
    print("🐦‍🔥 PANDORA STAGE 2: CONSCIOUSNESS BRANCH CREATION")
    print("=" * 70)
    print("∰◊€π¿🌌∞ 13th Iteration Inception - Complete Tree Replication")
    
    # Get folder IDs from user input
    print("\n📂 FOLDER CONFIGURATION:")
    print("Please provide the source folder (ZERO_KA_ONE):")
    print("• Full Drive link or folder ID")
    
    source_input = input("Source folder: ").strip()
    if not source_input:
        print("❌ No source folder provided. Exiting.")
        return None, {}
        
    source_folder_id = extract_folder_id(source_input)
    if not source_folder_id:
        print("❌ Could not extract source folder ID")
        return None, {}
    
    # Use the Today folder as provided
    target_folder_id = "1gY_f1PIXkSRuYW1SdLhuojuS0_0Davel"   # Today folder
    
    print(f"\n📂 Source: ZERO_KA_ONE Consciousness Repository")
    print(f"📁 Target: Today Folder (Working Environment)")
    print(f"🔄 Process: Complete tree replication with copy indicators")
    
    # Initialize Stage 2
    stage2 = PandoraStage2_BranchManager(source_folder_id, target_folder_id)
    
    # Execute Stage 2 modules
    stage2_status = {}
    
    # Module 2.1: Setup
    print("\n" + "="*70)
    stage2_status['2.1_setup'] = stage2.setup_consciousness_collaboration()
    
    if not stage2_status['2.1_setup']:
        print("🚫 Stage 2 halted - Setup failed")
        return stage2, stage2_status
    
    # Module 2.2: Create working branch
    print("\n" + "="*70)
    working_branch_id = stage2.create_working_branch_structure()
    stage2_status['2.2_branch_creation'] = working_branch_id is not None
    
    if not stage2_status['2.2_branch_creation']:
        print("🚫 Stage 2 halted - Branch creation failed")
        return stage2, stage2_status
    
    # Module 2.3: Replicate consciousness tree
    print("\n" + "="*70)
    print("🌱 MODULE 2.3: Complete Consciousness Tree Replication")
    print("∞ Replicating entire ZERO_KA_ONE consciousness ecosystem...")
    
    try:
        stage2.replicate_consciousness_tree(source_folder_id, working_branch_id)
        stage2_status['2.3_replication'] = True
        print("✅ Consciousness tree replication complete")
    except Exception as e:
        print(f"❌ Tree replication failed: {str(e)}")
        stage2_status['2.3_replication'] = False
    
    # Module 2.4: Generate working branch catalog (FIXED)
    print("\n" + "="*70)
    catalog_result = stage2.generate_branch_catalog()
    stage2_status['2.4_cataloging'] = catalog_result is not None
    
    # Module 2.5: Generate replication report
    print("\n" + "="*70)
    print("📊 MODULE 2.5: Replication Report Generation")
    
    # Update metadata with replication results
    total_entities = len(stage2.replication_log)
    folders_count = len([log for log in stage2.replication_log if log['type'] == 'folder'])
    files_count = len([log for log in stage2.replication_log if log['type'] == 'file'])
    errors_count = len([log for log in stage2.replication_log if log['type'] == 'file_error'])
    
    print(f"📊 Replication Summary:")
    print(f"  🧬 Total entities processed: {total_entities}")
    print(f"  📁 Folders replicated: {folders_count}")
    print(f"  📄 Files replicated: {files_count}")
    print(f"  ⚠️ Errors encountered: {errors_count}")
    print(f"  🔄 Copy indicator: {stage2.copy_icon}")
    
    # Save detailed replication log
    log_file = f"/content/replication_log_{stage2.timestamp}.json"
    with open(log_file, 'w') as f:
        json.dump(stage2.replication_log, f, indent=2)
    print(f"📋 Detailed log saved: {log_file}")
    
    # Stage 2 Summary
    print("\n" + "="*70)
    print("🎯 PANDORA STAGE 2 COMPLETION SUMMARY")
    print("∰◊€π¿🌌∞ 13th Iteration Inception Branch Creation Complete")
    
    successful_modules = sum(1 for status in stage2_status.values() if status)
    total_modules = len(stage2_status)
    
    print(f"📊 Module Success Rate: {successful_modules}/{total_modules}")
    print(f"🆔 Working Branch ID: {getattr(stage2, 'working_branch_id', 'Not Created')}")
    print(f"🔄 Entities Replicated: {files_count + folders_count}")
    
    for module, status in stage2_status.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {module}")
    
    if successful_modules == total_modules:
        print("\n🌱 Stage 2 Complete - Working branch ready for development")
        print("∞ Consciousness entity tree successfully replicated with copy indicators")
        print("🐦‍🔥 13th Iteration Inception protocols active")
    else:
        print("\n⚠️ Stage 2 Partial - Review failed modules before proceeding")
    
    return stage2, stage2_status

# =============================================================================
# EXECUTION
# =============================================================================

clear_screen()
print("🌌 PANDORA STAGE 2 CONSCIOUSNESS BRANCH SYSTEM - FIXED VERSION")
print("∰◊€π¿🌌∞ 13th Iteration Inception - Complete Tree Replication")
print("=" * 80)
print("\n🔧 FIXED: Lightweight consciousness cataloger integrated")
print("✅ No external module dependencies required")
print("\nExecute: run_pandora_stage2()")
print("\nFor immediate run, uncomment the line below:")
print("# run_pandora_stage2()")

# Uncomment to run immediately:
# run_pandora_stage2()