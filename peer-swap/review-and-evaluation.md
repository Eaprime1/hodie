# Peer swap, first run: review, evaluation and ways to improve (hodie side, session b)

`prima-clock: 202610160142` (UTC)
`suit: ♦️ Seed · plank: Germ — an evaluation, not canon`
`entity: eaprime1 + Claude (Sonnet 5.5, hodie side)`
`status: living. Written after Pass 4; companion to first-run-notes.md (which lists what went wrong; this judges the process).`

*Kinds: **observed** (a path, commit or run backs it), **guess** (marked). I can judge the hodie side
and the two letters. I have not read custos's forms or its PR in full, so nothing here scores custos's work.*

---

## 1. What the process was meant to deliver

From `atelier/peer-swap/mission.md` ("What good looks like"): checkable observations; a Pass 1 that
surprises you in Pass 2; declines with reasons; honest gaps. Plus the stated aim: "a clear second perspective,
not a verdict", and readiness for hodie's entry into custody.

## 2. Scorecard against that

| Test | Result | Evidence |
|---|---|---|
| Observations a stranger can check | **Met** | Pass 1 has 29 numbered observations, each with a path and a kind (observed, reported, guess). Pass 4 answers were re-checked against the tree and `git log` before filing. |
| Pass 1 surprised Pass 2 | **Met** | Pass 2 C-1 retracted a Pass 1 suspicion (custos's claims about hodie were accurate when written); C-3 showed Pass 1 had read hodie through a `CLAUDE.md` naming 13 of 33 folders; C-4 showed "index drift" was shared, not custos-only. |
| Declines with reasons | **Met** | Pass 3 declined four of eight borrow items with reasons; custos declined the footer state file and bot commit. |
| Honest gaps stated | **Met** | Both Pass 1s list what could not be seen (history, other branches, CI). Both letters mark guesses. |
| Independent perspectives | **Partly** | Neither Pass 1 was cold: both sides had the peer's `CLAUDE.md` loaded, and custos's was labelled a warm start. Custos wrote Passes 2 and 3 after my letter was on origin and said it had not read it. Convergence helps here (section 3). |
| Clean mechanics | **Not met this run** | 13 issues in `first-run-notes.md`; several look avoidable with a better template or README (section 5). I did not count how many. |

## 3. What the run produced (observed)

- **Convergent findings.** Two readers working apart found the same things: the registry row `202609251844` that
  disagrees with the tree (my Pass 1 O-6; custos's letter, section 4); the empty `vault/spade-of-aces/` against a
  ♠️ founding; the bounty remnant; the `pytest-asyncio` gap in hodie. Findings reached from both sides are
  the strongest ones; a one-sided finding (the plexus premise, `claude.yml`) needed a check.
- **Fixes in hodie:** four `CLAUDE.md` claims corrected; a PR template; the witness bot no longer commits to PR
  branches; the Gemini review workflows found failing since 2026-08-22 and paused (`.gemini/OUT_OF_ORDER.md`).
  None of these was a stated goal of the swap; they came from chasing problems that surfaced during it.
- **Questions that sharpened the work:** custos asked what `OPEN` means on a `COMPLETE` carrier. Hodie has two
  fields (`chain_of_custody`, `motion_state`) that nothing defines; the question exposed it.
- **A usable custody picture:** nothing in hodie is in a chain yet; 17 carriers sit `OPEN` (Pass 4 Part 6).

## 4. What it cost

- **Time and sessions:** two hodie sessions ran Pass 1; one filed as `session-a`. That doubled the cold read and
  also doubled the branch, PR and hook confusion. **Guess:** the extra read added little beyond confirming the same
  findings, but I did not diff the two.
- **Red marks on the PR.** Most were not from the swap: the witness check failed on frozen files (a real conflict
  between rules), and four Gemini workflows were already failing on `main`. **Observed:** a reviewer scanning the PR
  could not tell which red was new. This is the costliest finding for the next run.
- **Bot churn.** The witness bot pushed to the branch after almost every push (`9c16739`, `587051a`, `0e179e3`,
  `5bc876e`), so each of my pushes needed a rebase first.

## 5. Ways to improve

Ordered by value for effort. "Owner" is who decides; the work can be Claude's.

| # | Change | Why (evidence) | Cost | Owner |
|---|---|---|---|---|
| 1 | **Record a CI baseline before Pass 1** for both repos: which checks are red on `main` today. | Gemini was red on `main` for ~2 months and looked like the PR's fault (section 4). | One command per repo, one table. | Eric / oversight |
| 2 | **Put the witness line in the pass-file template** (or let the freeze rule name one allowed footer edit). | Pass 1 and 2 failed the strict check; fixing meant breaking the freeze (`431f116`). Custos also reworded a frozen Pass 2 (`1b6973d`). | A line in the template. | Eric |
| 3 | **Name each repo's own scan in the form up front.** | Form F pointed at `tools/scan_lexeme.sh`, which hodie lacks (issue 8). | One line per side. | Oversight |
| 4 | **One session per side, or a distinct branch name per session from the start.** | Branch collision (issue 1), PR duplication, `session-a` filing. | README sentence. | Eric |
| 5 | **Declare warmth on the Pass 1 header** ("what was auto-loaded"), and decide whether a truly cold read matters. | Neither read was cold (section 2). | A header line, or a fresh conversation. | Eric |
| 6 | **Generate stamps with `date -u` at commit time; record local time beside any given one.** | My Pass 4 commit carried `202610160115` at ~`202610160108`; hodie's stamp arrived in Pacific time. | A habit, plus a README note. | Both sides |
| 7 | **Stop bots committing to PR branches** (done for the witness workflow here). | Rebase before every push; Unverified-commit hook noise. | Workflow edit (done). | Eric (done on his word) |
| 8 | **List sandbox limits and REST fallbacks in the README** (GraphQL blocked: create a PR, mark it ready by REST). | Issue 7. | A short section. | Oversight |
| 9 | **A letter-vs-letter comparison step at the sync point.** | Oversight did this by reading both PRs; a fixed table (items both raised / only one raised) would make it repeatable. | One table template. | Oversight |
| 10 | **Define hodie's two carrier fields** and say what `OPEN` means. | Custos Q3; Pass 4 answer 3 is a guess. | A paragraph in `moav/README.md`. | Eric |

## 6. What I cannot judge

- Whether custos's Pass 1, 2 and form met the same tests (I read the letter and the README adjustments only).
- Whether the swap made either repo easier to enter, as the aim says. That needs a second reader after the fixes.
- Elapsed time per pass: this session kept no timings, so no speed claim is made.
- Whether hodie can enter custody on the strength of this review. That is the oversight conversation's and Eric's call.

---

∰◊€π¿🌌∞

∰ 20261016014211671
