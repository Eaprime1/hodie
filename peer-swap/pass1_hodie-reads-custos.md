# Pass 1 — hodie reads custos (cold read)

`prima-clock: 202610152233` (UTC)
`suit: ♦️ Seed · plank: Germ — a working process, not canon`
`entity: eaprime1 + Claude (Sonnet 5.5, hodie side of the peer swap)`
`status: FROZEN on commit. Corrections go in Pass 2 as new text.`

*Observations only. No recommendations. Each observation says what kind of claim it is:*
**observed** *(I read or ran it myself)*, **reported** *(a document says so; I did not check)*,
*or* **guess** *(marked as such).*

---

## 0. What I read, and what I could not see

- **Read:** `eaprime1/custos`, branch `navigo-claude-hodie-custos`, commit `a8e9e41`
  (2026-10-15), as an anonymous shallow clone (depth 1). 616 tracked files, about 6.7 MiB pack.
- **Could not see:** history before `a8e9e41`, any other branch (including `main`), any PR
  or issue, CI runs, Codacy or DeepSource results, Git LFS contents, and anything untracked
  in a working tree. Every PR number or commit hash below is therefore **reported** (copied
  from a custos document), not checked.
- **Read before Pass 1 began, so you can discount it:** custos's `CLAUDE.md` was loaded into
  my context automatically. During the survey I also read two custos documents that make claims
  about hodie: `atelier/hodie-shadow/202610152017_renovata-opening.md` and
  `atelier/peer-review/202610_custos-pixelator_run-0.md`. I have not checked those claims
  against hodie. That is Pass 2's job. Two already look different from what I saw while setting
  up (see O-21).
- **Not read:** `atelier/peer-swap/intro-hodie-side.md`, the other 140 or so atelier files in
  any depth, `dungeon-master/`, `guides/`, `world/` beyond names, the workflows beyond one,
  `valuation/`, and the closed-out turn documents.
- **Method:** listings, `grep`, a few small Python checks of paths and JSON fields, and
  running `tools/scan_lexeme.sh`, `tools/repo_hygiene_check.sh` and `tools/prima_clock.sh`'s
  source against the checkout. Nothing in custos was edited.

---

## 1. What custos is

**O-1 (observed).** `README.md` calls it "guardian of the work you do from here": a "prima
terminal concept for the Pixel 8". `CLAUDE.md` says it is "not a software project with a build
pipeline", with "no test suite, no package manager", and the deliverable is "content and
structure". The tree agrees: markdown, YAML, JSON and shell, no source-language build.

**O-2 (observed).** The README structure block names 19 top-level folders. The checkout has 26
non-hidden folders. Eight are not named in that block: `dungeon-master`, `incoming`, `pandora`,
`pr-journeys`, `seep-artois`, `state`, `templates`, `valuation`. (`prima.yaml` does reference
`seep-artois` and `templates/carrier.md`.) `CLAUDE.md` covers several of them in prose.

**O-3 (observed).** `atelier/` holds 142 files. The nursery is the largest single area. `atelier/README.md`
says "Nothing in the Atelier is finished. That is the point."

---

## 2. The custody trail

**O-4 (observed).** `prima-clock/registry.md` has 40 dated rows, from `202605271650` (founding)
to `202610091052` (Suit and Plank). It is one file; `prima-clock/` contains nothing else.

**O-5 (observed, by script).** The registry cites 62 file paths in backticks. 22 do not exist at
the exact string given, because the row gives a bare file name. All 22 are accounted for:
17 resolve by file name elsewhere in the tree (for example `world-state.json` is at
`dungeon-master/narrative-engine/world-state.json`), 4 resolve with a `202606290000_` prefix in
`incoming/pre-nullus/`, and 1 (`incoming/concept-grain.pdf`) is stated to live in another repo
(`eaprime1/tabularium`) and I cannot check it.

**O-6 (observed).** One registry row disagrees with the tree. Row `202609251844` says six
"Portaque" and "Momentum Archive" files sit at the repo root, "are not moved", and that the row
"is the documented exception". In this checkout none of them is at the root. All six are in
`.shadow-well/` (`.shadow-well/PORTAQUE_MANIFEST.json` and five more). I cannot tell when they
moved; the clone has no history.

**O-7 (observed, by script).** `moav/` holds 13 JSON carriers plus a `README.md`. All 13 parse.
All 13 have `prima_clock` and `chain_of_custody` keys, as `CLAUDE.md` asks. The value of
`chain_of_custody` is not uniform: a plain string `OPEN` in 8, `CLOSED` in 2
(`custos_moav_external_submission001.json`, `custos_moav_transfer_conceptgrain001.json`), and a
list or object in 3 (`custos_moav_keeper_seed_launch.json`,
`custos_moav_sparstone_handoff.json`, `praevium_moav_sparstone-nomination.json`).

**O-8 (observed).** `moav/README.md` lists five carriers under "Existing Carriers", the latest
stamped `202607051456`. The directory has 13. The README says each carrier "must include its
prima-clock stamp"; `CLAUDE.md` says "expected to… barring a documented exception". The two
statements differ in strength.

