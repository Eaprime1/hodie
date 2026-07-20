# THE hodie — System Pinnacle Workshop: Status Audit

**Date**: 2026-07-19
**Session branch**: `claude/hodie-system-audit-0ydnam`
**Purpose**: Baseline snapshot of the workshop's actual operating state — what's firing, what's broken, what's stale — so future work can be measured against it. Dust-off pass #1.

---

## 1. Executive Summary

The workshop has been idling for about a month (last merge to `main` was **2026-06-19**, PR #144). During that idle stretch, two automated processes have kept firing on their own and both are unhealthy:

1. **`Sync hodie from Google Drive`** — a daily cron job — has failed **every single run for at least the last 30 days straight** (likely longer; the workflow has 99 total runs since 2026-04-13). Root cause: the backing **GCP project has been deleted**, so the Drive service-account credential is dead. This is not the bug a currently-open PR (#143) was written to fix — that PR fixes a different, secondary issue.
2. **`Hodie — Sovran Voice`** — the PR-greeter workflow — has been running with **structurally invalid YAML** since 2026-06-13/15. It has no `runs-on`, no job key under `jobs:`, and an empty script block in its first step. Every push to `main` that touches the file, and every PR going forward, gets a failing/invalid workflow status from it. Gemini already diagnosed this twice in auto-filed issues (#145, #146) that have sat untouched for 5 weeks.

Beyond those two, the rest of the repo is in reasonable shape: 13 other CI workflows are wired up (Claude review, Gemini review/triage, Pylint, Copilot, footer-witness, package build), one PR is open and stale, two issues are open and stale, and the `.eric/` continuity log has a 6-month gap (last dated session note: 2026-01-06) — consistent with the "idle, stale, needs tuning" read on the workshop right now.

---

## 2. The two processes actually "firing frequently"

### 2.1 `sync-hodie.yml` — daily, 100% failure streak

- **Schedule**: `0 12 * * *` (noon UTC daily) + manual dispatch
- **File**: `.github/workflows/sync-hodie.yml`
- **History**: 99 runs total since 2026-04-13. The most recent 30 runs (2026-06-20 → 2026-07-19) are **all failures**, one per day, no exceptions.
- **Actual error** (from today's run, job `88192705091`):
  ```
  googleapiclient.errors.HttpError: <HttpError 403 ... returned
  "Project #801196094598 has been deleted.". Details:
  "[{'message': 'Project #801196094598 has been deleted.', 'domain': 'global', 'reason': 'forbidden'}]">
  ```
  The service account backing `secrets.GDRIVE_SERVICE_ACCOUNT_KEY` belongs to a GCP project that no longer exists. Every run fails in ~1 second at the very first Drive API call (`list_folder`) — it never gets far enough to touch any file-download logic.
- **Fix required**: infrastructure-side, not code. A new GCP project + service account (or restoring the old project) is needed, with a fresh key rotated into the `GDRIVE_SERVICE_ACCOUNT_KEY` repo secret. No amount of script changes fixes a 403 "project deleted."
- **Open PR #143** ("Repair Drive sync failure...") targets a *different* bug — a Google Workspace file with an undownloadable MIME type causing a hard exit — and has been open since **2026-05-04** (2.5 months). It's a real fix for a real (secondary) bug, but merging it will not stop the daily failures, because the 403 happens before that code path is ever reached.

### 2.2 `sovran-voice.yml` — fires on every PR, structurally broken

- **Trigger**: `pull_request: [opened, ready_for_review]`
- **File**: `.github/workflows/sovran-voice.yml`
- **Problem**: the `jobs:` block has no job id and no `runs-on` — `permissions:` and `steps:` are nested directly under `jobs:`. The first step (`Post Hodie Comment`) has an empty `script:` body. A second step (`Hodie marks the day`) duplicates the "post a comment" intent but runs unconditionally, without the fork-check guard the first step has.
- **Run history**: 4 runs total. Only the very first (2026-05-31, before the file was edited into its current shape) succeeded. The next 3 pushes to the file (2026-06-13, 2026-06-15, 2026-06-20) all show `conclusion: failure`, and GitHub displays them by file path instead of workflow name — the signature of an unparseable workflow file.
- **Already diagnosed, not yet fixed**: Gemini auto-filed two issues about this — **#145** (2026-06-13) and **#146** (2026-06-15) — both proposing a dry-run test workflow and pointing at the missing `permissions`/structure. Both are still open, untouched since filing.
- **Effect on new PRs**: any PR opened against `main` right now will pick up a failing/invalid check from this workflow.

**These two are the "process firing frequently and has issues" — one is an infra/credentials problem (daily, needs a human with GCP access), the other is a code problem (per-PR, fixable in the repo).**

---

## 3. Repository pulse

- **Last commit to `main`**: `7afaaa2` — 2026-06-19, PR #144 ("Codacy fixes + Hodie sovran identity"). ~1 month of quiet before this audit.
- **Working tree**: clean on `claude/hodie-system-audit-0ydnam` (forked from `main`).
- **Open PRs**: 1 — #143 (Drive sync repair, stale 2.5 months, doesn't fix the actual current failure — see 2.1).
- **Open issues**: 2 — #145, #146 (both diagnosing the sovran-voice break, stale ~5 weeks — see 2.2).

---

## 4. CI/CD workflow inventory (15 registered)

| Workflow | Trigger | State |
|---|---|---|
| Claude Code Review | PR opened/sync/ready | active |
| Claude Code | `@claude` mention | active |
| Prima Witness Footer Check | push/PR on md/py/rst | active, `continue-on-error: true` (soft-fails, doesn't block) |
| gemini-dispatch / -invoke / -review / -triage | `@gemini-cli`, PR open | active |
| Pylint | push | active |
| Python Package (conda) | push | active |
| **Sync hodie from Google Drive** | daily cron | **active, failing daily (2.1)** |
| **Hodie — Sovran Voice** | PR opened/ready | **active, broken YAML (2.2)** |
| Copilot / Copilot cloud agent / Copilot code review | dynamic | active |
| pages-build-deployment | dynamic | active |

Everything except the two flagged above appears to be firing normally (no other workflow shows a persistent failure streak in the sampled history).

---

## 5. Prima Witness / `quepad` compliance snapshot

- `quepad/state.json` last scan: **2026-04-26** — nearly 3 months stale. The CI job that runs the scanner does **not** write results back to the repo (by design, per the workflow's own comment), so `state.json` only advances when someone commits a fresh scan.
- Of 132 known files at that last scan: **8 compliant**, **124 non-compliant** (missing the `∰ YYYYMMDDHHMMSSMS` footer witness line). The check runs in `continue-on-error: true` mode, so this isn't currently blocking anything — it's informational debt, not a gate.

---

## 6. Continuity gap

`.eric/` — the session-notes/continuity folder — has dated notes running from `session_notes_2025-12-30.md` through `session_notes_2026-01-06.md`, then nothing dated until this file. Six-plus months of session continuity wasn't logged here, even though repo activity (PRs #137–144) continued through June. Matches the "idling, stale" read — the workshop kept building but stopped narrating itself.

---

## 7. Baseline metrics (for the next audit to diff against)

| Metric | Value @ 2026-07-19 |
|---|---|
| Days since last `main` commit | ~30 |
| `sync-hodie.yml` consecutive failing runs | ≥30 (full visible history) |
| `sovran-voice.yml` consecutive failing runs | 3 of last 3 (since 2026-06-13) |
| Open PRs | 1 (#143) |
| Open issues | 2 (#145, #146) |
| Footer-witness compliance | 8/132 files (6%), scan stale since 2026-04-26 |
| Registered CI workflows | 15 |

---

## 8. Recommended next actions (unordered priority — pick what to tackle first)

1. **Rotate `GDRIVE_SERVICE_ACCOUNT_KEY`** — needs a human with GCP console access; nothing in-repo can fix a deleted project. Until this happens, `sync-hodie.yml` will keep failing daily, whether or not PR #143 merges.
2. **Fix `sovran-voice.yml`'s YAML structure** — this one's fixable directly in the repo (add a job id + `runs-on`, remove the dead empty-script step, keep the fork-guard). Can close #145/#146 once done.
3. **Decide on PR #143** — merge it anyway (it's a legitimate fix for the MIME-type bug, just not *the* daily blocker), or fold its fix into a combined sync-hodie repair once GCP creds are rotated.
4. **Refresh `quepad/state.json`** — re-run the footer-witness scanner and commit the result so the compliance number reflects current reality, not April.
5. **Resume `.eric/` session notes** — even short entries — to close the continuity gap going forward.

---

∰ 20260719000000000
