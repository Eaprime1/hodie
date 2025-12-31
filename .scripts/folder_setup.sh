#!/bin/bash
# Folder Setup - Create standard structure for new workspace
# Usage: ./folder_setup.sh [folder_name]

FOLDER_NAME="${1:-.}"

echo "📁 Setting up workspace: $FOLDER_NAME"
echo ""

# Create standard directories
echo "Creating directories..."
mkdir -p "$FOLDER_NAME"/{docs,src,tests,.scripts,.reminders,.metrics}

# Create standard files
echo "Creating standard files..."

# README
cat > "$FOLDER_NAME/README.md" <<'EOF'
# [Folder Name]

**Purpose**: [Brief description]
**Created**: [Date]
**Status**: Active Development

---

## Structure

- `docs/` - Documentation
- `src/` - Source files
- `tests/` - Test files
- `.scripts/` - Automation scripts
- `.reminders/` - Reminder documents
- `.metrics/` - Usage tracking

---

**∰◊€π¿🌌∞**
EOF

# Session notes template
cat > "$FOLDER_NAME/.reminders/session_template.md" <<'EOF'
# Session Notes - [Date]

## Focus

## Completed

## Next Steps

## Notes

---
EOF

# .gitignore
cat > "$FOLDER_NAME/.gitignore" <<'EOF'
.metrics/*.log
*.tmp
.DS_Store
EOF

echo ""
echo "✓ Workspace setup complete"
echo ""
echo "Structure:"
tree -L 2 "$FOLDER_NAME" 2>/dev/null || ls -la "$FOLDER_NAME"