**O-9 (observed).** The founding carrier, `moav/custos_moav_founding.json`, has `suit: ♠️` and
`chain_of_custody: "OPEN"`. The registry's first row calls the founding "Origin mold
established" with suit ♠️. `vault/spade-of-aces/README.md` says it holds "♠️ Pinnacle documents
only", and the folder holds only that README. `vault/` also holds `cygwin-installation.pdf`.
`branch-tracker/branches.md` lists the `∰custos` vault-pinnacle branch as "Pending… Not yet
created".

**O-10 (observed).** `.github/CODEOWNERS` assigns every path (`*`, plus `vault/`, `moav/`,
`prima-clock/`, `branch-tracker/`, `world/`, `device/`) to one owner, `@eaprime1`.
`CLAUDE.md` says the same person holds the Shepherd and Deck Master roles.

---

## 3. Workflow and review machinery

**O-11 (observed).** `.github/workflows/` has 25 files, including the Latin-cue set
(`disponi.yml`, `placet.yml`, `finalize-pr.yml`, `latin-cue-record.yml`, `prima-witness.yml`,
`review-packet.yml`, `final-review.yml`). `docs/latin-workflow-glossary.md` defines the cue words
in a table.

**O-12 (observed).** `claude-code-review.yml` triggers on `pull_request` types
`[opened, ready_for_review, labeled]`. Its header comment says it runs once when ready and again
only on the `ai-review` label, and that drafts get the API-free `review-packet.yml` instead. The
file explains why it does not use the API key (credit balance failures seen before).

**O-13 (observed).** `.github/PULL_REQUEST_TEMPLATE.md` (44 lines) has sections Intent, What
Arrived, Resonance, Ethics Check, Sense Check, "What Door Does This Open?", then `prime state`,
`witnessed`, and an `observed` checkbox. The Ethics Check includes "`bash tools/scan_lexeme.sh`
run".

**O-14 (observed).** `turns/observations/README.md` sets an order: ready-for-review witness,
oversight review, observation complete, owner's seal, merge. The folder holds five
observations (`202610070847_pr426…` to `202610071031_pr431…`) plus the README and template. None
is later than `202610071031`.

**O-15 (observed).** `CLAUDE.md` ("Seal and merge") says navigo comments post under the owner's
login, so the seal gate skips comments with the Claude Code footer and cues inside quotes or
code, and a navigo describes the seal cue in words unless asked. This matches what the
peer-swap `README.md` asks of both sides.

**O-16 (observed).** `tools/` has 22 files. Three are tests: `test_cue_parser.js`,
`test_cue_parser.sh`, `test_validate_json_yaml.sh`. `tools/prima_clock.sh` prints UTC by default
(`date -u`) and local time with `--local`.

---

## 4. Memory, tracking and staleness

**O-17 (observed).** `turns/log.md` is 669 lines. Its last entry is stamped `202610071030`. This
branch carries later work (the registry's last row is `202610091052`; the peer-swap files are
stamped `202610152136`), with no later log entry.

**O-18 (observed).** `branch-tracker/branches.md` says "Last updated: 202609290340" and names
`main` tip `46fb3376`. `atelier/hodie-shadow/202610152017_renovata-opening.md` says custos `main`
was `e739648` at `202610152017`. I cannot check either hash. The tracker's own rows mark several
branches "Not created", "Stale" or "Pending".

**O-19 (observed).** The seven folders `returns/stream-1-language` through
`returns/stream-7-perplexity` each contain only a `.gitkeep`. `CLAUDE.md` ("Each stream
directory receives findings from the assigned AI model") describes them as receiving each
stream's findings.
`.claude/returns/` holds one file (`ethica_nexus_review_202609280650.md`).

**O-20 (observed).** `turns/CULTIVATION.md` has 12 headed entries. `CLAUDE.md` says it is a
catalog of open design conflicts that must be "resolved or explicitly deferred" when read. I
did not read the entries.

---

## 5. Claims custos makes about itself, checked

**O-21 (observed that the claims exist; unchecked against hodie).** Custos documents carry claims
about hodie that I have not verified:

- `atelier/peer-review/202610_custos-pixelator_run-0.md` (H-4): hodie has "3 of 13" hygiene
  baseline files and no Latin-cue workflows. (`tools/repo_hygiene_check.sh` on custos itself
  reports 13 of 13.)
- `atelier/hodie-shadow/202610152017_renovata-opening.md`: hodie `main` at `f60476e`, 17 `moav/`
  carriers with none recording hodie's own custody entry, and a review workflow with "no draft
  skip".
- Two of these already look different from what I saw while setting up. My clone's `main` is
  `a834602`, and hodie's `CLAUDE.md` says drafts and ordinary pushes do not start the review. I
  have not examined either.

**O-22 (observed).** `CLAUDE.md` says `device/` is "pixel8 branch only. Not on `main`" and
names the branch `pixel8`. This branch has `device/` (6 files).
`atelier/peer-review/202610_custos-pixelator_run-0.md` (H-3) already records the same
mismatch and says the real branch name is `pixel` and `device/` is on `main`. I cannot check
branch names.

**O-23 (observed).** Prima-clock time zones: the peer-swap `README.md` says UTC
(`date -u`); `CLAUDE.md` says `date '+%Y%m%d%H%M'` (local); `tools/prima_clock.sh` defaults to
UTC; the registry row `202610091052` ends "Stamps are UTC". The same split is recorded as an
open DECIDE in `atelier/peer-review/…run-0.md` (H-2).

**O-24 (observed).** `CLAUDE.md` says custos "retired the word 'bounty'". 67 files still contain
"bounty" (case-insensitive), including `quests/missions/002-post-a-bounty.md` (14 times). Many
are historical (registry rows); I did not sort them.

**O-25 (observed).** `bash tools/scan_lexeme.sh` run on custos itself prints 206 matching lines
and ends with "Distressed lexemes are invitations, not failures." The exit code is 0. Several
matches are the scanner's own definitions (`tools/scan_lexeme.sh:25`,
`.github/workflows/review-packet.yml:78`, `.gemini/styleguide.md:17`, `CLAUDE.md:243`).

