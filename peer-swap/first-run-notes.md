# Peer swap, first run: issues and adaptations (hodie side, session b)

`prima-clock: 202610160124` (UTC)
`suit: ♦️ Seed · plank: Germ — notes for the next run, not canon`
`status: living notes. Unlike Passes 1 to 3 this file is not frozen.`

*Eric: "this is our first attempt at this... so it is going to be rocky." These notes keep what was
rocky and what each fix was, so the second run can start from them. Kinds: **observed**, **guess**.
Times are UTC. Everything below happened on 2026-10-15 and 2026-10-16.*

---

## 1. Issues met

| # | Issue | What happened (observed) | How it was handled |
|---|---|---|---|
| 1 | Two hodie-side sessions ran Pass 1 | Both pushed to `feature/peer-swap-hodie-side`; my push was rejected (non-fast-forward, other session's `d494054`). | I did not force-push. Eric chose to keep both. Mine went to `...-b`; oversight later filed session A's Pass 1 and form under `peer-swap/session-a/`. |
| 2 | The branch model was unclear | The README said one branch per side; sessions assumed a shared branch. Eric clarified: each side keeps its work on its own repo's branch, and the letter is the document that crosses. | Clarified in chat; custos README now has "Adjustments after the oversight review". |
| 3 | The cold read was not cold | Custos `CLAUDE.md` auto-loaded into context, and I read two custos documents about hodie during setup. Custos's own Pass 1 was also a warm start. | Both disclosed at the top of each Pass 1 (Pass 1 section 0). |
| 4 | The strict footer check vs the freeze rule | `scripts/footer_witness.py --strict` needs `∰` plus 17 digits at the end of every new `.md`. My Pass 1 and Pass 2 ended with `∰◊€π¿🌌∞`, so the check failed (run `38822410290`). | Left frozen until Eric said to append the line; done in `431f116`, no other change. Pass 3 onward carried the line from the start. |
| 5 | The witness bot moves the branch tip | `footer-witness.yml` pushed `quepad: refresh witness scan state` onto every PR branch. Pushes were rejected until I rebased; commits showed Unverified; the stop hook warned each time. | Rebased before every push. Fixed in the workflow (section 3). |
| 6 | Stop hook false alarms | Hook compared the local branch name to the remote tracking ref and said commits were unpushed when they were not; later it flagged only the bot commit. | Renamed the local branch and set the tracking ref by hand; declined to rewrite bot commits. |
| 7 | Tooling limits in the sandbox | `gh pr create` failed with HTTP 403 (GraphQL blocked); no `pytest-asyncio` so 25 tests failed. | Opened and edited the PR through the REST API; marked ready with `POST /repos/{owner}/{repo}/pulls/{n}/ccr/ready_for_review`; installed the dev dependency in the sandbox only. |
| 8 | "My repo's own scan" was not defined for hodie | Form F named `tools/scan_lexeme.sh`, which hodie does not have. | Eric approved using the footer-witness check (the command CI runs). |
| 9 | A wrong claim in my Pass 1 | I wrote that two custos claims about hodie "look different". Pass 2 C-1 showed they were accurate when written and had since moved. | Retracted in Pass 2 as new text; Pass 1 itself not edited. |
| 10 | Stamps drifted | The Pass 4 commit message carried `202610160115` when the real time was about `202610160108`; custos has a Pass 2 reworded after its freeze (`1b6973d`). | Both named in PR comments and notes. Rule for next time: generate the stamp from `date -u` at commit time, never type it. |
| 11 | The stamp zone | Eric gave hodie's stamp in Pacific time. | Recorded both: `202610151805` Pacific, `202610160105` UTC (offset confirmed by running both clocks). |
| 12 | Hodie was missing basics custos expected | No PR template, and `CLAUDE.md` was stale in four places (domains 16 vs 15, scripts "21+" vs 29, stdlib-only vs `pytest-asyncio`, deleted `claude.yml`). | Fixed in this PR (Pass 4 Part 1). |
| 13 | Custos independence discipline | Custos wrote Passes 2 and 3 after hodie's letter was already on origin; only the writer's discipline kept it independent. | Custos stated in its Pass 3 header that it had not read the hodie letter. |

## 2. What was adapted

- `CLAUDE.md`: four corrections.
- `.github/PULL_REQUEST_TEMPLATE.md`: new, five short sections, with the seal-and-merge line.
- `peer-swap/session-a/*`: witness line appended to each file (on Eric's word, labeled commit).
- `.github/workflows/footer-witness.yml`: state commit limited to the default branch (section 3).
- Process: pull and rebase before every push; REST calls instead of GraphQL; the witness line in the file template.

## 3. The workflow fix

`footer-witness.yml` step "Commit refreshed scan state" ran on every `push`. It now runs only on a push to the
default branch (`github.ref == refs/heads/<default_branch>`). **Cost, honestly:** feature-branch scans still run and
still fail strict mode, but they no longer write `quepad/state.json`, so that file stops tracking per-branch scans.
Whether a branch push can then re-flag a file the state file would have remembered, I did not test (**guess:** not for
PRs, which use `--git-base origin/main`). The old behaviour is a one-line revert. Not fixed here: the seal gate in
`finalize-pr.yml` still has no footer guard (Pass 4 Part 6, item 8).

### 3b. Follow-up (2026-10-15, evening Pacific): all auto-commits off

Eric asked that nothing commit on its own until it is verified. Four steps did: the witness state refresh, the daily
Drive sync (`sync-hodie.yml`), and the journey-doc write in `finalize-pr.yml` and `auto-finalize.yml`. All four now
run only when the repo variable `AUTO_COMMITS` is `true`; it is unset, so they are off. The sync still runs and prints
`git status` for `hodie/` so a dry run is visible. With the finalize workflows, a finalized PR gets its label and
comment but no journey doc until the variable is set. I could not test these on GitHub from here; I checked that the
YAML parses and the embedded scripts pass `node --check`. The old bot commits on this branch (`4e2c96e`, `5bc876e`)
stay Unverified in history; I did not rewrite them. A squash merge would drop them from `main`.

The finalize gate (`finalize-pr.yml`) requires `## Intent`, `## What Arrived`, `## Resonance` and a `∰` in the PR body. The
PR template I added first had none of the last three, so the first `@claude finalize` (2026-10-16 02:06 UTC) was refused with
those three gaps. The template and the PR body now match the gate; the Resonance text in the PR body is a Claude draft for
Eric to rewrite.

Small fixes made in the same pass: `CONTRIBUTING.md` (new), a pointer to `PLEXUS_STAGES` in `PLEXUS_SYSTEM.md`, and a
note in `moav/README.md` that `COMPLETE` is not sealed. Left alone: `LICENSE` (the owner's choice), issue templates,
the seal-gate footer guard, `wellspring/` triage, `branch-tracker/branches.md` refresh.

## 4. For the second run

1. Put the witness line in the pass-file template so no file needs a post-freeze edit.
2. Say in the README who creates each branch, and that a second session on the same side needs its own branch name.
3. Name the repo's own scan in the form for each side. Hodie's is `scripts/footer_witness.py --strict`.
4. Generate stamps with `date -u '+%Y%m%d%H%M'` at commit time; record the local time zone beside any stamp Eric gives.
5. Tell sessions that GraphQL may be blocked and give the REST commands for creating a PR and marking it ready.
6. State up front which sources are warm (auto-loaded `CLAUDE.md`) so every Pass 1 can say how cold it was.
7. Decide whether a deviation after a freeze (like `431f116` and custos's `1b6973d`) needs a named exception path.

---

∰◊€π¿🌌∞

∰ 20261016012408691
