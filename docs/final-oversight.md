# Final Oversight and the File Review Checklist

**Prima-clock:** 202610161240
**Suit:** ♦️ Diamond, 1/3 plank. Phase C of three, ported from custos (custos#456 to #458).

*The last look before a merge, run only when the owner says so.*

## What it is

Two workflows and a set of offline-tested rules:

- `.github/workflows/file-review.yml` posts one living comment per PR: a checklist of the
  PR's files. Files for reading start unticked and the Shepherd ticks them. Files not for
  reading are ticked by the rules in `.github/review-skip.json`, with a reason. A tick belongs
  to one version of a file, so a push that changes the file clears it.
- `.github/workflows/final-oversight.yml` checks a PR on its current head and posts the result as
  one comment. It reports. It does not seal, does not merge and does not edit the PR.

## What the oversight checks (on the PR's current head)

| Check | Passes when | Counts as |
|---|---|---|
| Checks and statuses | every check run and commit status is green or skipped; none pending | must pass |
| Review threads | none open | must pass |
| Seal covers this head | a seal comment ("Finalized — entered into the ledger") exists, and no commit but a bot's journey document (touching only `pr-journeys/`) follows it | must pass |
| File review | the checklist comment names this head, lists every file, and every file to read is ticked | must pass |
| Watched paths | lists files under `moav/`, `branch-tracker/` and the seal path, and says which the PR body does not name | information |

Differences from custos: hodie has no observation folder, so there is no observation row, and
hodie has no stale-claims tool, so there is no stale row. Hodie's journey document is committed to
the base branch at the seal, so on a hodie PR nothing normally follows the seal.

The rules live in `.github/scripts/final-oversight.js`; `final-oversight-run.js` gathers the facts
from GitHub and hands them over. The rules are tested offline by `scripts/test_final_oversight.js`
(43 checks) and `scripts/test_file_review.js` (29 rows), run in CI by `seal-path-tests.yml`.

## How the owner's approval works

The oversight job runs in a GitHub **environment** named `final-oversight` that lists the owner as a
required reviewer. Until the owner approves, the job shows **Waiting** on the PR and nothing runs.

**One-time setup (the owner does this in the repo settings of `eaprime1/hodie`):**

1. Settings, Environments, New environment, name it `final-oversight`.
2. Tick "Required reviewers" and add the owner. Save.
3. Create a label named `final-oversight` (Issues, Labels).

Without step 2 GitHub creates the environment with no protection and the job would run without
waiting. Check it once after setup.

## How to use it

1. Read the files on the checklist and tick them.
2. Seal with `@claude finalize`. The oversight checks that a seal exists.
3. Add the `final-oversight` label to the PR.
4. Approve the waiting run. Read the comment it posts.
5. If it is green, merge on the owner's word. If it is red, fix the item, and the new head waits for a
   new approval. A fix is a new commit after the seal, so the seal row goes red until the PR is sealed again.

## Safety

- The rules run from the **base branch**, not from the PR, so a PR cannot loosen the gate that reviews
  it. A PR that changes these files is reviewed by the old version and the change is listed under
  watched paths.
- Only PRs from this repository run it. A fork PR is skipped.
- It needs no secrets and no paid model.
- The first run is on the first PR *after* this one merges, because the rules must be on the base
  branch.

---

∰ 20261016123459039