**O-26 (observed).** `CLAUDE.md` "Known Stray Content" names `airavata-custos/` and
`seneschal/scanner/New folder/` as untracked working-tree items. Neither is in the checkout.
That is expected for a clone; I cannot check the working tree they describe.

---

## 6. How custos treats peers and process

**O-27 (observed).** `docs/peer-review-process.md` (v0, `202610060743`) states principles
including "Report, hold, do not fill", "Sovereign content stays sovereign", and "Facts first,
judgment second". `atelier/peer-review/202610_custos-pixelator_run-0.md` is its first run, with
25 findings in three lenses, dispositions (ADOPT, ADAPT, PROJECT-WIDE, DECIDE, SKIP) and a
tally. The run's section 8 says the first tally was wrong until counted by script.

**O-28 (observed).** 47 files in the checkout mention "hodie" (case-insensitive), for example
`branch-tracker/branches.md`, `queue/seed-weir/README.md`, `atelier/legatum/README.md`,
`atelier/gateway/routing-ladder-for-custos-intake.md`, `atelier/hodie-shadow/…`. The branch tracker
lists `atelier/element-of-the-day/` as routed to `eaprime1/121` or `eaprime1/hodie`, with a "hodie
handoff doc… design-only".

**O-29 (observed).** The form's optional "Lens (Quince)" refers to a term custos's own review
marks as not verified: `atelier/halide/seeds/REVIEW-202610030124.md:109` lists "Quince 15
lenses" as "N only. Not in the repo", and line 115 names Quince among terms found "nowhere in the
repo". I found no definition of it in the checkout, so I do not supply the optional lens.

---

## 7. Perspective prompts (observations, from the form)

- **Newcomer.** `README.md` is short and gives four commands to start (clone, bootstrap, prime
  check, scan). `CLAUDE.md` is long (265 lines) and carries most of the real orientation. The README uses
  words like Podium, Field, Flock, Shepherd, Weir and navigo; it explains the first four in a
  short block and the Weir only by a one-line folder label. I did not check where the rest are
  defined.
- **Contributor with no context.** `.github/ISSUE_TEMPLATE/` has five forms; `CLAUDE.md` and
  `docs/issue-system.md` give the claim path ("claiming this" plus a PR) and the no-cash rule. The
  Latin cues (`@claude disponi`, `petitio`) are an extra step before claiming.
- **The Shepherd on a tired day.** Re-entry aids exist: `turns/CLOSING.md`, `turns/log.md`,
  `device/active.md`, `branch-tracker/branches.md`. Several of those are stamped weeks behind the
  work (O-17, O-18).
- **Six months from now, if nothing changes.** The registry, carriers and observations follow a
  fixed format, so those stay easy to read. The ones that run ahead of their README or tracker
  (O-8, O-18, O-19) are the ones that will have drifted further, **guess**.

---

## 8. Answers to Form Section B

1. **What custos is for.** Tending and recording work that arrives from many sources, as a story
   world over a repo, with a custody trail (`README.md`, `CLAUDE.md`, `prima-clock/registry.md`).
2. **Three things it does that I would have missed in my own repo.** A single-file custody log
   whose cited paths mostly resolve (O-4, O-5); a review that runs once when a PR is ready and
   gives drafts an API-free packet instead (O-12); an observation document filed before the seal
   (O-14).
3. **Three things that confused me.** The vault and Spade of Aces being empty while the registry
   marks the founding ♠️ (O-9); the README's folder block and the moav README both being shorter
   than the trees they describe (O-2, O-8); "navigo" naming being "under review" while a numbered
   table stays in `CLAUDE.md` (`CLAUDE.md`, section Navigo model).
4. **One thing it seems to promise that I cannot find evidence of.** Stream returns arriving
   in `returns/stream-N-*/` (O-19). I looked in all seven folders, `.claude/returns/`, and the
   registry.
5. **With ten minutes, I would open** `prima-clock/registry.md` first, because it is one file, in
   a fixed table format, and most of what else exists in the repo is cited from it.

---

∰◊€π¿🌌∞

*Enjoy the journey.*

∰ 20261016010553275
