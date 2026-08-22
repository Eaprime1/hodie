# BRANCH TRACKER

Living inventory of every branch in `eaprime1/hodie`, per the Mobius-Closed
branch retention policy adopted 2026-08-21 (see `BRANCH_STRATEGY.md`).
Branches are never deleted — this doc is where "finished" gets recorded
instead of deletion.

**Baseline for ahead/behind below**: `origin/main` at `373dcd9` (2026-08-21,
before this session's cleanup commits).

---

## Structural Branches

Permanent by design — never candidates for closure, regardless of ahead/behind.

| Branch | Role | Notes |
|---|---|---|
| `main` | Hub default | The branch everything else is measured against. |
| `radix` | Permanent go-between (`main → radix → ֍hodie֎`) | 0 ahead, 49 behind as of this pass — was 0-ahead only because it had just been fast-forwarded to main in PR #147 (2026-07-20), not because it's disposable. Carried over this same warning from the retired cleanup script. |
| `֍hodie֎` | Published branch | Same as `radix` above — 0 ahead, 49 behind, structural not disposable. |

---

## Branches Needing Review — real unmerged work, not closure candidates

| Branch | Ahead / Behind | Latest commit | Notes |
|---|---|---|---|
| `claude/nifty-franklin-fxwp3r` | 30 ahead, 8 behind | `856a7b8` (2026-07-24) "fix: move comment.body checks from job if: to env: gate steps (Codacy HIGH)" | Largest unmerged branch by far — 30 unique commits. Needs a real look before any disposition; not touched by this pass. |
| `copilot/cleanup-prs-with-issues` | 2 ahead, 25 behind | `232216b` (2026-07-29) "quepad: refresh witness scan state [skip ci]" | 2 unique commits — check what they carry before deciding. |
| `feature/crawler-pixel8-adaptation` | 1 ahead, 43 behind | `9832017` (2026-07-28) "Add comprehensive Windows and cross-platform development setup documentation (#160)" | 1 unique commit not yet on main. |

---

## Mobius-Closed Branches

*Content fully absorbed into `main` (0 ahead as of this pass, re-verified
2026-08-21 — not assumed from the retired script's stale 2026-07-20 witness
list). Retained per policy, not deleted.*

| Branch | Behind | Latest commit | Notes |
|---|---|---|---|
| `claude/branch-cleanup-and-witness-fix` | 25 | `a5db042` (2026-07-20) "quepad: refresh witness scan state [skip ci]" | |
| `claude/fix-codacy-issues` | 4 | `70cff92` (2026-07-28) "quepad: refresh witness scan state [skip ci]" | |
| `claude/hodie-system-audit-0ydnam` | 43 | `7adef26` (2026-07-20) "Add finalization journey closing note" | Was on the retired script's delete-list. |
| `claude/session-save-point-20260720` | 21 | `2ec45a6` (2026-07-20) "quepad: refresh witness scan state [skip ci]" | |
| `claude/triadic-entanglement-doc` | 15 | `4ee41f2` (2026-07-21) "quepad: refresh witness scan state [skip ci]" | |
| `claude/upgrade-hodie-repo-XEFEy` | 210 | `017b551` (2026-04-24) "Merge pull request #98 from Eaprime1/copilot/ci-unblock-footer-witness" | Was on the retired script's delete-list. |
| `copilot/add-icon-to-footer` | 31 | `ce75e95` (2026-07-19) "Merge branch 'main' into copilot/add-icon-to-footer" | Previously flagged in `.journey/BRANCHES_WITH_WORK.md` (2026-07-20) as "7 commits ahead, should be merged" — re-verified 2026-08-21 and its content has since fully landed in main (0 ahead now). That doc is stale; this table supersedes it. |
| `copilot/fix-code-issues` | 85 | `a03bed1` (2026-04-27) "Merge branch 'main' into copilot/fix-code-issues" | Was on the retired script's delete-list. |
| `copilot/improve-setup-scripts-security` | 410 | `de45d92` (2026-04-13) "Merge branch 'main' into copilot/improve-setup-scripts-security" | Was on the retired script's delete-list. |
| `shadow/wisp-codex-202604` | 121 | `5500e30` (2026-04-25) "Merge pull request #129 from Eaprime1/copilot/repair-and-improve-functionality" | Was on the retired script's delete-list. |

**Name mismatch flagged, not resolved**: the retired script's delete-list
also named `copilot/add-pisces-icon-footer`, which does not match any branch
that currently exists on the remote (closest match by content/date is
`copilot/add-icon-to-footer`, listed above as Mobius-Closed). Possibly a
typo in the original script, or a branch that was renamed/already gone
before this pass. Not chasing further — noting it here so it isn't silently
lost.

---

## Superseded

- `.journey/CLEANUP_SPAWN_BRANCHES.sh` — retired 2026-08-21, no longer deletes branches. Kept as a pointer to this doc.
- `.journey/BRANCHES_WITH_WORK.md` — dated 2026-07-20, stale (see `copilot/add-icon-to-footer` note above). This doc replaces it as the living source of truth.
