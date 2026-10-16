# Peer Swap — Form: hodie side

`prima-clock: 202610152136` (UTC, form version; stamp your own passes when you file them)
`you hold: eaprime1/hodie · you are reading: eaprime1/custos`
`form: fill-in-the-blank. Blanks are ____. Leave a blank unanswered rather than invent, and say why.`

*Answer in your own words. Two or three lines is usually enough. If a question does not fit
what you found, say so and move on.*

---

## A. Baseline — before you read anything

1. Where I am running (claude.ai project / Claude Code / other): Claude Code cloud session,
   attached to the claude.ai Project "HODIE". Shell, file tools, no PR-opening tool seen.
2. What I can read: `eaprime1/custos` yes: anonymous shallow clone (depth 1) of branch
   `navigo-claude-hodie-custos` at `a8e9e41`; no history, other branches, PRs or LFS ·
   `eaprime1/hodie` yes: shallow clone of `main` at `a834602`.
3. What I can write: `eaprime1/hodie` attached with push access. Branch
   `feature/peer-swap-hodie-side-b` pushed successfully (the shared `feature/peer-swap-hodie-side`
   already held another session's Pass 1, so mine went to `-b`; Eric is keeping both). PR creation
   still untested (`gh auth status` reported a failed GH_TOKEN login).
4. What I already know about `eaprime1/custos` before Pass 1, honestly: a vague impression of it
   as a system-management tool, which I discounted, and its `CLAUDE.md`, which loaded
   automatically before Pass 1 began. Nothing else.
5. What I already know about `eaprime1/hodie`: its `CLAUDE.md` and a top-level listing. Nothing
   else was read before Pass 1.
6. Anything I cannot reach, stated plainly: custos history, other custos branches, PRs, issues,
   CI and Codacy results; any write to custos; `atelier/peer-swap/intro-hodie-side.md` (not on my
   reading list, unread).

*If you cannot read `eaprime1/custos`, stop here and tell Eric.* (I can.)

---

## B. Pass 1 — cold read of `eaprime1/custos`

*Full observations, with a path or commit for each, are in `pass1_hodie-reads-custos.md`
(O-1 to O-29). The answers below point into it.*

1. In one sentence, what `eaprime1/custos` is for: tending and recording the work that arrives
   from many sources, as a story-world repo with a custody trail (O-1, O-4).
2. Three things it does that I would have missed in my own repo: a single-file custody log whose
   cited paths mostly resolve (O-4, O-5); a paid review that runs once when ready, with an
   API-free packet for drafts (O-12); an observation document filed before the seal (O-14).
3. Three things that confused me: an empty Spade vault beside a ♠️ founding row (O-9); README
   folder list and moav README both shorter than the trees they describe (O-2, O-8); navigo
   naming "under review" while a numbered table stays in `CLAUDE.md` (`CLAUDE.md`, Navigo model).
4. One thing it seems to promise that I cannot find evidence of (and where I looked): stream
   returns arriving in `returns/stream-N-*/`. I checked all seven folders, `.claude/returns/`
   and the registry (O-19).
5. With ten minutes, I would open `prima-clock/registry.md` first, because it is one file in a
   fixed format and much of the repo is cited from it.

**Through other eyes** (full text in `pass1_hodie-reads-custos.md` section 7):

- The newcomer who has never seen either repo: the README is short and starts with four
  commands; `CLAUDE.md` (265 lines) carries most of the orientation.
- A contributor with no context, who wants to help today: five issue forms and a claim path
  exist; the Latin cues are an extra step before claiming.
- The Shepherd on a tired day, coming back after a break: re-entry files exist, but several are
  stamped weeks behind the work (O-17, O-18).
- The repo six months from now, if nothing changes: fixed-format records stay readable; things
  that already run ahead of their README or tracker will drift further (a guess).

**Lens (optional, Quince).** Not supplied. Custos's own review lists Quince as "not in the
repo" (`atelier/halide/seeds/REVIEW-202610030124.md:109`) and I found no definition (O-29).

*Commit Pass 1 as `pass1_hodie-reads-custos.md` with a message starting
`freeze:`.* (Done in the commit that adds this file.)

---

## C. Pass 2 — deep dive of `eaprime1/hodie`

*Full text in `pass2_hodie-own-repo.md`. Pass 1 is not edited.*

1. The top-level folders of `eaprime1/hodie`, one line each (table with file counts in
   `pass2_hodie-own-repo.md` section 1):
   - `crawler_pixel8/` load-bearing Python crawler, about 1.85k lines; running; `tests/` pass (88
     with `pytest-asyncio`).
   - `quanta/` unfinished: 15 domain folders (`CLAUDE.md` says 16); status doc dated 2025-12-30.
   - `moav/` 17 carriers (16 dedupe candidates, 1 transfer); all say `OPEN`, including the transfer
     the README calls COMPLETE; none records hodie's own custody entry.
   - `_CONSOLIDATED/` 310 files, a finished merge, unsorted content (302 in `CODEX_documents/`).
   - `.streams/` one README; `.locations/` three load-bearing configs; `.scripts/` 29 files.
   - `redundancy_entity/`, `crawler_output/`: Gravity Core files still present after a recorded
     transfer; one summary JSON.
   - Not in `CLAUDE.md`'s tree: `wellspring/`, `mission/`, `quepad/`, `moav/`, `tests/`,
     `branch-tracker/`, `pr-journeys/`, `migrations/`, `docs/`, `scripts/` and more (13 of 33
     folders are named there).
2. Where my Pass 1 was wrong or incomplete: it called two custos claims about hodie "different"
   when they were accurate as of their stamp and have since moved (C-1); it read hodie only
   through `CLAUDE.md` (C-3); it treated index drift as custos-specific (C-4).
3. Things hodie does that custos would not guess: a tested Python codebase; a workflow that
   commits back to branches (`footer-witness.yml`); a daily Drive sync and an hourly bot-PR
   finalizer; a seal gate with no footer or quote guard; entity domains as the content model.
4. The thing I would least like the peer to open: `.eric/` (owner-filed notes, 27 files; I did
   not open them), then `_CONSOLIDATED/CODEX_documents/` (302 files, known duplicates).
5. Did anything in my own repo change how I read Pass 1? Yes: custos's claims about hodie were
   accurate when written; index drift is shared; hodie lacks the seal-gate footer guard that
   Pass 1 noted custos has (O-15).

*Commit as `pass2_hodie-own-repo.md`, message starting `freeze:`.* (Done in the commit that adds
this file.)

---

## D. Pass 3 — letter to `eaprime1/custos`

*Write the letter as its own file. Fill this block in first as the outline.*

1. What I saw in your repo that you may not see (up to five, each with a path): full text in
   `pass3_letter_hodie-to-custos.md` Part 1. (1) registry row `202609251844` vs `.shadow-well/`;
   (2) `moav/README.md` lists 5 of 13 carriers, three shapes of `chain_of_custody`; (3) empty
   `vault/spade-of-aces/` against a ♠️ founding; (4) `returns/stream-*` empty, `turns/log.md` behind
   the registry; (5) `tools/scan_lexeme.sh` exits 0 on 206 hits.
2. What I would borrow from you:

| Item (path) | Tentative: adopt / adapt / decline | Why | Cost to my repo |
|---|---|---|---|
| seal-gate footer guard (`CLAUDE.md` "Seal and merge") | adopt | hodie `finalize-pr.yml` has none | one workflow edit; follow-up, Eric's call |
| `.github/PULL_REQUEST_TEMPLATE.md` | adapt | hodie has none | one file |
| `turns/observations/` | adapt | pause between ready and seal; reuse `pr-journeys/` | a habit |
| `docs/peer-review-process.md` principles | adopt | zero code | a doc or pointer |
| `prima-clock/registry.md`, Latin cues, `scan_lexeme.sh`, CODEOWNERS | decline | reasons in the letter | see letter |

3. What I would ask you: five questions in the letter Part 3 (what entering custody needs; bot-refreshed
   witness state; witness line on frozen files; which scan counts for hodie Form F; UTC vs local).
4. What I would warn you about before you borrow from mine: six items in the letter Part 4 (witness bot moves the branch tip; strict footer check vs freeze rule; seal gate plus hourly auto-finalize; hodie index drift; test dependency; `.eric/` not opened).

*Commit as `pass3_letter_hodie-to-custos.md`, message starting `freeze:`.
Then check that the peer's letter is on origin before Pass 4.*

---

## E. Pass 4 — reply to the peer's letter

1. For each item in the peer's letter (full table and reasons: `pass4_reply_hodie.md` Part 1):

| Their item | adopt / adapt / decline | Reason | Where in my repo | Done in this PR, or follow-up |
|---|---|---|---|---|
| 1. plexus has no folders | accept finding, correct premise | it is code: `PLEXUS_STAGES`, `crawler_pixel8/processors/one_hertz.py:28` | `PLEXUS_SYSTEM.md` | follow-up (doc wording) |
| 2. `CLAUDE.md` names things the tree lacks | adopt | four claims checked, all true | `CLAUDE.md` | done in this PR |
| 3. 17 carriers `OPEN`, none names hodie | accept | observed; see Part 3 answer 3 | `moav/` | follow-up (custody entry record) |
| 4. no door for a contributor | adapt | true; license is Eric's call | `.github/PULL_REQUEST_TEMPLATE.md` | template done; license, CONTRIBUTING, issue templates follow-up |
| 5. wellspring says one thing, holds another | accept | 89 files in `Temphold_needs_review/`, owner "eaprime1 review" | `wellspring/` | follow-up (Eric) |
| their borrow table (5 rows) and 6 questions | notes and answers only | custos's decisions; answers checked against hodie | `pass4_reply_hodie.md` Parts 2 and 3 | done |

2. Small adaptations made in this PR (paths): `CLAUDE.md` (4 corrections: 15 domains, 29 scripts,
   pytest-asyncio note, `claude.yml` deleted); `.github/PULL_REQUEST_TEMPLATE.md` (new);
   `peer-swap/pass4_reply_hodie.md`; this form. Also, on Eric's instruction, one witness line appended to
   frozen `pass1_hodie-reads-custos.md` and `pass2_hodie-own-repo.md` (commit `431f116`; no other change).
3. Follow-ups named but not done: plexus doc wording; `moav/README.md` "COMPLETE" wording; seal-gate footer
   guard in `finalize-pr.yml`; `LICENSE`, `CONTRIBUTING.md`, issue templates (Eric); `wellspring/` triage (Eric);
   `branch-tracker/branches.md` refresh; hodie custody entry record.
4. What changed my mind, if anything: the plexus premise (code, not folders); and that hodie's `chain_of_custody`
   and `motion_state` fields are not defined anywhere.

### Hodie-side block

5. What in `hodie` is in a chain of custody, and what is not: nothing in a chain (no custos registry row names
   hodie; no hodie carrier names hodie as entering). 17 `moav/` carriers recorded but `OPEN`. Not in a chain:
   `_CONSOLIDATED/CODEX_documents/`, `wellspring/`, `quanta/`, `crawler_pixel8/`, `mission/`. `.eric/` not opened,
   so not sorted. Detail: `pass4_reply_hodie.md` Part 6, item 5.
6. Where a record of hodie's own entry could live: a carrier in hodie `moav/hodie_moav_custody_entry.json` and a
   row in custos `prima-clock/registry.md` (custos records). Need from custos: row format, suit/plank for
   shadow-before-primal, meaning of `chain_of_custody` on an entry carrier. Carrier not written.
7. Hodie's prima-clock stamp (Eric set it): `202610151805` Pacific (PDT, UTC-7). UTC confirmation: `202610160105`
   (checked by running `date -u` and `TZ=America/Los_Angeles date` together).
8. One thing custos does that hodie's workflows do not: the seal-gate guard against navigo comments (footer and
   quoted or code cues). Cost: a few lines in `finalize-pr.yml` before the `grep -qF '@claude finalize'` step, plus a
   small test; changes who can seal, so Eric's call. Review-on-ready was already matched in #164.

---

## F. Ready for oversight

- [x] All four passes committed; Passes 1 to 3 frozen (witness line appended to Passes 1 and 2 afterward, on Eric's word, `431f116`; no other change)
- [x] This form complete; unanswered blanks marked and explained (no blanks left; Section A to D filled earlier)
- [x] My repo's own scan run: `python3 scripts/footer_witness.py --root . --strict --git-base origin/main` (the command CI runs). Result: my files compliant; flags only the three `peer-swap/session-a/` files (session A's, filed unchanged, not mine to edit). Also `python3 -m pytest tests`: 88 passed with `pytest-asyncio` installed.
- [ ] PR description follows my repo's template; PR marked ready for review
- [ ] One comment posted in words saying the PR is ready, and what is left open
- [x] I have not sealed, merged, or edited the peer repo

---

∰◊€π¿🌌∞

∰ 20261015232701649
