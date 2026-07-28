# Mission Seed Procedure

**Status**: DRAFT
**Created**: 2026-07-19
**Purpose**: A consistent way to turn "we should really do X" into tracked, findable work — instead of letting it live only in a chat transcript that nobody re-reads.

---

## The problem this solves

A PR is inert. It can't act on its own — nothing happens to it unless a workflow fires or someone clicks a button. The same is true of a conversation: once it ends, anything said in it that wasn't captured *somewhere durable* is gone in practice, even if the text is technically still there in a PR description or session log.

Case in point — PR #98 (`claude/upgrade-hodie-repo-XEFEy`, see `.eric/BRANCH_FINALIZATION_2026-07-19.md` for the full story): a session split its work into "PR 1" (CI unblock — opened, merged) and "PR 2" (four real engineering items — async bug fix, `HODIE_LOCATION` wiring, a `tests/` scaffold, `one_hertz.py`). PR 2 was never opened. No issue captured it either. The four items happened to get done later through unrelated work, but nobody could confirm that without manually checking each one, months later, during an unrelated audit. That's luck, not process.

**A mission seed is the fix**: the moment something is identified as real, worth doing, but out of scope for the PR/conversation in front of you, it gets written down in one consistent place, in one consistent shape, so it can be found again — and so a review pass (like this one) can check "was this ever planted?" instead of re-discovering it by accident.

---

## Where seeds live

`mission/seeds/SEED_<slug>.md` — one file per seed. Short slug, no dates in the filename (the file itself carries dates).

Template:

```markdown
# SEED: <short title>

Status: SEED
Scope: internal | external
Origin: <link — PR #, issue #, audit doc, conversation date>
Created: YYYYMMDD

## What

<One or two sentences. What needs to happen.>

## Why

<Why it's real — what breaks or stays broken without it.>

## Target

<internal: which repo/area it belongs to>
<external: who/what has to act — a person, a service, another team.
 hodie has no reach past a workflow or a button-click here; if the actor
 isn't inside this ecosystem, say so explicitly instead of leaving it implied.>

## Acceptance

<How you'd know it's done, if known. "Unknown yet" is fine for a fresh seed.>
```

---

## Status lifecycle

Uses the same `Status: X` convention `.scripts/acp_proceed.sh` already drives (`acp_proceed.sh SEED PLANTED` advances it in place):

| Status | Meaning |
|---|---|
| `SEED` | Captured. Nobody's committed to it yet. |
| `PLANTED` | Has an owner — a GitHub issue (internal) or a named external target — that others can track independently of this file. |
| `ACTIVE` | Someone/something is actively working it. |
| `COMPLETE` | Done. Leave the seed file in place (it's the record), link the PR/commit that closed it. |
| `DROPPED` | Explicitly decided against. Say why — a dropped seed with no reason is the same silent-loss failure this procedure exists to prevent. |

A seed does not go from `SEED` straight to deleted. It moves through the states or it's marked `DROPPED` with a reason. Silence is the failure mode, not any particular outcome.

---

## Promoting a seed (`SEED` → `PLANTED`)

**Internal** (actionable inside this repo or a sibling repo in the ecosystem):
File a GitHub issue, label it `mission`, and link back to the seed file in the issue body. The seed file's `Target` field names the repo.

**External** (needs a person, service, or system outside what hodie/Claude can reach):
The seed file itself *is* the tracking artifact — there's no workflow to hand it to. Fill in `Target` with exactly who/what needs to act, and check back on it manually rather than assuming it'll surface on its own.

---

## Closure discipline — tie-in to finalization passes

Whenever branches, PRs, or a conversation are being finalized/closed out (like this 2026-07-19 pass), check their descriptions and comments for anything that reads like a seed — a "next PR," a "we should also," a "follow-up needed" — that was never captured. Either:

1. Write it as a `SEED` file now, or
2. Confirm it already happened (like PR #98's case — do the legwork, don't assume), or
3. Explicitly decide it's not worth doing and say so out loud (doesn't need a seed file for something never captured in the first place, but do note it in the finalization report).

Don't let a branch or PR disappear silently carrying an unexamined promise.

---

∰ 20260719000000002
