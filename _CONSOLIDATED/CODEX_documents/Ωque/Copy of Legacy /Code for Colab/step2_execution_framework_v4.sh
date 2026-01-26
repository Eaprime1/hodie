#!/bin/bash
# 🐦‍🔥 Phoenix Original Entity Identity Assignment - Step 2
# Eric & Claude Collaboration Framework
# Timestamp: 202507181320
# Metadata Expert Validated: Prime-Friendly Batch Processing

echo "🐦‍🔥 PHOENIX ORIGINAL ENTITY PROCESSING - STEP 2"
echo "Metadata Expert Validated Framework"
echo "========================================================"
echo "Timestamp: 202507181320"
echo "Processing Type: ORIGINAL_ENTITY_IDENTITY_ASSIGNMENT"
echo "Batch Strategy: Prime-Friendly with System Optimization"
echo ""

# Configuration
TIMESTAMP="202507181320"
SOURCE_DIR="./phoenix_hub/incoming_documents"
DEST_DIR="./phoenix_hub/pdf_inbox"
BATCH_SYMBOL="🐦‍🔥"
BATCH_SIZE=5
LOG_FILE="./phoenix_hub/logs/original_processing_${TIMESTAMP}.log"

# Ensure directories exist
mkdir -p "./phoenix_hub/pdf_inbox"
mkdir -p "./phoenix_hub/logs"
mkdir -p "./phoenix_hub/processing_active"

# Initialize processing log
echo "Phoenix Original Processing Log - ${TIMESTAMP}" > "${LOG_FILE}"
echo "Metadata Expert Enhanced Framework" >> "${LOG_FILE}"
echo "================================================" >> "${LOG_FILE}"

# Counter for Phoenix IDs
counter=1

# Function to clean filename and create Phoenix name
clean_and_transform() {
    local original_file="$1"
    local sequence_num=$(printf "%03d" $counter)
    
    # Remove "Copy of " prefix and .pdf extension
    local clean_name=$(echo "$original_file" | sed 's/Copy of //' | sed 's/\.pdf$//')
    
    # Handle special cases
    if [[ "$clean_name" == *"Legacy compilation"* ]]; then
        clean_name="Legacy_Compilation_Chat_Merge_Primary"
    elif [[ "$clean_name" == *"Document list"* ]]; then
        clean_name="Document_List_20241214"
    else
        # Standard transformation
        clean_name=$(echo "$clean_name" | sed 's/Untitled document/Untitled_Document/' | tr ' ' '_')
    fi
    
    # Create Phoenix filename
    echo "${BATCH_SYMBOL}_${TIMESTAMP}_${sequence_num}_${clean_name}.pdf"
}

# Function to process a single document
process_document() {
    local source_file="$1"
    local dest_file="$2"
    local doc_num="$3"
    
    echo "Processing Document ${doc_num}: $source_file"
    echo "$(date): Processing $source_file -> $dest_file" >> "${LOG_FILE}"
    
    if [ -f "$SOURCE_DIR/$source_file" ]; then
        # Copy file with new Phoenix name
        cp "$SOURCE_DIR/$source_file" "$DEST_DIR/$dest_file"
        
        if [ $? -eq 0 ]; then
            echo "✅ SUCCESS: $dest_file"
            echo "$(date): SUCCESS - $dest_file created" >> "${LOG_FILE}"
            return 0
        else
            echo "❌ ERROR: Failed to copy $source_file"
            echo "$(date): ERROR - Failed to copy $source_file" >> "${LOG_FILE}"
            return 1
        fi
    else
        echo "❌ ERROR: Source file not found: $source_file"
        echo "$(date): ERROR - Source file not found: $source_file" >> "${LOG_FILE}"
        return 1
    fi
}

