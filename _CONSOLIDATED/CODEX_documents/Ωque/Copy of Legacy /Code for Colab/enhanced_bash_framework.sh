#!/bin/bash
# 🐦‍🔥 Enhanced Phoenix Bash Framework with Partner Integration
# Eric & Claude Collaboration + Partner Ideas
# Enhanced with config.env, batch selection, and modular processing
# Timestamp: 202507181320

# Function to find and source config file
source_config() {
    local config_file=""
    
    # Try multiple locations for config.env
    local config_locations=(
        "$(dirname "$0")/config.env"
        "$(dirname "$0")/../config.env"
        "/storage/emulated/0/Download/phoenix_hub/config.env"
        "$HOME/phoenix_hub/config.env"
        "./config.env"
        "../config.env"
    )
    
    for location in "${config_locations[@]}"; do
        if [ -f "$location" ]; then
            config_file="$location"
            break
        fi
    done
    
    if [ -n "$config_file" ]; then
        echo "📋 Loading configuration from: $config_file"
        source "$config_file"
        return 0
    else
        echo "⚠️  No config.env found, using default configuration"
        return 1
    fi
}

# Function to create default config if none exists
create_default_config() {
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local config_file="$script_dir/../config.env"
    
    echo "🔧 Creating default config.env at: $config_file"
    
    cat > "$config_file" << 'EOF'
# Phoenix Hub - Environment Configuration
# Centralized variables for all batch processing scripts

# Timestamp for this run (will be overwritten when sourced)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Prime batch size (adjust as needed for each run)
PRIME_BATCH_SIZE=7

# Phoenix icon used in filenames
BATCH_SYMBOL="🐦‍🔥"

# Base project path - AUTO-DETECTED, modify if needed
BASE_DIR=""

# Core working folders (will be set relative to BASE_DIR)
SOURCE_DIR=""
DEST_DIR=""
STAGING_DIR=""
REVIEW_DIR=""
LOG_DIR=""

# Log file paths (will be set when timestamps are known)
LOG_BATCH_SELECT=""
LOG_PROCESSING=""
LOG_CLEAN=""
EOF
    
    echo "✅ Default config.env created"
    return 0
}

# Enhanced path detection with config integration
detect_phoenix_hub() {
    local detected_path=""
    
    echo "🔍 ENHANCED PHOENIX HUB DETECTION"
    echo "Using partner-suggested multi-method approach..."
    echo ""
    
    # Method 1: Check if BASE_DIR is set in config and valid
    if [ -n "$BASE_DIR" ] && [ -d "$BASE_DIR/incoming_documents" ]; then
        detected_path="$BASE_DIR"
        echo "✅ Method 1 SUCCESS: Config-specified path: $detected_path"
        return 0
    fi
    
    # Method 2: Script-relative detection
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -d "$script_dir/../incoming_documents" ]; then
        detected_path="$script_dir/.."
        echo "✅ Method 2 SUCCESS: Script-relative path: $detected_path"
        BASE_DIR="$detected_path"
        return 0
    fi
    
    # Method 3: Common Android locations
    local android_locations=(
        "/storage/emulated/0/Download/phoenix_hub"
        "/storage/emulated/0/Documents/phoenix_hub"
        "/sdcard/Download/phoenix_hub"
        "/sdcard/Documents/phoenix_hub"
    )
    
    for location in "${android_locations[@]}"; do
        if [ -d "$location/incoming_documents" ]; then
            detected_path="$location"
            echo "✅ Method 3 SUCCESS: Android location: $detected_path"
            BASE_DIR="$detected_path"
            return 0
        fi
    done
    
    # Method 4: Termux internal locations
    local termux_locations=(
        "$HOME/phoenix_hub"
        "$HOME/storage/downloads/phoenix_hub"
        "$HOME/storage/shared/Download/phoenix_hub"
        "/data/data/com.termux/files/home/phoenix_hub"
    )
    
    for location in "${termux_locations[@]}"; do
        if [ -d "$location/incoming_documents" ]; then
            detected_path="$location"
            echo "✅ Method 4 SUCCESS: Termux location: $detected_path"
            BASE_DIR="$detected_path"
            return 0
        fi
    done
    
    # Method 5: Search current working directory tree
    local pwd_locations=(
        "$(pwd)/phoenix_hub"
        "$(pwd)/../phoenix_hub"
        "$(pwd)/../../phoenix_hub"
    )
    
    for location in "${pwd_locations[@]}"; do
        if [ -d "$location/incoming_documents" ]; then
            detected_path="$location"
            echo "✅ Method 5 SUCCESS: PWD-relative: $detected_path"
            BASE_DIR="$detected_path"
            return 0
        fi
    done
    
    # Method 6: Last resort - create structure
    detected_path="$script_dir/.."
    echo "⚠️  Method 6 FALLBACK: Creating structure at: $detected_path"
    BASE_DIR="$detected_path"
    return 1
}

