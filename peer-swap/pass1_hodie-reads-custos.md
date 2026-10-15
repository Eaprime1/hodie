# Pass 1 — hodie reads custos (cold read)

`prima-clock: 202610152233` (UTC)
`suit: ♦️ Seed · plank: Germ — a working record, not canon`
`entity: eaprime1 + Claude (Sonnet 5.5), hodie side of the peer swap`
`status: FROZEN at commit. Corrections go in later passes as new text.`
`reads: eaprime1/custos, branch navigo-claude-hodie-custos, commit a8e9e41`

*Observations only. No recommendations; those belong to Pass 3.*

---

## 0. What I read, and what I did not

**Read.** A shallow clone of custos at `a8e9e41` (one commit visible, 616 files). I opened
`CLAUDE.md`, `README.md`, `prima.yaml` (head), `prima-clock/registry.md`, `vault/` (both
READMEs), `moav/README.md` and every carrier's stamp and custody field, `branch-tracker/branches.md`
(head), `turns/` (listing, `log.md` tail, `observations/README.md`, one observation), `tools/`
(listing, `peer_inventory.sh` head), `.github/` (listing, `PULL_REQUEST_TEMPLATE.md`,
`CODEOWNERS` head, `claude-code-review.yml` head, `finalize-pr.yml` head), `atelier/README.md`.
I ran `bash tools/scan_lexeme.sh` and `bash tools/prime_check.sh` (both read-only).

**Not seen.** Git history, blame, PRs, issues, Actions runs and CI results (shallow clone, no
working `gh`). Other branches (`main`, `pixel8`, `radix`, `֍custos֎`). The contents of
`world/`, `quests/` (beyond a listing), `guides/`, `docs/` (beyond one file), `pr-journeys/`,
`dungeon-master/`, `valuation/`, `incoming/`, `returns/`, most of `atelier/`. Anything outside
this one branch.

**Not a cold read, in three ways. Oversight should weigh the rest of this file with these in view.**

1. This session is attached to a claude.ai Project named "custos". Its description and
   instructions named custos's architecture, sibling repos and vocabulary before I opened a file.
2. While searching custos for the word "hodie" (192 case-insensitive hits in 40 files), I opened
   the head of `atelier/hodie-shadow/202610152017_renovata-opening.md`, `docs/peer-review-process.md`
   and `atelier/peer-review/202610_custos-pixelator_run-0.md`. These are custos's own account of
   hodie, written before this swap. I have **not** checked any of their claims about hodie
   against hodie in this pass. Where I cite them below, I say so.
3. I did not open `intro-hodie-side.md`, `form-custos-side.md` or `intro-custos-side.md`.

---

## 1. Shape

- **O1.** custos describes itself as "not a software project with a build pipeline": content
  and structure — quests, world lore, shell tools, device state, workflow configuration
  (`CLAUDE.md`, "What This Repository Is").
- **O2.** File counts by top-level folder (my `find`, this checkout): `atelier/` 142,
  `pr-journeys/` 115, `.github/` 35, `docs/` 33, `tools/` 22, `turns/` 21, `dungeon-master/` 19,
  `guides/` 17, `incoming/` 16, `moav/` 14, `valuation/` 13, `vault/` 3, `prima-clock/` 1,
  `branch-tracker/` 1. The custody folders are small; the nursery and the generated journeys are large.
- **O3.** There are 25 files in `.github/workflows/`. `CLAUDE.md` ("Review Gates", "CI") names nine
  of them.
- **O4.** One workspace folder per AI voice sits at the root: `.claude/`, `.gemini/`,
  `.chatgpt/`, `.perplexity/`, `.codex/`, `.grok/`, `.copilot/`, `.agents/` (`CLAUDE.md`, "Navigo model").

## 2. Process the repo enforces

- **O5. Seal and merge are separate from authorship.** `CLAUDE.md` ("Seal and merge"): the owner's
  comment seals; footer-carrying comments and quoted cues cannot seal; a navigo describes the cue
  in words. `finalize-pr.yml` header: allowed commenters are OWNER/MEMBER/COLLABORATOR/bot; gates
  are template sections, resolved threads, green CI.
