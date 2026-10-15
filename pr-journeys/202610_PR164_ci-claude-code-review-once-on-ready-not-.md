# PR Journey: #164 — ci: Claude Code Review once on ready, not on every push [prima-clock 202610152203]

**Repository:** Eaprime1/hodie  
**prima-clock:** 202610152209  
**Branch:** `claude/review-on-ready-only` → `main`  
**Author:** @Eaprime1  
**State:** FINALIZED  

## Intent

Stop hodie's paid Claude review from running on every push to a draft PR. Run it once when a PR opens non-draft or is marked ready, and again only when the owner adds the `ai-review` label. This is the project-interrupt fix for the creative method's cost and safety, ahead of the custos/hodie peer swap.

## What Arrived

- `.github/workflows/claude-code-review.yml`: trigger types `[opened, ready_for_review, labeled]`; job gate for drafts, forks and bots; concurrency group split so an unrelated label cannot cancel a running review; self-modified-workflow guard (this PR edits that file, so the review skips here by design); action pinned to the commit SHA custos uses.
- `CLAUDE.md` and `.github/REVIEW_SETUP.md`: updated to match.
- Checked: `scripts/check_workflow_injection.py` passes on all 15 workflows; YAML parses.
- Not changed: no hodie-specific review prompt.

## Resonance

*Pattern borrowed from custos and adapted. The first small thing hodie takes from the peer, before the swap starts.*

## The Arc

| Event | prima-clock | Actor |
|---|---|---|
| Opened | 202610152204 | @Eaprime1 |
| Finalized | 202610152209 | @Eaprime1 |

## CI Record

| Check | Result |
|---|---|
| GitGuardian Security Checks | ✅ |

## DeepSource Record

*Not configured for this repo.*

## Review Scores

| Dimension | Score | Note |
|---|---|---|
| Correctness | 5/5 | 1 CI check(s) — all passed |
| Consistency | 5/5 | Template complete · ethics 3/3 |
| Scope | 5/5 | 4 file(s) changed |
| Verification | 3/5 | 1 check run(s) completed |
| **Valuation** | **High** | 18/20 |

## Ethics Check

- ✅ No credentials, personal material or private names
- ✅ Nothing outside the review workflow and its two docs changed
- ✅ Stamp 202610152203

## What Door Does This Open?

*Not recorded.*

---
**prima-clock:** 202610152209  
**witnessed:** true  
*⏱ Hodie — the daily ledger records what arrived · ∰⏱*