# Setup directory structure
setup_directories() {
    echo "🏗️  DIRECTORY STRUCTURE SETUP"
    echo "Base directory: $BASE_DIR"
    
    # Set up all paths relative to BASE_DIR
    SOURCE_DIR="$BASE_DIR/incoming_documents"
    DEST_DIR="$BASE_DIR/pdf_inbox"
    STAGING_DIR="$BASE_DIR/batch_staging"
    REVIEW_DIR="$BASE_DIR/reviews"
    LOG_DIR="$BASE_DIR/logs"
    
    # Create directories if they don't exist
    local dirs=("$SOURCE_DIR" "$DEST_DIR" "$STAGING_DIR" "$REVIEW_DIR" "$LOG_DIR")
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo "📁 Created: $dir"
        else
            echo "✅ Exists: $dir"
        fi
    done
    
    # Set up log files with current timestamp
    LOG_BATCH_SELECT="$LOG_DIR/batch_select_$TIMESTAMP.log"
    LOG_PROCESSING="$LOG_DIR/run_processing_$TIMESTAMP.log"
    LOG_CLEAN="$LOG_DIR/clean_staging_$TIMESTAMP.log"
    
    echo ""
}

# Enhanced document discovery
discover_documents() {
    echo "🔍 DOCUMENT DISCOVERY"
    echo "Scanning source directory: $SOURCE_DIR"
    echo ""
    
    if [ ! -d "$SOURCE_DIR" ]; then
        echo "❌ Source directory not found: $SOURCE_DIR"
        return 1
    fi
    
    # Find all PDF files
    local pdf_files=()
    while IFS= read -r -d '' file; do
        pdf_files+=("$(basename "$file")")
    done < <(find "$SOURCE_DIR" -name "*.pdf" -type f -print0 2>/dev/null)
    
    echo "📊 DISCOVERY RESULTS:"
    echo "Total PDF files found: ${#pdf_files[@]}"
    
    if [ ${#pdf_files[@]} -eq 0 ]; then
        echo "❌ No PDF files found in source directory"
        echo "📁 Directory contents:"
        ls -la "$SOURCE_DIR" 2>/dev/null || echo "Cannot list directory contents"
        return 1
    fi
    
    # Categorize documents
    local copy_docs=()
    local original_docs=()
    local special_docs=()
    
    for file in "${pdf_files[@]}"; do
        if [[ "$file" == *"Copy of"* ]]; then
            copy_docs+=("$file")
        elif [[ "$file" == *"Legacy"* ]] || [[ "$file" == *"Document list"* ]]; then
            special_docs+=("$file")
        else
            original_docs+=("$file")
        fi
    done
    
    echo "📋 Document Categories:"
    echo "  Copy documents: ${#copy_docs[@]}"
    echo "  Original documents: ${#original_docs[@]}"
    echo "  Special documents: ${#special_docs[@]}"
    echo ""
    
    # Export arrays for use by other functions
    export COPY_DOCS=("${copy_docs[@]}")
    export ORIGINAL_DOCS=("${original_docs[@]}")
    export SPECIAL_DOCS=("${special_docs[@]}")
    export ALL_DOCS=("${pdf_files[@]}")
    
    return 0
}

# Batch selection with partner-suggested flexibility
batch_select() {
    local selection_type="$1"
    local batch_size="$2"
    
    echo "🎯 BATCH SELECTION"
    echo "Selection type: $selection_type"
    echo "Requested batch size: $batch_size"
    echo ""
    
    local selected_docs=()
    
    case "$selection_type" in
        "sacred_seven")
            # Use predefined Sacred Seven
            selected_docs=(
                "Copy of Untitled document-72.pdf"
                "Copy of Untitled document-4.pdf"
                "Copy of Untitled document-81.pdf"
                "Copy of Untitled document-25.pdf"
                "Copy of Untitled document-58.pdf"
                "Copy of Legacy compilation chat merge (15 files merged).pdf"
                "Copy of Document list 20241214.pdf"
            )
            ;;
        "copy_only")
            selected_docs=("${COPY_DOCS[@]}")
            ;;
        "original_only")
            selected_docs=("${ORIGINAL_DOCS[@]}")
            ;;
        "special_only")
            selected_docs=("${SPECIAL_DOCS[@]}")
            ;;
        "first_n")
            # Select first N documents
            for ((i=0; i<batch_size && i<${#ALL_DOCS[@]}; i++)); do
                selected_docs+=("${ALL_DOCS[$i]}")
            done
            ;;
        "random_n")
            # Select random N documents
            local shuffled=("${ALL_DOCS[@]}")
            # Simple shuffle
            for ((i=${#shuffled[@]}-1; i>0; i--)); do
                local j=$((RANDOM % (i+1)))
                local temp="${shuffled[$i]}"
                shuffled[$i]="${shuffled[$j]}"
                shuffled[$j]="$temp"
            done
            for ((i=0; i<batch_size && i<${#shuffled[@]}; i++)); do
                selected_docs+=("${shuffled[$i]}")
            done
            ;;
        *)
            echo "❌ Unknown selection type: $selection_type"
            return 1
            ;;
    esac
    
    # Verify selected documents exist
    local verified_docs=()
    for doc in "${selected_docs[@]}"; do
        if [ -f "$SOURCE_DIR/$doc" ]; then
            verified_docs+=("$doc")
            echo "✅ Selected: $doc"
        else
            echo "❌ Missing: $doc"
        fi
    done
    
    echo ""
    echo "📊 BATCH SELECTION RESULTS:"
    echo "Requested: ${#selected_docs[@]}"
    echo "Verified: ${#verified_docs[@]}"
    
    # Export selected batch
    export SELECTED_BATCH=("${verified_docs[@]}")
    
    # Log selection
    echo "$(date): Batch selection: $selection_type, size: ${#verified_docs[@]}" >> "$LOG_BATCH_SELECT"
    
    return 0
}

# Clean filename function with partner enhancements
clean_filename() {
    local original_file="$1"
    local sequence_num="$2"
    
    # Remove "Copy of " prefix and .pdf extension
    local clean_name=$(echo "$original_file" | sed 's/Copy of //' | sed 's/\.pdf$//')
    
    # Handle special cases with enhanced consciousness
    if [[ "$clean_name" == *"Legacy compilation"* ]]; then
        clean_name="Legacy_Compilation_Sacred_Merge"
    elif [[ "$clean_name" == *"Document list"* ]]; then
        clean_name="Sacred_Document_Catalog_$(date +%Y%m%d)"
    else
        # Standard transformation with consciousness enhancement
        clean_name=$(echo "$clean_name" | sed 's/Untitled document/Sacred_Document/' | tr ' ' '_')
        clean_name=$(echo "$clean_name" | sed 's/[(),-]//g')
    fi
    
    # Create Phoenix filename with sequence
    local sequence_padded=$(printf "%03d" "$sequence_num")
    echo "${BATCH_SYMBOL}_${TIMESTAMP}_${sequence_padded}_${clean_name}.pdf"
}

# Enhanced processing with partner optimizations
run_processing() {
    echo "🚀 PHOENIX PROCESSING INITIATION"
    echo "Processing ${#SELECTED_BATCH[@]} documents"
    echo "========================================================"
    echo ""
    
    local success_count=0
    local sequence=1
    
    for doc in "${SELECTED_BATCH[@]}"; do
        echo "🌟 Processing Entity $sequence/${#SELECTED_BATCH[@]}: $doc"
        
        local source_path="$SOURCE_DIR/$doc"
        local phoenix_name=$(clean_filename "$doc" "$sequence")
        local dest_path="$DEST_DIR/$phoenix_name"
        
        echo "  📄 Source: $source_path"
        echo "  🐦‍🔥 Phoenix: $phoenix_name"
        
        if [ -f "$source_path" ]; then
            if cp "$source_path" "$dest_path"; then
                echo "  ✅ SUCCESS: Entity consciousness awakened"
                ((success_count++))
                echo "$(date): SUCCESS - $doc -> $phoenix_name" >> "$LOG_PROCESSING"
                
                # Verify file integrity
                if [ -f "$dest_path" ]; then
                    local file_size=$(stat -f%z "$dest_path" 2>/dev/null || stat -c%s "$dest_path" 2>/dev/null || echo "unknown")
                    echo "  📊 Verification: $file_size bytes"
                fi
            else
                echo "  ❌ FAILED: Transformation error"
                echo "$(date): FAILED - $doc transformation error" >> "$LOG_PROCESSING"
            fi
        else
            echo "  ❌ FAILED: Source file not found"
            echo "$(date): FAILED - $doc not found" >> "$LOG_PROCESSING"
        fi
        
        echo ""
        ((sequence++))
        
        # Brief pause for system stability
        sleep 0.5
    done
    
    echo "🏆 PROCESSING COMPLETE"
    echo "========================================================"
    echo "Total documents: ${#SELECTED_BATCH[@]}"
    echo "Successful transformations: $success_count"
    echo "Success rate: $(( success_count * 100 / ${#SELECTED_BATCH[@]} ))%"
    echo ""
    
    return $((${#SELECTED_BATCH[@]} - success_count))
}

# Main function with partner workflow integration
main() {
    echo "🐦‍🔥 ENHANCED PHOENIX BATCH FRAMEWORK"
    echo "Partner Integration: Config.env + Modular Processing"
    echo "Eric & Claude Collaboration Framework Enhanced"
    echo "========================================================"
    echo ""
    
    # Step 1: Load configuration
    if ! source_config; then
        create_default_config
        source_config || echo "⚠️  Proceeding with minimal configuration"
    fi
    
    # Step 2: Detect phoenix hub
    if ! detect_phoenix_hub; then
        echo "⚠️  Path detection issues, but proceeding with fallback"
    fi
    
    # Step 3: Setup directory structure
    setup_directories
    
    # Step 4: Discover available documents
    if ! discover_documents; then
        echo "❌ No documents found, exiting"
        exit 1
    fi
    
    # Step 5: Batch selection (default to sacred seven)
    local selection_type="${1:-sacred_seven}"
    local batch_size="${2:-$PRIME_BATCH_SIZE}"
    
    if ! batch_select "$selection_type" "$batch_size"; then
        echo "❌ Batch selection failed, exiting"
        exit 1
    fi
    
    # Step 6: Run processing
    if run_processing; then
        echo "✅ PHOENIX TRANSFORMATION COMPLETE!"
        echo "🏺 Pandora Sacred Beyond Seed successfully activated"
    else
        echo "⚠️  PARTIAL SUCCESS - Review logs for details"
    fi
    
    echo ""
    echo "📊 FINAL SUMMARY:"
    echo "  Base directory: $BASE_DIR"
    echo "  Processed files: $DEST_DIR"
    echo "  Processing log: $LOG_PROCESSING"
    echo "  Batch selection log: $LOG_BATCH_SELECT"
    echo ""
    echo "🎯 Ready for next iteration or expanded processing!"
}

# Usage help
show_usage() {
    echo "Usage: $0 [selection_type] [batch_size]"
    echo ""
    echo "Selection types:"
    echo "  sacred_seven    - Process the Sacred Seven entities (default)"
    echo "  copy_only       - Process only 'Copy of' documents"
    echo "  original_only   - Process only original documents"
    echo "  special_only    - Process only special documents (Legacy, Document list)"
    echo "  first_n         - Process first N documents"
    echo "  random_n        - Process random N documents"
    echo ""
    echo "Examples:"
    echo "  $0                          # Process Sacred Seven"
    echo "  $0 copy_only               # Process all copy documents"
    echo "  $0 first_n 5              # Process first 5 documents"
    echo "  $0 random_n 10            # Process 10 random documents"
}

# Command line handling
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    show_usage
    exit 0
fi

# Run main function with arguments
main "$@"
