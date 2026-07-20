#!/bin/bash
# Hodie Spawn Branch Cleanup
# Run this locally to delete the finalized spawn branches

echo "Hodie Branch Finalization Cleanup"
echo "=================================="
echo ""
echo "The following spawn branches (ahead=0) have been witnessed"
echo "in commit 58cd6f3 and are ready for deletion:"
echo ""

# Spawn branches to delete
branches=(
  "claude/hodie-system-audit-0ydnam"
  "claude/upgrade-hodie-repo-XEFEy"
  "copilot/add-pisces-icon-footer"
  "copilot/cleanup-prs-with-issues"
  "copilot/fix-code-issues"
  "copilot/improve-setup-scripts-security"
  "feature/crawler-pixel8-adaptation"
  "radix"
  "shadow/wisp-codex-202604"
  "֍hodie֎"
)

echo "Ready to delete ${#branches[@]} branches."
echo ""
read -p "Proceed with deletion? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
  for branch in "${branches[@]}"; do
    echo "Deleting: $branch"
    git push origin --delete "$branch"
  done
  echo ""
  echo "✓ Cleanup complete"
else
  echo "Cleanup cancelled"
fi