- **O6. An observation document sits before the seal.** `turns/observations/README.md` gives the
  order (recensio, oversight review, complete, seal, merge). `turns/observations/202610071031_pr431_observation.md`
  shows one: sections Seen, Fixed, Carried forward, Scans, Ready for the seal, Result. In it the
  seal came first and the document after, and it says so. `turns/log.md` (tail) says the gate does
  not enforce the order and lists that as open in `turns/CULTIVATION.md`.
- **O7. The paid review is rationed.** `.github/workflows/claude-code-review.yml` header comment
  and `on:` block: `types: [opened, ready_for_review, labeled]`; runs once when ready and again
  only on the `ai-review` label; drafts get the API-free `review-packet.yml`.
- **O8. Session memory is append-only and split by purpose.** `turns/`: `log.md` (669 lines,
  newest at the bottom), `CLOSING.md`, `AAR.md`, `CULTIVATION.md` (163 lines, "open design
  conflicts"), `review-surface.md`. Each log entry carries `witnessed: true` and one-word `resonance`.
- **O9. PR template** (`.github/PULL_REQUEST_TEMPLATE.md`): Intent, What Arrived, Resonance, Ethics
  Check (five boxes, one of them "scan_lexeme run"), Sense Check, What Door Does This Open.
- **O10. Placeholder scanner.** `bash tools/scan_lexeme.sh` run here: five hits, all inside the
  scanner's own pattern definitions, `world/the-the.md:88`, `CLAUDE.md:243` and
  `review-packet.yml:79`. Output ends "Distressed lexemes are invitations, not failures."

## 3. The custody trail

- **O11. Registry.** `prima-clock/registry.md` is one table, 48 lines. First row `202605271650`
  (founding), last row `202610091052`. Exactly one row carries ♠️ in the suit column (the founding row).
- **O12. A documented exception is a row, not silence.** Row `202609251844` records six files
  that sit at the repo root outside any workspace, says they are left in place on purpose, and
  says the row *is* the closure of their custody. Row `202608311051` says a report has no carrier
  and the routing footprint is the registry row plus an index entry.
- **O13. MOAV carriers.** 13 JSON files in `moav/`. Stamps are present on all 13. `chain_of_custody`:
  8 `OPEN`, 2 `CLOSED` (`custos_moav_external_submission001.json`, `custos_moav_transfer_conceptgrain001.json`),
  3 structured differently (`custos_moav_keeper_seed_launch.json`, `custos_moav_sparstone_handoff.json`,
  `praevium_moav_sparstone-nomination.json`). `moav/README.md` "Existing Carriers" lists five.
- **O14. Staleness is written down.** `branch-tracker/branches.md`: rows marked "Not created",
  "Stale", "Not re-verified since — may be behind current `main` tip". `CLAUDE.md` ends with
  "Known Stray Content" naming things that "should not be assumed to be in scope".
- **O15. Vault.** `vault/README.md`: "origin molds… the source of all copies." `vault/spade-of-aces/README.md`:
  "No document is placed here without a prima-clock stamp." Files under `vault/`: two READMEs and
  `vault/cygwin-installation.pdf`.

## 4. Tooling

- **O16.** `tools/peer_inventory.sh` (head) compares two checkouts by git blob id and "Never writes
  to either repo." `docs/peer-review-process.md` v0 (head only) names it step 2 of a peer review.
- **O17.** `tools/test_cue_parser.sh` plus `.github/scripts/cue-parser.js`: per `turns/log.md`
  (tail), a 54-row offline test. I did not run it.
- **O18.** `bash tools/prime_check.sh` prints "Prime state: 3 / Next prime: 5". `CLAUDE.md`:
  "Advance only when a development phase completes."

## 5. Where hodie appears in custos

- **O19.** 192 hits for "hodie" (case-insensitive) in 40 files. Per `CLAUDE.md`, `seeds/env_setup.sh`
  is "ported/adapted from hodie's `.scripts/env_setup.sh`" and `prima-witness.yml` is "ported/adapted
  from hodie's stricter `footer-witness.yml`".
- **O20.** (custos's view, unchecked by me.) `atelier/peer-review/202610_custos-pixelator_run-0.md`
  gives hodie "3 of 13" against custos's hygiene baseline. `atelier/hodie-shadow/202610152017_renovata-opening.md`
  says hodie's `moav/` holds 17 carriers and none records hodie's own entry into custody.
  `atelier/element-of-the-day/hodie-handoff.md` calls hodie "the intended later home for a
  general daily-reports system; that system is not yet defined or deployed."

---

## 6. What confused me

- **C1. `device/` on `main`?** `CLAUDE.md`: "Device Layer (`device/`) — pixel8 branch only… Not on
  `main`." This checkout has `device/` with six files. I cannot tell which branch this commit
  descends from (shallow), so this is either a stale sentence or a branch artifact. I do not know which.
- **C2. Three naming schemes for the same role.** `CLAUDE.md` "Navigo model" has nav1/navigo2/nav3/nav5;
  the next paragraph says "Naming is under review (as of 2026-09-27)" and uses "Navigo Claude";
  `prima-clock/registry.md` rows also use "navigo15", "nav1 · Sonnet 4.6".
- **C3. Stale counts.** `CLAUDE.md` names nine workflows; 25 exist (O3). `moav/README.md` lists five
  carriers; 13 exist (O13). `branch-tracker/branches.md` says "Last updated: 202609290340" while the
  registry's last row is `202610091052`.
- **C4. "Known Stray Content".** `CLAUDE.md` names `airavata-custos/` and `seneschal/scanner/New folder/`.
  Neither path exists in this checkout.
- **C5. "No bounties" and bounty remain.** `CLAUDE.md`: "custos retired the word 'bounty'." Still
  present: `atelier/README.md` lines 21, 22, 28 ("Bounty open", "Bounty #187") and
  `quests/missions/002-post-a-bounty.md`. Possibly historical; not marked as such where I looked.

## 7. A promise I cannot find evidence of

**The vault.** `vault/README.md` and `CLAUDE.md` say it is where documents "have passed formal
custody" and "the vault holds the mold" if a working copy is lost. Where I looked: `vault/` and
`vault/spade-of-aces/` (no entries, only READMEs), the registry's suit column (one ♠️ row, the
founding), `branch-tracker/branches.md` (the `∰custos` vault pinnacle branch is "Pending — Not
yet created"), and the one stray file (`vault/cygwin-installation.pdf`: the word "cygwin" appears in
`seep-artois/`, `device/`, `queue/` and `turns/log.md`; I did not read those hits, and the
PDF has no stamp that I can see). I found the
mechanism described in detail and no entry that used it. I may have missed a vault on another branch.

## 8. Through other eyes

- **The newcomer who has never seen either repo.** `README.md` opens with a three-layer diagram and
  a folder tree, so "what is this" lands fast. Terms such as Shepherd, Podium, Flock and navigo
  arrive in the first paragraphs; I did not read `world/lore.md` to see whether they are defined
  there.
- **A contributor with no context who wants to help today.** `README.md` "Workflow" points to open
  issues with `mission` or `sparstone-trial` labels, each with a bash completion check, and says
  claim by commenting. Before working, two Latin cues are expected (`@claude disponi`, `@claude petitio`).
  I did not read `CONTRIBUTING.md`. The path exists; I cannot judge its friction.
- **The Shepherd on a tired day.** Helps: `CLAUDE.md` is long but organized, `turns/CLOSING.md` is a
  checklist, and indexes carry "Last updated" lines. Hurts: the newest log entry is at the bottom of
  669 lines, and two indexes disagree with the registry (C3). I did not time a re-entry.
- **The repo six months from now, if nothing changes.** My guess, not evidence: the indexes in C3
  keep lagging, `atelier/` and `pr-journeys/` keep growing, and the vault stays empty unless
  something is placed there.

## 9. Lens (Quince)

Left unanswered. I found no definition of Quince in what I read. custos's own review of its
halide seeds says it is "nowhere in the repo" (`atelier/halide/seeds/REVIEW-202610030124.md`
line 109, and `round-one-seed_202610031417.md` line 100). I would be inventing the lens.

---

∰◊€π¿🌌∞

∰ 20261015223313000 — pass 1 first witness (hodie reads custos)
