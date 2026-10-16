# Pass 2 — hodie dives into hodie (own repo)

`prima-clock: 202610152313` (UTC)
`suit: ♦️ Seed · plank: Germ — a working record, not canon`
`entity: eaprime1 + Claude (Sonnet 5.5, hodie side of the peer swap)`
`status: FROZEN on commit. Pass 1 (`pass1_hodie-reads-custos.md`) is not edited; corrections are below as new text.`

*Pass 1 in hand. Observations carry a kind: **observed** (I read or ran it), **reported** (a
document says so), **guess** (marked). No recommendations here; those belong in Pass 3.*

---

## 0. What I read

- **Read:** `eaprime1/hodie` `main` at `a834602` (full history fetched: 562 commits, first
  `29faed2` on 2025-12-24, not shallow). This branch is `feature/peer-swap-hodie-side-b`.
- **Ran:** `git ls-files` counts per folder; JSON parsing of `moav/*.json`; custos's own
  `tools/repo_hygiene_check.sh` against this checkout (read-only); `python3 -m pytest tests`.
  The tests need `pytest-asyncio`, which `pyproject.toml` lists as a dev dependency but this
  sandbox lacked. I installed it in the sandbox only; no repo file changed.
- **Not read in depth:** the 302 files in `_CONSOLIDATED/CODEX_documents/`, the 114 in `wellspring/`,
  the 27 in `.eric/` (owner-filed notes; I counted, I did not open), `quanta/` beyond one status file,
  and most workflow bodies beyond their headers.
- **Another hodie-side Pass 1 exists** on `feature/peer-swap-hodie-side` (`d494054`). I have not read
  it beyond its section headings, so this pass does not lean on it.

---

## 1. Folder inventory (Form C.1)

712 files are tracked on `main` (714 on this branch, which adds `peer-swap/`). 17 root files;
33 top-level folders on `main`. `CLAUDE.md`'s structure tree names 13 of the 33.

| Folder | Files | What it is | Load-bearing / finished / unfinished |
|---|---|---|---|
| `crawler_pixel8/` | 17 | The Python crawler: `core/` (processor ABC, content types, stream utils), `processors/` (parser, pattern extractor, `entity_queue_processor.py`, `one_hertz.py`), `cli/` (four tools), `config.py` | **Load-bearing, running.** About 1.85k lines in `core/`, `processors/` and `config.py`. `CLAUDE.md` lists one of the four CLI tools (`test_crawler.py`) and two of the four processors. |
| `tests/` | 7 | pytest suite for the crawler plus `test_footer_witness.py` | **Passing:** 88 passed with `pytest-asyncio` installed; 25 fail without it ("async def functions are not natively supported"). `pyproject.toml` has `asyncio_mode = "auto"`. |
| `quanta/` | 54 | Entity domains and character documents | **Unfinished.** 15 domain folders (`CLAUDE.md` says 16). `quanta/ENTITY_DEVELOPMENT_STATUS.md` says "Last Updated: 2025-12-30". |
| `moav/` | 18 | `README.md` + 17 carriers: 16 dedupe candidates (to `eaprime1/duplicatus`) and 1 transfer (`hodie_moav_transfer_gravity_core.json`) | **Active, unresolved.** All 17 parse and have `prima_clock` and `chain_of_custody`. All 17 say `OPEN`, including the transfer that `moav/README.md` calls "COMPLETE". Not in `CLAUDE.md`'s tree. |
| `_CONSOLIDATED/` | 310 | `CODEX_documents/` (302), `today_exports/` (4), `download_research/` (2), plus `CONSOLIDATION_INVENTORY.md` and `DEDUPLICATION_LOG.md` | **Finished as a merge, unsorted as content.** The dedupe carriers in `moav/` are about this material. |
| `wellspring/` | 114 | Hodie's own intake/holding zone ("Head pressure: 1 item at a time"), with `CODEX_fragments_needs_review/` and `Temphold_needs_review/` | **Unfinished by design.** Not in `CLAUDE.md`'s tree. |
| `.streams/`, `.locations/`, `.scripts/` | 1, 4, 29 | `.streams/` is one `README.md` (prime, codex, gamemaster); `.locations/` has `mulberry`, `pixel8a`, `codespaces` configs; `.scripts/` has 29 files (`CLAUDE.md` says "21+") | `.locations/` **load-bearing** (custos ported `env_setup.sh` from here, per custos `CLAUDE.md`, reported). `.streams/` **description only**, no stream artifacts tracked there. |
| `redundancy_entity/`, `crawler_output/` | 19, 2 | Gravity Core files; crawler summaries | `redundancy_entity/` still here although `moav/hodie_moav_transfer_gravity_core.json` says it was copied to `eaprime1/gravitar` on `202608220615`. `crawler_output/` holds one summary JSON and a `.gitkeep`. |
| `.github/` | 18 | 15 workflows, `REVIEW_SETUP.md`, `labeler.yml`, `copilot-instructions.md` | **Load-bearing.** No `CODEOWNERS`, no `PULL_REQUEST_TEMPLATE.md`, no `sovran-labels.yml`. |
| `mission/` | 10 | Mission seeds and briefs. Three files (`BRANCH_STRATEGY.md`, `NAVIGO.md`, `PLEXUS_SYSTEM.md`) are 8-line "Historical Record" stubs pointing to the root copies | **Finished as a move.** Not in `CLAUDE.md`'s tree. |
| `quepad/` | 3 | "Pad of Q": witness-scan state (`state.json`), registry, README | **Load-bearing and noisy:** the footer-witness workflow commits to it on every push (see 3.2). |
| `branch-tracker/`, `pr-journeys/`, `migrations/`, `docs/`, `scripts/` | 1, 4, 3, 1, 2 | Branch inventory (baseline `373dcd9`, 2026-08-21); PR journey records; a from-unexusi sync; one doc; two checker scripts | Small, each purposeful. |
| `.eric/`, `.claude/`, `.journey/`, `.sovran/`, `.valox/`, `.agents/`, `.codex/`, `.gemini/`, `.reminders/`, `.githooks/`, `_TODAY/`, `_SORTING/`, `_BOX_SIMULATION/`, `.server_root/` | 27, 14, 3, 1, 4, 2, 5, 2, 1, 2, 8, 2, 1, 1 | Session notes; AI-voice workspaces and setup guides; branch records; identity and lint-telemetry files; hooks; drop zones | A mix. `_TODAY/` has inbox files from April; `_SORTING/` has one batch from 2025-12-31. I did not open `.eric/` or `.reminders/`. |