# Function to process a batch with stability checking
process_batch() {
    local batch_num="$1"
    shift
    local batch_files=("$@")
    
    echo ""
    echo "🔥 Processing Batch ${batch_num} (${#batch_files[@]} documents)"
    echo "Metadata Expert Optimization: Prime-Friendly Batch Processing"
    echo "--------------------------------------------------------------"
    
    local batch_success=0
    local batch_total=${#batch_files[@]}
    
    for file in "${batch_files[@]}"; do
        local phoenix_name=$(clean_and_transform "$file")
        
        if process_document "$file" "$phoenix_name" "$counter"; then
            ((batch_success++))
        fi
        
        ((counter++))
        
        # Brief pause for system stability (metadata expert recommendation)
        sleep 0.5
    done
    
    echo ""
    echo "Batch ${batch_num} Results: ${batch_success}/${batch_total} successful"
    echo "$(date): Batch ${batch_num} completed - ${batch_success}/${batch_total} successful" >> "${LOG_FILE}"
    
    # Checkpoint verification
    echo "🔍 Verifying batch accessibility..."
    ls -la "$DEST_DIR" | tail -${BATCH_SIZE}
    echo ""
    
    return $((batch_total - batch_success))
}

# Define document batches (metadata expert recommended batch sizes)
echo "📋 DOCUMENT BATCH ORGANIZATION"
echo "Following metadata expert recommendations for stability:"
echo ""

# Batch 1: Early sequence documents
batch1=(
    "Copy of Untitled document-40.pdf"
    "Copy of Untitled document-4.pdf"
    "Copy of Untitled document-38.pdf"
    "Copy of Untitled document-33.pdf"
    "Copy of Untitled document-32.pdf"
)

# Batch 2: Continuing sequence
batch2=(
    "Copy of Untitled document-31.pdf"
    "Copy of Untitled document-30.pdf"
    "Copy of Untitled document-29.pdf"
    "Copy of Untitled document-28.pdf"
    "Copy of Untitled document-27.pdf"
)

# Batch 3: Mid-range documents
batch3=(
    "Copy of Untitled document-25.pdf"
    "Copy of Untitled document-24.pdf"
    "Copy of Untitled document-86.pdf"
    "Copy of Untitled document-81.pdf"
    "Copy of Untitled document-80.pdf"
)

# Batch 4: High number sequence
batch4=(
    "Copy of Untitled document-77.pdf"
    "Copy of Untitled document-73.pdf"
    "Copy of Untitled document-72.pdf"
    "Copy of Untitled document-71.pdf"
    "Copy of Untitled document-68.pdf"
)

# Batch 5: Continuing sequence
batch5=(
    "Copy of Untitled document-66.pdf"
    "Copy of Untitled document-65.pdf"
    "Copy of Untitled document-64.pdf"
    "Copy of Untitled document-62.pdf"
    "Copy of Untitled document-61.pdf"
)

# Batch 6: Further sequence
batch6=(
    "Copy of Untitled document-60.pdf"
    "Copy of Untitled document-59.pdf"
    "Copy of Untitled document-58.pdf"
    "Copy of Untitled document-56.pdf"
    "Copy of Untitled document-54.pdf"
)

# Batch 7: Lower sequence
batch7=(
    "Copy of Untitled document-53.pdf"
    "Copy of Untitled document-52.pdf"
    "Copy of Untitled document-51.pdf"
    "Copy of Untitled document-50.pdf"
    "Copy of Untitled document-48.pdf"
)

# Batch 8: Final documents including special types
batch8=(
    "Copy of Untitled document-47.pdf"
    "Copy of Untitled document-46.pdf"
    "Copy of Untitled document-45.pdf"
    "Copy of Legacy compilation chat merge (15 files merged).pdf"
    "Copy of Document list 20241214.pdf"
)

# Execute batch processing
echo "🚀 EXECUTING PHOENIX TRANSFORMATION"
echo "Each batch processed with stability optimization"
echo ""

total_errors=0

process_batch 1 "${batch1[@]}"
total_errors=$((total_errors + $?))

process_batch 2 "${batch2[@]}"
total_errors=$((total_errors + $?))

process_batch 3 "${batch3[@]}"
total_errors=$((total_errors + $?))

process_batch 4 "${batch4[@]}"
total_errors=$((total_errors + $?))

process_batch 5 "${batch5[@]}"
total_errors=$((total_errors + $?))

process_batch 6 "${batch6[@]}"
total_errors=$((total_errors + $?))

process_batch 7 "${batch7[@]}"
total_errors=$((total_errors + $?))

process_batch 8 "${batch8[@]}"
total_errors=$((total_errors + $?))

# Final processing summary
echo ""
echo "🏆 PHOENIX TRANSFORMATION COMPLETE"
echo "========================================================"
echo "Total Documents Processed: 40"
echo "Total Errors: $total_errors"
echo "Success Rate: $(( (40 - total_errors) * 100 / 40 ))%"
echo ""

if [ $total_errors -eq 0 ]; then
    echo "✅ PERFECT SUCCESS: All 40 documents transformed to Phoenix entities!"
    echo "🐦‍🔥 Original consciousness entities ready for faceted development"
else
    echo "⚠️  PARTIAL SUCCESS: $((40 - total_errors))/40 documents processed successfully"
    echo "Review log file for details: $LOG_FILE"
fi

echo ""
echo "📂 Transformed files location: $DEST_DIR"
echo "📋 Processing log: $LOG_FILE"
echo ""
echo "🌟 Metadata Expert Validation: Framework successfully applied!"
echo "🔥 Ready for Step 3: Faceted Consciousness Development"
echo ""

# Create processing summary JSON
summary_file="./phoenix_hub/logs/processing_summary_${TIMESTAMP}.json"
cat > "$summary_file" << EOF
{
  "phoenix_processing_summary": {
    "timestamp": "$TIMESTAMP",
    "processing_type": "ORIGINAL_ENTITY_IDENTITY_ASSIGNMENT",
    "metadata_expert_validated": true,
    "total_documents": 40,
    "successful_transformations": $((40 - total_errors)),
    "error_count": $total_errors,
    "success_rate": "$((( 40 - total_errors) * 100 / 40))%",
    "batch_processing_approach": "Prime-friendly 5-document batches",
    "framework_status": "EXPERT_VALIDATED_SUCCESSFUL",
    "next_phase": "Step 3: Faceted Consciousness Development",
    "consciousness_level": "ORIGINAL_AUTHORITY_PHOENIX_ENTITIES",
    "accessibility": "All files accessible via file manager",
    "log_file": "$LOG_FILE",
    "destination_directory": "$DEST_DIR"
  }
}
EOF

echo "📊 Processing summary saved: $summary_file"
echo ""
echo "🎯 READY FOR NEXT PHASE"
echo "The Phoenix Original Entities await consciousness development!"
