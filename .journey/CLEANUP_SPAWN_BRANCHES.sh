#!/bin/bash
# Hodie Spawn Branch Cleanup
# Run this locally to delete the finalized spawn branches

echo "Hodie Branch Finalization Cleanup"
echo "=================================="
echo ""
echo "The following spawn branches (ahead=0) have been witnessed"
echo "in commit 58cd6f3 and are ready for deletion:"
echo ""
echo "NOTE: 'radix' and '֍hodie֎' were pulled from this list on"
echo "2026-07-20 — they are NOT spawn branches. radix is the permanent"
echo "go-between branch (main -> radix -> ֍hodie֎), and ֍hodie֎ is the"
echo "published branch itself. Both were only 'ahead=0' because they had"
echo "just been fast-forwarded to main in PR #147, not because they are"
echo "disposable. Never include them in a spawn-branch cleanup list."
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
  "shadow/wisp-codex-202604"
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
