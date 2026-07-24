# PR Journey: #155 — fix: remove @mention from sovran-voice; fix invalid JSON in quepad/state.json

**Repository:** Eaprime1/hodie  
**prima-clock:** 202607240516  
**Branch:** `claude/nifty-franklin-fxwp3r` → `main`  
**Author:** @Eaprime1  
**State:** FINALIZED  

## Intent

Two targeted fixes on the hodie branch after the main workflow correctness PR (#154) was merged:

1. Remove `@${author}` mention from `sovran-voice.yml` — the daily ledger was tagging the PR author on open, triggering email notifications.
2. Fix invalid JSON in `quepad/state.json` — the quepad scanner ran twice and appended duplicate `last_scan` and `last_seen` keys, which makes the file unparseable by strict JSON parsers.

> **Note:** The four workflow correctness fixes (regex escape in `parseSection`, uppercase checkbox matching, pagination for comment upsert, auth gate on `@claude check`) were included in the previously merged PR #154. This PR contains only the two changes visible in the diff.

## What Arrived

Two files changed:

- **`.github/workflows/sovran-voice.yml`** — removed `const author = pr.user.login` and the `@${author}` opening line; the daily ledger now posts without tagging anyone
- **`quepad/state.json`** — removed duplicate `last_scan` top-level key and duplicate `last_seen` key in the `INVENTORY.md` entry (kept latest timestamp `20260724023605660` in both cases)

## Resonance

*clarified*

## The Arc

| Event | prima-clock | Actor |
|---|---|---|
| Opened | 202607240400 | @Eaprime1 |
| Finalized | 202607240516 | @Eaprime1 |

## CI Record

| Check | Result |
|---|---|
| Codacy Static Code Analysis | ✅ |
| build (3.11) | ✅ |
| build (3.10) | ✅ |
| build (3.12) | ✅ |
| claude-review | ✅ |
| build (3.12) | ✅ |
| build (3.10) | ✅ |
| build (3.11) | ✅ |
| GitGuardian Security Checks | ✅ |

## DeepSource Record

*Not configured for this repo.*

## Review Scores

| Dimension | Score | Note |
|---|---|---|
| Correctness | 5/5 | 9 CI check(s) — all passed |
| Consistency | 5/5 | Template complete · ethics 2/2 |
| Scope | 5/5 | 1 file(s) changed |
| Verification | 5/5 | 9 check run(s) completed |
| **Valuation** | **High** | 20/20 |

## Ethics Check

- ✅ No secrets or credentials introduced
- ✅ Changes are targeted fixes only — sovran-voice behavior unchanged except mention removal; quepad state data is identical minus the duplicate keys

## What Door Does This Open?

*Not recorded.*

---
**prima-clock:** 202607240516  
**witnessed:** true  
*⏱ Hodie — the daily ledger records what arrived · ∰⏱*

∰⏱🃏 20260724054842000