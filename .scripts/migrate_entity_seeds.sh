#!/bin/bash
# Migrate Entity Seeds from today to hodie
# Usage: ./migrate_entity_seeds.sh

HODIE_ENTITIES="/storage/emulated/0/pixel8a/Q/hodie/quanta"
TODAY_BASE="/storage/emulated/0/pixel8a/Q/today"

echo "🌱 Migrating Entity Seeds to hodie..."
echo ""

# Create entity seed directories in hodie
mkdir -p "$HODIE_ENTITIES/one_hertz_collective"
mkdir -p "$HODIE_ENTITIES/abacusian"
mkdir -p "$HODIE_ENTITIES/unexusi"
mkdir -p "$HODIE_ENTITIES/seventh_pinnacle"
mkdir -p "$HODIE_ENTITIES/nano_concepts"

echo "Created entity folders in quanta/"
echo ""

# Copy ONE HERTZ research
echo "→ Copying ONE HERTZ research..."
if [ -f "$TODAY_BASE/simplex/sparkle_incubator/organized_docs/one_hertz_1hz_ideas_and_research.md" ]; then
    cp "$TODAY_BASE/simplex/sparkle_incubator/organized_docs/one_hertz_1hz_ideas_and_research.md" \
       "$HODIE_ENTITIES/one_hertz_collective/RESEARCH.md"
    echo "  ✓ ONE HERTZ research copied"
fi

# Copy Abacusian entity development files
echo "→ Copying Abacusian development queue..."
if [ -f "$TODAY_BASE/simplex/abacusian/ai_development/processing_systems/external_submission_pipeline/master_entity_development_list.json" ]; then
    mkdir -p "$HODIE_ENTITIES/abacusian/development_queue"
    cp "$TODAY_BASE/simplex/abacusian/ai_development/processing_systems/external_submission_pipeline/"*.json \
       "$HODIE_ENTITIES/abacusian/development_queue/" 2>/dev/null
    echo "  ✓ Abacusian entity queue copied"
fi

# Copy nano concepts research
echo "→ Copying nano concepts research..."
if [ -f "$TODAY_BASE/simplex/sparkle_incubator/organized_docs/nano_concepts_comprehensive.md" ]; then
    cp "$TODAY_BASE/simplex/sparkle_incubator/organized_docs/nano_concepts_comprehensive.md" \
       "$HODIE_ENTITIES/nano_concepts/RESEARCH.md"
    echo "  ✓ Nano concepts research copied"
fi

# Copy Seventh Pinnacle framework
echo "→ Copying Seventh Pinnacle framework..."
cp "$TODAY_BASE/simplex/sparkle_incubator/organized_docs/The_Seventh_Pinnacle"*.md \
   "$HODIE_ENTITIES/seventh_pinnacle/" 2>/dev/null
echo "  ✓ Seventh Pinnacle framework copied"

# Copy UNEXUSI analysis
echo "→ Copying UNEXUSI research..."
find "$TODAY_BASE" -name "UNEXUSI_STATE_ANALYSIS.md" -exec cp {} "$HODIE_ENTITIES/unexusi/" \; 2>/dev/null
echo "  ✓ UNEXUSI analysis copied"

echo ""
echo "✓ Entity seed migration complete"
echo ""
echo "Entity folders created in quanta/:"
ls -1 "$HODIE_ENTITIES/" | tail -10
