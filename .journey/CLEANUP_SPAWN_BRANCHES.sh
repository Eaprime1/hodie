#!/bin/bash
# Hodie Spawn Branch Cleanup — RETIRED 2026-08-21
#
# This script used to hard-delete "finalized" spawn branches from origin.
# hodie adopted custos's Mobius-Closed branch policy on 2026-08-21: branches
# are never deleted. Once a branch's content has fully landed elsewhere
# (usually main), it gets labeled "Mobius-Closed" in branch-tracker/branches.md
# instead — the branch stays, the work it carried is done.
#
# See: BRANCH_STRATEGY.md ("Branch Retention Policy") and
#      branch-tracker/branches.md (the living inventory that replaces this
#      script's one-off delete list).
#
# This file is kept, not deleted, for path continuity — same reasoning the
# policy itself applies to branches.

echo "CLEANUP_SPAWN_BRANCHES.sh is retired — hodie no longer deletes branches."
echo "See BRANCH_STRATEGY.md (Branch Retention Policy) and branch-tracker/branches.md."
exit 0