---

## 2. Where Pass 1 was wrong or incomplete

**C-1 (retraction).** Pass 1 section 0 and O-21 said two of custos's claims about hodie "already
look different". Neither was wrong. History shows `f60476e` dated 2026-08-22, with no commits on
`main` between that date and 2026-10-15 22:03 UTC. So custos's statement that hodie `main` was
`f60476e` at `202610152017` matches. Its statement that the review workflow had "no draft skip"
also matched until `a1bdfb3` / `a01af52` (#164) changed it to `[opened, ready_for_review, labeled]`
that same afternoon, after custos wrote it. My "look different" was a comparison against a
newer state. I should have said "since moved".

**C-2 (confirmed).** custos's `atelier/peer-review/…run-0.md` said hodie has 3 of 13 hygiene files and
no Latin-cue workflows. Running custos's `tools/repo_hygiene_check.sh` against hodie gives
`Present: 3 Missing: 10`. Present: `README.md`, `CLAUDE.md`, `.gitignore`. Missing: `LICENSE.md`, `.prime`,
`.github/CODEOWNERS`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/sovran-labels.yml`,
`tools/scan_lexeme.sh`, `tools/prime_check.sh`, `tools/validate_json_yaml.sh`,
`.github/workflows/validate-json-yaml.yml`, `docs/stale-branch-closure.md`. No workflow or
`.github` file mentions `disponi`, `petitio`, `placet` or "latin".

**C-3 (incomplete).** Pass 1 read hodie only through its `CLAUDE.md`, which names 13 of 33 folders.
Several things hodie has that Pass 1 compared custos against were invisible there: `moav/`,
`wellspring/`, `quepad/`, `mission/`, `tests/`, `branch-tracker/`, `pr-journeys/`.

**C-4 (generalizes Pass 1).** Pass 1 read index drift as a custos trait (O-2, O-8, O-17, O-18).
Hodie has the same kind: `CLAUDE.md` says 16 domains (15 on disk) and "21+" scripts (29);
`moav/README.md` says COMPLETE where the carrier says OPEN; `quanta/ENTITY_DEVELOPMENT_STATUS.md`
is dated 2025-12-30; `branch-tracker/branches.md` has a 2026-08-21 baseline; `redundancy_entity/`
remains after its recorded transfer.

---

## 3. Things hodie does that custos would not guess (Form C.3)

**3.1.** It has a tested Python codebase. `tests/` runs 88 passing tests, against custos's shell
tools, which are described as untested (`atelier/peer-review/…run-0.md` CP-3, reported).

**3.2.** A workflow commits back to branches. `.github/workflows/footer-witness.yml` runs on
`push` and ends with `git commit -m "quepad: refresh witness scan state [skip ci]"` and
`git push`. This is visible on the swap branches: `d19e3dd` (on `feature/peer-swap-hodie-side`)
and `897130c` (on `-b`) are bot commits added after each Pass 1 push. Custos's `CLAUDE.md` says its
own `prima-witness.yml` is "stateless: no bot commits".

**3.3.** It has a daily Drive sync and an hourly bot-PR finalizer. `.github/workflows/sync-hodie.yml`
runs on `cron: '0 12 * * *'` (noon UTC) and on manual dispatch. `.github/workflows/auto-finalize.yml`
runs on check-suite completion and hourly, and finalizes open bot-authored PRs older than an hour
with all gates green.

**3.4.** Its seal gate differs from custos's. `.github/workflows/finalize-pr.yml` triggers on
`issue_comment` and runs if the author association is `OWNER`, `MEMBER` or `COLLABORATOR`, or the
author is `github-actions[bot]`. The gate step is `grep -qF '@claude finalize'` on the comment
body. A search of the file for "footer" or "Claude Code" finds nothing. Custos's comparable gate
skips comments with the Claude Code footer and cues inside quotes or code (custos `CLAUDE.md`,
"Seal and merge", reported).

**3.5.** Entity domains are the content model. `quanta/` holds domains written as characters with
dialogue examples and development stages (`quanta/ENTITY_DEVELOPMENT_STATUS.md`). `CLAUDE.md` says
"Entities represent domains achieving awareness (not tools)."

**3.6.** It holds a pipeline for "pressure" rather than a nursery: `wellspring/README.md` ("Head
pressure: 1 item at a time"), `quepad/README.md` (queue intake pad, "egressum-Q"). Custos has a
comparable `queue/` and `.shadow-well/` (Pass 1 O-6, O-9); I have not compared their rules.

**3.7.** Its custody conventions come from custos. `moav/README.md` says the naming convention was
"Adopted from custos's `moav/README.md`"; custos's `prima-witness.yml` and `seeds/env_setup.sh` were in turn
adapted from hodie's `footer-witness.yml` and `.scripts/env_setup.sh` (custos `CLAUDE.md`, reported). I did not check either
direction beyond those two statements.

---

## 4. The thing I would least like the peer to open (Form C.4)

`.eric/` (27 files). They are owner-filed session notes and continuity records, and the process
rule is that personal material stays where its owner filed it. I did not open them, so I cannot say
what they hold. Second: `_CONSOLIDATED/CODEX_documents/` (302 files), because it is unsorted volume
with known duplicates (the 16 dedupe carriers in `moav/`), and a reader would meet repeats before
anything finished.

---

## 5. Did anything in my own repo change how I read Pass 1? (Form C.5)

Yes, three things:

1. **Custos's claims about hodie were accurate when written** (C-1, C-2). I should weigh Pass 1's
   suspicion of them less.
2. **Index drift is shared, not custos-specific** (C-4). Pass 1 listed it as a custos observation;
   in hodie it is the same shape.
3. **The seal gate differs in a way custos's `CLAUDE.md` already guards against** (3.4). Pass 1
   noted the footer guard (O-15) as something custos does; Pass 2 shows hodie lacks it.

Not changed: Pass 1's reading of the custody trail (O-4 to O-10). Hodie has no counterpart
(`prima-clock/` does not exist here), so nothing in hodie confirms or contradicts it.

---

## 6. Corrections to Form A

- A.3 (what I can write): push to a hodie branch works (`feature/peer-swap-hodie-side-b`). Opening
  a PR is still untested.
- A.1: the Project this session is attached to is named "HODIE".

---

∰◊€π¿🌌∞

*Enjoy the journey.*

∰ 20261016010553290
